# GOSTA Session Launcher Template v1.4

**Purpose:** Paste this prompt (with placeholders filled) into a new Cowork or Code session to bootstrap a GOSTA scope. The AI will scaffold the directory, copy templates, load context, and begin Phase 0.

**Usage:** Copy this file → replace all `{{PLACEHOLDER}}` values → paste the filled prompt into a fresh session.

**Relationship to startup.md:** This template is a manual-fill alternative to `cowork/startup.md`, which is the **primary entry point** (see `CLAUDE.md`). Both produce identical session structures. When they diverge, `startup.md` is authoritative — it is actively maintained and incorporates the latest protocol extensions. Use this template when you prefer manual editing over interactive Q&A.

---

## — START OF PROMPT — (copy from here)

You are running a GOSTA scope. Your first task is to set up the session directory and begin the Bootstrap phase.

### 1. Protocol & Framework

Read these files before doing anything else:

```
cowork/gosta-cowork-protocol.md                        ← Execution protocol (v3.15) — full read
cowork/deliberation-protocol.md                        ← Full read if deliberation enabled; skim §1-§3 if disabled
GOSTA-agentic-execution-architecture.md:
  - Section 0  (overview, tiers, implementation)       ← Required
  - Section 9  (operating document template)           ← Required for OD authoring
  - Section 14.7 (deliberation escalation)             ← Required if deliberation enabled
  - Section 21 (OD authoring guide)                    ← Required for OD authoring
  - Sections 1-3 (principles, architecture, layers)    ← Read if context allows
```

You are bound by the protocol. Follow it precisely — especially Phase Gate Enforcement (§5.1), domain model authoring rules (§3.1), and guardrail architecture (§4.1).

### 2. Session Identity

| Field | Value |
|-------|-------|
| **Session Name** | `{{SESSION_NAME}}` |
| **Governor** | {{GOVERNOR_NAME}} |
| **Date** | {{DATE}} |
| **Scope Type** | {{SCOPE_TYPE: finite / ongoing}} |
| **Complexity** | {{COMPLEXITY: simple / moderate / complex}} |
| **Mode** | {{MODE: cowork / code / both}} |
| **Independence Level** | {{INDEPENDENCE_LEVEL: 1 / 2 / 3}} (default: 2) |
| **Deliberation Mode** | {{DELIBERATION_MODE: enabled / disabled}} (default: disabled) |

### 3. Goal

{{GOAL — 1-3 sentences. What are we trying to produce or achieve?}}

### 4. Why GOSTA

{{WHY — What failure mode does structured governance prevent here? Why not just do it ad-hoc?}}

### 5. Domain Models

**Domain model count guidance:** GOSTA works best with 3-5 domain models per scope. Fewer than 3 limits cross-domain tension detection (the core analytical value). More than 5 increases context consumption and scoring time without proportional benefit. If selecting outside this range:
- Fewer than 3: AI will suggest adding a domain to provide a contrasting perspective. Note: Deliberation Protocol requires minimum 3 domain models; with fewer, deliberation mode is unavailable.
- More than 5: AI will present resolution options — (a) use all N models, (b) use top 5 by quality gate score, (c) use 3-4 core + stage others as Phase 2 additions, (d) merge overlapping models. Governor chooses.

{{Choose ONE of the following options and delete the others:}}

**Option A — Reuse existing domain models:**
Copy these domain models into `sessions/{{SESSION_NAME}}/domain-models/`:
{{LIST_OF_PATHS — e.g.:
- sessions/prior-project/domain-models/value-creation.md
- sessions/prior-project/domain-models/marketing.md
}}

**Option B — Create new domain models from source material:**
Create applied domain models (protocol §3.1) from these sources:
{{LIST_OF_SOURCES — e.g.:
- Domain: Value Creation | Source: reference/value-creation-source.pdf
- Domain: Technical Feasibility | Source: reference/current-codebase-state.md
}}

Rules: minimum 6 concepts, organized by theme, ~120 lines, applied not encyclopedic. Use `cowork/templates/domain-model.md` as structural template. Include Hypothesis Library if extending beyond 3 components (§3.1 rule 6).

**Option C — Hybrid (reuse some, create some):**
{{Specify which to reuse and which to create, with sources for new ones.}}

### 6. Reference Materials

Copy these files into `sessions/{{SESSION_NAME}}/reference/`. For each file, specify its **consumption role**:
- **`options-universe`** — Contains the items this session will evaluate, sequence, or prioritize (e.g., feature inventory, product backlog, strategy alternatives). AI MUST read before OD tactic generation.
- **`context`** — Background material informing understanding (e.g., market research, competitive analysis). Read as needed.

