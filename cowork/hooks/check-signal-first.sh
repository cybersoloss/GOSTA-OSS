#!/usr/bin/env bash
# GOSTA Hook: Signal-first discipline check (V8.7 — M1 of Plan #3)
# Triggered by PreToolUse on the Task tool.
# Verifies that an `in_progress` signal stub exists for the dispatched
# ACT-ID before allowing the Task dispatch to proceed.
#
# Domain-agnostic — reads identifier patterns from the session's OD
# §Framework-Version Markers when present, or falls back to the canonical
# GOSTA identifier set.
#
# Failure mode: WARN (not BLOCK). Emits a warning entry to
# debug-logs/orchestrator-trace.md and debug-logs/hook-warnings.md, but
# allows the dispatch to proceed.
#
# Protocol reference: GOSTA spec §8.7 (mechanizable subset of
# documentation-only discipline) + cowork protocol §6.3 (signal-first rule).

set -euo pipefail

INPUT=$(cat)

EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
SESSION_DIR=$(echo "$INPUT" | jq -r '.cwd // empty')
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

# Only fire on PreToolUse for Task tool
if [ "$EVENT" != "PreToolUse" ] || [ "$TOOL_NAME" != "Task" ]; then
    echo '{"continue": true}'
    exit 0
fi

# Resolve session directory — same pattern as log-dispatch.sh
TRACE_FILE=""
WARN_FILE=""
SIGNALS_DIR=""

if [ -d "${SESSION_DIR}/signals" ]; then
    SIGNALS_DIR="${SESSION_DIR}/signals"
    TRACE_FILE="${SESSION_DIR}/debug-logs/orchestrator-trace.md"
    WARN_FILE="${SESSION_DIR}/debug-logs/hook-warnings.md"
else
    # Walk up looking for sessions/*/signals/ structure
    CHECK_DIR="$SESSION_DIR"
    for _ in 1 2 3 4 5; do
        FOUND=$(ls -d "${CHECK_DIR}"/sessions/*/signals 2>/dev/null | head -1)
        if [ -n "$FOUND" ]; then
            SIGNALS_DIR="$FOUND"
            SESS=$(dirname "$FOUND")
            TRACE_FILE="${SESS}/debug-logs/orchestrator-trace.md"
            WARN_FILE="${SESS}/debug-logs/hook-warnings.md"
            break
        fi
        CHECK_DIR=$(dirname "$CHECK_DIR")
    done
fi

# If no signals/ directory found, signal-first discipline is not active for
# this session — exit silently.
if [ -z "$SIGNALS_DIR" ]; then
    echo '{"continue": true}'
    exit 0
fi

DESCRIPTION=$(echo "$INPUT" | jq -r '.tool_input.description // ""')
PROMPT=$(echo "$INPUT" | jq -r '.tool_input.prompt // ""')
COMBINED="${DESCRIPTION} ${PROMPT}"

# Extract identifier patterns from the dispatch.
# Default canonical GOSTA identifier set (word-boundary anchored).
# Sessions may extend via OD §Framework-Version Markers; this hook reads
# the OD if present and adds session-specific identifier patterns.
PATTERNS='\bACT-[0-9]+\b|\bTAC-[0-9]+\b|\bSTR-[0-9]+\b|\bDELIB-[0-9]+\b'

# Look for OD and extend patterns from §Framework-Version Markers if present
SESS_DIR=$(dirname "$SIGNALS_DIR")
OD_FILE="${SESS_DIR}/operating-document.md"
if [ -f "$OD_FILE" ]; then
    # Extract session-specific identifiers declared as "Session-specific identifiers" row.
    # Match patterns like "FOO-N" / "BAR-N" / "BAZ-N" within the markers section.
    EXTRA_PATTERNS=$(awk '/## Framework-Version Markers/,/^## /' "$OD_FILE" 2>/dev/null \
        | grep -oE '\b[A-Z]{2,}-[0-9N]\b' \
        | sed 's/-N$/-[0-9]+/' \
        | sort -u \
        | sed 's/^/\\b/;s/$/\\b/' \
        | tr '\n' '|' \
        | sed 's/|$//')
    if [ -n "$EXTRA_PATTERNS" ]; then
        PATTERNS="${PATTERNS}|${EXTRA_PATTERNS}"
    fi
fi

# Extract all matching identifiers from the dispatch
DISPATCHED_IDS=$(echo "$COMBINED" | grep -oE "$PATTERNS" | sort -u)

# If no recognizable ACT-IDs found, the dispatch isn't a phase-action
# dispatch — skip the check (e.g., debug dispatches, ad-hoc subagents).
if [ -z "$DISPATCHED_IDS" ]; then
    echo '{"continue": true}'
    exit 0
fi

# For each dispatched ID, check for a matching in_progress signal stub.
MISSING_IDS=""
for ID in $DISPATCHED_IDS; do
    # Match if any signal file in signals/ contains the ID in its filename
    # AND the file contains an `in_progress` status marker.
    MATCH=$(grep -l -E "Status:[[:space:]]*in_progress" "${SIGNALS_DIR}"/*"${ID}"*.md 2>/dev/null | head -1 || true)
    if [ -z "$MATCH" ]; then
        # Also check for any signal file at all matching the ID (might be completed already)
        ANY_MATCH=$(ls "${SIGNALS_DIR}"/*"${ID}"*.md 2>/dev/null | head -1 || true)
        if [ -z "$ANY_MATCH" ]; then
            MISSING_IDS="${MISSING_IDS} ${ID}"
        fi
    fi
done

# If all dispatched IDs have matching signals, exit clean
if [ -z "$MISSING_IDS" ]; then
    echo '{"continue": true}'
    exit 0
fi

# Emit warning to trace file and warnings file
WARNING_MSG="V8.7-M1 SIGNAL-FIRST WARNING: Task dispatch references ACT-ID(s) [${MISSING_IDS# }] without matching signal stub in ${SIGNALS_DIR}/. Signal-first discipline (cowork protocol §6.3) requires writing an in_progress signal stub before dispatching. Dispatch proceeding (WARN, not BLOCK)."

if [ -n "$TRACE_FILE" ] && [ -f "$TRACE_FILE" ]; then
    cat >> "$TRACE_FILE" << ENTRY

### [${TIMESTAMP}] HOOK-WARNING — signal-first discipline [HOOK-GENERATED]
${WARNING_MSG}
ENTRY
fi

if [ -n "$WARN_FILE" ]; then
    mkdir -p "$(dirname "$WARN_FILE")" 2>/dev/null || true
    cat >> "$WARN_FILE" << ENTRY

[${TIMESTAMP}] M1 SIGNAL-FIRST: ${WARNING_MSG}
ENTRY
fi

# WARN mode — allow dispatch to proceed
echo '{"continue": true}'
