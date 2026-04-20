#!/usr/bin/env bash
# GOSTA Hook: Automatic dispatch logging for orchestrator trace
# Triggered by PreToolUse, PostToolUse, and SubagentStop on the Task tool.
# Appends §19.2-format entries to debug-logs/orchestrator-trace.md.
#
# Entries are marked [HOOK-GENERATED] to distinguish from model-written entries.
# This script is domain-agnostic — it logs whatever the Task tool receives/returns.
#
# Usage: Configured in .claude/settings.json via hooks. Receives JSON on stdin.
# Requires: jq, bash 4+
#
# Protocol reference: GOSTA-Cowork Protocol §19.7

set -euo pipefail

# Read JSON from stdin
INPUT=$(cat)

EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // empty')
SESSION_DIR=$(echo "$INPUT" | jq -r '.cwd // empty')
TOOL_USE_ID=$(echo "$INPUT" | jq -r '.tool_use_id // empty')
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

# Resolve trace file path. The session directory is the cwd.
# Look for debug-logs/orchestrator-trace.md relative to cwd.
# If not found, try to find it by searching for the session directory pattern.
TRACE_FILE=""
if [ -f "${SESSION_DIR}/debug-logs/orchestrator-trace.md" ]; then
    TRACE_FILE="${SESSION_DIR}/debug-logs/orchestrator-trace.md"
else
    # Walk up looking for a sessions/*/debug-logs/ structure
    CHECK_DIR="$SESSION_DIR"
    for _ in 1 2 3 4 5; do
        if ls "${CHECK_DIR}"/sessions/*/debug-logs/orchestrator-trace.md 2>/dev/null | head -1 | read -r FOUND; then
            TRACE_FILE="$FOUND"
            break
        fi
        CHECK_DIR=$(dirname "$CHECK_DIR")
    done
fi

# If no trace file found, debug logging is not enabled for this session — exit silently.
if [ -z "$TRACE_FILE" ]; then
    echo '{"continue": true}'
    exit 0
fi

# Temp directory for correlating PreToolUse → PostToolUse pairs (duration calculation)
HOOK_TMP="${SESSION_DIR}/.hook-dispatch-tmp"
mkdir -p "$HOOK_TMP" 2>/dev/null || true

case "$EVENT" in
    PreToolUse)
        TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

        # Only log Task dispatches
        if [ "$TOOL_NAME" != "Task" ]; then
            echo '{"continue": true}'
            exit 0
        fi

        DESCRIPTION=$(echo "$INPUT" | jq -r '.tool_input.description // "unknown"')
        PROMPT=$(echo "$INPUT" | jq -r '.tool_input.prompt // ""')

        # Truncate prompt if >500 words (per §19.2)
        WORD_COUNT=$(echo "$PROMPT" | wc -w | tr -d ' ')
        if [ "$WORD_COUNT" -gt 500 ]; then
            TRUNCATED=$(echo "$PROMPT" | head -c 1500)
            PROMPT="${TRUNCATED}... [truncated, ${WORD_COUNT} words total]"
        fi

        # Write dispatch entry
        cat >> "$TRACE_FILE" << ENTRY

### [${TIMESTAMP}] DISPATCH — ${DESCRIPTION} [HOOK-GENERATED]
- **Tool use ID:** ${TOOL_USE_ID}
- **Prompt:** ${PROMPT}
ENTRY

        # Save start time for duration calculation
        echo "$TIMESTAMP" > "${HOOK_TMP}/${TOOL_USE_ID}.start"
        ;;

    PostToolUse)
        TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

        if [ "$TOOL_NAME" != "Task" ]; then
            echo '{"continue": true}'
            exit 0
        fi

        # Calculate duration if we have a start time
        DURATION="unknown"
        START_FILE="${HOOK_TMP}/${TOOL_USE_ID}.start"
        if [ -f "$START_FILE" ]; then
            START_TS=$(cat "$START_FILE")
            # Best-effort duration — depends on date command capabilities
            if command -v gdate &>/dev/null; then
                START_EPOCH=$(gdate -d "$START_TS" +%s 2>/dev/null || echo "0")
                END_EPOCH=$(gdate -u +%s)
            else
                START_EPOCH=$(date -d "$START_TS" +%s 2>/dev/null || echo "0")
                END_EPOCH=$(date -u +%s)
            fi
            if [ "$START_EPOCH" != "0" ]; then
                ELAPSED=$((END_EPOCH - START_EPOCH))
                DURATION="${ELAPSED}s"
            fi
            rm -f "$START_FILE"
        fi

        # Extract result summary (first 300 chars of tool output)
        RESULT=$(echo "$INPUT" | jq -r '.tool_output // .tool_result // "no output captured"' | head -c 300)

        cat >> "$TRACE_FILE" << ENTRY

### [${TIMESTAMP}] RETURN — ${TOOL_USE_ID} [HOOK-GENERATED]
- **Duration:** ${DURATION}
- **Output summary:** ${RESULT}
ENTRY
        ;;

    SubagentStop)
        AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id // "unknown"')
        TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // "none"')

        cat >> "$TRACE_FILE" << ENTRY

### [${TIMESTAMP}] SUBAGENT COMPLETE — ${AGENT_ID} [HOOK-GENERATED]
- **Transcript:** ${TRANSCRIPT}
ENTRY
        ;;
esac

# Always allow the tool call to proceed
echo '{"continue": true}'