{{LIST_OF_REFERENCE_FILES — e.g.:
- uploads/product-spec.pdf → reference/product-architecture.pdf (options-universe)
- sessions/prior-project/07-roadmap.md → reference/prior-roadmap.md (context)
}}

### 7. Prior Session Learnings (optional)

{{Choose ONE:}}

**Option A — Inherit learnings from a prior session:**
Read and surface relevant learnings from:
{{PATH_TO_PRIOR_LEARNINGS — e.g.: sessions/prior-project/learnings.md}}

Present each relevant learning and ask me (Governor) how to incorporate it:
- **Into OD** — add as guardrail, constraint, or assumption
- **Into domain model** — add as quality principle, anti-pattern, or hypothesis
- **Note only** — acknowledged but not structurally embedded

Record incorporation decisions in `decisions/governor-decisions.md`.

**Option B — No prior learnings.**
Skip.

### 8. Constraints

{{LIST_OF_CONSTRAINTS — e.g.:
- Solo founder / small team: build effort must be executable
- EU-first: GDPR compliance is Day 1
- No customer development in scope
- Budget: < $5 in API costs per phase
}}

### 9. Success Criteria

{{WHAT_DOES_DONE_LOOK_LIKE — e.g.:
- Feature sequence with every decision referencing domain model concepts
- 2-3 candidate sequences, materially different
- Governor selects one with recorded reasoning
- Final roadmap with phase gates and kill conditions
}}

### 10. Governor Hypotheses (optional)

{{Do you have specific hypotheses you want tested? If yes, list them. They'll be added to the relevant domain model's Hypothesis Library as user-submitted entries — explicitly tested during analysis and reported on separately (protocol §3.1 rule 7). If no, delete this section.}}

### 11. Deliberation Configuration (only if Deliberation Mode = enabled)

{{Delete this section entirely if Deliberation Mode = disabled.}}

**Agent Roster:**

| Agent ID | Domain Model | Role | Model/Provider | Notes |
|----------|-------------|------|----------------|-------|
| {{AGENT_ID_1}} | {{DOMAIN_1}} | domain_agent | default | |
| {{AGENT_ID_2}} | {{DOMAIN_2}} | domain_agent | default | |
| {{AGENT_ID_3}} | {{DOMAIN_3}} | domain_agent | default | |
| COORD-1 | — | coordinator | default | No domain model |

**Cadence:**
- Trigger: {{DELIBERATION_TRIGGER: on_governor_request / on_schedule / on_signal}} (default: on_governor_request for finite, on_schedule for ongoing)
- Max Rounds: {{MAX_ROUNDS}} (default: 5 for finite, 2 for ongoing)
- New Argument Gate (Round 4+): {{NEW_ARG_GATE: enabled / disabled}} (default: enabled)
- Governor Interaction: {{GOV_INTERACTION: at_synthesis / mid_deliberation}} (default: at_synthesis)
- Agent Timeout: {{AGENT_TIMEOUT}} (default: 5 min for Code mode, 1 session for Cowork)
- Cost Budget: {{COST_BUDGET}} (default: no limit)

**Isolation Mode (Cowork mode only):**
- {{ISOLATION_MODE: single_session_sequential / multi_session}} (default: single_session_sequential)

**Termination Thresholds:**
- Convergence: {{CONVERGENCE_DEFINITION}} (default: for 3 agents — "all agents within 3 points on recommendation, no new hard disagreements for 1 round"; for 4-7 agents — "all agents within 2 points on recommendation, no new hard disagreements for 1 round")
- New Argument: {{NEW_ARGUMENT_DEFINITION}} (default: "introduces a domain concept not previously cited, or applies an existing concept to a scenario not previously analyzed")
- Stall: {{STALL_DEFINITION}} (default: "2 consecutive rounds with zero position changes and no new arguments from any agent")

---

## Your Execution Steps

**Do these in order. Do not skip or compress steps.**

**Step A — Scaffold the directory:**

*Code mode:*
```bash
mkdir -p sessions/{{SESSION_NAME}}/{domain-models,reference,signals,health-reports,decisions,deliverables,session-logs}
```

If deliberation is enabled:
```bash
mkdir -p sessions/{{SESSION_NAME}}/deliberation
```

