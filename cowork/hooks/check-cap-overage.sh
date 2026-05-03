#!/usr/bin/env bash
# GOSTA Hook: Cap-overage detection (M3 of Plan #3)
# Triggered by PostToolUse on Write/Edit tools targeting declared-deliverable paths.
# Surfaces output cap overages to Governor visibility.
#
# Domain-agnostic — reads per-deliverable caps from OD when declared.
# Sessions without explicit cap declarations skip the check (no false-positive WARN).
#
# Failure mode: WARN only. Cap-overage is sometimes substantively justified
# (DEC-PG-03 C precedent). Hook surfaces to Governor; never blocks.
#
# Protocol reference: GOSTA spec §8.7 (mechanizable subset of
# documentation-only discipline) + cowork protocol §22.4 (cap declarations).

set -euo pipefail

INPUT=$(cat)

EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
SESSION_DIR=$(echo "$INPUT" | jq -r '.cwd // empty')
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

# Only fire on PostToolUse for Write/Edit tools
if [ "$EVENT" != "PostToolUse" ]; then
    echo '{"continue": true}'
    exit 0
fi
case "$TOOL_NAME" in
    Write|Edit) ;;
    *) echo '{"continue": true}'; exit 0 ;;
esac

# Resolve session directory
SESS_DIR=""
TRACE_FILE=""
WARN_FILE=""
OD_FILE=""

if [ -f "${SESSION_DIR}/operating-document.md" ]; then
    SESS_DIR="$SESSION_DIR"
