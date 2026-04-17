# GOSTA Session Startup v1.5

**Purpose:** Interactive session bootstrapper. Read this file, then guide the Governor through setting up a new GOSTA session — no manual template editing required.

**Usage:** In Claude Code or Cowork, say: "Read cowork/startup.md and start a new session."

**Relationship to session-launcher-template.md:** This file automates the same process interactively. The template is the manual fill-and-paste alternative. Both produce identical session structures.

---

## Instructions for the AI

You are setting up a new GOSTA session interactively. Follow these steps exactly.

### Phase 1: Collect Inputs

Ask the Governor for each input below. Ask them **one group at a time** — do not dump all questions at once. Use sensible defaults where indicated. If the Governor gives a short answer, that's fine — you'll expand it into the template format.

**Group 1 — Identity:**

Ask:
- What should this session be called? (lowercase, hyphenated — e.g., `product-mvp`, `market-analysis`)
- Finite scope (bounded project with deliverable) or ongoing (recurring cycles)?
- How complex is this scope? (simple = 1-2 strategies, moderate = 3-4, complex = 5+)
  - Use this to set defaults: simple → expect 1-3 domains, 1-2 phases, lighter Material Tensions; moderate → 3-4 domains, 2-3 phases; complex → 4-5 domains, 3+ phases, denser phase gate Material Tensions section
- Mode: cowork, code, or both? (default: code)
- Independence level 1, 2, or 3? (default: 2)
  - 1 = ask before every action
  - 2 = work autonomously within approved bounds, surface decisions at review points
  - 3 = maximum autonomy with post-hoc reporting

- Deliberation mode? (default: no)
  - **No** — Standard sequential assessment. Domains evaluated one at a time, synthesized by a single AI. Sufficient for most scopes.
  - **Yes** — Multi-agent deliberation. One agent per domain model, a Coordinator synthesizes, Governor resolves dissents. Use when: 3+ domains, cross-domain tensions are expected, stakes are high enough that independent evaluation adds value. Requires 3-5 domain models (minimum 3; recommended 5-7, viable 8-10 with 4+ rounds, >10 cluster-then-synthesize). See the Deliberation Protocol.
  - If the Governor says yes, note it — Group 3A will collect deliberation-specific configuration.

- Shortfall logging? (default: no)
  - **No** — Standard session, no framework observation logging.
  - **Yes** — During execution, the AI will log protocol gaps, domain model inconsistencies, reference pool issues, deliberation friction, and other framework shortfalls as they are encountered. Requires a shortfall log file path (default: `[project]/session-shortfall-log.md`). Entries are appended in real-time, not post-hoc. Useful for framework improvement cycles and PCCA.
  - If the Governor says yes, note it — the AI will create or append to the shortfall log during Phase 3 execution and all subsequent phases.

- Evidence collection mode? (default: no)
  - **No** — Session works with Governor-provided reference materials only. Use when: evidence base is pre-existing (reference pools, uploaded documents, prior session deliverables).
  - **Yes** — AI agents collect evidence from external sources during execution. Use when: session assesses something external (vendor, market, regulation, competitor) where evidence doesn't exist yet and must be gathered. Activates §14.8 Evidence Collection Architecture and the Evidence Collection Protocol.
  - If Yes AND scope type is "ongoing": warn — *"Evidence collection currently supports single-phase collection only. Periodic re-collection (monitoring, rolling updates) is not yet supported (§14.8 extension point §10.1). Collection will run once during the designated phase. Proceed?"*
  - If the Governor says yes, note it — Group 3B will collect evidence-collection-specific configuration.

Auto-fill (do not ask — compute automatically):
- Governor: In Code mode, read from git config (`git config user.name`). In Cowork mode, git config is unavailable — include "Governor: [please confirm your name]" in the Phase 2 summary table and wait for correction.
- Date: Today's date
- FFR (Fresh Framework Read): **Always enabled** — performed automatically at Phase 3 Step 1. The AI scans all spec headings, reads relevant sections from the spec before reading protocols, and flags any spec-protocol inconsistencies. This is not optional — it prevents reasoning from stale derivative files. The Governor does not need to request it.

**Group 2 — Goal and Why:**

Ask:
- What are we trying to produce or achieve? (1-3 sentences)
- Why use GOSTA for this? What failure mode does structured governance prevent? (If the Governor says "just do it" — suggest: "Without governance, the AI will make scope decisions silently, and you won't know what was decided until the output looks wrong.")

**Group 3 — Domain Models:**

First, explain the distinction:
> **Domain models** are structured knowledge files that ground the AI's reasoning — they define what "good" and "bad" look like in a specific domain (e.g., Value Creation, Marketing, Sales). Every AI recommendation must trace back to a concept in a domain model. Without them, the AI reasons from general training data, which risks hallucination.
>
> **Reference materials** are raw inputs — product docs, regulations, research, prior work. They inform domain models and provide context, but the AI doesn't score against them directly. Each reference material has a **consumption role**:
> - **`options-universe`** — Contains the items being evaluated, sequenced, or prioritized by this session (e.g., a feature inventory, product backlog, list of strategic alternatives). The AI MUST read these before generating tactics in the operating document. Without them, the session has evaluation lenses but nothing to evaluate.
> - **`context`** — Background material informing understanding (e.g., market research, competitive analysis, regulatory summaries). Read as needed during execution.

Then show what's available:

```
Available domain models in this repo:
```

Scan these directories and list all `.md` files found:
- `domain-models/` (repo root — shared models)
- `sessions/*/domain-models/` (session models)

For each, show: file path and first line (the model name).

Number the models 1–N in your output so the Governor can reference them by number.

Then ask:
- Which existing domain models do you want to reuse? (enter numbers, "all", or "none")
- Do you need new domain models created? If yes, what domains and from what source material? (If the Governor provides only a domain name or keywords, apply minimum viable expansion at Step 5: draft Core Concepts + Quality Principles + Anti-Patterns and present for Governor review before running the quality gate.)
- Do you have reference files? For each, specify the path and its role:
  - **options-universe** — the things this session will evaluate (e.g., a feature inventory, product backlog)
  - **context** — background material (e.g., market research, prior analysis)
  - (list as: `path → role`, or "none")