*Cowork mode:* You cannot run bash. Tell the Governor the directory structure needed, then create files into it as subsequent steps proceed. The directory exists implicitly once the first file is written into it. If deliberation is enabled, include the `deliberation/` directory in the structure description.

**Step B — Copy protocol infrastructure:**

*Code mode:*
```bash
cp cowork/gosta-cowork-protocol.md sessions/{{SESSION_NAME}}/
cp cowork/CLAUDE.md sessions/{{SESSION_NAME}}/
```

If deliberation is enabled:
```bash
cp cowork/deliberation-protocol.md sessions/{{SESSION_NAME}}/
```

*Cowork mode:* Read `cowork/gosta-cowork-protocol.md` and `cowork/CLAUDE.md`, then recreate them as new files at the target paths. If deliberation is enabled, also copy `cowork/deliberation-protocol.md`. Confirm with Governor before copying large files.

Note: `CLAUDE.md` is the Claude Code directive — it tells the AI how to behave when entering this session directory in future sessions. Copy it as-is — no session-specific customization needed.

If debug logging is enabled and running in Claude Code mode:
```bash
# Copy or merge hooks configuration into session .claude/settings.json
cp cowork/templates/hooks-settings.json sessions/{{SESSION_NAME}}/.claude/settings.json
```
This enables automatic dispatch logging (§19.7) via `cowork/hooks/log-dispatch.sh` and closeout auditing via `cowork/hooks/audit-closeout.sh`. If `.claude/settings.json` already exists, merge the `hooks` array from `hooks-settings.json` into the existing file.

**Step C — Copy template stubs:**

*Code mode:* `cp cowork/templates/{operating-document.md,learnings.md,gosta-framework-feedback.md} sessions/{{SESSION_NAME}}/`

If deliberation is enabled:
*Code mode:* `cp cowork/templates/synthesis-verification.md sessions/{{SESSION_NAME}}/`

*Cowork mode:* Read each stub from `cowork/templates/` and recreate at the target path.

Files to copy into `sessions/{{SESSION_NAME}}/`:
- `operating-document.md` — will be populated in Step H
- `learnings.md` — stub, populated at retrospective (includes Deliberation Patterns and Domain Model Feedback sections when deliberation is enabled)
- `gosta-framework-feedback.md` — stub, populated when framework gaps are found
- `synthesis-verification.md` — (deliberation only) Governor's checklist for verifying Coordinator synthesis against position papers.

These are intentionally empty stubs at this stage.

**Step D — Copy reference materials** (from §6 above). Preserve the consumption role assigned in §6. Add a comment at the top of each reference file (or in a `reference/README.md` index) noting its role: `options-universe` or `context`.

**Step E — Copy or create domain models** (from §5 above).

*Code mode:* `cp [source-path] sessions/{{SESSION_NAME}}/domain-models/`
*Cowork mode:* Read each source file and recreate at the target path.

**Pre-built model note:** Models copied from prior sessions may have been created under earlier quality standards. Before running the quality gate on reused models, present this choice: "(a) Run quality gate and upgrade any gaps — AI-assisted, Governor reviews changes. (b) Use as-is with a grandfathering note — 'Model used successfully in prior session [X]; known gaps noted.' (c) Replace with new model." If the model was used in a completed, successful session, option (b) is acceptable.

Run quality gate on every domain model (reused or new):

| Check | What to verify | If fails |
|---|---|---|
| Minimum concepts | ≥3 concepts required / 6+ recommended — flag if below 6 | Warn Governor: "Model [name] has [N] concepts. 6+ recommended for full analytical depth." |
| Specificity test | For each concept: does the *description* explain how this concept applies specifically to this session's product/context, not just define it generically? Evaluate description content, not concept name — standard terminology is fine if the description differentiates. | Flag generic concept descriptions. Propose context-specific rewording of the description. |
| Distinctiveness test | For each Quality Principle: would this produce different results in another domain? | Flag and propose rewrite. |
| Anti-pattern specificity | For each Anti-Pattern: is this basic critical thinking? | Flag and propose domain-specific alternative. |
| Application context | Does the model state what session/domain it's for? | Add application context header. |
| Structure completeness | All 6 components present? (Core Concepts, Concept Relationships, Quality Principles, Anti-Patterns, Hypothesis Library, Guardrail Vocabulary) | Warn: "Model missing [components]. Minimum viable: 3 components." |

After running the gate on all models, compile all failures. Present options per failed model: fix now (AI-assisted), proceed with warning, or replace. Do not proceed to Step F until all models are resolved.