else
    CHECK_DIR="$SESSION_DIR"
    for _ in 1 2 3 4 5; do
        FOUND=$(ls "${CHECK_DIR}"/sessions/*/operating-document.md 2>/dev/null | head -1)
        if [ -n "$FOUND" ]; then
            SESS_DIR=$(dirname "$FOUND")
            break
        fi
        CHECK_DIR=$(dirname "$CHECK_DIR")
    done
fi

if [ -z "$SESS_DIR" ]; then
    echo '{"continue": true}'
    exit 0
fi

OD_FILE="${SESS_DIR}/operating-document.md"
TRACE_FILE="${SESS_DIR}/debug-logs/orchestrator-trace.md"
WARN_FILE="${SESS_DIR}/debug-logs/hook-warnings.md"

# Extract written file path
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    echo '{"continue": true}'
    exit 0
fi

# Look for a declared cap in the OD for this file path.
# Two formats supported:
#   (1) Inline declaration: **Cap (declared...):** [path-pattern]: [N KB | N words]
#   (2) Table format (canonical OD template):
#       ## Per-Deliverable Caps
#       | Path Pattern | Cap (declared) | Rationale |
#       | path-pattern | N KB / formula | rationale |
# Sessions that don't declare caps get no check.
BASENAME=$(basename "$FILE_PATH")
CAP_LINE=$(grep -E "Cap[[:space:]]*\(declared.*\)[[:space:]]*:.*${BASENAME}" "$OD_FILE" 2>/dev/null | head -1 || true)

if [ -z "$CAP_LINE" ]; then
    # Try inline format with path pattern (e.g., "phase-N-act-N-*.md")
    PATH_PATTERN=$(echo "$BASENAME" | sed 's/[0-9]\+/[0-9]+/g')
    CAP_LINE=$(grep -E "Cap[[:space:]]*\(declared.*\)" "$OD_FILE" 2>/dev/null | grep -E "$PATH_PATTERN" | head -1 || true)
fi

if [ -z "$CAP_LINE" ]; then
    # Try table format: scan the Per-Deliverable Caps section's data rows.
    # Extract basename stem (e.g., "position" from "position-test.md") and
    # match against table data rows whose first cell pattern fits the basename.
    BASENAME_STEM=$(echo "$BASENAME" | sed -E 's/[-._].*//' | sed -E 's/[0-9]+$//')
    CAPS_SECTION=$(awk '/^## Per-Deliverable Caps/{f=1; next} /^## /{if(f) f=0} f' "$OD_FILE" 2>/dev/null || true)
    if [ -n "$CAPS_SECTION" ] && [ -n "$BASENAME_STEM" ]; then
        CAP_LINE=$(echo "$CAPS_SECTION" \
            | grep "^|" \
            | grep -v "^|[[:space:]]*-" \
            | grep -vi "Path Pattern\|Path[[:space:]]*Pattern" \
            | grep -v "\[e\.g\." \
            | grep -v "\[e\\\\\.g\\\\\." \
            | grep -F "$BASENAME_STEM" \
            | head -1 || true)
    fi
fi

if [ -z "$CAP_LINE" ]; then
    # No cap declared — skip silently.
    echo '{"continue": true}'
    exit 0
fi

# Extract cap value from the line (look for "N KB" or "N words")
CAP_KB=$(echo "$CAP_LINE" | grep -oE '[0-9]+[[:space:]]*KB' | grep -oE '[0-9]+' | head -1 || true)
CAP_WORDS=$(echo "$CAP_LINE" | grep -oE '[0-9]+[[:space:]]*words' | grep -oE '[0-9]+' | head -1 || true)

# Formula-based cap support (Plan #17): if no fixed-value cap matched, try
# parsing a formula cap of shape "base=N kb + M kb × VAR" or
# "base=N kb + M kb * VAR" (× and * both supported). Resolves VAR by reading
# the artifact's YAML front matter for "VAR: <integer>". Falls back to base
# value only when VAR not found in front matter.
if [ -z "$CAP_KB" ] && [ -z "$CAP_WORDS" ]; then
    FORMULA_BASE=$(echo "$CAP_LINE" | grep -oiE 'base=[0-9.]+[[:space:]]*kb' | grep -oE '[0-9.]+' | head -1 || true)
    FORMULA_PER=$(echo "$CAP_LINE" | grep -oiE '\+[[:space:]]*[0-9.]+[[:space:]]*kb[[:space:]]*[×*]' | grep -oE '[0-9.]+' | head -1 || true)
    FORMULA_VAR=$(echo "$CAP_LINE" | grep -oE '[×*][[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*' | sed 's/[×*][[:space:]]*//' | head -1 || true)

    if [ -n "$FORMULA_BASE" ] && [ -n "$FORMULA_PER" ] && [ -n "$FORMULA_VAR" ]; then
        # Try to read VAR from artifact's YAML front matter (between --- markers)
        INPUT_COUNT=$(awk '/^---$/{flag=!flag; next} flag' "$FILE_PATH" 2>/dev/null \
            | grep -E "^${FORMULA_VAR}:" \
            | head -1 \
            | grep -oE '[0-9]+' \
            | head -1 \
            || true)
        if [ -n "$INPUT_COUNT" ]; then
            CAP_KB=$(awk "BEGIN { printf \"%d\", $FORMULA_BASE + $FORMULA_PER * $INPUT_COUNT }")
        else
            # Fallback: front-matter field absent; use base value only
            CAP_KB=$(awk "BEGIN { printf \"%d\", $FORMULA_BASE }")
        fi
    fi
fi

# Compute current artifact size
ACTUAL_BYTES=$(wc -c < "$FILE_PATH" | tr -d ' ')
ACTUAL_KB=$(( (ACTUAL_BYTES + 1023) / 1024 ))
ACTUAL_WORDS=$(wc -w < "$FILE_PATH" | tr -d ' ')

OVERAGE=""
if [ -n "$CAP_KB" ] && [ "$ACTUAL_KB" -gt "$CAP_KB" ]; then
    RATIO=$(awk "BEGIN { printf \"%.1f\", $ACTUAL_KB / $CAP_KB }")
    OVERAGE="size: ${ACTUAL_KB}KB vs cap ${CAP_KB}KB (${RATIO}× over)"
fi
if [ -n "$CAP_WORDS" ] && [ "$ACTUAL_WORDS" -gt "$CAP_WORDS" ]; then
    RATIO=$(awk "BEGIN { printf \"%.1f\", $ACTUAL_WORDS / $CAP_WORDS }")
    OVERAGE="${OVERAGE}${OVERAGE:+, }words: ${ACTUAL_WORDS} vs cap ${CAP_WORDS} (${RATIO}× over)"
fi

if [ -z "$OVERAGE" ]; then
    echo '{"continue": true}'
    exit 0
fi

# Emit cap-overage warning
WARNING_MSG="V8.7-M3 CAP-OVERAGE WARNING: ${FILE_PATH} exceeds declared cap — ${OVERAGE}. Cap-overage is sometimes substantively justified per DEC-PG-03 C precedent; surfacing for Governor visibility (WARN, not BLOCK)."

if [ -f "$TRACE_FILE" ]; then
    cat >> "$TRACE_FILE" << ENTRY

### [${TIMESTAMP}] HOOK-WARNING — cap overage [HOOK-GENERATED]
${WARNING_MSG}
ENTRY
fi

mkdir -p "$(dirname "$WARN_FILE")" 2>/dev/null || true
cat >> "$WARN_FILE" << ENTRY

[${TIMESTAMP}] M3 CAP-OVERAGE: ${WARNING_MSG}
ENTRY

echo '{"continue": true}'
