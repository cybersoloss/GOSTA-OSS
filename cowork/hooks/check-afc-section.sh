#!/usr/bin/env bash
# GOSTA Hook: AFC frame-audit section presence check (M4 of Plan #3)
# Triggered by PostToolUse on Write/Edit tools targeting deliverables/.
# Verifies that AFC-enabled sessions produce deliverables containing the
# required Frame Integrity Validation section (per cowork protocol §12.12).
#
# Domain-agnostic — checks for canonical section headers regardless of
# domain content. Conditional on AFC declaration in the session.
#
# Failure mode: WARN at deliverable production. (BLOCK at closeout is
# enforced via V6 Layer B / cowork protocol §5.5; this hook surfaces the
# missing section earlier so it can be corrected before closeout.)
#
# Caveat: section presence does NOT verify content quality. Sycophantic or
# boilerplate frame-audit content passes this check. Quality auditing is
# U1's territory (independent reviewer at deliverable boundary).
#
# Protocol reference: GOSTA spec §9.2 (AFC) + cowork protocol §12.12
# (Frame Integrity Validation).

set -euo pipefail

INPUT=$(cat)

EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
SESSION_DIR=$(echo "$INPUT" | jq -r '.cwd // empty')
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

if [ "$EVENT" != "PostToolUse" ]; then
    echo '{"continue": true}'
    exit 0
fi
case "$TOOL_NAME" in
    Write|Edit) ;;
    *) echo '{"continue": true}'; exit 0 ;;
esac

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    echo '{"continue": true}'
    exit 0
fi

# Fire on writes to deliverables/ AND deliberation/[DELIB-NNN]/synthesis-report.md
# AND health-reports/phase-gate-*.md within a session directory.
# Per cowork-protocol §12.12 and deliberation-protocol §4.4 Frame Integrity
# Validation, synthesis-report and phase-gate request files are Governor-facing
# artifacts that propagate to deliverables; they warrant the same §12.12 audit
# as deliverable artifacts. Coverage extension per Plan #19 (Pattern 13 scope
# extension justified: synthesis-report and phase-gate files are consumed by
# Governor and frame-drift in them cascades to deliverables).
if ! echo "$FILE_PATH" | grep -qE '/deliverables/[^/]+\.md$|/deliberation/[^/]+/synthesis-report\.md$|/health-reports/phase-gate-[^/]+\.md$'; then
    echo '{"continue": true}'
    exit 0
fi

# Resolve session directory from the file path. Supports all three covered
# path patterns: /deliverables/, /deliberation/[DELIB-NNN]/synthesis-report.md,
# /health-reports/phase-gate-*.md.
SESS_DIR=$(echo "$FILE_PATH" | sed -E 's|/deliverables/.*$||; s|/deliberation/[^/]+/synthesis-report\.md$||; s|/health-reports/phase-gate-[^/]+\.md$||')
if [ ! -f "${SESS_DIR}/operating-document.md" ] && [ ! -f "${SESS_DIR}/01-scope-definition.md" ] && [ ! -f "${SESS_DIR}/CLAUDE.md" ]; then
    # Not a recognizable session directory
    echo '{"continue": true}'
    exit 0
fi

OD_FILE="${SESS_DIR}/operating-document.md"
SCOPE_FILE="${SESS_DIR}/01-scope-definition.md"
CLAUDE_FILE="${SESS_DIR}/CLAUDE.md"
TRACE_FILE="${SESS_DIR}/debug-logs/orchestrator-trace.md"
WARN_FILE="${SESS_DIR}/debug-logs/hook-warnings.md"

# Check whether AFC is declared for this session.
# AFC declaration patterns: "Analytical Frame Contract", "AFC enabled",
# "AFC declared", "Frame Declaration (AFC".
AFC_DECLARED="no"
for SRC in "$OD_FILE" "$SCOPE_FILE" "$CLAUDE_FILE"; do
    if [ -f "$SRC" ] && grep -qE 'Analytical Frame Contract|AFC[[:space:]]+(enabled|declared)|Frame Declaration[[:space:]]*\(AFC' "$SRC" 2>/dev/null; then
        AFC_DECLARED="yes"
        break
    fi
done

if [ "$AFC_DECLARED" = "no" ]; then
    # AFC not active for this session — section presence not required.
    echo '{"continue": true}'
    exit 0
fi

# Check deliverable for canonical Frame Integrity / AFC frame-audit section header.
# Accept any of the canonical patterns.
HEADER_FOUND="no"
if grep -qE '^#{1,6}[[:space:]]+(Frame Integrity Validation|AFC Frame Audit|§12\.12 Frame Integrity|Frame Audit|G-FrameIntegrity Validation)' "$FILE_PATH" 2>/dev/null; then
    HEADER_FOUND="yes"
fi

if [ "$HEADER_FOUND" = "yes" ]; then
    echo '{"continue": true}'
    exit 0
fi

# Section missing — emit warning
WARNING_MSG="V8.7-M4 AFC SECTION WARNING: ${FILE_PATH} is a deliverable produced by an AFC-enabled session, but no Frame Integrity Validation section header found (expected one of: '## Frame Integrity Validation', '## AFC Frame Audit', '## §12.12 Frame Integrity', '## Frame Audit', '## G-FrameIntegrity Validation'). Cowork protocol §12.12 requires AFC-enabled deliverables to contain a Frame Integrity Validation section. Surface to Governor (WARN at production; closeout phase gate enforces BLOCK via V6 Layer B). Note: section presence is checked here, not content quality."

if [ -f "$TRACE_FILE" ]; then
    cat >> "$TRACE_FILE" << ENTRY

### [${TIMESTAMP}] HOOK-WARNING — AFC section presence [HOOK-GENERATED]
${WARNING_MSG}
ENTRY
fi

mkdir -p "$(dirname "$WARN_FILE")" 2>/dev/null || true
cat >> "$WARN_FILE" << ENTRY

[${TIMESTAMP}] M4 AFC-SECTION: ${WARNING_MSG}
ENTRY

echo '{"continue": true}'