**Step F — Check for sibling session learnings** (protocol §16.3):
Scan `sessions/` **recursively** (including nested subdirectories) for any `learnings.md` and `gosta-framework-feedback.md` files. *Code mode:* `find sessions -name "learnings.md" -o -name "gosta-framework-feedback.md"`. *Cowork mode:* manually check each directory and subdirectory. For files with substantive content (>5 non-empty lines), identify the most relevant to this scope and surface those first.

If deliberation is enabled for this scope, specifically look for these sections in prior learnings files:
- **Deliberation Patterns** → Agent Behavioral Patterns, Recurring Disagreement Patterns, Deliberation Effectiveness, Threshold Calibration
- **Domain Model Feedback** → proposed domain model changes from prior deliberation outcomes

These inform roster configuration, termination threshold tuning, and domain model adjustments before execution begins.

Governor decides whether to incorporate each relevant pattern:
- **Into OD** — add as guardrail, constraint, or assumption
- **Into domain model** — add as quality principle, anti-pattern, or hypothesis
- **Note only** — acknowledged but not structurally embedded

Record incorporation decisions in `decisions/governor-decisions.md`.

**Step G — Create 01-scope-definition.md** using the scope-definition template (`cowork/templates/scope-definition.md`). Populate with §2-§9 from this prompt.

**Step H — Draft operating-document.md:**

**OD authoring path decision:** If complexity is `complex` or the goal resists clean decomposition, use the structured OD Drafting Protocol (`cowork/od-drafting-protocol.md`) instead of direct authoring. The OD Drafting Protocol uses targeted decomposition questions before authoring. For simple/moderate scopes, proceed with direct authoring below.

**Before drafting:** Read all reference materials with role `options-universe` (from §6). These contain the items the session will evaluate, sequence, or prioritize. Candidate tactics and strategies must be generated FROM this material — not invented from general knowledge. If no options-universe material exists, tactics are generated from domain model concepts and Governor input.

Follow GOSTA's five-layer hierarchy (framework Section 9 for template, Section 21 for authoring guide). Include:
- Goal with guardrails (hard/soft severity, thresholds, recovery specs for soft)
- Objectives with measurable targets and deadlines
- Strategies with WMBTs (What Must Be True)
- Tactics with hypotheses, kill conditions, success metrics, bootstrap cycles
- Initial actions
- Review cadences
- Graduation stage: 1
- Multi-Domain Assessment section with deliberation mode setting
- **If deliberation enabled:** Full `## Deliberation` section populated from §11 inputs — agent roster table, cadence config, isolation mode, termination thresholds, and deliberation file structure. Use the OD template's Deliberation section as the structural reference.

**Constraint-to-guardrail encoding (mandatory):** Every constraint from §8 must be encoded as a guardrail at the Goal level — one constraint, one guardrail. Do not leave constraints only in the scope definition; constraints without corresponding guardrails have no enforcement during execution. After drafting guardrails, verify: for each §8 constraint, does a guardrail exist that would catch a violation? If not, add one.

Formatting examples (not exhaustive — encode ALL Governor constraints, not just these):
- "Analysis only / no recommendations" → `G-Analytical: All output must be descriptive or explanatory. No prescriptive policy recommendations. Severity: hard.`
- "Regulatory constraint (GDPR, etc.)" → encode as a hard compliance guardrail
- "No external comms" → encode as a hard communication guardrail
- "Self-serve constraint" → encode as a hard guardrail requiring purchase completable without sales calls or demos
- "Solo founder" → encode as a hard delivery constraint guardrail

Present the complete OD to Governor for approval.

**OD Approval Loop:**
- If Governor approves: proceed to Step I.
- If Governor requests changes: apply changes, re-present modified sections, ask for approval again.
- If Governor wants to discuss: discuss, then re-present when ready.
- If Governor requests more than 3 rounds of changes, surface: "We've iterated 3 times. Options: (a) continue iterating, (b) accept current version noting remaining concerns, (c) redesign from a different angle."

**Do NOT proceed until Governor approves the OD.**

**Step I — Create 00-BOOTSTRAP.md** using the bootstrap template (`cowork/templates/00-BOOTSTRAP.md`). Set status to `active`, phase to `Phase 0: Bootstrap`, graduation stage to `1`.

**Step J — Present Bootstrap Phase Gate:**

