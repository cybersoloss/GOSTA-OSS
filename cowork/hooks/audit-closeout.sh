#!/usr/bin/env bash
# GOSTA Hook: Closeout file audit
# Triggered by SessionEnd. Walks the session directory and checks for template stubs.
# Writes a compliance report to debug-logs/closeout-audit.md.
#
# Detection heuristic: a file is a template stub if >=40% of its non-blank,
# non-header lines contain unresolved bracket placeholders like [scope-name],
# [timestamp], [N], [date], etc. Lines that are markdown table headers or
# formatting (|---|) are excluded from the count.
#
# This script is domain-agnostic — it checks any .md file in the session directory.
#
# Usage: Configured in .claude/settings.json via SessionEnd hook. Receives JSON on stdin.
# Requires: bash 4+, grep, awk
#
# Protocol reference: GOSTA-Cowork Protocol §19.7, §5.5

set -euo pipefail

INPUT=$(cat)
SESSION_DIR=$(echo "$INPUT" | jq -r '.cwd // empty')
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

# Find the session directory — look for 00-BOOTSTRAP.md as anchor
SESS_ROOT=""
if [ -f "${SESSION_DIR}/00-BOOTSTRAP.md" ]; then
    SESS_ROOT="$SESSION_DIR"
else
    # Search for session directory under cwd
    FOUND=$(find "$SESSION_DIR" -maxdepth 3 -name "00-BOOTSTRAP.md" -type f 2>/dev/null | head -1)
    if [ -n "$FOUND" ]; then
        SESS_ROOT=$(dirname "$FOUND")
    fi
fi

if [ -z "$SESS_ROOT" ]; then
    # No session directory found — not a GOSTA session, exit silently
    exit 0
fi

AUDIT_FILE="${SESS_ROOT}/debug-logs/closeout-audit.md"
mkdir -p "$(dirname "$AUDIT_FILE")" 2>/dev/null || true

# Header
cat > "$AUDIT_FILE" << HEADER
# Closeout File Audit [HOOK-GENERATED]
**Session:** $(basename "$SESS_ROOT")
**Generated:** ${TIMESTAMP}
**Method:** Automatic template-stub detection (cowork/hooks/audit-closeout.sh)

| File | Lines | Placeholder Lines | Ratio | Status |
|---|---|---|---|---|
HEADER

STUB_COUNT=0
POPULATED_COUNT=0
EMPTY_COUNT=0

# Walk all .md files in the session directory
while IFS= read -r FILE; do
    REL_PATH="${FILE#${SESS_ROOT}/}"

    # Skip files in append-only directories that are expected to grow
    # (signals/, decisions/ contain operational data, not templates)
    case "$REL_PATH" in
        deliberation/round-*) continue ;;
        debug-logs/closeout-audit.md) continue ;;
    esac

    TOTAL_LINES=$(wc -l < "$FILE" | tr -d '[:space:]')

    if [ "$TOTAL_LINES" -eq 0 ]; then
        echo "| \`${REL_PATH}\` | 0 | — | — | **EMPTY** |" >> "$AUDIT_FILE"
        EMPTY_COUNT=$((EMPTY_COUNT + 1))
        continue
    fi

    # Count non-blank, non-header, non-separator lines
    # Exclude: blank lines, lines that are only markdown table separators (|---|),
    # lines that are only markdown headers (#), lines that are only ---
    CONTENT_LINES=$(grep -cvE '^\s*$|^\s*\|[-:|]+\|?\s*$|^\s*#+\s*$|^\s*---+\s*$' "$FILE" 2>/dev/null || true)
    CONTENT_LINES=$(echo "$CONTENT_LINES" | tr -d '[:space:]')
    CONTENT_LINES=${CONTENT_LINES:-0}

    if [ "$CONTENT_LINES" -eq 0 ]; then
        echo "| \`${REL_PATH}\` | ${TOTAL_LINES} | — | — | **EMPTY** (headers only) |" >> "$AUDIT_FILE"
        EMPTY_COUNT=$((EMPTY_COUNT + 1))
        continue
    fi

    # Count lines containing unresolved bracket placeholders
    # Match patterns like [scope-name], [timestamp], [N], [date], [name],
    # [current phase], etc. — but NOT markdown links [text](url) or
    # checkbox syntax [x] / [ ]
    PLACEHOLDER_LINES=$(grep -cE '\[[A-Za-z][A-Za-z _-]*(\|[^\]]+)?\]' "$FILE" 2>/dev/null || true)
    PLACEHOLDER_LINES=$(echo "$PLACEHOLDER_LINES" | tr -d '[:space:]')
    PLACEHOLDER_LINES=${PLACEHOLDER_LINES:-0}
    # Subtract lines that are markdown links: [text](url)
    LINK_LINES=$(grep -cE '\[[^\]]+\]\(' "$FILE" 2>/dev/null || true)
    LINK_LINES=$(echo "$LINK_LINES" | tr -d '[:space:]')
    LINK_LINES=${LINK_LINES:-0}
    PLACEHOLDER_LINES=$((PLACEHOLDER_LINES - LINK_LINES))
    [ "$PLACEHOLDER_LINES" -lt 0 ] && PLACEHOLDER_LINES=0

    if [ "$CONTENT_LINES" -gt 0 ]; then
        RATIO=$((PLACEHOLDER_LINES * 100 / CONTENT_LINES))
    else
        RATIO=0
    fi

    if [ "$RATIO" -ge 40 ]; then
        STATUS="**STUB**"
        STUB_COUNT=$((STUB_COUNT + 1))
    else
        STATUS="populated"
        POPULATED_COUNT=$((POPULATED_COUNT + 1))
    fi

    echo "| \`${REL_PATH}\` | ${TOTAL_LINES} | ${PLACEHOLDER_LINES} | ${RATIO}% | ${STATUS} |" >> "$AUDIT_FILE"

done < <(find "$SESS_ROOT" -name "*.md" -type f | sort)

# Summary
cat >> "$AUDIT_FILE" << SUMMARY

## Summary

- **Populated:** ${POPULATED_COUNT}
- **Stub/Template:** ${STUB_COUNT}
- **Empty:** ${EMPTY_COUNT}

SUMMARY

if [ "$STUB_COUNT" -gt 0 ] || [ "$EMPTY_COUNT" -gt 0 ]; then
    cat >> "$AUDIT_FILE" << WARNING
**Compliance status: VIOLATIONS DETECTED.** ${STUB_COUNT} template stubs and ${EMPTY_COUNT} empty files survived to session close. Per §5.5, template stubs surviving to session close is a protocol violation.
WARNING
else
    cat >> "$AUDIT_FILE" << PASS
**Compliance status: PASS.** All scaffolded files are substantively populated.
PASS
fi