**Domain model count guidance:** GOSTA works best with 3-5 domain models per scope. Fewer than 3 limits cross-domain tension detection (the core analytical value). More than 5 increases context consumption and scoring time without proportional benefit. If the Governor selects outside this range:
- Fewer than 3: suggest adding a domain — "Consider adding [domain] to provide a contrasting perspective."
- More than 5: present this resolution: (a) Use all N models — confirm context cost impact, (b) Use top 5 by quality gate score, (c) Use 3-4 core models + stage others as Phase 2 additions, (d) Merge overlapping models into a composite. Governor chooses.

**Group 3A — Deliberation Configuration (only if Governor chose deliberation = yes in Group 1):**

Skip this group entirely if deliberation mode is disabled. If enabled, ask:

> You chose multi-agent deliberation. I need a few configuration decisions. I'll suggest defaults based on your scope type and domain count — just confirm or override.

Then present these with computed defaults (do not ask all at once — present the roster first, then cadence):

**Roster:**
- Auto-generate the agent roster from the domain models selected in Group 3. One agent per domain model. Assign Agent IDs as `[2-4 letter domain abbreviation]-1` (e.g., `VC-1` for Value Creation, `MKT-1` for Marketing, `NIS2-1` for NIS2). Add `COORD-1` as coordinator with no domain model.
- Present the roster table and ask: "Does this roster look right? Any agents to add, remove, or rename?"

**Cadence (present with defaults, ask for overrides):**
- **Trigger:** Default based on scope type and independence level:
  - Finite scopes: `on_governor_request` (Governor explicitly requests deliberation at phase gates or key decisions)
  - Ongoing scopes: `on_schedule` (deliberation at tactic/strategy review cadence)
  - **Independence level override:** If independence ≥ 3, `on_governor_request` produces a dead configuration — the Governor is not reviewing during execution, so deliberation never fires. Override to `on_phase_gate` (system self-invokes deliberation at each phase transition) and warn: *"At independence level 3, `on_governor_request` would require you to manually trigger deliberation — but you've chosen post-hoc reporting. I'm defaulting to `on_phase_gate` so the system invokes deliberation autonomously at each phase transition. Override?"*
  Ask: "When should deliberation trigger? Default: [computed default]."
- **Max Rounds:** Default: 5 for finite, 2 for ongoing. Ask: "Maximum deliberation rounds? Default: [computed default]."
- **New Argument Gate (Round 4+):** Default: enabled. Terminates deliberation if no genuinely new arguments emerge after Round 4. Ask: "Enable New Argument Gate to stop deliberation when agents are just restating positions? Default: enabled."
- **Governor Interaction:** Default: `at_synthesis` (Governor sees the final synthesis report). Alternative: `mid_deliberation` (Governor can intervene between rounds). Ask: "Review at synthesis only, or do you want to intervene mid-deliberation? Default: at synthesis."
- **Cost Budget:** Optional. Ask: "Want to set a per-deliberation cost budget? (e.g., max tokens or dollar amount, or 'no limit'). Default: no limit."

**Isolation Mode (Cowork mode only):**
- If mode is `cowork` or `both`, ask: "Deliberation isolation: (a) single-session sequential — all agents run in one conversation, simpler but less isolation. (b) multi-session — each agent in a separate conversation, maximum isolation but N+2 sessions per deliberation. Default: single-session sequential."
- If mode is `code`, skip — Code mode uses parallel subagents automatically.

**Termination Thresholds (present defaults, ask for confirmation):**
Auto-compute defaults from domain count and complexity:
- **Convergence:** For 3 agents → "all agents within 3 points on recommendation, no new hard disagreements for 1 round." For 4-5 agents → 2-point spread. For 6-7 agents → 2-point spread.
- **New Argument:** Default: "introduces a domain concept not previously cited, or applies an existing concept to a scenario not previously analyzed."
- **Stall:** Default based on domain model richness: if models are thin (<5 concepts each) → 1 round of zero progress. If rich (15+ concepts) → 2 consecutive rounds.

Present: "Here are the termination thresholds I'd recommend based on your [N] domains and [complexity] scope. Confirm or adjust?"

**Group 3B — Evidence Collection Configuration (only if Governor chose evidence collection = yes in Group 1):**

Skip this group entirely if evidence collection mode is disabled. If enabled, ask:

> You chose evidence collection. I need a few configuration decisions.

- **Execution environment:** Auto-detected from Group 1 mode setting.
  - **Code mode:** Collection agents dispatched as parallel subagents. Capability test (Step 5d) determines normal vs pre-fetch mode.
  - **Cowork mode:** No subagent dispatch available. Collection runs as sequential role-plays in one conversation. The AI adopts each agent's role in sequence. Information isolation between "agents" is not possible — the adversarial role is especially important to counteract confirmation bias from sequential execution. No Governor decision needed — auto-detected.

- **Collection topology:** Auto-detected from OD target count; Governor confirms.
  - Single-target (default for one assessment target)
  - Multi-target-shared (multiple targets, shared agent pool)
  - Multi-target-parallel (multiple targets, per-target agent pools)
  - If total agents > 15 (multi-target-parallel): recommend sequential batching — complete each target's full collection cycle before starting the next. Governor decides batch vs. parallel.

- **Collection agent count:** Auto-computed from domain model groupings. Default: `ceil(domain_count / 2) + 1 discovery + 1 adversarial`. Multi-target-parallel multiplies by target count. Present computed count and ask Governor to confirm.

- **Adversarial collection:** Enabled by default. Two modes:
  - **Counter-framing** (default for hypothesis-driven and exploratory) — counter-framing generated from OD objectives (hypothesis inversion) or what the session's domain models exclude from their analytical scope (exploratory). Governor reviews counter-framing before dispatch.
  - **Cross-verification** (for purely factual assessments) — adversarial agent independently re-collects and verifies a sample of other agents' factual claims. Use when no evaluative direction exists to counter.
  Auto-selected based on assessment type. Governor can override.