```
## Phase Gate: Phase 0 (Bootstrap) → Phase 1

### Exit Criteria Assessment

| Criterion | Status | Evidence |
|---|---|---|
| Directory scaffolded | [met/not_met] | sessions/{{SESSION_NAME}}/ with all subdirectories |
| Protocol and CLAUDE.md copied | [met/not_met] | Files present in session directory |
| Domain models created/copied and quality-gated | [met/not_met] | [N] models, quality gate results |
| Reference materials copied | [met/not_met] | [N] files in reference/ |
| Scope definition created | [met/not_met] | 01-scope-definition.md populated |
| Operating document drafted and Governor-approved | [met/not_met] | OD approved [date] |
| Bootstrap file created | [met/not_met] | 00-BOOTSTRAP.md populated |
| Prior learnings reviewed | [met/not_met/not_applicable] | [N] learnings incorporated / skipped |

### Key Findings
- [Any issues, tensions, or observations from the bootstrap process]

### Blocking Tensions
- [Any unresolved issues that would prevent Phase 1. If none: "None identified."]

### Material Tensions
- [Tensions that don't block Phase 1 but should inform execution. Scan domain model Hypothesis Libraries and Concept Relationships for competing claims; check whether any Governor hypothesis conflicts with domain model consensus. If none: "None identified."]

### Deliberation Assessment
- [If deliberation was already enabled in §2 and configured in §11: confirm readiness. "Deliberation mode is enabled with [N] domain agents. Agent roster, cadence, and thresholds are configured in the OD's Deliberation section. Deliberation protocol and file structure are in place. Ready to execute deliberation when triggered."]
- [If deliberation was NOT enabled but 3+ domain models are loaded AND material tensions exist: flag as potential deliberation trigger per Framework §14.7. Ask Governor whether to enable the Deliberation Protocol. Default: No (standard sequential assessment). If Yes: collect §11 configuration and update the OD with the Deliberation section before proceeding.]
- [If deliberation enabled: verify the OD contains a complete `## Deliberation` section with roster table, cadence config, and termination thresholds. If any are missing, flag and fix before advancing.]

### Pre-Flight Validation Gate Results (from GOSTA §8.7)

Per-invariant outcomes at this phase boundary. PASS / WARN / BLOCK / N/A. BLOCK rows prevent advancement; WARN rows require explicit Governor acknowledgment. Reference §8.7.3 for invariant definitions.

