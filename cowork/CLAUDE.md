# GOSTA Session — Claude Code Directive

When working inside a GOSTA session directory, follow the **GOSTA-Cowork Protocol** (`cowork/gosta-cowork-protocol.md`).

## Session Start (MANDATORY)

Every time you enter a GOSTA session directory:

1. **Read `00-BOOTSTRAP.md`** — this is your orientation. It tells you what phase you're in, what happened last session, and what's pending.
2. **Read files in the Context Loading Order** specified in the bootstrap file.
3. **Check OD staleness** — if 2+ phases or review cycles have passed since the OD was last updated, flag it: "OD may be stale. Last updated [date]. Recommend refreshing before proceeding."
4. **Report status** to the Governor and ask what they want this session.

## Core Rules

- **Never modify the Operating Document without Governor approval.** Draft changes, present them, wait for approval.
- **Signal-first execution** — write a signal stub (`| ACT-ID | in_progress | timestamp |`) to `signals/` BEFORE starting each action. Update to `completed` or `failed` after. An action without a signal stub has not started; an action without a completion update has not finished. See protocol §6.3 Action Completion Gate.
- **Use Phase Gate Enforcement** at every phase transition — produce the structured Phase Gate Request (protocol §5.1) before proceeding.
- **Kill before pivot** when kill conditions are formally met (protocol §7.1). Don't soften kills into pivots without Governor justification.
- **Classify tensions** as Blocking/Material/Informational (protocol §5.1 Step 3b). Only halt on Blocking.
- **Reference pool agent** — if a session's reference pool exceeds 50 items, use `cowork/tools/pool-agent.py query` to retrieve relevant articles. Do NOT load the full pool YAML into context. Score thresholds: ≥0.58 read full article, 0.50–0.57 excerpt only, <0.50 ignore. See protocol §18.5.
- **Log framework feedback** whenever you notice gaps in how GOSTA handles a situation.
- **Guardrails are above baseline** — if you see a guardrail set below the current metric baseline, flag it as a calibration issue.
- **Surface risks explicitly** in every health report — the Risk Factors section (§14.3.9) must be non-empty and substantive. Generic dismissals are themselves a flag.
- **Check signal-recommendation alignment** — if most signals trend negative but you recommend persevere, state why with specific countervailing evidence.

## Output Paths

Deliverables and session artifacts go in their canonical directories. Do not mix them:

| Output type | Directory | Examples |
|---|---|---|
| Deliverables | `deliverables/` | Analysis reports, scorecards, gap analyses, feedback documents |
| Session logs | `session-logs/` | `session-NNN.md` — episodic logs of what happened each session |
| Signals | `signals/` | Append-only signal files |
| Health reports | `health-reports/` | Computed health assessments |
| Decisions | `decisions/` | Governor decisions, append-only |

**Session-specific additions:** During bootstrap, the AI may add a `## Session Directives` section below this file's standard content. Session directives may specify additional context loading, analytical standards, or scope-specific rules — but they must NOT override the output paths above. If a session directive specifies a deliverable path that conflicts with `deliverables/`, the directive is in error; use `deliverables/`.

## File Operations

- Commit at meaningful checkpoints: end of phase, after Governor decisions, after deliverable completion.
- Do NOT push without Governor approval.
- Use append-only for signals/ and decisions/ files — never edit existing entries.
- The bootstrap file (00-BOOTSTRAP.md) is the ONLY file that gets fully overwritten each session.

## Multi-Domain Scoring

When scoring against multiple domain models:
- Default to **Level 2 — Sequential Isolation** (score one domain fully before the next, no back-revision)
- Use 1-10 integer scale, no half-points (protocol §7.6)
- For >10 items, calibrate with 3 representative items first

## Starting a New Session

Use the session launcher template to bootstrap a new GOSTA scope:

1. **Copy and fill:** `cowork/session-launcher-template.md` — replace all `{{PLACEHOLDER}}` values
2. **Paste** the filled prompt into a fresh Cowork or Code session
3. The AI will scaffold `sessions/[name]/`, copy templates, load context, and begin Phase 0

The `sessions/` directory (at repo root) is the standard location for new scopes. Legacy scopes remain in `experiments/`.

### Manual Bootstrap (alternative)

If not using the launcher template:
1. Create the session directory and required subdirectories:
   ```bash
   mkdir -p sessions/[name]/{domain-models,reference,signals,health-reports,decisions,deliverables,session-logs}
   ```
2. Copy templates: `cp cowork/templates/* sessions/[name]/`
3. Copy protocol + directive: `cp cowork/gosta-cowork-protocol.md cowork/CLAUDE.md sessions/[name]/`
4. Create applied domain models using `templates/domain-model.md` (not generic — see protocol §3.1)
5. Run a Bootstrap Session (protocol §5.2) — draft the OD for Governor approval
6. Governor reviews and approves the OD before first execution session