- **Evidence quality audit mode:**
  - **Directional** (default for hypothesis-driven assessments) — checks for sycophantic over-collection of confirming evidence. Threshold: 70%.
  - **Coverage** (default for exploratory assessments) — checks that all domain model core concepts have adequate evidence. Threshold: 80%.
  Auto-selected based on assessment type. Governor can override.

- **URL verification sample rate:** Default 100% Tier 1 + 30% Tier 2. Adjust if collection volume is very high.

- **Independence level interaction:** Auto-computed from Group 1 independence level.
  - Independence 1-2: All quality gate warnings/failures require Governor review.
  - Independence 3: Only FAIL-level outcomes halt. Warnings auto-resolve with logged rationale. Adversarial counter-framing auto-dispatched. Reconciliation minor adjustments auto-resolve; concept invalidations halt.
  Present computed behavior and ask: *"At independence [N], evidence collection gates will behave as follows: [description]. Confirm or override?"*

- **Source attribution tier policy:** Use framework defaults (§14.8 default 3-tier) or customize?

- **Gap analysis thresholds:** Use protocol defaults (3 Tier 1/2 items per domain) or customize per domain?

- **Pool-agent integration:** Enable if expected evidence items > 50?

**Group 4 — Constraints and Success:**

Ask:
- What constraints apply? (budget, timeline, team size, regulatory, technical)
- What does "done" look like? What are the success criteria?

**Group 5 — Prior Learnings (auto-detected):**

Scan `sessions/` **recursively** for `learnings.md` and `gosta-framework-feedback.md` files (including nested subdirectories). In Code mode use: `find sessions -name "learnings.md" -o -name "gosta-framework-feedback.md"`. In Cowork mode: manually check each directory and subdirectory. For each file found, count substantive lines. If a file has more than 5 lines of substantive content (section headings or bullet points with actual text — excluding blank lines and placeholder text), show it:

```
Found prior learnings:
1. sessions/my-first-session/learnings.md (47 lines)
2. sessions/vendor-evaluation/learnings.md (32 lines)
...
```

Before asking, scan each file's section headings for topic relevance to the new scope. Identify the top 3-5 most relevant files. Present these first with a one-line relevance note, followed by the full list. Example:

```
Most relevant to your scope:
1. sessions/vendor-evaluation/learnings.md — domain model quality + analytical confidence calibration
2. sessions/policy-analysis/learnings.md — informed user patterns + guardrail firing conditions

All prior learnings:
1. sessions/my-first-session/learnings.md (18 lines)
2. sessions/vendor-evaluation/learnings.md (82 lines) ← recommended
...
```

Ask: "Want me to review any of these for relevant patterns? (list numbers, 'recommended' for the pre-filtered set, or 'skip')"

**Group 6 — Governor Hypotheses (optional):**

Ask: "Do you have specific hypotheses you want tested? These get added to the relevant domain model's Hypothesis Library as user-submitted entries — they'll be explicitly tested during analysis and reported on separately. (Enter them or 'skip')"

### Phase 2: Confirm

Present a summary table of all collected inputs:

```
Session:          [name]
Governor:         [name]
Date:             [date]
Scope Type:       [finite/ongoing]
Complexity:       [simple/moderate/complex]
Mode:             [cowork/code/both]
Independence:     [1/2/3]
Deliberation:     [enabled/disabled]
Evidence Collection: [enabled/disabled]
Shortfall Log:    [enabled/disabled — if enabled, path to log file]
FFR:              always enabled (auto)
Goal:             [goal text]
Why GOSTA:        [why text]
Domain Models:    [list — reuse/create/hybrid] ([N] total)
Reference Files:  [list with roles — e.g., "product-research.pdf (options-universe), market-research.pdf (context)" or none]
Constraints:      [list]
Success Criteria: [list]
Prior Learnings:  [list or skip]
Hypotheses:       [list or skip]
```

If deliberation is enabled, also show:

```
--- Deliberation Config ---
Agent Roster:     [agent IDs with domain assignments]
Coordinator:      COORD-1
Trigger:          [on_governor_request / on_schedule / on_signal / on_phase_gate]
Max Rounds:       [N]
Governor Interaction: [at_synthesis / mid_deliberation]
Isolation:        [single_session_sequential / multi_session] (Cowork mode only)
Cost Budget:      [value or "no limit"]
Convergence:      [definition]
New Argument:     [definition]
Stall:            [definition]
```

If evidence collection is enabled, also show:

```
--- Evidence Collection Config ---
Topology:         [single-target / multi-target-shared / multi-target-parallel]
Targets:          [target list]
Agent Count:      [N] (formula: ceil(domain_count/2) + 1 discovery + 1 adversarial)
Adversarial Mode: [counter-framing / cross-verification]
Quality Audit:    [directional (threshold: 70%) / coverage (threshold: 80%)]
URL Verification: [Tier 1: 100%, Tier 2: 30%]
Independence:     [level N — gate behavior description]
Tier Policy:      [framework default / custom]
Pool-Agent:       [enabled if >50 items / disabled]
```

Ask: "Does this look right? Any changes before I scaffold?"

Wait for confirmation. If the Governor says to change something, update and re-confirm.

### Phase 3: Execute

Once confirmed, execute these steps in order. Report progress after each step.

**Step 1 — Fresh Framework Read (FFR) and protocol loading:**

FFR is mandatory before any protocol or OD work. It prevents reasoning from stale derivative files. Perform in this order:

**1a. FFR — Spec heading scan:**
Scan all `##`-level headings in `GOSTA-agentic-execution-architecture.md` to build a complete section map. Note every section number and title. This is your table of contents for the session.

**1b. FFR — Read relevant spec sections:**
Based on the session scope (collected in Phase 1), identify which spec sections are relevant and read them in full from the spec itself. At minimum, always read:
- Section 0 (overview, tiers, implementation)
- Section 9 (operating document template) — required for OD authoring
- Section 13 (domain models) — required for domain model quality gating
- Section 21 (OD authoring guide) — required for OD authoring
- If deliberation enabled: Section 14 (multi-agent deliberation) in full
- Sections 1-3 (principles, architecture, layers) if context allows