- V1 Retrieval Contract Validation: [PASS — all (unit, pool) cells VALIDATED | WARN — N CORPUS-FIT-GAP / M VOCABULARY-MISMATCH cells with logged disposition | BLOCK — K unresolved ESCALATE cells | N/A — Phase 0 does not consume per-unit retrieval]
- V2 Build Artifact Shape Verification: [PASS — shape matches expected chunking | WARN — suspicious N_emb == N_files for non-trivial inputs | BLOCK — downstream depends on chunk-level discrimination and shape is wrong | N/A — no build artifact produced this phase]
- V3 Decision Spine Consistency: [PASS — OD/scope symmetric difference empty | BLOCK — K named entities in scope not in OD or vice-versa | N/A — only checked at Phase 1 entry]
- V4 Continuous Capture Operationalization: [PASS — capture artifacts non-empty proportional to friction | WARN — capture empty AND friction observed; resolution: backfill OR explicit "no capture-class observations apply" | N/A — no continuous-capture mode flag active]
- V5 Runtime Import Verification: [PASS — import-test succeeded in orchestrator runtime | BLOCK — module(s) missing: list | N/A — no runtime tools in use yet]
- V6 Declared Artifact Existence and Population: [PASS — Layer A (every CLAUDE.md / OD / scope-declared artifact present with non-zero content) AND Layer B (templated artifacts populated; no remaining `[POPULATE: ...]` sentinels; per-section word counts above floor) | BLOCK — missing-or-empty OR template-shaped list with disposition: create-or-populate-now / defer-with-reason / remove-from-declaration. At closeout phase gate, V6 fires explicitly on closeout-mandated artifacts.]
- V7 Vertical-Fit on Inherited Artifacts: [PASS — concept coverage ≥70% for inherited domain models | WARN — coverage below threshold; disposition: extend / accept-with-acknowledgment / substitute | N/A — no inherited artifacts]
- V8 Subagent Dispatch Capability Smoke-Test: [PASS — probe subagent's marker file observable from orchestrator AND no-op tool calls clean in subagent runtime | BLOCK — environment-mismatch surfaced (path-resolution / permission scope / tool callability differs); disposition: reroute-path / extend-sandbox / collapse-to-orchestrator | N/A — only at bootstrap when subagent dispatch declared, OR session does not declare subagent dispatch]
- V9 Inheritance Framework-Residue Audit: [PASS — residue list empty (no tokens in inherited artifact absent from inheriting session's declarations) | WARN — N residue tokens surfaced; per-token Governor disposition: update / acknowledge-as-historical / extend-declarations | N/A — only at Phase 1 entry when session inherits artifacts, OR session does not inherit]

### Recommendation
[advance | iterate | restructure — with reasoning]

### Governor Action Required
YES — approve phase gate and advance to Phase 1.
```

Wait for Governor approval before proceeding to Phase 1.

## — END OF PROMPT —

---

## Template Maintenance Notes

**Version:** 1.4
**Protocol version:** 3.15
**Framework version:** 6.1
**Deliberation Protocol version:** 0.7

When the protocol or framework is updated, check:
- §3 file structure (Step A/B/C alignment)
- §3.1 domain model rules (Step E quality gate)
- §5.1/§5.2 session lifecycle (Step H-J alignment)
- §16.3 cross-session learning (Step F)
- Framework Sections 9 and 21 (Step H OD authoring)
- OD Drafting Protocol (Step H path decision) against `cowork/od-drafting-protocol.md`
- §11 deliberation config against deliberation-protocol.md §2.1 and OD template Deliberation section
- Deliberation Assessment (Step J) against deliberation-protocol.md §3.5

**Placeholder reference:**

| Placeholder | Required | Description |
|-------------|----------|-------------|
| `{{SESSION_NAME}}` | Yes | Directory name under `sessions/`. Lowercase, hyphenated. |
| `{{GOVERNOR_NAME}}` | Yes | Human Governor's name. |
| `{{DATE}}` | Yes | Start date (YYYY-MM-DD). |
| `{{SCOPE_TYPE}}` | Yes | `finite` or `ongoing`. |
| `{{COMPLEXITY}}` | Yes | `simple`, `moderate`, or `complex`. |
| `{{MODE}}` | Yes | `cowork`, `code`, or `both`. |
| `{{INDEPENDENCE_LEVEL}}` | No | 1, 2, or 3. Default: 2. |
| `{{DELIBERATION_MODE}}` | No | `enabled` or `disabled`. Default: disabled. |
| `{{GOAL}}` | Yes | What the scope produces. |
| `{{WHY}}` | Yes | Why structured governance is needed. |
| `{{LIST_OF_PATHS}}` | Conditional | Existing domain model file paths (Option A/C). |
| `{{LIST_OF_SOURCES}}` | Conditional | Source material for new domain models (Option B/C). |
| `{{LIST_OF_REFERENCE_FILES}}` | Yes | Reference files with consumption roles (`options-universe` or `context`). |
| `{{PATH_TO_PRIOR_LEARNINGS}}` | No | Path to prior session's learnings.md. |
| `{{LIST_OF_CONSTRAINTS}}` | Yes | Scope constraints. |
| `{{WHAT_DOES_DONE_LOOK_LIKE}}` | Yes | Success criteria. |
| `{{AGENT_ID_N}}` | Conditional | Agent IDs (when deliberation enabled). One per domain model. |
| `{{DOMAIN_N}}` | Conditional | Domain model name for each agent (when deliberation enabled). |
| `{{DELIBERATION_TRIGGER}}` | Conditional | `on_governor_request`, `on_schedule`, or `on_signal`. |
| `{{MAX_ROUNDS}}` | Conditional | Max deliberation rounds. Default: 5 finite, 2 ongoing. |
| `{{NEW_ARG_GATE}}` | No | `enabled` or `disabled`. Default: enabled. |
| `{{GOV_INTERACTION}}` | No | `at_synthesis` or `mid_deliberation`. Default: at_synthesis. |
| `{{AGENT_TIMEOUT}}` | No | Timeout per agent per round. Default: 5 min (Code), 1 session (Cowork). |
| `{{COST_BUDGET}}` | No | Per-deliberation cost cap. Default: no limit. |
| `{{ISOLATION_MODE}}` | Conditional | Cowork mode only. `single_session_sequential` or `multi_session`. |
| `{{CONVERGENCE_DEFINITION}}` | Conditional | When agents have agreed. See deliberation protocol §2.1. |
| `{{NEW_ARGUMENT_DEFINITION}}` | Conditional | New argument vs. restatement. See deliberation protocol §2.1. |
| `{{STALL_DEFINITION}}` | Conditional | Rounds of zero progress before termination. |