**1c. Read protocols (derived from spec — spec takes precedence if conflicts found):**
```
cowork/gosta-cowork-protocol.md          ← Full read (execution protocol)
cowork/deliberation-protocol.md          ← Full read if deliberation enabled; skim §1-§3 if disabled (for awareness)
```

**1d. Flag inconsistencies:**
If any protocol section contradicts the spec section it derives from, log the inconsistency to the session's shortfall log (if one exists) or note it for the Governor before proceeding. The spec wins.

> **Why this order matters:** The spec is the source of truth. Protocols operationalize the spec but may lag behind edits. Reading the spec first means you recognize drift when you see it in the protocols, rather than absorbing protocol errors as truth.

**Step 2 — Scaffold directory:**

*Code mode:*
```bash
mkdir -p sessions/[SESSION_NAME]/{domain-models,reference,signals,health-reports,decisions,deliverables,session-logs}
```

If deliberation is enabled, also create:
```bash
mkdir -p sessions/[SESSION_NAME]/deliberation
```

If evidence collection is enabled, also create:
```bash
# Subdirectories generated from session's domain models + fixed dirs (discovery, adversarial, raw)
# Pattern: osint/[domain-model-short-name]/ for each domain model, plus fixed dirs
# Example for 7 domains: osint/{fin-market,competitive,product-adapt,governance,regulatory,market-position,customer,discovery,adversarial,raw}
mkdir -p sessions/[SESSION_NAME]/osint/{[DOMAIN_DIRS],discovery,adversarial,raw}
```

*Cowork mode:* You cannot run bash. Tell the Governor the directory structure needed, then create files into it as subsequent steps proceed. The directory exists implicitly once the first file is written into it. If deliberation is enabled, include the `deliberation/` directory in the structure description.

**Pool-agent model check (Code mode only):**
If the session will use reference pools with >50 items or large document indexing (§18.5), verify the embedding model is available:

```bash
# Check if model exists
ls cowork/tools/pool-agent/models/model.onnx

# If missing — download and quantize (~90MB download, ~22MB result)
python3 cowork/tools/pool-agent.py setup-model
```

If the model file is missing, alert the Governor: *"The pool-agent embedding model is not installed. Reference pool semantic search and large document indexing will not work until it's set up. Run `python3 cowork/tools/pool-agent.py setup-model` to download and install it (requires internet, one-time setup). Shall I run it now?"* Do not silently skip this — sessions that need pool-agent will fail at build/query time without the model.

**Web search capability check (required when OSINT collection or external evidence gathering is planned):**

If the session includes an OSINT collection phase, evidence gathering from external sources, or any tactic that depends on live web data, verify web search works before proceeding to scaffold:

1. **Run a test query.** Execute a simple web search (e.g., search for the target vendor's name) and confirm results are returned.
2. **If web search is available:** Record in the bootstrap's Execution Capabilities: `Web search: verified (tool: [WebSearch/WebFetch/other])`.
3. **If web search is denied or unavailable:** Alert the Governor immediately:

   *"Web search is not available in this environment. OSINT collection agents will be unable to gather live evidence — they will fall back to training knowledge only (cutoff: [date]). This means: (a) no post-cutoff events will be captured, (b) evidence items cannot include verifiable URLs, (c) all evidence carries [TRAINING-KNOWLEDGE] annotation. Options: (1) Grant web search permission and re-verify. (2) Proceed with training-knowledge-only collection — evidence base will be weaker and §14.3.11 verification checks will have limited value since the primary hallucination vector (live web collection) is absent. (3) Pause session until web search is available."*

4. **If web search works for the main agent but not for subagents (Code mode):** When dispatching parallel collection agents as subagents, the subagents may not inherit web search permissions. Verify by dispatching a single test subagent with a web search task before dispatching all collection agents. If subagents are blocked: collect web search results in the main agent context first, then pass the raw results to subagents for structuring and classification.

Do not silently proceed with OSINT collection when web search is unavailable — the Governor must explicitly accept the degraded evidence base. A session that plans for web-sourced evidence but executes on training knowledge alone has a capability mismatch that affects every downstream phase.

**Step 3 — Copy protocol infrastructure:**

*Code mode:*
```bash
cp cowork/gosta-cowork-protocol.md sessions/[SESSION_NAME]/
cp cowork/CLAUDE.md sessions/[SESSION_NAME]/
```

If deliberation is enabled:
```bash
cp cowork/deliberation-protocol.md sessions/[SESSION_NAME]/
```

If evidence collection is enabled:
```bash
cp cowork/evidence-collection-protocol.md sessions/[SESSION_NAME]/
```

*Cowork mode:* Read `cowork/gosta-cowork-protocol.md` and `cowork/CLAUDE.md`, then recreate them as new files at the target paths. If deliberation is enabled, also copy `cowork/deliberation-protocol.md`. If evidence collection is enabled, also copy `cowork/evidence-collection-protocol.md`. Confirm with Governor before copying large files: "I'll copy the protocol file (~N lines) into your session directory — confirm?"

**CLAUDE.md customization:** `CLAUDE.md` is the Claude Code directive — it tells the AI how to behave when entering this session directory in future sessions. Copy the template first, then append a `## Session Directives` section at the bottom with session-specific content:
- Context loading order (references to OD, domain models, reference materials)
- Analytical standards or anti-sycophancy rules specific to this scope
- Framework feedback logging instructions (if dual-purpose session)
- Any Governor-specified behavioral constraints

**Do NOT override the Output Paths section.** The template CLAUDE.md defines canonical output directories (`deliverables/` for deliverables, `session-logs/` for session logs). Session directives must not redirect deliverables to `session-logs/` or any other directory. If you need to list expected deliverable filenames, list them with their canonical paths: `deliverables/[name].md`.

In Cowork mode, apply the same customization when recreating the file — the template content plus the session-specific `## Session Directives` section appended at the bottom.

**Step 4 — Copy template stubs:**

*Code mode:* `cp cowork/templates/{operating-document.md,learnings.md,gosta-framework-feedback.md} sessions/[SESSION_NAME]/`

If deliberation is enabled:
*Code mode:* `cp cowork/templates/synthesis-verification.md sessions/[SESSION_NAME]/`

*Cowork mode:* Read each stub from `cowork/templates/` and recreate at the target path.

Files to copy into `sessions/[SESSION_NAME]/`:
- `operating-document.md` — will be populated in Step 9
- `learnings.md` — stub, populated at retrospective (includes Deliberation Patterns and Domain Model Feedback sections when deliberation is enabled)
- `gosta-framework-feedback.md` — stub, populated when framework gaps are found
- `synthesis-verification.md` — (deliberation only) Governor's checklist for verifying Coordinator synthesis against actual position papers. Used after each deliberation cycle.

These are intentionally empty stubs at this stage.

**Step 5 — Copy or create domain models:**
- If reusing: copy specified files into `sessions/[SESSION_NAME]/domain-models/`
  - *Code mode:* `cp [source-path] sessions/[SESSION_NAME]/domain-models/`
  - *Cowork mode:* Read each source file and recreate at the target path
- If creating from source resources: follow `cowork/domain-model-authoring-protocol.md` (11-step extraction procedure). Uses `cowork/templates/domain-model.md` as the structural template and protocol §3.1 as quality rules.
- If creating from Governor expertise only (no source document): follow protocol §3.1.1 (first-cycle correction-derived procedure). The first cycle runs ungrounded with Governor drafts; Governor corrections become the raw material for the domain model, which is a required deliverable of the first cycle.

**Pre-built model note:** Domain models copied from prior sessions may have been created under earlier quality standards. Before running the gate on reused models, present this choice: "(a) Run quality gate and upgrade any gaps — AI-assisted, Governor reviews changes. (b) Use as-is with a grandfathering note — 'Model used successfully in prior session [X]; known gaps noted.' (c) Replace with new model." If the model was used in a completed, successful session, option (b) is acceptable.

**Run quality gate on every domain model (reused or new):**

| Check | What to verify | Fail action |
|---|---|---|
| Minimum concepts | ≥6 concepts in Core Concepts section | Warn Governor: "Model [name] has only [N] concepts. Minimum is 6. Expand or proceed with reduced analytical depth?" |
| Specificity test | For each concept: does the *description* explain how this concept applies specifically to this session's product/context, not just define it generically? Evaluate description content, not concept name — standard terminology is fine if the description differentiates. | Flag generic concept descriptions. Propose context-specific rewording of the description. |
| Distinctiveness test | For each Quality Principle: would this principle produce different results in another domain? If no, it's too generic. | Flag and propose rewrite. |
| Anti-pattern specificity | For each Anti-Pattern: is this already basic critical thinking? (e.g., "don't ignore data") | Flag and propose domain-specific alternative. |
| Application context | Does the model state what session/domain it's written for? | Add application context header. |
| Structure | Does the model have all 6 components? (Core Concepts, Concept Relationships, Quality Principles, Anti-Patterns, Hypothesis Library, Guardrail Vocabulary) | Warn: "Model [name] is missing [components]. Minimum viable: 3 components (Core Concepts + Quality Principles + Anti-Patterns). Full 6-component model recommended." |

After running the quality gate on all domain models, compile all failures. Present to the Governor with options per failed model:
- **Fix now** — AI will redraft the model based on the specific quality gate feedback. Governor reviews and approves the redraft. Do not proceed until the redraft is approved.
- **Proceed with warning** — Model used as-is. Outputs from this model carry a quality warning noting the specific gap.
- **Replace** — Use a different model instead.

Do not proceed to Step 6 until all models either pass the quality gate or the Governor has accepted a warning for each failure.

**Domain Model Adaptations requirement:** If any domain model received a quality gate WARNING (proceeded with warning), the Domain Model Adaptations section in the OD is **required** (not optional) for that model. The adaptations table must declare per-concept applicability (applies / does-not-apply / requires-interpretation) so agents score against constrained definitions rather than the model's generic framing.

**Step 5b — Query Evidence Archive (only if evidence collection is enabled):**

After domain models are finalized and before generating the evidence collection config:

1. Query the Evidence Archive (`cowork/evidence-archive/`) for existing evidence matching the session's target(s) and domains.
2. At Tier 0: use pool-agent to search an archived evidence index (if one exists). If no archive exists yet (this is the first evidence-collecting session), skip — report "No evidence archive found. This session will start fresh."
3. Report to Governor: *"Found [N] archived items for [target], [M] still within effective date, [K] expired."*
4. Governor decides: import relevant archived items into the session's evidence pool (copied, not linked — session evidence is self-contained), or start fresh.
5. Imported archived items are flagged for re-verification (evidence-collection-protocol §10.2) against current sources.
6. Gap analysis in the evidence collection config accounts for imported items — new collection focuses on gaps, updates, and expired-item replacements.

**Step 5c — Generate evidence collection config (only if evidence collection is enabled):**

After archive query (Step 5b) and before reference materials (Step 6), auto-generate the evidence collection configuration from the session's domain models:

1. Map each domain model's core concepts to candidate search queries (concept-to-query mapping)
2. Group domain models into collection agent categories
3. Generate discovery query templates from the session scope
4. Generate adversarial counter-framing from OD objectives
5. Account for archived evidence imported in Step 5b — reduce search scope for concepts already covered by current (non-expired) archived items
6. Present the evidence collection config to the Governor for review
7. Write to `sessions/[SESSION_NAME]/evidence-collection-config.md` (populated from `cowork/templates/evidence-collection-config.md`)

**Step 5d — Subagent capability test (only if evidence collection is enabled, Code mode only):**

After evidence collection config is finalized, before execution begins:

1. Dispatch a test agent with instructions to load WebSearch via ToolSearch and execute one search
2. Record result in `sessions/[SESSION_NAME]/osint/capability-test.md`
3. Report to Governor: *"Normal mode — agents will search independently"* or *"Pre-fetch mode — I will search, agents will analyze"*
4. No Governor decision required — this is automatic detection, not a configuration choice
5. In Cowork mode, skip this step — cowork-sequential mode is auto-detected from the session mode

Note: This replaces the existing "Web search capability check" for evidence collection sessions. The existing web search check (above) still applies for sessions that need web data without the full evidence collection pipeline.

**Step 6 — Copy reference materials** (if any specified). Preserve the consumption role assigned by the Governor in Group 3. Add a comment at the top of each reference file (or in a `reference/README.md` index) noting its role: `options-universe` or `context`.

**Narrative Options-Universe Gate (required when options-universe document is narrative-only):**

If the options-universe document does not contain an explicit, numbered item list (no section titled "Feature Inventory," "Item List," "Options," "Canonical Feature Inventory," or equivalent with enumerated entries), the AI must:

1. Derive a discrete item list from the narrative. Apply boundary-resolution judgment — each item must have a clear name, a brief description, and a boundary note specifying what it excludes (preventing classification drift during scoring). **The derived inventory must contain ONLY these three columns (name, description, boundary note). Do not add scoring dimensions, domain model classifications, adjacency types, priority levels, or any other evaluative columns. The inventory is a neutral input to deliberation — any classification added here anchors all agents before scoring begins.**

2. Present the derived list to the Governor BEFORE proceeding to Step 7 or OD authoring:

   *"I derived the following [N] items from [document name]. Before I run scoring against these, please confirm: (a) are any items missing? (b) are any items misclassified — merged or split incorrectly? (c) are the boundary notes accurate? [table] Confirm to proceed, or provide corrections."*

3. Wait for explicit Governor confirmation. Do NOT proceed to scoring or tactic generation until the item list is confirmed.

4. Log the derivation and confirmation as a signal: `options_universe_confirmed | [N] items | Governor confirmed [date]`. This signal is referenced at every subsequent phase gate to confirm that the scoring inventory is Governor-verified.

This gate applies only to `options-universe` role documents. `context` role documents do not require item list derivation.

**Step 7 — Review prior learnings** (if selected):
Read each selected learnings file. Review the "What Worked," "What Broke," and "Findings" sections. Apply this filter:
- **Include:** Entries about domain model quality, framework/protocol patterns, guardrail design, phase gate structure, or topic-specific insights that apply to the new scope's domain
- **Include (cross-domain):** Entries about AI reasoning patterns, session management, or Governor-AI interaction — these apply regardless of scope domain
- **Include (deliberation):** If the new scope has deliberation enabled, specifically review prior sessions' "Deliberation Patterns" sections (agent behavioral patterns, recurring disagreements, threshold calibrations) and "Domain Model Feedback" entries. These inform roster configuration, termination threshold tuning, and domain model adjustments before execution begins.
- **Skip:** Entries about operational metrics (signal counts, cost tracking, CI/CD) unless the new scope is also operational; entries about specific products or decisions that don't generalize

For each included entry, present it to the Governor with three options:
- **Incorporate into OD** — add as a guardrail, constraint, or assumption in the operating document
- **Incorporate into domain model** — add as a quality principle, anti-pattern, or hypothesis
- **Note but don't incorporate** — acknowledged but not structurally embedded

Record incorporation decisions in the session's `decisions/governor-decisions.md`.

**Step 8 — Create 01-scope-definition.md:**
Use `cowork/templates/scope-definition.md`. Populate from collected inputs.

Note: `00-BOOTSTRAP.md` is numbered 00 because it is the entry point for all future sessions — every future session reads it first. `01-scope-definition.md` is numbered 01 as the first content document. Both are created in this bootstrap session; the numbering reflects session re-entry order, not creation order.

**Step 9 — Draft operating-document.md:**

**OD authoring path decision:** Before drafting, determine which authoring path to use:
- **Direct authoring (default for simple/moderate scopes):** Follow the guidance below. Suitable when the Governor's goal, constraints, and success criteria are clear enough to decompose directly.
- **Structured OD Drafting Protocol (`cowork/od-drafting-protocol.md`):** Use when the Governor's input meets any of the following concrete triggers:
  1. **Complexity trigger:** Group 1 complexity is `complex` (5+ strategies expected)
  2. **Decomposition failure:** The goal statement from Group 2 resists clean decomposition into objectives — i.e., you cannot derive 2+ distinct, measurable objectives without making assumptions the Governor hasn't stated
  3. **Domain unfamiliarity:** The scope spans 2+ domains where the Governor self-reported low familiarity or provided no source material
  4. **Litmus test failure:** The goal statement from Group 2 fails the §21.3 litmus test (contains embedded timelines, numbers, or methods that need stripping before it qualifies as a goal)
  5. **Vague intent:** The Governor's input is expressed as a question rather than a structured brief ("I want to figure out X", "help me plan Y", "what should we do about Z")

  If any trigger is met, recommend the structured path: *"Your scope triggers [name the specific trigger] — I'd recommend using the structured OD drafting process, which asks targeted decomposition questions before authoring. Shall I use that, or proceed with direct drafting?"*

**Before drafting:** Read all reference materials with role `options-universe`. These contain the items the session will evaluate, sequence, or prioritize. Candidate tactics and strategies in the OD must be generated FROM this material — not invented from general knowledge. If no options-universe material exists, tactics are generated from domain model concepts and Governor input.

Follow GOSTA's five-layer hierarchy (see framework Section 9 for template, Section 21 for authoring guide). Include:
- Goal with guardrails (hard/soft severity, thresholds, recovery specs for soft)
- Objectives with measurable targets and deadlines
- Strategies with WMBTs (What Must Be True)
- Tactics with hypotheses, kill conditions, success metrics, bootstrap cycles
- Initial actions
- Review cadences (action cycle, tactic review, strategy review, goal review)
- Graduation stage: 1
- Multi-Domain Assessment section with deliberation mode setting
- **If deliberation enabled:** Full `## Deliberation` section populated from Group 3A inputs — agent roster table, cadence config, isolation mode, termination thresholds, and deliberation file structure. Use the OD template's Deliberation section as the structural reference.
- **If evidence collection enabled:** Full `## Evidence Collection` section populated from Group 3B inputs — topology, targets, agent count, adversarial mode, quality gate config, and evidence collection phase designation. Use the OD template's Evidence Collection section as the structural reference.

**Constraint-to-guardrail encoding (mandatory):** Every constraint the Governor provided in Group 4 must be encoded as a guardrail at the Goal level — one constraint, one guardrail. Do not leave constraints only in the scope definition; constraints without corresponding guardrails have no enforcement during execution. After drafting guardrails, verify: for each Group 4 constraint, does a guardrail exist that would catch a violation? If not, add one.

When populating guardrails, classify each as `mechanical` (explicit numeric threshold checkable by direct comparison) or `interpretive` (qualitative judgment required). All guardrails with clear numeric comparisons should be `mechanical`. Default: `interpretive`.

Formatting examples (not exhaustive — encode ALL Governor constraints, not just these):
- "Analysis only / no recommendations" → `G-Analytical: All output must be descriptive or explanatory. No prescriptive policy recommendations. Severity: hard. Evaluation: interpretive.`
- "No external comms" → encode as a hard communication guardrail (typically interpretive)
- "Regulatory constraint (GDPR, etc.)" → encode as a hard compliance guardrail (typically interpretive)
- "Budget cap $50K" → `G-Budget: Total spend ≤ $50,000. Severity: hard. Evaluation: mechanical.`
- "Self-serve constraint" → encode as a hard guardrail requiring purchase completable without sales calls or demos (typically interpretive)
- "Solo founder" → encode as a hard delivery constraint guardrail (typically interpretive)

**G-6 Deliberation Calibration (required when deliberation mode is enabled):**

If Deliberation Mode = enabled and an agent roster is defined, the G-6 traceability guardrail threshold MUST equal the agent roster size — not the general §14.7 multi-domain minimum of ≥3.

Calibration rule:
- N = number of domain agents in the roster (excluding COORD-1)
- Tolerated fallback proxies = number of agents whose failure is acceptable per-feature (default: 0 unless Governor specifies otherwise at roster definition)
- G-6 threshold = N − tolerated_fallback_proxies (floor: N if no fallbacks tolerated)

Validation check at OD authoring time: If G-6 threshold < N and no fallback proxy allowance is declared, flag as an OD authoring error. The AI must not proceed without correcting the threshold or getting explicit Governor acceptance of the lower floor with documented rationale.

The §14.7 minimum of ≥3 applies only when deliberation mode is disabled. When deliberation is enabled, the roster defines the floor — §14.7 is superseded.

**OD writing strategy (prevents output-length failures):** Do not attempt to write the entire OD in a single file operation. Complex ODs (5+ strategies, deliberation config, many tactics) will exceed output token limits and fail silently. Instead:
1. Write the file with the header, Goal (Layer 1), and Objectives (Layer 2).
2. Use Edit/append to add Strategies (Layer 3).
3. Use Edit/append to add Tactics (Layer 4) — including the scoring matrix, deliberation config, and kill conditions.
4. Use Edit/append to add Actions (Layer 5), review cadences, and the Deliberation section.
5. After all sections are written, read the complete file back to verify structural integrity before presenting to the Governor.

Present the complete OD to Governor for approval.

**OD Approval Loop:**
- If Governor approves: proceed to Step 10.
- If Governor requests changes: apply changes, re-present the modified sections, and ask for approval again. Repeat until approved. Do not proceed to Step 10 until the OD is explicitly approved.
- If Governor wants to discuss before deciding: discuss, then re-present when ready.
- If the Governor requests more than 3 rounds of changes, surface: "We've iterated 3 times. Options: (a) continue iterating, (b) accept the current version noting remaining concerns, or (c) redesign from a different angle." This prevents runaway loops and surfaces fundamental misalignment.

**Do NOT proceed until Governor approves the OD.**

**Step 10 — Create 00-BOOTSTRAP.md:**
Use `cowork/templates/00-BOOTSTRAP.md`. Set:
- Status: `active`
- Phase: `Phase 0: Bootstrap`
- Graduation Stage: `1`
- Context loading order pointing to all created files
- "What Happened Last Session": "Bootstrap session. Directory scaffolded, domain models loaded, OD drafted and approved."
- "What Is Pending": "Governor approval of Phase Gate 0 → Phase 1 transition."

**Step 11 — Present Bootstrap Phase Gate:**

```
## Phase Gate: Phase 0 (Bootstrap) → Phase 1

### Exit Criteria Assessment

| Criterion | Status | Evidence |
|---|---|---|
| Directory scaffolded | [met/not_met] | sessions/[name]/ with all subdirectories |
| Protocol and CLAUDE.md copied | [met/not_met] | Files present in session directory |
| CLAUDE.md output paths consistent | [met/not_met] | Session directives do not override canonical output paths (deliverables/ for deliverables, session-logs/ for session logs) |
| Domain models created/copied and quality-gated | [met/not_met] | [N] models, all passed quality gate / [issues noted] |
| Reference materials copied | [met/not_met] | [N] files in reference/ |
| Scope definition created | [met/not_met] | 01-scope-definition.md populated |
| Operating document drafted and Governor-approved | [met/not_met] | OD approved [date] |
| Bootstrap file created | [met/not_met] | 00-BOOTSTRAP.md populated |
| Evidence collection configured | [met/not_met/not_applicable] | Config populated, archive queried, capability tested / not applicable |
| Prior learnings reviewed | [met/not_met/not_applicable] | [N] learnings incorporated / skipped |

### Key Findings
- [Any issues, tensions, or observations from the bootstrap process]

### Blocking Tensions
- [Any unresolved issues that would prevent Phase 1 from proceeding. If none: "None identified."]

### Material Tensions
- [Tensions that don't block Phase 1 but should inform execution. To populate: scan each domain model's Hypothesis Library and Concept Relationships for competing claims, then check whether any Governor hypothesis conflicts with domain model consensus. Examples: "Domain A implies X; Domain B implies not-X — unresolved." "Governor hypothesis assumes Y is primary driver; no domain model confirms primacy." If none: "None identified."]

### Deliberation Assessment
- [If deliberation was already enabled in Group 1 and configured in Group 3A: confirm readiness. "Deliberation mode is enabled with [N] domain agents. Agent roster, cadence, and thresholds are configured in the OD's Deliberation section. Deliberation protocol and file structure are in place. Ready to execute deliberation when triggered."]
- [If deliberation was NOT enabled but 3+ domain models are loaded AND material tensions exist between domains: flag as a potential deliberation trigger per Framework §14.7. Ask Governor: "The material tensions above involve competing domain perspectives. Would you like to enable the Deliberation Protocol for high-stakes decisions in this scope? This invokes multi-agent evaluation (one agent per domain model) with structured disagreement resolution. Default: No — standard single-agent assessment with sequential domain consultation." If Governor says yes at this point: collect Group 3A inputs now and update the OD with the Deliberation section before proceeding.]
- [If deliberation enabled: verify the OD contains a complete `## Deliberation` section with roster table, cadence config, and termination thresholds. If any are missing, flag and fix before advancing.]

### Recommendation
[advance | iterate | restructure — with reasoning]

### Governor Action Required
YES — approve phase gate and advance to Phase 1.
```

Wait for Governor approval before proceeding to Phase 1.

### What Happens After Phase 1 Approval

Once the Governor approves the phase gate, execute this transition immediately:

1. Update `00-BOOTSTRAP.md`: set Status to `active`, Phase to `Phase 1: [first phase name from OD]`, and update "What Is Pending" to reflect the first action in the OD.
2. Emit a message to the Governor: "Bootstrap complete. Session is now in Phase 1. Ready to begin execution per the operating document. Shall I proceed with [first action from OD]?"
3. Wait for Governor confirmation before executing initial actions.

**Post-session — Evidence Archive promotion (only if evidence collection was enabled):**

After the Governor approves the final deliverable and the session concludes:

1. Coordinator presents the evidence pool summary to the Governor: total items, tier distribution, domains covered, quality gate results.
2. Governor selects which items to promote to the Evidence Archive (default: all Tier 1 + Tier 2 items that passed quality gates; Governor can include/exclude specific items).
3. For each promoted item, compute `effective_until` based on evidence-collection-protocol §12.3 domain-specific aging defaults. Governor can override per item.
4. Write promoted items to `cowork/evidence-archive/[target]/`.
5. Update the archive index for future pool-agent queries.

From Phase 1 onward, the protocol governs everything (§5.1). This startup file's job is done. Key operating rules:
- Follow review cadences defined in the OD
- Signal-first execution: write signal stub before each action, update after (protocol §6.3)
- Compute health at review points (protocol §7)
- Enforce phase gates at every phase transition (protocol §5.1)
- **Closeout file audit before completion signal** (protocol §5.5): After the final phase retrospective, list all session files, confirm each is populated or marked N/A, and flag any shortfall log entries with suggested fixes targeting files outside the session directory as post-session PCCA actions for the Governor

---

## Edge Cases

**Governor wants to start without domain models:** Not recommended. Without domain models, the AI reasons from general training data — every recommendation is ungrounded. At minimum, create 3-component models (Core Concepts + Quality Principles + Anti-Patterns) during bootstrap. The AI can draft these from the Governor's description of the domain.

**Governor selects fewer than 3 domain models:** Warn: "Fewer than 3 models limits cross-domain tension detection, which is GOSTA's primary analytical value. Consider adding [suggested domain] to provide a contrasting perspective." Note: the Deliberation Protocol requires a minimum of 3 domain models. With fewer than 3, deliberation mode is unavailable — use standard sequential assessment only. If the Governor already chose deliberation = yes in Group 1, this is a hard block: "You chose deliberation mode, which requires 3+ domain models. Please add at least [3 - N] more domain model(s) or disable deliberation."

**Governor chose deliberation but has incompatible settings:** If the Governor selects deliberation = yes but mode = cowork with more than 5 domain agents, warn: "Cowork mode single-session deliberation with 6+ agents is likely to exceed context limits. Options: (a) reduce to 5 agents by merging related domains, (b) use multi-session isolation, (c) switch to code mode for parallel execution."

**Governor selects more than 5 domain models:** Warn: "More than 5 models increases context consumption and scoring time. Consider whether all models add a distinct analytical perspective. Models with overlapping concepts can be merged."

**Multiple sessions need to share an OD approval:** Each session has its own OD. If the Governor wants to share structure, use the session launcher template to create each session separately, reusing domain models and reference materials.

**Governor is unavailable mid-bootstrap:** Save all progress. Update bootstrap file with current state. The next session picks up where this one left off — that's the protocol's stateless design.

---

## Maintenance Notes

**Version:** 1.6
**Depends on:** `session-launcher-template.md`, Cowork Protocol, Framework, Deliberation Protocol, Evidence Collection Protocol (`cowork/evidence-collection-protocol.md`), OD Drafting Protocol (`cowork/od-drafting-protocol.md`)

When the protocol or framework is updated, check:
- Quality gate criteria (Step 5) against protocol §3.1 and §5.2
- OD authoring guidance (Step 9) against framework Sections 9 and 21
- OD authoring path decision (Step 9) against `cowork/od-drafting-protocol.md`
- OD Deliberation section (Step 9) against deliberation-protocol.md §2.1 and OD template
- Phase gate format (Step 11) against protocol §5.1
- Closeout file audit reference (post-Phase 1 rules) against protocol §5.5
- Deliberation Assessment (Step 11) against deliberation-protocol.md §3.5
- Group 3A defaults against deliberation-protocol.md §2.1 calibration guidance and §3.0 round count guidance
- Group 3B defaults against evidence-collection-protocol.md and §14.8
- Evidence collection config template (Step 5c) against `cowork/templates/evidence-collection-config.md`
- Evidence archive promotion (post-session) against evidence-collection-protocol.md §12
- Domain model template (Step 5) against `cowork/templates/domain-model.md`
- Domain model extraction procedure (Step 5) against `cowork/domain-model-authoring-protocol.md`
