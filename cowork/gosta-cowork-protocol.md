# GOSTA-Cowork Protocol v3.15

**Purpose:** Defines how to run the GOSTA framework with a session-based AI (Claude Cowork or Claude Code) as orchestrator/executor, with a human Governor. No custom infrastructure required — just files and disciplined conversation.

**Dual-mode:** This protocol works in two environments:
- **Cowork mode** — Conversation-based (Claude Cowork, ChatGPT, etc.). AI is stateless between sessions. Context loaded via conversation or system prompt. All state lives in files. In Cowork mode, begin every session by asking: "Please share the contents of 00-BOOTSTRAP.md or tell me to read it."
- **Code mode** — Tool-based (Claude Code, Cursor, etc.). AI reads/writes files directly, uses git, runs scripts. Persistent within a session but not across sessions. See §18 for Code-mode specifics.

**Reusable:** Copy the `cowork/` folder into any new session. Project-specific configuration lives in the operating document and scope definition, not here.

**Reference:** GOSTA Framework — Agentic Execution Architecture. For framework navigation, see §0.3 (Reading Guide — Document Map, Implementation Tiers, Selection Guide).

---

## 1. The Two Actors

**Governor (Human):** Final decision authority. Defines goals, approves strategies, makes kill/pivot/persevere decisions, sets guardrails. The Governor is the only actor who can modify the operating document's goal, objective, and strategy layers.

**AI Session (Claude Cowork or Claude Code):** Operates in three concurrent modes (from GOSTA §6.2):
- **Authoring Mode:** Drafts OD elements, strategies, tactics, kill conditions. Governor reviews and approves.
- **Execution Mode:** Reads approved OD, generates work plans, dispatches actions, collects signals. Runs autonomously within approved bounds.
- **Governance Mode:** Computes health reports, compares A/B tests, detects conflicts, surfaces recommendations. Governor makes decisions.

**Role mapping to framework components:** The AI Session unifies the framework's Orchestrator (§7.1-7.2: planning, health computation, recommendations) and Executor (§7.3: action-level task execution) into a single conversational agent. When deliberation mode is enabled and triggered, the AI Session additionally plays the Coordinator role (synthesis, disagreement identification) and each Domain Agent role (domain-grounded position papers) in sequence. These are logically distinct roles with different authorities and constraints — see §7.5 for the role-switching protocol that enforces boundaries during single-session sequential deliberation. In Code mode, Domain Agents and Coordinator run as separate subagent processes, making role separation structural rather than behavioral.

Stateless between sessions — all persistent state lives in files.

---

## 2. Scope Types

### 2.1 Finite Scope

A bounded project with a defined end state and deliverable. Examples: product roadmap creation, market analysis, architectural design, competitive assessment.

**Characteristics:**
- Has phases that progress linearly toward the deliverable
- Ends when the deliverable is produced and accepted
- Review cadence is per-phase, not calendar-based
- Kill conditions are about approach viability, not ongoing metrics
- Success = deliverable produced, meeting quality criteria

**Phase progression:** Bootstrap → [Domain-specific phases] → Governor Review → Deliverable

### 2.2 Ongoing Operational Scope

A continuous operation with recurring cycles. Examples: content publication, sales pipeline management, product iteration, customer development.

**Characteristics:**
- Has recurring cycles (weekly action, monthly tactic review, quarterly strategy review)
- No defined end — runs until Governor decides to conclude
- Review cadence is calendar-based
- Kill conditions are about metric thresholds over time
- Success = sustained progress toward objectives

**Cycle pattern:** Plan → Execute → Signal → Review → Decide → Repeat

**Suggested cadence defaults:** Action cycle: weekly. Tactic review: every 2-4 weeks. Strategy review: monthly or quarterly. Goal review: quarterly. Adjust based on domain velocity — fast-moving domains (content, sales) use shorter cycles; slow-moving domains (hiring, infrastructure) use longer ones.

### 2.3 Common Elements (Both Scope Types)

Both types use the same:
- File structure (Section 3)
- Operating document format (Section 4)
- Signal format (Section 6)
- Health computation method (Section 7)
- Decision recording format (Section 8)
- Session lifecycle (Section 5)
- Scoring protocol (Section 7.6)
- Framework feedback mechanism (Section 10)

The difference is in cycle cadence and termination condition, not in structure.

---

## 3. File Structure

```
[session-name]/
├── 00-BOOTSTRAP.md              ← THE entry point. Every session starts here.
├── gosta-cowork-protocol.md     ← This file (or symlink to cowork/). How to operate.
├── 01-scope-definition.md       ← What this session is and why.
├── operating-document.md        ← The living OD. System configuration.
│
├── domain-models/               ← Knowledge that grounds reasoning.
│   └── [domain].md                 One file per domain model.
│                                   IMPORTANT: Domain models must be APPLIED to the
│                                   session's context, not generic encyclopedic
│                                   reference. See §3.1 for guidance.
│
├── reference/                   ← Raw inputs with typed consumption roles:
│   └── [ref].md                    options-universe = items being evaluated/
│                                   sequenced (feature inventories, backlogs,
│                                   strategy alternatives). AI MUST read
│                                   before OD tactic generation.
│                                   context = background material (research,
│                                   regulations, competitive analysis).
│                                   Read as needed. See framework §17.2.4.
│
├── signals/                     ← Append-only signal logs.
│   └── [date]-signals.md           One file per review period.
│
├── health-reports/              ← Output of review computations.
│   └── [date]-[type]-review.md
│
├── decisions/                   ← Governor decisions. Append-only.
│   └── governor-decisions.md
│
├── deliverables/                ← What the session produces.
│   └── [NN]-[name].md              Numbered sequentially (01-tension-analysis.md, etc.)
│                                   Each starts with: date, scope name, temporal validity, source tiers.
│                                   Tournament candidates: [NN]-[name]-cell-[X].md
│                                   (e.g., 01-blog-post-cell-A.md, 01-blog-post-cell-B.md).
│                                   Winner identified in tournament_selection decision.
│                                   Non-selected candidates retained for structural memory.
│
├── session-logs/                ← Episodic memory. One per session.
│   └── session-[NNN].md
│
├── session-status.md            ← Live dashboard. Overwrite-only.
│                                   Updated at every major checkpoint.
│                                   Shows current scope state at a glance.
│                                   Governor can watch in a separate terminal.
│
├── learnings.md                 ← Structural memory. Patterns, anti-patterns,
│                                   calibrated norms discovered across sessions.
│
├── gosta-framework-feedback.md  ← Shortfalls, gaps, enhancements discovered
│                                   while running. Feeds back to GOSTA spec.
│
├── deliberation/               ← (When deliberation mode is active only)
│   └── round-[NNN]/               One directory per deliberation round.
│       ├── [agent-id]-position.md    Position papers (Round 1) or response papers (Round 2+)
│       ├── interim-assessment.md     Coordinator interim assessment after each round
│       ├── synthesis-report.md       Coordinator final synthesis
│       └── proxy-[agent-id].md       (If agent failed) Coordinator-generated proxy. See Deliberation Protocol §7.1.
│
├── debug-logs/                 ← (When debug logging is enabled only)
│   ├── orchestrator-trace.md      Orchestrator's own actions + all dispatch records
│   └── [AGENT-ID].trace.md        Child agent self-reported execution traces
│
└── osint/                      ← (When evidence collection mode is active only)
    ├── capability-test.md          Execution environment detection result
    ├── evidence-index.yaml         Master index of all collected evidence items
    ├── evidence-manifest.md        Human-readable manifest for assessment agents
    ├── evidence-engagement-audit.md  (Path 2 only — non-deliberation sessions)
    ├── evidence-domain-reconciliation.md  Reconciliation report
    ├── [domain-1]/                 Evidence items by domain (dirs from domain models)
    ├── [domain-2]/
    ├── discovery/                  Open-ended discovery items
    ├── adversarial/                Adversarial agent items + verification report
    └── raw/                        Pre-fetch mode raw search output
```

**File conventions:**
- All files are Markdown for universal readability
- Signal and decision files are append-only — never edit existing entries, only add
- The operating document is versioned by date stamps within the file (not separate files)
- Session logs are numbered sequentially (session-001, session-002, etc.)
- The bootstrap file and session-status file are the ONLY files that get overwritten each session — bootstrap at session start/end, session-status at every major checkpoint

### 3.1 Domain Model Authoring

**When creating a domain model from source resources** (documents, regulations, book chapters), follow the step-by-step extraction procedure in `cowork/domain-model-authoring-protocol.md`. That protocol operationalizes the rules below and the template structure in `cowork/templates/domain-model.md`.

Domain models must be **applied and contextual**, not generic encyclopedic references.

**Wrong:** A concept table listing 30 Kaufman definitions with "Framework Layer Affected" columns. This gives the AI knowledge but no judgment criteria.

**Right:** Narrative prose that connects theory to the session's specific domain. Example: "The average CISO receives dozens of vendor pitches per week. A feature's marketability is partly determined by whether it can break through Preoccupation without requiring an extended education campaign."

**Rules:**
1. Each domain model must state its **Application Context** — what session/domain it's written for
2. Concepts should be organized by **theme**, not listed alphabetically
3. Each concept should include **domain-specific implications** for scoring or decision-making
4. Keep to ~120 lines per model (not ~220). Shorter, applied models produce better scoring than longer, generic ones
5. **Never run analysis against a keyword-only or name-only domain model.** Keyword models produce zero analytical value — no tensions, no reframing, just summaries. If the Governor provides only keywords, the AI must expand to a 3-component minimum (Core Concepts + Quality Principles + Anti-Patterns) and present for review before proceeding.
6. If extending a 3-component model to 4, add the **Hypothesis Library** first — it is the single highest-value component above the floor (validated in simulation: it generated non-obvious strategic recommendations that the other 3 components could not)
7. **User hypothesis injection:** At bootstrap, after domain selection, prompt: "Do you have specific hypotheses you want tested?" If yes, add user hypotheses to the relevant domain model's Hypothesis Library as `user-submitted` entries. During assessment, explicitly test user hypotheses alongside model hypotheses. In output, report user hypothesis status: confirmed / partially confirmed / not confirmed / insufficient data. This serves informed users who bring domain knowledge the pre-built models don't capture.
8. **Domain count bounds:** GOSTA works best with 3-5 domain models per scope. Fewer than 3 limits cross-domain tension detection — the core analytical value of multi-domain assessment. More than 5 increases context consumption and scoring time without proportional benefit. If the Governor selects outside this range, surface the trade-off and confirm before proceeding.
9. **Deliberation feedback as update source.** When deliberation mode is active, deliberation cycles produce domain model feedback signals (Deliberation Protocol §12.4): overridden recommendations suggesting miscalibration, concession patterns suggesting shallow reasoning, unused concepts suggesting irrelevance, and missing concepts suggesting gaps. These are surfaced in the `learnings.md` Domain Model Feedback section at strategy review cadence. The Governor reviews each proposed change and decides: apply (update the model), defer (need more evidence), or reject (scope-specific, not a model issue). Domain models are never auto-updated from deliberation feedback — Governor approval is always required.
10. **Retrieval faithfulness at authoring time (§14.3.2).** Agents cite domain model concepts during execution and deliberation. Concepts with vague boundaries are susceptible to narrowing (agent uses only one manifestation), broadening (agent applies beyond defined scope), or semantic drift (meaning shifts through paraphrasing). When authoring concepts: define what the concept does NOT include, provide 2-3 application examples to prevent fixation on one manifestation, and flag common misapplications. See the domain model template's distortion-prevention guidance for the full pattern.

### 3.1.1 First-Cycle Domain Model Creation (from Framework §21.11)

When an OD references a domain for which no domain model exists and no source material is available, the first execution cycle operates ungrounded. The Governor's judgment substitutes for domain knowledge (§21.11). This is acceptable for **one cycle only**.

**During the first cycle:**
- All agent outputs are presented as **drafts requiring Governor review**, not finished deliverables.
- The Governor's edits, rejections, and approvals are the primary quality signal.
- The AI tracks the Governor's correction patterns — these become the raw material for the domain model.

**After the first cycle (or first strategy review, whichever comes first):**

The AI drafts a domain model derived from the Governor's corrections, not from its own initial output:

1. **Collect correction patterns.** Review all Governor edits, rejections, and approvals from the cycle. Group by type:
   - Consistent rewrites of tone, framing, or vocabulary → candidate **Core Concepts** (what the Governor considers correct domain language)
   - Rejected content formats or approaches → candidate **Anti-Patterns** (what bad looks like in this domain)
   - Approval criteria the Governor applied → candidate **Quality Principles** (what good looks like)
   - Hard rejections with stated reasons → candidate **Guardrail Vocabulary** (what is forbidden)
   - Governor-suggested alternative approaches → candidate **Hypothesis Library** entries

2. **Draft the model.** Assemble into the template structure (`cowork/templates/domain-model.md`). Set Source to "Governor corrections from [session/cycle ID]" and note the limitation — this model is derived from one cycle of corrections, not from established domain literature. Minimum viable: 3 components (Core Concepts + Quality Principles + Anti-Patterns).

3. **Present for Governor review.** The Governor may approve, supplement with domain knowledge from their own expertise, or provide source materials for a fuller model (in which case, switch to `domain-model-authoring-protocol.md`).

4. **Run the quality gate** (startup.md Step 5 gate). Correction-derived models will likely fail the Specificity test on first draft — the AI may not understand *why* the Governor made certain corrections. Flag gaps explicitly: "I observed you consistently reject [X], but I don't have enough context to explain the underlying principle. Can you clarify?"

**The mandate (Framework §21.11):** Treat domain model creation as a **required deliverable** of the first cycle, not an optional enhancement. A second cycle without a domain model compounds ungrounded judgment — each cycle's errors become the next cycle's baseline.

**When Governor lacks domain expertise (Framework §21.11, `[ROBUST]`):**

If the Governor indicates uncertainty about domain model quality during step 3 above (e.g., cannot clarify domain principles when asked, defers domain judgment, or states limited familiarity with the domain), the AI should ask:

> "It sounds like this domain may be outside your core expertise. That's fine — we have three ways to build a reliable domain model:
> 1. **Source materials** — Do you have textbooks, industry standards, or regulatory documents for this domain? I can build the model from those instead of from your corrections.
> 2. **Domain expert** — Is there someone with domain expertise who could review the domain model? They wouldn't need to be involved in the rest of the session — just model review.
> 3. **Proceed with annotation** — I'll build the model from available information but mark it `[UNVALIDATED]`. All assessments grounded in it will carry that annotation until it's validated.
>
> Which approach works for you?"

If the Governor chooses option 1, switch to `domain-model-authoring-protocol.md` with the provided source materials. If option 2, proceed with model drafting and present to the designated expert for review before running the quality gate. If option 3, create the model with `[UNVALIDATED]` annotation in the model header; the AI must propagate `[UNVALIDATED-DOMAIN-MODEL]` in all health report assessments and Governor decision presentations that rely on concepts from that model, until the model is validated at a future strategy review.

---

## 4. Operating Document Format

The OD follows GOSTA's five-layer hierarchy. Use the template in `cowork/templates/operating-document.md`.

**Field complexity determination (before populating the template):** The OD template marks tactic fields with `[CORE]`, `[ROBUST]`, and `[ADVANCED]` conditional headers. Before drafting, determine which field complexity level the scope requires:
- **Always include `[CORE]` fields** — required for any GOSTA implementation.
- **Include `[ROBUST]` fields** if the scope adopts any of: A/B testing, domain model stacking, deliberation, or detailed dependency tracking. Check the scope's Multi-Domain Assessment configuration — if Independence Level ≥ 2 or Deliberation Mode = enabled, the ROBUST condition is met. Note: tournament execution fields are marked `[ESSENTIAL]` and are included when the tactic declares tournament mode — they do not require the ROBUST condition.
- **Include `[ADVANCED]` fields** if the scope uses metric lag modeling or metric prerequisites.
For inapplicable ROBUST/ADVANCED fields within an included level, write `N/A` rather than omitting the field — this makes the omission deliberate and auditable.

**OD Staleness Triggers** (from GOSTA §17.2.1):

The OD must be refreshed when any of these occur:
- Scoring reveals patterns that contradict OD assumptions
- Governor makes a decision that changes strategic direction
- A kill condition is evaluated and changes the tactic landscape
- External constraints change (regulatory, competitive, resource)
- 2 ungated phases or review cycles pass without an OD review

When an OD is flagged as stale, the AI must surface this at the start of the next session: "The Operating Document was last updated [date]. [Trigger] has occurred since then. Recommend refreshing before proceeding."

**OD Deliberation section (when Deliberation Mode = enabled):** The OD must include a `## Deliberation` section containing: Agent Roster table (agent ID, domain model, role), Deliberation Cadence (trigger, min/max rounds, new argument gate), Termination Thresholds (convergence, stall), Governor Interaction mode, and isolation mode (Cowork: single-session-sequential or multi-session). See Deliberation Protocol §2.1 for the full specification and startup.md Step 9 for the authoring procedure.

### 4.1 Guardrail Architecture (from GOSTA §5.1-5.3)

Every guardrail in the OD must declare:
- **Severity:** `hard` (zero-tolerance, halt immediately) or `soft` (recoverable). Default: `hard`.
- **Evaluation:** `mechanical` (numeric threshold, deterministic check) or `interpretive` (qualitative, requires AI judgment). Default: `interpretive`. See GOSTA §5.1.
- **Threshold:** The numeric or boolean boundary.
- **Recovery** (soft only): What the AI does when breached — must be concrete and executable without Governor input. Example: "defer excess hours to next cycle" not "handle appropriately."

**Violation detection:** At each action cycle (ongoing) or phase gate (finite), the AI checks every inherited guardrail:
1. Collect the guardrail chain: Goal guardrails + Objective guardrails + Strategy guardrails + Tactic guardrails
2. **Evaluate mechanical guardrails first** (§5.4 of the specification): For each `mechanical` guardrail, compare current metric value against threshold — this is a deterministic check with no AI interpretation. Report results as definitive pass/fail. Mechanical guardrails always receive `confirmed` epistemic classification (§14.3.8) for the evaluation logic. However, when the input signals feeding the comparison carry provenance flags (`[STALE]`, `[PROVENANCE-INCOMPLETE]`), note these alongside the result so the Governor can assess input data reliability independently.
3. **Then evaluate interpretive guardrails:** For each `interpretive` guardrail, assess using domain context, signal trends, and qualitative judgment. Report results with epistemic classification (§14.3.8).
4. If **hard** guardrail breached: halt execution, emit violation signal, escalate to Governor immediately
5. If **soft** guardrail breached at Stage 3+: apply declared recovery, log as `guardrail_recovery` in decision log, notify Governor at next review
6. If **soft** guardrail breached at Stage 1-2: escalate to Governor (same as hard)

**Spirit-vs-letter detection:** If an outcome technically meets a guardrail's letter but may violate its intent, emit a `guardrail_interpretation` signal. Present to Governor: the guardrail text, the observed outcome, the potential spirit violation, and a recommendation to tighten the language.

**Calibration check:** At OD creation and every OD refresh, verify that Metric Boundary guardrails are set above current baseline (for worse-is-higher metrics) or below current baseline (for worse-is-lower metrics). Flag any guardrail set at or below the starting state — it will fire from Day 0 and flood the signal pipeline.

**Cross-strategy guardrails:** Distribution-constrained guardrails (e.g., "max 60% of revenue from one channel") are evaluated BEFORE individual strategy decisions within the same review.

**Analytical guardrails (for analytical scopes):** Guardrails may express quality criteria rather than metric boundaries. These use categorical or structural thresholds (e.g., "each conclusion must reference ≥3 domains", "no assessment without source tier attribution"). Violation detection is by structural check at deliverable completion, not metric comparison at action cycles.

**Guardrail evaluation timing:** Guardrails declare their evaluation timing:
- `per-phase` — checked at every phase gate (default for operational guardrails)
- `deliverable` — checked only at scope completion when the deliverable is produced (for quality criteria that require the full output to evaluate, e.g., "multi-domain coverage", "bias balance")

Declare timing in the OD. If undeclared, default is `per-phase`.

**Analytical relevance guardrail:** For analytical scopes, add this guardrail by default: "Each domain assessment must contain at least one claim that directly addresses the user's question (or a decomposed sub-question)." This catches assessments that are topically related but analytically disconnected — a domain that describes its subject area without linking to the analytical question. Evaluation: after each domain assessment, check whether any claim directly answers or informs the user's question. If not, flag as "disconnected." This is distinct from the domain-overlap guardrail (which catches duplication); this catches irrelevance.

**Domain model replacement protocol:** When a guardrail violation is caused by input quality (bad domain model) rather than execution quality (bad tactic), the response is **replace**, not kill/pivot/persevere:
1. **Detect:** Guardrail violation or quality flag traced to a specific domain model
2. **Identify:** Which domain model(s) caused the failure
3. **Select replacement:** Present Governor with alternatives: (a) pre-built model from `domain-models/examples/`, (b) upgraded version of the current model, (c) new model built from source material using `cowork/domain-model-authoring-protocol.md`, (d) AI-expanded model from Governor-provided keywords (minimum viable: 3 components per §3.1 rule 5). Governor selects; if (c), Governor must provide or approve the source resource before authoring begins. If the replacement is a pre-built model (option a), ask the Governor for adaptation intent: Adapt or Preserve as independent lens (same criteria as startup.md Group 3).
4. **Re-execute:** Re-run only the replaced domain's assessment — do not re-run domains that passed
5. **Re-synthesize:** Run synthesis again with the replacement assessment alongside preserved good assessments
6. **Cost:** In a product context, charge only for the re-run portion (partial credit, not full analysis)

### 4.1a Analytical Frame Contract (from GOSTA §9.2, §21.2a)

For any scope where the deliverable answers an analytical question (assessment, evaluation, exposure analysis, market characterization, regulatory mapping, roadmap sequencing), the OD declares an **Analytical Frame Contract (AFC)** — a four-field declaration derived from the goal during bootstrap (startup.md Group 2A) and stored in the OD.

**Fields:**

| Field | Definition |
|---|---|
| **Stance** | Who the assessor stands alongside (e.g., dependent organization, buyer, market observer, policy maker, product team) |
| **Output Verb** | What the deliverable does (e.g., expose, evaluate, characterize, map, sequence) |
| **Failure Mode** | What the assessment protects against (e.g., unmanaged dependency, bad purchase, missed market shift) |
| **Prohibited Frame** | What the deliverable must NOT become — the frame that would answer a different question than the stated goal. "—" if no other frame applies. |
| **Verdict Vocabulary** (recommended) | AFC-consistent terms for deliverable verdicts. Reduces interpretive ambiguity at §12.12 validation. |

**When required:** Any analytical/assessment scope. Skip for non-analytical scopes (operational, content production, code implementation) where the deliverable is an artifact rather than an answer.

**Interaction with guardrails:** The AFC and guardrails are orthogonal. Guardrails constrain execution boundaries (what must not be violated). The AFC constrains the analytical frame (what question the session answers). A session may have a guardrail "no purchase recommendations" AND an AFC with Prohibited Frame "procurement advisory" — both enforce the same intent through different mechanisms. The guardrail is a self-attestation check; the AFC enables mechanical content-level validation (§12.12).

**Frame consistency rule:** When the OD declares an AFC, all subsidiary sections must be frame-consistent — every OBJ analytical question, STR rationale, TAC hypothesis, and deliverable description must be answerable from the AFC's Stance perspective and must use the AFC's Output Verb. F-16 (startup.md Step 9) enforces this at OD drafting time.

---

## 5. Session Protocol

### 5.1 Session Lifecycle (All Sessions)

Every session, regardless of type, follows this sequence:

**Step 1 — Orient.** Read `00-BOOTSTRAP.md`. Understand: What session is this? What phase/cycle are we in? What happened last session? What's pending? What does the Governor expect this session?

**Step 1b — State conflict resolution.** `[ROBUST]` After loading the bootstrap, cross-check state claims against authoritative sources before proceeding. If conflicts are detected between bootstrap, OD, and decision log:
1. **Decision log is authoritative for decisions** (append-only, tamper-evident). If the decision log records a `kill` but the OD still shows the tactic as `active`, the OD update was missed — apply the decision to the OD before proceeding.
2. **OD is authoritative for structure** (layers, entities, guardrails). If the OD contains entities not referenced in the bootstrap, the bootstrap summary is stale — regenerate bootstrap from the OD and decision log.
3. **Bootstrap is an informational summary.** When it conflicts with OD or decision log, regenerate from sources. Do not treat bootstrap state claims as overriding OD or decision log.
4. **Health reports are derived artifacts.** If input signals changed since the last health report, the report is stale — note this and re-derive at the next health computation step.
5. **If conflicts are detected:** Emit a `bootstrap_anomaly` signal listing each conflict with its resolution. Present the conflict summary to the Governor at the start of Step 3 (Execute) before taking any actions. If a conflict is ambiguous (e.g., two decision log entries that contradict each other), halt and ask the Governor to resolve before proceeding.

**Step 2 — Load context.** Read files specified in bootstrap's "Context Loading Order" section. At minimum: operating document + relevant domain models. For reviews: also load signals and prior health reports.

**Step 3 — Execute.** Perform the session's purpose (see session types below). **Before executing each action**, validate against the inherited guardrail chain (§4.1). If any hard guardrail would be violated by the planned action, halt and escalate to the Governor before proceeding. If a soft guardrail would be violated, apply the declared recovery (Stage 3+) or escalate (Stage 1-2). **Grounding check:** Every recommendation and analysis produced during execution must cite specific domain model concepts (§12.2). If the AI cannot ground a claim in a loaded domain model, it flags the claim as `[UNGROUNDED]` before presenting it.

**Step 3b — Deliberate (at decision points).** Before presenting any recommendation that requires a Governor decision (kill, pivot, persevere, phase advance, approve, reject), the AI must:
(a) Identify at least one **tension** — a point where different domain models, different layers of the hierarchy, or different evaluation criteria produce competing recommendations.
(b) Present the tension with each side's reasoning, grounded in specific domain model concepts.
(c) If no genuine tension exists, state explicitly: "All inputs agree on [recommendation]. No competing interpretation identified." This itself is a challengeable statement.

Each tension must be classified by severity:
- **Blocking** — Cannot proceed without Governor input. The AI must halt and wait for a decision.
- **Material** — Affects the outcome but has a defensible default. The AI states its default recommendation and proceeds unless the Governor overrides.
- **Informational** — Noted for completeness. No Governor action required.

Only Blocking tensions require explicit Governor response. This prevents tension fatigue — if every phase produces 5-8 tensions of equal apparent weight, the Governor stops engaging with them.

**Question-reframing tension:** A special subtype where the user's question decomposes into sub-questions with different answers (e.g., "Is quantum computing ready?" → "Ready to use? Mostly no. Ready to defend against? Yes, start now."). This is not disagreement between domains — it's the analysis revealing that the question itself contains multiple questions. Present as: "Your question contains N hidden questions with different answers." This is often the highest-value insight for naive users.

**Step 3c — Coherence check (at authoring time).** `[ROBUST]` After creating or modifying any OD element (tactic, strategy, objective, guardrail), run the semantic coherence checks from §12.7: C1 (kill condition evaluability — blocking), C2 (allocation arithmetic — auto-correct), C3 (temporal ordering — flag), C4 (entity reference integrity — blocking). At strategy review sessions, also run R1-R4 cross-entity invariants and the reconciliation check (§12.8). Coherence checks are lightweight at Tier 0 — the AI verifies mentally and reports results inline. The goal is to catch semantic issues *before* they enter the OD, not after.

**Step 4 — Record.** Write outputs to appropriate files (signals, deliverables, decisions). **Grounding check:** Before recording each signal, verify provenance (§12.3) and attribution (§12.4). Signals missing provenance are flagged `[PROVENANCE-INCOMPLETE]`. Signals missing attribution are rejected — assign attribution before recording.

**Step 5 — Update bootstrap.** Overwrite `00-BOOTSTRAP.md` with current state: what phase we're in, what was completed, what's pending, what the Governor needs to decide. **Prospective memory obligation (§18.2.5):** when updating "What Is Pending," scan all active tactics for approaching deadlines — kill conditions within 1 review cycle of their deadline, A/B test decision dates, deferred precondition timeouts — and surface them explicitly. Deadlines that exist only inside tactic specs are invisible until it's too late.

**OD mutation logging.** When any OD field is edited after bootstrap approval (goal correction, strategy revision, tactic modification, guardrail recalibration), append an entry to the session log's OD Mutations section (see session-log template):
- **What changed:** Field name + old value → new value (or summary if lengthy).
- **Cascade check:** Which downstream OD sections were reviewed for consistency with this change. List section IDs explicitly.
- **Cascade skipped:** Which downstream sections were NOT reviewed, with rationale (e.g., "TAC-3/TAC-4 — no dependency on goal framing" or "not checked — context pressure").
- **Changes applied downstream:** What was modified as a result of the cascade check.

For goal corrections specifically, the Goal Correction Procedure (startup.md Step 9) mandates AFC re-derivation + mini-PCCA. The mutation journal records the PCCA's scope and findings. This does NOT replace the Decision History entry required by the Goal Correction Procedure — both are written. The Decision History records the decision itself; the mutation journal records what was checked for cascade impact and what was not.

**Step 6 — Write session log.** Create `session-logs/session-NNN.md` capturing: date, session type, what was discussed/decided/produced, what domain models were consulted, any framework feedback items discovered.

**Step 6b — Update session status.** Overwrite `session-status.md` with current scope state. This file is the Governor's live dashboard — it must always reflect the latest checkpoint. Update triggers: session start, session end, phase gates, decision points, health computations, deliberation round completions, signal batch recordings, and any event that changes scope health or pending Governor actions. Use the template in `cowork/templates/session-status.md`. If deliberation is active, also update `deliberation-status.md` per Deliberation Protocol §1.

**Phase Gate Enforcement Protocol:**
1. At phase completion, the AI MUST produce a structured Phase Gate Request:
   ```
   ## Phase Gate: [Phase N] → [Phase N+1]
   **Exit Criteria Assessment:** [met | partially_met | not_met] per criterion
   **Key Findings:** [What was learned in this phase]
   **Blocking Tensions:** [list, if any]
   **Material Tensions:** [list with defaults]
   **Recommendation:** [advance | iterate | restructure]
   **Governor Action Required:** [YES — explicit approval needed | NO — proceeding with defaults]
   **Signal Coverage:** [N of M actions in this phase have completion signals in signals/. List any gaps.]
   **Synthesis Verification (if deliberation completed this phase):** [completed — verification.md at [path] | Governor skipped — acknowledged | N/A — no deliberation completed this phase]
   **Shortfall Log:** [If shortfall logging is enabled: N entries logged this phase / no entries. If no entries were logged, state: "No shortfalls encountered this phase" or explain why none were logged despite issues arising.]
   **Shortfall Cross-Check (if shortfall logging enabled):** For each Session Lifecycle Compliance item that required AI correction (stale/missing/template-only/incomplete), verify a corresponding shortfall entry exists. If not: [writing missing entries now — IDs: SFL-NNN | all corrections have corresponding entries | no corrections were needed].
   **Pre-Flight Validation Gate Results (from GOSTA §8.7):** Per-invariant outcomes at this phase boundary.
   - V1 Retrieval Contract Validation: [PASS — all (unit, pool) cells VALIDATED | WARN — N CORPUS-FIT-GAP / M VOCABULARY-MISMATCH cells with logged disposition | BLOCK — K unresolved ESCALATE cells | N/A — phase does not consume per-unit retrieval]
   - V2 Build Artifact Shape Verification: [PASS — shape matches expected chunking | WARN — suspicious N_emb == N_files for non-trivial inputs | BLOCK — downstream depends on chunk-level discrimination and shape is wrong | N/A — no build artifact produced this phase]
   - V3 Decision Spine Consistency: [PASS — OD/scope symmetric difference empty | BLOCK — K named entities in scope not in OD or vice-versa | N/A — only checked at Phase 1 entry]
   - V4 Continuous Capture Operationalization: [PASS — capture artifacts non-empty proportional to friction | WARN — capture empty AND friction observed; resolution: backfill OR explicit "no capture-class observations apply" | N/A — no continuous-capture mode flag active]
   - V5 Runtime Import Verification: [PASS — import-test succeeded | BLOCK — module(s) missing: list | N/A — only checked at first tool invocation per session]
   - V6 Declared Artifact Existence: [PASS — every CLAUDE.md / OD / scope-declared artifact present with non-zero content | BLOCK — missing-or-empty list with disposition: create-now / defer-with-reason / remove-from-declaration]
   - V7 Vertical-Fit on Inherited Artifacts: [PASS — concept coverage ≥70% | WARN — coverage below threshold; disposition: extend / accept-with-acknowledgment / substitute | N/A — only checked at Phase 1 entry]
   Any BLOCK row prevents phase advancement. WARN rows require explicit Governor acknowledgment. Reference §8.7.3 for invariant definitions and §8.7.2 for failure-mode semantics.
   **Session Lifecycle Compliance:**
   - 00-BOOTSTRAP.md reflects current phase: [yes — shows Phase N | no — stale at Phase M]
   - Session log for completed sessions in this phase: [session-NNN.md populated | missing | template-only]
   - Orchestrator trace entries since last gate (if debug logging enabled): [N entries covering M dispatches | incomplete — K of M dispatches missing, writing retroactive entries now | N/A — debug logging not enabled]
   - session-status.md: [current — updated at Phase N completion | stale — last updated Phase M | template-only — never populated]
   - deliberation-status.md (if deliberation enabled): [current — updated at Round N completion | stale — last updated Round M | template-only — never populated | N/A — deliberation not enabled]
   - Active feature toggles: [debug_logging: on/off | evidence_collection: on/off | shortfall_logging: on/off | AFC: declared/not_declared | deliberation: enabled/disabled]
   ```
2. **Session Lifecycle Compliance is AI-blocking, not Governor-blocking.** The AI must fix lifecycle compliance issues before presenting the gate to the Governor: stale bootstrap → update it; missing session log → write it; incomplete orchestrator trace when debug logging is enabled → write retroactive entries for all dispatches that occurred in the phase (if dispatch details cannot be reconstructed, log this gap as a shortfall entry); template-only session-status.md → populate from current state; template-only deliberation-status.md when deliberation is enabled → populate from deliberation state. The Governor does not see lifecycle compliance failures — they are pre-gate corrections.
3. If any Blocking tensions exist, the AI MUST NOT proceed until the Governor responds.
4. If no Blocking tensions exist and exit criteria are met, the AI states "Proceeding to Phase N+1 in next message unless Governor intervenes" and waits ONE message turn before continuing.
5. Compressing multiple phases into a single uninterrupted flow is a protocol violation.
6. If any exit criterion is `partially_met`, the AI must state what's missing and recommend: (a) iterate to close the gap, or (b) advance with the gap noted as a risk. Governor decides.
7. **Advance-with-degradation:** A 4th phase gate option alongside advance/iterate/restructure. Used when: the phase produced partial output, known failures are documented, and re-running would produce the same result. Subsequent phases proceed with the partial output AND the failure documentation as inputs. The failure itself becomes context — not a reason to halt, but information that shapes downstream work.
8. **Input fidelity attestation (Phase Gate 0→1 only):** The Phase Gate 0→1 request must include an additional field:
   ```
   **Input Fidelity (F-16):** [passed — 0 flags | N flags — all resolved by Governor (list flag IDs) | NOT RUN — blocking]
   ```
   If F-16 was not run during bootstrap, this is a Blocking Tension — the AI must run it before the gate can advance. If it was run and the Governor resolved all flags, the gate records the resolution. This field is Governor-verifiable: the Governor remembers whether they saw fidelity flags during bootstrap and can challenge a false "passed" attestation.

9. **Kill condition discriminating power check (Phase Gate 0→1 only):** Before advancing from Bootstrap to Phase 1, assess each tactic's kill condition for discriminating power given the known inputs. For each kill condition, ask: "Given this session's reference pool composition, domain model framing, and scope constraints, could this kill condition plausibly trigger?" If the answer is no — e.g., a kill condition of "fewer than 50% of articles map to any feature" paired with a pool curated specifically for that feature domain — flag it as `non-discriminating` and recommend the Governor recalibrate to a threshold that would actually detect a meaningful mismatch. Example recalibration: instead of "fewer than 50% of articles map to any feature" (absolute threshold, trivially passed), use "fewer than 4 of 8 features have ≥10 evidence items from a 139-article pool" (relative threshold, catches real misalignment). Non-discriminating kill conditions are not blocking — the Governor may proceed with acknowledgment — but they should be surfaced as a Material Tension in the Phase Gate assessment.

10. **Dependency Amendment Gate** `[ROBUST]` **(finite roadmap scopes with dependency graph deliverables):** If any Phase N synthesis output directly contradicts or requires modification of an approved Phase N-1 dependency graph, the amendment must be registered and presented as a named Governor decision BEFORE the subsequent sequencing phase begins. It is NOT activated by general phase gate approval.

   Procedure:
   - **Register:** Name the amendment `DEP-AMEND-NNN` with: feature ID, original classification (as approved), proposed amended classification, basis (which synthesis finding or agent position recommends the change), and a circular dependency flag (does the amendment resolve or create a cycle? — if creates, block until cycle is resolved separately).
   - **Present at gate:** Include DEP-AMEND-NNN as a distinct named decision item in the Phase Gate request, separate from the general exit criteria table: *"Named Amendment Decision Required — DEP-AMEND-NNN: [feature] classification change from [original] to [proposed]. Basis: [reference]. Circular dependency: [resolved / none / creates cycle at F-X]. Governor: Accept or Reject?"*
   - **Record:** Governor's decision on DEP-AMEND-NNN is written to `decisions/governor-decisions.md` as a standalone entry. Signal type: `dep_amendment_decision`.
   - **Timing:** The amendment is applied to the dependency graph only AFTER Governor Accept. Sequencing must not proceed with the amended graph until explicitly accepted. If rejected, sequencing proceeds with the original approved graph.

   This item applies when: (a) a dependency graph is a Phase N-1 deliverable, AND (b) Phase N synthesis produces a finding that changes a feature's tier, prerequisite, or ordering constraint. If neither condition is met, this item is skipped.

11. **Cross-Phase Consistency Check (CPCC)** `[ROBUST]` **(finite scopes with dependency graph + agent prerequisite registries):** Before applying Phase 1 dependency graph constraints to composite scores, the AI must execute a circular dependency check across the combined constraint set.

   Procedure:
   - **Collect:** Set A = dependency graph edges (F-X → F-Y means F-Y requires F-X). Set B = all prerequisite registry constraints from domain agents (F-Y launch requires F-Z operational).
   - **Merge:** Build a combined directed constraint graph. Tag each edge with its source (dependency-graph or agent-ID:registry).
   - **Cycle detection (mechanical):** For each feature F, check whether a transitive path F → ... → F exists. This check requires no domain judgment.
   - **Clean:** Log `CPCC: no circular dependencies detected across [N] features. Constraint application proceeding.` and continue.
   - **Cycle found:** Register as `CD-NNN`. Include: cycle path with edge sources tagged, constraint types involved, and at least two resolution options (e.g., scope amendment, sequencing split, prerequisite relaxation). Present CD-NNN to the Governor with resolution options. Constraint application is BLOCKED until Governor accepts a resolution and a clean re-run confirms the cycle is eliminated.

   Scope: Required when (a) a dependency graph is a Phase 1 deliverable AND (b) domain agents produce prerequisite registries during Phase 2 deliberation. If either condition is absent, CPCC is skipped.

### 5.2 Session Types

**Bootstrap Session**
- Trigger: First session of a new session
- Purpose: Create OD, ingest domain models, establish initial plan
- Output: Draft OD for Governor approval, populated domain-models/ folder
- Next: Governor approves/modifies OD, then first execution session
- **Keyword disambiguation:** When user keywords map to multiple candidate domain models (e.g., "politics" → Diplomatic & International OR Domestic Politics), present the options explicitly: "Your keyword [X] matches multiple analytical lenses: [Option A], [Option B]. Which best fits your question?" Do not silently choose one — this is a value-affecting decision the Governor must make.
- **Domain model quality gate:** After domain models are created or selected, run the 3 quality tests (from GOSTA §13.3): (1) Specificity — does each concept's *description* explain how it applies specifically to this session's product/context, not just define the concept generically? Evaluate the description content, not the concept name — standard terminology (Kaufman terms, article numbers) is fine if the description differentiates. For models with Preserve adaptation intent (startup.md Group 3), evaluate the Application Context header only — general-purpose concept descriptions are expected and correct; do not flag as specificity failures. (2) Distinctiveness — would this principle produce different results in another domain? (3) Anti-Pattern specificity — is this already basic critical thinking? If any test fails, warn: "This domain model may produce generic results. Consider adding Hypothesis Library/Guardrail Vocabulary, making concepts domain-specific, or using a pre-built model." If Governor proceeds with a flagged model, annotate the output with a quality warning. **Quality gate output must include:** (a) Overall grade: `PASS` / `PASS-WITH-FLAGS` / `FLAG-FOR-REVIEW`; (b) Flag count and severity breakdown: "PASS — 0 critical, 0 material, 3 informational flags"; (c) Flag severity criteria: CRITICAL = concept is generic to the point of being meaningless, MATERIAL = concept is real but underspecified (may produce undifferentiated scores), INFORMATIONAL = nuance lacking but concept is operable; (d) Governor decision prompt: for CRITICAL flags "Governor review required — flag may invalidate scoring," for MATERIAL flags "Governor discretion — flag may produce undifferentiated domain scores," for INFORMATIONAL flags "May proceed without review." **(e) Cross-model redundancy check (optional, multi-domain sessions):** When multiple domain models are loaded, identify concept pairs across models with overlapping scope. For each overlap, assess: do the concepts produce different evaluative *conclusions* on the same policy options (productive tension — no action needed), or similar conclusions from different frames (potential noise — flag for Governor review)? This check is informational and not blocking.
- **Guardrail feasibility check:** After the OD is drafted and before presenting the Phase Gate 0→1 assessment, verify that each guardrail referencing evidence or data inputs can be enforced given the session's actual inputs. For each guardrail: (1) identify what data source the guardrail requires (e.g., "counter-evidence receives equal weight" requires a pool that contains counter-evidence), (2) assess whether the reference pool, domain models, or other inputs can supply that data, (3) if a guardrail cannot be feasibly enforced — e.g., a falsification guardrail paired with a pool that is >70% incident-reporting and structurally underrepresents success cases — flag it as `feasibility-limited` in the Phase Gate assessment with an explanation of the structural limitation. The Governor decides: (a) proceed with the guardrail in observation mode (document attempts but don't treat absence of evidence as confirmation), (b) modify the guardrail to match available inputs, or (c) add supplementary inputs (e.g., Governor provides 5 success-case reference items to enable falsification). This check is informational — it does not block the Phase Gate, but it prevents the session from claiming to honor guardrails that its inputs structurally cannot support.
- **Structured input detection (informed users):** If the Governor's question contains multiple clauses with analytical connectors ("given that," "assuming," "because"), treat as pre-structured. Show detected structure: "I detected: (1) primary question, (2) embedded hypothesis, (3) analytical constraints. Is this correct?" If confirmed, skip decomposition and map directly to domain assignments.

**Execution Session**
- Trigger: Governor says "let's work" or equivalent
- Purpose: Execute actions from current plan, produce deliverables
- Output: Deliverables in deliverables/, signals in signals/
- Next: Continue execution or trigger review if phase gate reached

**Review Session**
- Trigger: Governor says "run [tactic/strategy/goal] review" or phase gate reached (finite) or cadence reached (ongoing)
- Purpose: Compute health, assess kill conditions, surface recommendations
- Output: Health report in health-reports/, recommendations for Governor
- Next: Governor makes decisions, recorded in decisions/

**Decision Session**
- Trigger: Governor has pending decisions from a review
- Purpose: Present trade-offs, record Governor's decisions, update OD if needed
- Output: Updated decisions/governor-decisions.md, possibly updated OD
- Next: Resume execution with updated direction

**Ad-Hoc Session**
- Trigger: Governor has a question, wants to explore, or needs analysis
- Purpose: Flexible — answer questions, run analysis, explore alternatives
- Output: Varies — may produce signals, may update learnings
- Next: Whatever the Governor decides

### 5.3 Scope-Type-Specific Session Patterns

**Finite scope typical flow:**
```
Bootstrap → Execution → Execution → Phase Review →
Governor Decision → Execution → Phase Review →
Governor Decision → ... → Final Deliverable → Closeout
```

**Ongoing scope typical flow:**
```
Bootstrap → Action Cycle → Execution → Execution →
Tactic Review → Governor Decision → Action Cycle →
... → Strategy Review → Governor Decision → ...
```

### 5.4 Mandatory Retrospective

Every session must include a Retrospective as the final phase before closure.

**Trigger:** Automatically activated when the primary deliverable is produced (finite scope) or when the Governor initiates `conclude_scope` (ongoing scope).

**Required outputs:**
1. `learnings.md` — Populated with: Validated Patterns, Anti-Patterns, Calibrated Norms, Cross-Domain Insights.
2. `gosta-framework-feedback.md` — Populated with: Framework gaps, protocol shortfalls, enhancement ideas, each with evidence.

**Enforcement:** The session status cannot be set to `completed` in the bootstrap file until both files contain substantive entries (not stubs).

### 5.5 Closeout File Audit

After retrospective outputs are written and before the completion signal is emitted, the AI MUST perform a file audit of the session directory.

**Procedure:**
1. List all files in `sessions/[name]/` recursively (excluding subdirectory contents that are append-only logs like `signals/`).
2. For each file that was scaffolded during bootstrap (templates copied in Step 2): confirm it is either (a) substantively populated (not a template stub), or (b) explicitly marked N/A with a one-line reason at the top of the file.
3. If any file remains a template stub, populate it or write the N/A disposition before proceeding.

**Shortfall propagation check:**
4. Read the shortfall log (if one exists for this session). For each entry with a "Suggested Fix" that targets a file outside the session directory (e.g., a protocol file, startup.md, a shared template), flag it to the Governor as a post-session PCCA action: "Shortfall [ID] suggests a fix to [file]. This is outside session scope — adding to post-session PCCA queue."
5. If shortfall logging was enabled (check the OD or bootstrap config) but the shortfall log file is empty or contains only the header: flag to the Governor — "Shortfall logging was enabled but no entries were logged. Either (a) no shortfalls were encountered (confirm explicitly), or (b) shortfall logging was dropped during execution (this is itself a shortfall — log it now with a retrospective entry)." The AI must not silently close a session with an empty shortfall log when logging was enabled.

**Session log coverage:**
6. Verify that `session-logs/` contains a populated session log for every session conducted. Compare session count against log file count. Template stubs (fields containing only placeholder brackets) count as missing. Populate gaps from memory before closeout — partial reconstruction is acceptable, absence is not.

**Bootstrap file currency:**
7. Verify that `00-BOOTSTRAP.md` reflects the session's final state — current phase, completion status, and final pending items. If it references an earlier phase as current, update before closeout.

**Closeout compliance summary (mandatory output before completion signal):**

8. The AI MUST produce a structured closeout compliance table listing every scaffolded file and its disposition. This table is presented to the Governor as part of the closeout:

   ```
   ## Closeout File Audit
   | File | Status | Action |
   |---|---|---|
   | learnings.md | [populated | N/A: reason | STUB — populating now] | [none | populating | marking N/A] |
   | gosta-framework-feedback.md | [populated | N/A: reason | STUB — populating now] | [none | populating | marking N/A] |
   | session-status.md | [current | stale | template-only — populating now] | ... |
   | deliberation-status.md | [current | N/A — no deliberation | template-only — populating now] | ... |
   | [each additional scaffolded file] | ... | ... |
   ```

   Any file with status STUB or template-only is blocking — the AI must resolve it to "populated" or "N/A: [reason]" before the completion signal can be emitted. The Governor sees this table and can verify it against the session directory.

**Enforcement:** The completion signal cannot be emitted until steps 1-8 are complete. Template stubs surviving to session close is a protocol violation.

---

## 6. Signal Format

Signals are the data that flows upward through the hierarchy. Logged in markdown files in the signals/ folder.

### 6.1 Signal Entry Format

```markdown
### SIG-[sequential-number] | [date]
- **Source:** [execution | governor | external | computation]
- **Type:** [metric | completion | decision | observation | blocker]
- **Attribution:** [Goal] > [Objective] > [Strategy] > [Tactic] > [Action]
- **Data:** [The actual signal — numeric value, status, observation text]
- **Confidence:** [complete | partial | estimated]
- **Source Tier:** [Tier 1 sensor/market data | Tier 2 institutional analysis | Tier 3 quality journalism | Tier 4 partisan media | Tier 5 government statements | Tier 6 social media/unverified]
- **Source Credibility Modifier:** [optional: -neutral, -belligerent, -pro-X, -mediator — refines the tier when source stance matters]
- **Temporal Validity:** [explicit window or domain default — e.g., "48h", "1 week", "structural"]
- **Provenance:** [How this data was obtained — URL, file path, computation formula, Governor statement, or "AI training data — no current source verified"]
- **Notes:** [Optional context]
- **Agent Source:** [Optional — deliberation mode only. agent_id | coordinator | system. See Deliberation Protocol §7.3.]
```

**Compound signals:** When a single source contains multiple distinct claims, record as one signal with a structured Data field listing each claim separately. Each claim should be individually tagged for confidence and temporal validity. Signal count = number of formal entries, not number of claims.

### 6.2 Signal Types (from GOSTA §7.4; see Appendix B.3 for full index)

| Signal Type | Emitted By | Required Fields | When |
|---|---|---|---|
| `action_completion` | Executor (AI) | status (completed/failed), deliverable_ref, duration | After every action |
| `metric_value` | Orchestrator (AI) | metric_name, value, unit, trend (improving/flat/declining) | At each review |
| `guardrail_violation` | Orchestrator (AI) | guardrail_id, severity (hard/soft), threshold, actual, violation_cause | When guardrail breached |
| `guardrail_interpretation` | Orchestrator (AI) | guardrail_text, observed_outcome, spirit_concern | When spirit may be violated |
| `guardrail_recovery` | Orchestrator (AI) | guardrail_id, recovery_applied, reversal_condition | After soft recovery applied |
| `kill_condition` | Orchestrator (AI) | tactic_id, status (safe/approaching/met), detail | At each tactic review |
| `market_event` | Governor or External | event_description, affected_strategies, severity | When external change detected |
| `governor_decision` | Governor | decision_type, target, reasoning | After every Governor decision |
| `agent_degradation` | System | component (orchestrator/executor/governor), fallback_used | When AI fails or produces invalid output |
| `signal_pipeline_degradation` | System | stale_tactics, total_active, stale_count | When >50% of active tactics have stale signals (§7.13.1) |
| `signal_pipeline_failure` | System | last_signal_date, cycles_without_signals | When no new signals arrive for >2× shortest cadence (§7.13.1) |
| `milestone` | Orchestrator (AI) | milestone_name, phase, completion_percentage | At phase gates or major checkpoints |
| `blocker` | Executor (AI) or Governor | blocker_description, affected_tactics, severity (hard/soft), resolution_needed | When execution cannot proceed without intervention |
| `knowledge_flag` | Executor (AI) | discovery_description, domain_relevance, source | When executor discovers new research, industry changes, or competitor approaches during action execution — feeds domain model evolution |
| `narrative_assessment` | Orchestrator (AI) | narrative_actors[], competing_narratives[], credibility_assessment | At each analysis cycle when the information environment itself is an analytical variable (e.g., conflict analysis, political analysis) |
| `environmental` | Orchestrator (AI) or System | condition_id, previous_state, current_state, affected_entities[], severity (informational/significant/critical) | When a condition on the environmental watch list (§7.14) changes beyond its threshold. At Tier 0: AI checks watch list at strategy review start and Governor reports changes. |
| `dep_amendment_decision` | Governor | amendment_id (DEP-AMEND-NNN), feature_id, original_classification, amended_classification, decision (accept/reject), basis | When Governor accepts or rejects a dependency graph amendment at a phase gate (§5.1 item 10). Written as a standalone decision entry in decisions/governor-decisions.md. |
| `options_universe_confirmed` | Governor | document_name, item_count, confirmed_date | When Governor explicitly confirms the derived item list from a narrative options-universe document (startup.md Step 6 Narrative Options-Universe Gate). Emitted before scoring begins; referenced at all subsequent phase gates. |
| `cost_exceeded` | Orchestrator (AI) | tactic_id, category, budget, actual | When a tactic's per-cycle cost in any declared category exceeds its budget (§13.3) |
| `cost_data_missing` | Orchestrator (AI) | tactic_id, category | When actions don't report cost metadata for a declared cost category (§13.3) |
| `claim_propagation` `[ROBUST]` | Orchestrator (AI) | claim_summary, source_agent_id, source_round, grounding_status (grounded/ungrounded/partially-ungrounded), boundary_crossed (identity/planning/communication/memory/retrieval/execution/oversight), propagation_flag | When a claim crosses an agent trust boundary during deliberation. Emitted by the Coordinator when synthesizing position papers or by the orchestrator when incorporating deliberation outputs into health computation. See Framework §14.3.10 and Deliberation Protocol §4.4 Propagation Audit. |
| `absence` `[ROBUST]` | Orchestrator (AI) | expected_event, window (start–end), source (tactic_id or scope), severity (early_warning/significant/critical) | When an expected event fails to occur within its defined window. Particularly important for human-participant domains (disengagement is silent). Expected events seeded from domain model patterns, refined by data. |
| `stakeholder_interaction` `[ROBUST]` | Orchestrator (AI) | interaction_type (collaboration/conflict/mentoring/disengagement/governance_act), participants[], tactic_id (or null), impact_assessment (positive/negative/neutral/unknown), description | When interactions between human subjects of the objective occur outside the Governor↔AI axis. Captures dynamics the framework otherwise cannot see. Presented as separate health report section at strategy review. |
| `tournament_selection` | Orchestrator (AI) | tournament_mode, tournament_runs, selected_candidate (deliverable_ref), behavior_space (constrained only: dimensions × values), cell_scores (constrained only: per-cell per-model scores), selection_method (governor_choice / highest_mean / highest_minimum) | After tournament evaluation completes and Governor selects winner |

**Attribution is mandatory.** Every signal must trace to a specific element: `Goal > Objective > Strategy > Tactic > Action`. Signals without attribution are noise — the AI must assign attribution before recording. System-level signals (agent_degradation, signal_pipeline_degradation, signal_pipeline_failure, market_event, environmental) use `system` or `goal_id` as attribution.

**Signal integrity check (from GOSTA §14.3.9).** When recording signals that contain both quantitative data and qualitative narrative, the orchestrator performs a direction check. If the narrative direction contradicts the quantitative direction (e.g., metric declining but narrative frames as "promising"), the signal is tagged `[DIVERGENCE]`. Health computation uses the quantitative data and discounts the qualitative framing for divergence-tagged signals. The divergence is logged in the health report's Risk Factors section.

### 6.3 When to Emit Signals

- After every action completion
- When the Governor reports an observation or outcome
- When a review computation produces derived metrics
- When an external event affects the scope
- When a blocker is encountered
- When a guardrail is violated or approaching violation
- When the AI fails or produces invalid output

**Action Completion Gate (signal-first pattern).** Signal writing is the first step of each action, not the last. The execution sequence for every action is:

1. **Before starting:** Write a signal stub to `signals/[date]-signals.md`: `| [ACT-ID] | in_progress | [timestamp] |`
2. **Execute:** Do the action, produce the deliverable.
3. **After completing:** Update the signal stub to completed status with deliverable reference.

An action is not considered `completed` until: (a) its primary output artifact exists at the specified path, and (b) the `action_completion` signal has been updated from `in_progress` to `completed` or `failed`. The AI MUST NOT begin the next action until both conditions are met. This is a hard gate, not a reminder.

**Tournament-enabled actions.** When an action is part of a tournament (§4.6), the completion gate applies per-candidate, not per-tournament:

1. **Before each candidate:** Write signal stub: `| [ACT-ID]-run-[N] | in_progress | [timestamp] |`
2. **Execute:** Generate the candidate deliverable constrained to its cell assignment.
3. **After each candidate:** Update stub to completed with deliverable reference.
4. **After all candidates:** Write `tournament_selection` signal (§6.2) after Governor selects the winner. The tournament is not complete until the selection signal exists.

Each candidate is an atomic action with its own signal. The tournament-level selection is a separate signal emitted after evaluation. This preserves the signal-first pattern while accommodating N sequential generations.

**Compressed signal format `[MINIMAL]`.** When context pressure or session constraints prevent full signal emission (8+ fields), the following one-line format is always acceptable:

`| [ACT-ID] | [completed/failed] | [deliverable-ref] | [timestamp] |`

An incomplete signal is acceptable, a missing signal is not. The stub written in step 1 guarantees that even if the session crashes mid-action, there is a visible `in_progress` record — absence of a completion update is itself a signal (action started but never finished).

### 6.4 Signal Triage

When signal sources produce high-volume raw data (web search, API feeds, sensor streams), the AI must apply a triage filter before formal recording:

1. **Relevance:** Does this signal relate to an active tactic, strategy, or objective? If not, discard.
2. **Source credibility minimum:** Filter out Tier 6 (social media/unverified) in non-Information domains. In Information/Intelligence domains, Tier 6 is permitted but tagged.
3. **Temporal currency:** Filter signals older than the domain's validity window (e.g., discard military assessments older than 48h in active conflict).
4. **Deduplication:** If multiple sources report the same claim, record one signal citing the highest-tier source. Note corroboration count.

Triaged-out data is logged as "reviewed, not recorded" in the session log for auditability — the Governor can review triage decisions and override.

**Per-domain triage thresholds:** Monitor triage pass rates per domain. If any domain's triage ratio falls below 25%, flag: "Domain model [X] may not align with available intelligence for this topic. [N]% of sources passed triage." This is a leading indicator that the domain model will produce weak analysis — catching it at triage is cheaper than catching it at synthesis. Offer: (a) proceed with warning, (b) expand search parameters for that domain, (c) replace domain model — if Governor selects (c), follow the Domain model replacement protocol (§4) which routes to the appropriate creation procedure.

---

## 7. Health Computation

Health computation happens in-conversation during review sessions. The AI reads signal data and evaluates against OD thresholds.

### 7.1 Tactic Health (from GOSTA §20.3-20.5)

**Inputs:** Kill condition thresholds from OD, relevant signals since last review.

**Attribution Validation (from GOSTA §14.3.4):**

Before computing health, the orchestrator validates attribution on every signal in the input set:

1. **OD Reference Check:** For each signal, verify that `tactic_id` references a tactic currently in the OD and `strategy_id` references a strategy currently in the OD. If the OD has been restructured since the signal was recorded, the reference may be stale.
2. **Orphan Detection:** Signals referencing killed tactics, removed strategies, or restructured objectives are flagged as `[ORPHANED]`. Common causes: tactic was killed in a prior cycle, strategy was pivoted and renamed, OD restructuring changed IDs.
3. **Orphan Disposition:**
   - `[ORPHANED]` signals are **excluded from health computation by default**. They do not contribute to composite scores, trend detection, or kill condition evaluation.
   - The orchestrator logs excluded signals: "Excluded N orphaned signals from TAC-X health computation. Orphaned references: [list tactic_ids/strategy_ids that no longer exist]."
   - If the Governor believes an orphaned signal remains relevant (e.g., a renamed tactic that preserved the same hypothesis), the Governor can reclassify it with updated attribution. This is a Governor decision (§8) — the orchestrator does not re-attribute autonomously.
4. **Provenance Cross-Check:** Signals already flagged `[PROVENANCE-INCOMPLETE]` (§12.3) retain their 50% weighting. Signals flagged both `[PROVENANCE-INCOMPLETE]` and `[ORPHANED]` are excluded entirely — orphan status takes precedence.
5. **Temporal Validity Check (from GOSTA §14.3.3):** Signals older than 2 review cycles without refresh are flagged `[STALE]`. Stale signals are not excluded — they are treated as lower-confidence inputs (equivalent to `[PROVENANCE-INCOMPLETE]` 50% weighting). The health report's Grounding Status section lists stale signals for Governor disposition: refresh, accept, or discard.

**Computation:**
1. **Metric Status:** Compare each success metric against its OD threshold:
   - `exceeded` — above success target
   - `on_track` — between target and kill threshold, trend improving
   - `at_risk` — within 20% of kill threshold, or trend flat/declining
   - `failing` — below kill threshold
2. **Kill Condition Evaluation:**
   - Check `bootstrap_cycles` — if tactic is still in bootstrap, status = `safe` with note "Bootstrap active (N/M cycles)"
   - If post-bootstrap: compare metric against kill threshold → `safe | approaching (within 20%) | met`
   - If `met`: check for metric prerequisites (v6.1 §10) — unmet prerequisites suspend kill assessment
   - For execution-only tactics (§8.1.1): evaluate completion-based kill condition (revision count, deadline, cost, scope). A tactic with `Kill Condition: N/A` is a C1 violation — apply default ("deliverable not accepted after 3 revision cycles") and flag for Governor confirmation.
   **Kill Proximity Alerting (from GOSTA §14.3.9):** When a metric falls within the OD's kill proximity alert threshold (default: 20%) of its kill threshold, the orchestrator must: (a) include the metric in the health report's Kill Proximity Alerts table, (b) track consecutive cycles at this proximity, (c) if approaching trajectory persists for 2+ cycles, flag `kill_proximity_silent` if the Recommendation section does not explicitly address the approaching metric. This is a mechanical check — the orchestrator cannot skip it by framing the narrative positively.
3. **Hypothesis Status:** Based on metric trend direction over last 3+ data points:
   - `holding` — trend improving or stable above target
   - `weakening` — trend flat or declining but above kill threshold
   - `falsified` — trend declining below kill threshold with no recovery
4. **Human Creative Input Rate** (if applicable): cycles_with_input / total_cycles. Separate tactic effectiveness from input availability.
5. **Composite Health Score:** Normalize metric statuses: `exceeded=90, on_track=70, at_risk=40, failing=10`. Composite = weighted average of normalized values (weights default to equal unless OD specifies). Use for cross-tactic comparison and exhaustion-reactivation selection.
6. **Signal-Recommendation Consistency Check (from GOSTA §14.3.9):**
   - Count signals trending positive vs. negative since last review.
   - If majority negative (>50% of non-stale signals trend negative) AND recommendation is `persevere`:
     - Flag `recommendation_divergence` in health report Risk Factors section.
     - Require explicit `divergence_justification` citing specific countervailing evidence (e.g., "3 of 5 signals negative but SIG-12 shows leading indicator reversal confirmed by 2 independent sources").
     - If no justification provided, escalate to Governor with flag: "Recommendation diverges from signal trend without justification — potential sycophancy."
   - If majority positive AND recommendation is `kill`:
     - No flag needed — conservative recommendations are not sycophantic.
7. **Signal Integrity Check (from GOSTA §14.3.9):** Before computing health, check all signals in the input set for `[DIVERGENCE]` tags. For divergence-tagged signals, use quantitative data only — discard qualitative framing. Log count of divergence-tagged signals in the health report's Risk Factors section: "N signals flagged for narrative-quantitative divergence. Qualitative framing discounted for these signals."

**Output:** Health report with recommendation: `kill | pivot | persevere`

Every health report must include a Risk Factors and Negative Signals section (§14.3.9). This section is subject to the sycophancy self-check: if the section is empty or contains only generic risk language for 2+ consecutive reports, the orchestrator must flag `sycophancy_risk: generic_risk_section` in the System Health section. The Governor may then request a directed adversarial review.

**Sycophancy self-check timing:** The self-check executes after Step 7 (Signal Integrity Check) and before output generation. The orchestrator loads the previous cycle's Risk Factors section (or `[NONE]` if this is the first cycle) and evaluates: (a) whether the current Risk Factors section is non-empty and substantive, (b) whether signal-recommendation alignment is justified, and (c) whether kill proximity alerts have been addressed. This comparison is part of the health computation sequence, not a separate post-hoc step. At Tier 0, the previous cycle's health report should be in the context loading order; at Tier 1+, the comparison is automated against the health report store.

**Epistemic Classification (from GOSTA §14.3.8):**

Every recommendation carries an epistemic classification:

- `confirmed` — Recommendation supported by complete metric data, consistent signal trends, and full attribution chain. Classification basis: ≥3 corroborating signals from ≥2 independent sources, no stale signals in computation, no `[PROVENANCE-INCOMPLETE]` flags on primary evidence.
- `information_gap` — Recommendation based on incomplete data. Classification triggers: >50% of input signals flagged `[STALE]` or `[PROVENANCE-INCOMPLETE]`, fewer than 3 signals in computation, kill condition assessed from single data point, or bootstrap period just ended with minimal data. Specify what data would strengthen the assessment.
- `conditional` — Recommendation depends on an assumption not yet verified. Classification triggers: WMBT status inferred from indirect evidence, environmental watch list condition has changed but impact is unclear, or recommendation reverses if a specific testable condition fails. Specify the condition and its test.

**Autonomous decision constraint:** At Stage 3+, `kill` or `pivot` recommendations classified as `information_gap` are NOT eligible for autonomous execution — they must escalate to Governor. The system does not make irreversible decisions on insufficient evidence.

The classification appears in the health report recommendation line:
`- **Recommendation:** kill | **Classification:** information_gap — metric data limited to 2 signals over 1 cycle; minimum 3 signals over 2 cycles needed for confirmed kill assessment`

**Kill-vs-Pivot precedence** (from GOSTA §4.3):

| Condition | Decision |
|---|---|
| Pivoted 2+ times with no improvement | **Kill** — always, regardless of other signals |
| Kill condition formally met AND bootstrap complete | **Kill** — unless Governor articulates why the signal is misleading |
| Kill condition approaching, hypothesis shows partial positive signal | **Pivot** — restructure, new kill date |
| Kill condition met BUT Governor overrides | **pivot_override** — must be justified and tracked |

**Cross-strategy kill sequencing (from GOSTA §8.5.3)** `[ROBUST]` — When 2+ tactics from different strategies face kill recommendations at the same review, the orchestrator must present them as a batch for joint Governor consideration, not sequentially. Sequential presentation creates ordering bias (the first kill frees resources that change the calculus for subsequent kills). Batch presentation includes: all pending kill recommendations, their combined resource impact, and cross-strategy reallocation options. Tactics in a kill batch transition through `killing` intermediate status (not directly to `killed`) until the Governor has resolved the full batch. The `killing` state prevents other processes from reallocating the tactic's resources prematurely.

### 7.2 Strategy Health

**Inputs:** Tactic health reports, WMBT condition assessments, signals.

**Computation:**
1. **WMBT Status:** For each what-must-be-true condition:
   - `assumed` — no evidence yet (pre-bootstrap or early)
   - `holding` — tactic results support the assumption
   - `at_risk` — tactic results are mixed or weakening
   - `falsified` — tactic results directly contradict the assumption
2. **Approach Validation:** Aggregate from tactic portfolio:
   - `confirmed` — majority of tactics healthy, WMBTs holding
   - `uncertain` — mixed signals, some kills but some healthy
   - `disproven` — all tactics killed or WMBTs falsified
3. **Tactic Portfolio:** Count: healthy / at_risk / killed / pending
4. **Cross-domain conflict check:** If this strategy's metrics improve while a sibling strategy's metrics deteriorate, flag as potential cross-domain conflict and surface to Governor.

**Output:** Strategy health report with recommendation: `kill | pivot | persevere`

**Epistemic Classification (from GOSTA §14.3.8):**

Strategy health recommendations and WMBT status assessments carry epistemic classification:

- WMBT status assessments: Each condition (holding/at_risk/falsified) is classified. `holding` classified as `information_gap` means "not falsified yet but evidence is thin, not actively confirmed." `falsified` classified as `information_gap` means "appears falsified but from limited/stale data — may be a data quality issue."
- Strategy recommendations: Same classification rules as tactic health. An `information_gap` strategy kill blocks autonomous execution at Stage 3+.

**Upward cascade governance (from GOSTA §4.3)** `[ADVANCED]` — When a child scope (§3.5) autonomously kills one of its own tactics or strategies, the parent scope must NOT automatically cascade that kill upward. The parent orchestrator treats a child scope's internal kill as a `status: at_risk` signal on the parent tactic that owns the child scope — not as a kill trigger on the parent tactic itself. The parent Governor evaluates the impact at the next parent-level review: (a) if the child scope's remaining capacity can still deliver, the parent tactic perseveres; (b) if the child kill materially undermines the parent tactic's hypothesis, the parent Governor decides kill/pivot/persevere; (c) if the child scope has been fully killed or concluded with `failed_and_killed`, the parent tactic receives this as an action failure and the parent's normal failure protocol applies. No child scope event — regardless of severity — triggers automatic kill, pivot, or status change on the parent tactic.

### 7.3 Goal Health (from GOSTA §20.12) `[ROBUST]`

**Inputs:** Objective progress (from §7.2), strategy health reports, environmental signals (§6.2), Governor observations.

**Computation (Tier 0 — qualitative assessment at strategy review):**
1. **Objective Portfolio Assessment:**
   - For each objective: compute metric progress (current_value - baseline) / (target - baseline) × 100%. Deadline check: elapsed_time / deadline × 100%. If >75%, emit deadline warning signal. Strategy portfolio: count active/killed/exhausted strategies per objective. If all strategies under an objective are killed/exhausted with <50% objective progress: flag as objective failure, escalate to Governor.
   - Portfolio assessment: **strong** (majority on_track or exceeded), **moderate** (any at_risk, none failing), **weak** (majority failing or only one objective on_track).
2. **Environmental Alignment:**
   - Review environmental watch list entries (from OD). Check for changes since last goal review.
   - Assessment: **aligned** (watch list conditions stable, no significant environmental signals), **drifting** (accumulating significant signals or moderate watch list changes), **misaligned** (critical environmental signal or major watch list condition changed).
3. **Goal Health Composite:**
   - **healthy:** portfolio strong or moderate AND environment aligned
   - **at_risk:** portfolio moderate AND environment drifting, OR portfolio weak AND environment aligned
   - **reassess:** portfolio weak AND environment drifting/misaligned, OR any portfolio AND environment misaligned
4. **Recommendation:** maintain (healthy) | investigate (at_risk) | reassess (reassess). "Reassess" is NOT a kill — goals are directional. It means the Governor should review whether the goal's objectives still serve the intent given changed conditions.

**Output:** Goal health report (use `cowork/templates/health-report.md` Goal Health section)

**Epistemic Classification (from GOSTA §14.3.8):**

Goal health recommendations (`maintain | investigate | reassess`) carry epistemic classification. A `reassess` recommendation classified as `information_gap` means: "environmental data suggests reassessment may be needed, but the data is thin — verify environmental change before restructuring goals." A `reassess` classified as `conditional` means: "reassessment needed if assumption X holds — monitor X before committing to goal restructuring."

**Cross-Objective Tradeoff Detection (from GOSTA §20.12)** `[ROBUST]` — At each strategy review, when a scope has 2+ objectives under the same goal, the orchestrator checks whether any objective's declining metrics are temporally correlated with another objective's improving metrics. If correlation is found with a plausible causal mechanism (shared resources, shared customer base, operational capacity conflict), surface as `cross_objective_tradeoff` finding in the health report. Governor resolves via: `accept_tradeoff`, `constrain_improvement`, `rebalance_portfolio`, or `decompose_metric`. Log as `decision_type: cross_objective_tradeoff`. Unresolved tradeoffs escalate after 2 consecutive strategy reviews.

### 7.4 Phase Gate Assessment (finite scopes)

**Output:** Phase gate report with recommendation: `advance | iterate | restructure`

### 7.5 Multi-Domain Assessment

When the operating document references multiple domain models, the AI must consult them systematically — not blend them into a single undifferentiated analysis.

**Domain count bounds:** Minimum 3 domains for cross-domain tension surfacing — below 3, there are insufficient pairwise comparisons to produce meaningful disagreement. Maximum 5 domains at Tier 0 — beyond 5, pairwise comparison count (10 pairs) overwhelms synthesis and extends execution time past acceptable thresholds.

**Independence levels (three-level escalation model, from Framework §14.7):**
- **Level 1 — Conceptual Isolation (inline):** Same pass, but AI explicitly separates domain reasoning into labeled sections. Use when: domains are well-understood and decision is low-stakes.
- **Level 2 — Sequential Isolation (default):** Same agent scores one domain completely before the next. No back-revision. Use when: agent isolation is expensive and domains are sufficiently distinct. **This is the default.**
- **Level 3 — Deliberation (multi-agent):** Each domain model is assigned a dedicated Domain Agent that produces formal position papers. A Coordinator identifies disagreements, formulates targeted prompts, and produces a Synthesis Report. The Governor completes a pre-deliberation review (Framework §6.1) before Round 1, updating existing information channels as needed. Use when: 3+ domain models are active, Level 2 produced materially different per-domain recommendations, and the decision is high-stakes or the Governor requests adversarial evaluation. Governed by the Deliberation Protocol (cowork/deliberation-protocol.md, v0.7). Note: convergence can only trigger early termination after **Min Rounds** (Deliberation Protocol §5.1) — this hard floor prevents premature consensus before all domains have had sufficient exchange.

When deliberation mode is active, the orchestrator tracks sycophancy indicators across deliberation cycles per §14.3.9. If `low_dissent_frequency` is flagged (unanimity rate >60% across 3+ cycles with <1.0 mean hard disagreements), the orchestrator surfaces this in the next health report's System Health section: "Deliberation independence concern: [N] of [M] deliberations reached Round 1 unanimity with low dissent. Deliberation may not be adding adversarial value. Governor options: (a) continue monitoring, (b) add contrarian domain model to roster, (c) redact OD strategy rationale from shared context for one cycle to test anchoring."

**Escalation triggers:**
- Level 1 → Level 2: AI detects that a single-domain analysis would produce a different recommendation than the blended multi-domain analysis. Or: Governor requests independent assessments.
- Level 2 → Level 3: Per-domain recommendations are materially different AND decision meets deliberation criteria (strategy kill, feature sequencing, cross-domain conflict with 3+ domains). Or: Governor requests deliberation.

The Operating Document should declare which level is the baseline and whether deliberation mode is enabled.

**Level 3 in Cowork mode — two isolation options:**

- **Single-session sequential (default):** The AI Session plays all deliberation roles (Domain Agents, Coordinator) within one conversation, switching roles explicitly. Each role transition must be announced with a labeled boundary marker (see OD template §Role-Switching Protocol and Deliberation Protocol §8.2 Role-Switching Protocol). The AI loads only the assigned domain model when acting as a Domain Agent, and must not reference reasoning from prior agents' position papers. Back-revision of completed position papers is prohibited. This is practical for 3-5 agents but carries **role-bleed risk** — the Coordinator may be subtly biased by the domain positions it just wrote. Governor spot-checks synthesis against position papers per §12.5 (Synthesis Verification) to mitigate. If role-bleed is detected (Coordinator synthesis echoes last agent's framing without attribution), escalate to multi-session isolation or add explicit de-biasing step between last Domain Agent and Coordinator.

- **Multi-session:** Each Domain Agent runs in a separate conversation session. Coordinator runs in a subsequent session that reads all position paper files. Expensive (N+2 sessions for N domains per round) but provides true isolation. The Deliberation Protocol §8.2 specifies multi-session details.

**Role identity in single-session sequential:** The AI Session's role during deliberation is NOT "AI Session acting as Orchestrator" — it is the specific role it has announced (e.g., "Agent VC-1" or "Coordinator COORD-1"). The Orchestrator/Executor role is suspended for the duration of the deliberation. This distinction matters: the Coordinator must synthesize without advocacy, even though the same AI wrote all the position papers moments earlier. The role-switching protocol in the OD template enforces this boundary through explicit announcements and context constraints.

**Level 3 in Code mode:** Uses parallel subagent invocations (§18.6). Each agent receives the §8.5 three-element framing (protocol context, Governor oversight, domain scope boundary) to prevent refusals. Role separation is structural — each subagent is a separate process with no shared state.

**When required:**
- At every strategy review when 2+ domain models are referenced
- At any Governor decision point where the OD references 2+ domain models
- During feature/tactic prioritization that scores against multiple domain criteria

**Output:** Structured comparison showing each domain model's recommendation and the tensions between them.

**Information gap handling:** When deliberation or multi-domain assessment produces findings classified as `information_gap` (§14.3.8), the orchestrator logs the specified missing data as a signal collection target in the next cycle's action list. The orchestrator emits a `knowledge_flag` signal when the gap is resolved.

**Interpretive guardrail escalation:** When 2+ interpretive guardrails produce ambiguous results (`near-violation` or `unclear` status) in the same review cycle, and deliberation mode is enabled, consider escalation to Level 3 deliberation for multi-agent evaluation of the guardrail cluster.

**Dispatch Preamble (mandatory for every agent dispatch when any injectable feature is active):**

Before dispatching any agent (evidence collection, deliberation, deliverable drafting), the orchestrator assembles the Dispatch Preamble by checking each injectable feature:

| Feature | Condition | Injection Content |
|---|---|---|
| AFC | OD declares an AFC (§4.1a) | "Your assessment must [verb] from the perspective of [stance]. The failure this assessment protects against is [failure mode]. Do NOT produce [prohibited frame]." |
| Debug logging (§19.4) | Debug logging = enabled | Standard debug logging injection block per §19.4 |
| Evidence loading strategy | Evidence collection = enabled AND agent will consume evidence | Per evidence-collection-protocol §6.4: either evidence file paths (direct load) or pool store path + concept-to-query mappings (pool-agent retrieval), based on per-domain item count vs. threshold. |

**Assembly rule:** The orchestrator concatenates all active injection blocks into a single preamble block. The preamble is prepended to the agent's task-specific prompt.

**Dispatch Verification Check:** After assembling the dispatch prompt and before sending, the orchestrator performs a mechanical scan:

1. If AFC is active: scan the assembled prompt for the AFC Output Verb term. If absent, halt and fix. If Prohibited Frame is not "—" (none), also scan for the Prohibited Frame term. If absent, halt and fix. If Prohibited Frame is "—", skip the Prohibited Frame scan (there is no frame to prohibit).
2. If debug logging is active: scan for the §19.4 marker `<!-- DEBUG LOGGING — protocol §19 -->`. If absent, halt and fix.
3. If evidence loading strategy is active: scan for either evidence file paths (at least one `osint/` path) or a pool store path (`osint/pool-store/`). If neither is present, halt and fix.
4. Log the verification result to orchestrator-trace.md: `DISPATCH [agent-id]: preamble verified [AFC: yes/no] [DEBUG: yes/no] [EVIDENCE: direct/pool-agent/N/A]`

This replaces separate independent injection points that each require separate protocol compliance. One mechanism, one verification check, one failure point to monitor.

### 7.5a Evidence Collection Integration (from GOSTA §14.8)

When evidence collection mode is enabled for a session, the following integration points apply:

**Phase execution additions:**
- Evidence collection runs during its designated phase (specified in the OD's Evidence Collection section). All quality gates (source verification, evidence quality audit, adversarial review, §14.3.11 verification) must pass before the phase gate.
- Evidence-domain model reconciliation (evidence-collection-protocol §10.8) must complete before any assessment phase begins — whether that assessment uses deliberation or single-agent evaluation.
- The evidence collection configuration (`evidence-collection-config.md`) is a session file referenced alongside the OD.

**Evidence engagement during assessment:**
- When evidence collection is enabled AND deliberation is active: agent dispatch prompts include evidence engagement instructions (3-category citation: OSINT-ID, `[reference-pool: SOURCE-ID]`, `[training-knowledge]`). The Coordinator performs an evidence engagement audit per deliberation round. Scoring signals include an `evidence_basis` field (§14.3.3 extension). The synthesis report includes an Evidence Citation Index (§14.3.5 extension). The Propagation Audit includes `[EVIDENCE-SUPPORTED]` and `[EVIDENCE-PROVENANCE-LOST]` flags (§14.3.10 extension). See evidence-collection-protocol §10.7 Path 1.
- When evidence collection is enabled WITHOUT deliberation: the single assessment agent's prompt includes the same engagement instruction. Post-assessment audit by the coordinator. See evidence-collection-protocol §10.7 Path 2.
- Sessions without evidence collection use the existing §14.3 pipeline unchanged — no engagement audit, no `evidence_basis`, no Evidence Citation Index.

**Evidence Archive:**
- Framework-level evidence archive at `cowork/evidence-archive/`. Organized by assessment target.
- New sessions query the archive during bootstrap (startup.md Step 5b) and import relevant items.
- Post-session, Governor selects items to promote to the archive (startup.md post-session procedure).

### 7.6 Scoring Protocol (from GOSTA §20.10)

When scoring features, tactics, or options against domain model criteria:

**Scale (from Framework §20.10):** 1-10 integers. No half-points. No false precision.
- 1-2: Absent / negligible — the option does not address this criterion
- 3-4: Weak — marginal relevance, significant gaps
- 5-6: Moderate — functional but not differentiated
- 7-8: Strong — clear advantage, well-aligned
- 9-10: Exceptional — dominant on this criterion (rare)

**Aggregation:** Compute composite score as weighted average across criteria. Report the spread (min/max across criteria) alongside the composite — a feature scoring 7.0 composite from [6, 7, 7, 8] is very different from 7.0 from [3, 5, 10, 10]. The OD MUST declare the aggregation method: `mean` (default), `median`, or `trimmed-mean` (excludes highest and lowest agent per dimension). If a structural inversion pattern is accepted by the Governor (e.g., one agent systematically scores inversely on a class of features), note the estimated composite depression or inflation in the scoring matrix header so consumers of the scores know the systematic effect.

**Batch calibration:** When scoring >10 items, score 3 representative items first (one expected-high, one expected-mid, one expected-low) to calibrate the scale. Then score the remainder. Re-calibrate if scores cluster unnaturally.

**Per-domain anchoring (multi-domain scoring):** When scoring items across multiple domain models using Level 2 Sequential Isolation, the initial batch calibration establishes anchors for the first domain only. Before beginning each subsequent domain's scoring pass, define 3 reference anchors for that domain: one Strong example (7-10), one Moderate example (4-6), one Weak example (1-3), each with a one-line rationale grounded in that domain's concepts. These anchors serve as consistency references for all scores within that domain. If the total scoring decisions exceed 30 (e.g., 10 items × 3 domains), perform a mid-pass consistency check at the halfway point of each domain: compare the score just assigned against the domain's anchors and the first 3 scores in that domain. If drift is detected (scores have shifted >1 point from where the anchors would place equivalent items), flag and recalibrate before continuing.

**Regulatory adjustments:** Regulatory compliance scores should cap upward adjustments at +1.5 points to prevent compliance-driven features from dominating purely on regulatory weight.

### 7.7 Dependency Validation (from GOSTA §20.11)

When generating sequences (roadmaps, implementation orders, phase plans):

**Representation:** Dependencies are a DAG (directed acyclic graph). Each item declares its prerequisites.

**Validation rules:**
1. No item may appear in a sequence before all its prerequisites
2. Topological sort determines the minimum valid ordering
3. When multiple valid orderings exist, score each by composite value (sum of weighted scores × position discount)

**Enforcement:** Before presenting any sequence to the Governor, the AI must verify all dependencies are satisfied. In Code mode, this can be automated; in Cowork mode, the AI must visually verify.

### 7.8 A/B Testing (from GOSTA §4.2)

A/B testing is the mechanism for comparing competing tactics or competing strategies using shared metrics.

**Tactic-level A/B:** Two tactics under the same strategy test different approaches to the same hypothesis. Declare in the OD: which tactics are A/B variants, shared success metrics, comparison methodology, and minimum duration before comparison.

**Strategy-level A/B:** Two strategies compete for the same objective. Declare: which strategies are variants, shared objective metrics, activation schedule (sequential or parallel).

**At Tier 0 (stateless execution), A/B testing is sequential, not parallel.** Run Variant A for N cycles, then Variant B for N cycles, and compare. The AI tracks results in the signal log. Statistical rigor is reduced but the hypothesis-testing discipline is preserved.

**Comparison protocol:**
1. Both variants must run for the declared minimum duration (bootstrap + evaluation period)
2. At comparison time, compute health scores for both using identical metrics
3. Surface the comparison as a structured recommendation: which variant won, by how much, and confidence level
4. Governor decides: adopt winner, continue testing, or declare inconclusive

**OD declaration format:**
```markdown
### A/B Test: [Name]
- **Variants:** [TAC-A] vs [TAC-B] (or STR-A vs STR-B)
- **Shared Metrics:** [metrics used for comparison]
- **Schedule:** [sequential N cycles each | parallel]
- **Minimum Duration:** [N cycles per variant]
- **Comparison Method:** [composite score | single metric | Governor judgment]
```

---

## 8. Decision Recording

All Governor decisions are recorded in `decisions/governor-decisions.md`. Append-only.

### 8.1 Decision Entry Format

```markdown
### DEC-[sequential-number] | [date]
- **Session:** [session number]
- **Type:** [kill | pivot | persevere | approve | reject | promote | phase_advance | scope_change | pivot_override]
- **Target:** [Which tactic/strategy/objective/phase]
- **Decision:** [What was decided]
- **Reasoning:** [Why — referencing signals, domain model concepts, Governor judgment]
- **Domain Models Referenced:** [Which domain model concepts informed this]
- **Impact on OD:** [What changes in the operating document, if any]
```

### 8.2 Decision Types (see Framework Appendix B.2 for full canonical list)

**Common to both scope types:**
- `kill` — Terminate a tactic or strategy
- `pivot` — Redirect a tactic or strategy with modified approach
- `pivot_override` — Governor overrides a met kill condition with pivot (must be justified; tracked for accountability)
- `persevere` — Continue despite mixed signals
- `approve` — Accept a proposed plan, deliverable, or OD change
- `reject` — Reject with reasoning
- `scope_change` — Modify the scope definition

**Finite scope specific:**
- `phase_advance` — Move to next phase
- `iterate` — Repeat current phase with modifications
- `restructure` — Fundamentally reorganize the current phase (distinct from iterate — restructure changes phase structure, iterate repeats with modifications)
- `accept_deliverable` — Final deliverable accepted

**Ongoing scope specific:**
- `promote` — Advance graduation stage
- `rebalance` — Reallocate resources across tactics/strategies
- `pause` / `resume` — Temporarily halt/restart a tactic
- `revise_objective` — Modify objective targets based on learning
- `conclude_scope` — End the ongoing operation

**Cross-scope decision types (both scope types):**
- `cross_objective_tradeoff` — Resolve detected interference between objectives (§20.12)
- `informed_override` — Governor overrides AI assessment with domain expertise (§6.1)
- `guardrail_reclassify` — Governor changes guardrail severity soft↔hard (§5.1)
- `wmbt_refinement` — Refine WMBT wording without kill/pivot (§4.3)
- `portfolio_rebalance` — Shift resources between strategies (§4.3)
- `decision_reversal` — Reverse a prior autonomous decision (§4.3)
- `resolve_conflict` — Resolve cross-domain signal conflicts (§4.5)
- `tournament_selection` — Governor selects winning deliverable from tournament candidates (§4.6). Records: selected candidate, comparative scores, behavior cell map (constrained mode), selection rationale.

---

## 9. Context Management Across Sessions

### 9.1 The Bootstrap File (00-BOOTSTRAP.md)

Critical continuity mechanism. Updated at the end of every session. Use the template in `cowork/templates/00-BOOTSTRAP.md`.

### 9.2 Session Logs (Episodic Memory)

Each session log captures what happened. Use the template in `cowork/templates/session-log.md`.

### 9.3 Structural Memory (learnings.md)

Updated at strategy reviews (ongoing) or phase gates (finite). Use the template in `cowork/templates/learnings.md`.

---

## 10. Framework Feedback Mechanism

Running GOSTA with Cowork/Code-as-wrapper will surface gaps and potential enhancements. Capture them in `gosta-framework-feedback.md`. Use the template in `cowork/templates/gosta-framework-feedback.md`.

**When to log feedback:**
- When the AI can't figure out what GOSTA says to do in a specific situation
- When the spec's recommendation doesn't fit the session-based model
- When a domain model interaction produces unexpected results
- When health computation requires judgment calls not covered by §20
- When the Governor and AI disagree about what GOSTA prescribes
- When a useful pattern emerges that the spec should codify

---

## 11. Graduation and Autonomy

| Stage | What the AI Does Autonomously | What Requires Governor Approval |
|-------|------------------------------|-------------------------------|
| 1 | Nothing — presents everything for approval | All plans, all deliverables, all decisions |
| 2 | Generates plans and drafts | Governor approves all plans and deliverables |
| 3 | Executes routine actions without per-action approval | Non-routine actions, all kill/pivot decisions, OD changes |
| 4 | Makes tactic-level kill/persevere decisions when kill conditions are met | Strategy decisions, OD changes, new tactic creation |
| 5 | Manages full tactic lifecycle autonomously | Strategy creation/kill, OD modification, guardrail changes, goal changes |

**Starting stage:** All new sessions start at Stage 1. The Governor promotes explicitly via a decision entry.

**Never-autonomous decisions (any stage):**
- Strategy creation or kill (except approach_validation=disproven AND all tactics failed)
- Operating document modification
- Domain model changes
- Guardrail modification
- Goal changes
- Scope conclusion

### 11.1 Autonomy Safeguards (from GOSTA §6.7)

Four cross-cutting safeguards modify how stages operate at Tier 0. They never grant more autonomy — only narrow it.

**1. Degraded-mode autonomy (§6.7.1).** At session start, the AI checks grounding health as part of context loading. If any grounding component is degraded (data source offline, domain model stale, >50% of signals flagged `[PROVENANCE-INCOMPLETE]` or `[STALE]`, capability registry outdated), the AI announces the constraint and operates at one stage lower until Governor either fixes the issue or explicitly confirms the current stage. Log the grounding status and Governor's decision in the session log.

**2. Decision reversibility (§6.7.2).** Before executing any autonomous decision at Stage 3+, the AI states the reversibility assessment: fully reversible, partially reversible, or irreversible. Irreversible decisions (terminating external partnerships, publishing to external audiences, spending committed budget that cannot be reclaimed) require Governor approval regardless of stage. Tactic specifications should declare known irreversibility factors at creation time. If no declaration exists, default to `partially_reversible` for kills/pivots.

**3. Risk-magnitude thresholds (§6.7.3).** The Governor defines thresholds in the OD guardrail section: resource cost, timeline impact, stakeholder visibility, external commitment. Autonomous decisions exceeding any threshold require approval. If no thresholds are defined, the AI flags this during OD validation: "No autonomy magnitude thresholds defined. At Stage 3+, autonomous decisions will have no magnitude constraint beyond the non-delegable list." At least one threshold should be set at OD creation.

**4. Conditional autonomy grants (§6.7.4).** The Governor can attach conditions to autonomy in the OD: time-bounded ("Stage 3 expires April 30"), event-triggered ("revert SEO decisions to Stage 2 if algorithm update"), metric-triggered ("revert retention tactics to Stage 2 if churn >5%"), or scope-bounded ("Stage 4 for content tactics only"). The AI checks conditions at session start and announces status. When a condition fires, the AI applies the reversion and logs it. Conditions never widen autonomy above the current stage.

**Safeguard stacking:** Multiple safeguards may apply to the same decision. The most restrictive constraint wins.

---

## 12. Grounding and Quality Checks (from GOSTA §14)

The Framework defines eight grounding components (§14.3), organized by the hallucination category they prevent: form corruption (Schema Validation), substance corruption (Domain Knowledge Store, Capability Validation), signal corruption (Data Grounding), continuity corruption (Synthesis Verification, Cross-Boundary Claim Propagation), and reasoning corruption (Reasoning Depth Validation), plus Attribution as the structural prerequisite. Memory confabulation (continuity corruption) is mitigated architecturally by the file-based state model; claim laundering (continuity corruption) is mitigated by propagation tracking (§12.11). This section operationalizes each component for the Cowork Protocol. Grounding is not optional — it is the mechanism that prevents the framework's feedback loops from operating on hallucinated data. The components are checked at specific points in the session lifecycle (see §5.1 Steps 3 and 4) and during health computation (§7).

### 12.1 OD Structural Integrity — Schema Validation (from GOSTA §8, §14.3.1)

Before finalizing any OD, verify:
- Every objective traces to exactly one goal
- Every strategy traces to exactly one objective
- Every tactic traces to exactly one strategy
- Every action traces to exactly one tactic
- Guardrails only tighten downward (never relax at lower layers)
- Every tactic has: hypothesis, kill condition, success metric, timeline
- Every strategy has: rationale, WMBT conditions, not-doing declaration
- Guardrails are calibrated above current baseline (§5.3 of the specification) — not at target levels
- **No Contamination (v6.1 Rule 2):** Each layer contains only elements appropriate to that layer. Goals don't contain timelines (that's objectives). Strategies don't contain action details (that's tactics). If an element appears at the wrong layer, move it.
- **Feedback Obligation (v6.1 Rule 7):** Silence is a negative signal. The AI must emit signals for every action within a session. Cross-session silence is tracked by the Governor via bootstrap file staleness — if the bootstrap hasn't been updated for longer than the review cadence, the scope is drifting.
- **Layer Boundary Respect (v6.1 Rule 9):** The orchestrator never modifies elements above its authority level. Tactics can be adjusted by the orchestrator; strategies and goals require Governor approval. Even at Stage 5 graduation, goal changes are never autonomous.

**Enforcement.** OD structural integrity is checked at two points: (a) during Bootstrap Session before presenting the OD to the Governor for approval, and (b) at every Phase Gate before advancing. Failed checks are flagged as Blocking tensions — the AI halts and reports which integrity rules are violated. The AI does not silently fix structural errors; it surfaces them for Governor awareness, then fixes them with Governor approval.

**Relationship to Semantic Coherence Validation (§12.7).** This section (§12.1) validates *structural* correctness — are required fields present? do layers nest properly? §12.7 validates *semantic* correctness — do the values in those fields make sense together? Both run at authoring time. A tactic can pass structural validation (all fields present) while failing semantic validation (its kill condition references an unavailable metric). Together, §12.1 and §12.7 form the complete OD integrity check.

**In Code mode:** Validation scripts (§18.4) can automate these checks. Run them before every OD modification proposal.

### 12.2 Domain Model Grounding (from GOSTA §14.3.2)

Every recommendation, analysis, scoring rationale, and tactic hypothesis must cite specific domain model concepts by name. The AI does not reason from general training data when domain models are loaded — it reasons from the domain model and supplements with training data only when the domain model is silent on a topic.

**Enforcement protocol (applies to Executor and Orchestrator):**

1. **Before emitting any recommendation:** The AI checks whether the recommendation traces to at least one concept in a loaded domain model. If it does, the AI cites the concept(s) by name. If it does not, the AI flags the reasoning as `[UNGROUNDED]` — meaning it is based on AI training data, not on the domain model.

2. **`[UNGROUNDED]` flag treatment:** Ungrounded reasoning is not automatically rejected. It is surfaced to the Governor with the flag: "[This recommendation is not grounded in any loaded domain model. It is based on AI general knowledge. Confidence should be treated as lower than grounded recommendations.]" The Governor decides whether to accept, request a domain model update, or reject. If the Governor requests a domain model update: for adding concepts to an existing model, draft the additions following the template structure and present for Governor approval. For creating a new model to cover the ungrounded territory, follow `cowork/domain-model-authoring-protocol.md` if source material exists, or use the first-cycle correction-derived procedure (§3.1.1) if not.

3. **Anti-pattern detection:** During health computation (§7.1), the orchestrator checks whether tactic hypotheses still cite domain model concepts that remain current. If a domain model has been updated and a concept has been removed or significantly changed, the orchestrator flags affected tactics: "Tactic TAC-N's hypothesis cites [concept], which was [removed | modified] in domain model v[X]. Review needed."

4. **Domain model citation in deliverables:** Every deliverable (analysis report, scoring table, health report) must include a "Domain Concepts Applied" section or inline citations. This is not just good practice — it is the verification mechanism that enables the Governor to trace any claim back to its domain source.

5. **Scoring grounding:** During multi-domain scoring (§7.6), every score assignment must include a rationale that cites at least one domain concept. A score of "7/10" with no domain citation is a grounding violation. The AI self-checks: "Can I name the domain concept that justifies this score?" If not, the score is flagged as `[UNGROUNDED]`.

### 12.2.1 Reasoning Depth Validation (from GOSTA §14.3.7) `[ROBUST]`

The grounding checks in §12.2 verify that reasoning is *grounded* (cites real concepts) and *faithful* (doesn't distort definitions). This section verifies that reasoning is *deep enough* — that the AI engages substantively with cited concepts rather than using them as labels.

**When to apply:** At decision points (kill, pivot, persevere, phase advance, strategy review) and when generating recommendations (tactic proposals, strategy proposals, A/B test recommendations). Not required for routine action cycles or standard health computation.

**Three self-checks before presenting a recommendation:**

1. **Depth check.** "If I removed the concept citation from this recommendation, would the recommendation change?" If the answer is no, the concept is decorative. The AI must either deepen engagement (use the concept's internal distinctions to narrow or justify the recommendation) or flag: `[SHALLOW: This recommendation cites [concept] but does not fully engage with its [manifestations / preconditions / decision criteria]. Governor may request deeper analysis or accept as-is.]`

2. **Coverage check.** "Which domain model concepts relate to this decision's subject matter? Did I consider each one?" Before finalizing, the AI scans loaded domain models for concepts relevant to the decision that were NOT cited. Concepts reviewed and deemed irrelevant are logged as `considered_not_material: [concept, reason]`. This makes omissions deliberate and auditable rather than accidental and invisible.

3. **Chain integrity check.** "Does each reasoning step follow from the prior one, or am I assuming an intermediate conclusion without stating it?" The chain from domain concept → application → recommendation must not contain unjustified leaps. If the Governor would need to fill in an unstated assumption to follow the reasoning, the AI states that assumption explicitly.

**Interaction with tension surfacing (Step 3b):** Reasoning depth validation and tension surfacing are complementary. Tensions identify *where* multiple valid interpretations exist. Depth checks verify that each side of the tension was reasoned through substantively, not merely labeled. A recommendation that surfaces a tension but engages shallowly with both sides has not fulfilled either obligation.

### 12.3 Signal Provenance — Data Grounding (from GOSTA §14.3.3)

Every signal must carry provenance — evidence of where the data came from and how it was obtained. This prevents the feedback loop from operating on fabricated metrics.

**Provenance requirements by signal source:**

- **`execution` signals** (action completion): The AI states what it did, what output was produced, and where the output can be verified. For Code mode: commit hash, file path, test result. For Cowork mode: file reference, deliverable location, or session log entry.

- **`external` signals** (market events, web search results): The AI records the URL, search query, retrieval date, and source tier. If the AI cannot verify a claim (e.g., it "remembers" a statistic from training data but cannot find a current source), the signal is flagged as `confidence: estimated` and the provenance field states: "AI training data — no current source verified."

- **`computation` signals** (derived metrics, health scores): The AI states the formula used, the input signals by SIG-ID, and the computation result. This enables the Governor to audit: "Health score is 72. Based on what inputs?"

- **`governor` signals** (Governor-reported observations): Provenance is the Governor's statement. The AI records the Governor's exact words, the date, and the context.

**Enforcement.** Signal provenance is checked at Step 4 (Record) in the session lifecycle. Before writing a signal to the signals/ file, the AI verifies:
- Source field is populated (not blank, not "unknown")
- Confidence field reflects actual data completeness (not always "complete")
- For metric signals: computation method is stated
- For external signals: source URL or document reference exists

Signals that fail provenance checks are recorded with a `[PROVENANCE-INCOMPLETE]` flag. They enter the signal store but are weighted lower in health computation (§7.1) — a signal with incomplete provenance contributes 50% of a fully provenanced signal to composite health scores.

### 12.4 Attribution Validation (from GOSTA §14.3.4)

Every signal, output, and deliverable must trace to a specific element in the GOSTA hierarchy: Goal > Objective > Strategy > Tactic > Action. Attribution is the structural prerequisite that makes all other grounding components functional — without it, signals exist but cannot be aggregated into tactic or strategy health.

**Enforcement.** Attribution is mandatory in the signal format (§6.1). The AI assigns attribution at signal creation time, not retroactively. Signals without attribution are rejected — the AI must determine which tactic and strategy the signal belongs to before recording.

**System-level signals** (`agent_degradation`, `market_event`) use `system` as attribution — they affect the scope but do not trace to a specific tactic.

**In Code mode:** Attribution validation scripts (§18.4) check that every signal's tactic_id and strategy_id reference elements that actually exist in the current OD.

### 12.5 Synthesis Verification (from GOSTA §14.3.5) — Level 3 Only

When multi-agent deliberation is active (§7.5, Level 3), the Coordinator's synthesis of agent positions is a grounding risk. See Deliberation Protocol §9.3 for the full verification mechanism. At the Cowork Protocol level:

- The Governor reads position papers directly for every hard disagreement — not just the Coordinator's summary.
- At Tier 0 with ≤5 domain agents, the Governor reads all position papers against the synthesis.
- At Tier 0 with >5 agents, the Governor uses the spot-check protocol (Deliberation Protocol §9.3).
- The Coordinator includes verbatim recommendation quotes in the Synthesis Report.

This component is only active during Level 3 deliberation. Levels 1 and 2 do not involve a Coordinator and therefore have no synthesis verification requirement.

**Sycophancy verification (from GOSTA §14.3.9):** Governor synthesis verification obligations now include sycophancy verification: when reviewing synthesis reports, the Governor should check whether the Coordinator's framing of unresolved disagreements favors the OD's stated strategy. If the Coordinator consistently frames disagreements in ways that favor the status quo, this is coordinator sycophancy — flag for roster review. The Governor can compare the Coordinator's Sycophancy Assessment (§4.4) self-check against their own reading of position papers.

**Finding Classification verification (from Deliberation Protocol §9.3):** When reviewing a Synthesis Report, the Governor also verifies epistemic classifications: for each `confirmed` finding, verify the cited evidence exists in the Attribution Chains table; for each `information_gap`, verify the missing data is not already available elsewhere in the signal store; for each `conditional`, verify the condition is testable within the scope's timeline. See GOSTA §14.3.8.

**Extended grounding obligations when deliberation is active:** When the Deliberation Protocol is active, grounding obligations extend beyond the single-agent rules in §12.2. Domain Agents must ground position papers in their assigned domain model (domain concept citations, retrieval faithfulness, data grounding, schema validation). The Coordinator must ground synthesis in actual position paper content (attribution chains, no domain advocacy, synthesis verification). See Deliberation Protocol §10.5 (Grounding Obligations by Role) for the full per-role specification.

### 12.6 Capability Validation (from GOSTA §14.3.6)

Before proposing actions, the AI checks whether each action is operationally feasible given the current execution environment. At Tier 0, the gap between what the AI can describe and what it can execute is widest — the AI may propose actions requiring tools, platforms, or scale that don't exist.

**Capability awareness.** The AI maintains awareness of its actual operational boundaries from the bootstrap file and operating document. At minimum: what tools/platforms are accessible in the current session, what data sources the Governor can provide, what actions require Governor execution vs. AI execution, and what scale the scope operates at.

**Enforcement protocol:**

1. **Before proposing actions:** The AI checks each proposed action against declared capabilities. Can the deliverable actually be produced? Does the required tool/platform exist? Is the data source accessible? Is the scale realistic?

2. **Infeasible actions are reformulated, not silently included.** If an action assumes a capability that doesn't exist (e.g., "automated email drip" at Tier 0), the AI reformulates to a feasible equivalent (e.g., "manual email outreach with Governor sending") and notes the reformulation. If no feasible equivalent exists, the AI flags: "[ACTION INFEASIBLE] This action requires [capability] which is not available. Governor options: confirm capability exists, substitute action, or defer."

3. **Governor as second check.** The Governor reviews all proposed actions during the session. Capability flags are surfaced alongside actions for explicit Governor decision. The AI should not rely solely on Governor review — it should self-filter first.

4. **Capability changes.** When the Governor adds or removes tools/platforms between sessions, the AI updates its capability awareness from the bootstrap file at session start. Actions from prior sessions that depended on now-removed capabilities are flagged at the next tactic review.

5. **Scale checks.** The AI validates that proposed action scale matches scope reality: A/B test sample sizes, audience reach, production capacity, and Governor time availability. An action proposing "20 user interviews this week" when the Governor has 5 hours is a capability hallucination, not a domain error.

### 12.7 Semantic Coherence Validation (from GOSTA §8.1) `[ROBUST]`

Beyond structural schema checks (§12.1), the AI validates that OD elements are semantically coherent across layers. This catches specifications that pass schema validation but are collectively inconsistent.

**At tactic creation / OD authoring:**

1. **Kill condition evaluability (C1).** Before accepting a new tactic, the AI asks: "This kill condition references [metric]. Where will this data come from?" If the Governor cannot confirm a data source, the kill condition is revised before the tactic enters the OD. A tactic with an unevaluable kill condition can never be killed — it defeats the framework's core feedback mechanism. **For execution-only tactics** (deliverables, builds, analyses): if the tactic has `Kill Condition: N/A`, the AI flags the C1 violation and applies the default completion-based kill condition ("deliverable not accepted after 3 revision cycles") per §8.1.1. The Governor may override with a custom form (deadline_exceeded, cost_exceeded, scope_exceeded) but cannot leave the field as N/A.

2. **Allocation arithmetic (C2).** After any tactic creation, kill, pause, or resume, the AI verifies that `ALLOCATION_WEIGHT` sums to 1.0 for the affected strategy. If the sum is off, the AI renormalizes per §4.3 and announces the adjustment: "TAC-3 killed. Redistributed allocation: TAC-1 0.4→0.6, TAC-2 0.4→0.4. Sum: 1.0."

3. **Temporal ordering (C3).** When creating tactics with deadlines, the AI checks: does this tactic's estimated completion fall before its parent strategy's next review? If not: "TAC-5 estimated completion is March 30. Strategy review is March 15. This tactic's results won't be available for that review. Proceed, or adjust timeline?"

4. **Entity reference integrity (C4).** After drafting or modifying the OD, the AI scans all cross-references that name domain models or agents: Deduplication Rules table, Tactic Domain Model Dependencies, Evidence Collection agent domain assignments, Domain Model Adaptations table. Every name must match an entry in the Domain Models Referenced list or the Deliberation Agent Roster. Phantom references — names that look plausible but don't exist in the session — are flagged: "Deduplication rule references [OPS-1] but no agent with that ID exists in the roster. Remove or correct." **Blocking** — phantom references must be resolved before OD approval.

5. **Guardrail compatibility (R3, R4).** When the Governor introduces new guardrails, the AI reasons about compatibility with existing guardrails: "This new cost guardrail (max €5/outcome) may conflict with the inherited engagement guardrail (minimum 3 touchpoints per lead, which typically costs €6-8/outcome). Want to calibrate?"

**At strategy review:**

6. **Hypothesis-domain model coherence (R1).** The AI checks whether any active tactic's hypothesis references domain model concepts that have been modified or removed since the tactic was created. If so: "TAC-2's hypothesis cites 'founder authority premium' which was removed from the content-strategy domain model in session 8. The tactic is still running against a concept the domain model no longer supports."

7. **WMBT-objective alignment (R2).** The AI presents its alignment assessment for each strategy: "STR-1's WMBTs (organic reach >5K, engagement rate >3%) relate to OBJ-1's metric (qualified leads) because [reasoning]. Alignment: moderate — high engagement doesn't guarantee lead quality. Flag for Governor attention."

8. **Reconciliation check (§8.2.3).** The AI cross-references the decision log with OD state: "Since last strategy review: 4 decisions recorded, all applied correctly. All active tactics have authorization references. No unauthorized state found." Or: "TAC-7 exists in the OD but has no decision entry — it may have been created in a session I don't have full context for. Governor: confirm or remove?"

**What the AI does NOT do:** block the Governor from proceeding. Coherence flags are informational except for C1 (kill condition evaluability) and C4 (entity reference integrity), which are blocking — a tactic without an evaluable kill condition or an OD with phantom domain references must not proceed. All other flags are presented for Governor awareness. The Governor may accept known incoherence with reasoning that the AI records.

### 12.8 Decision-to-State Traceability (from GOSTA §8.2) `[ROBUST]`

At Tier 0, the AI is the sole modifier of OD files. Traceability is maintained by writing the decision entry *before* modifying the OD file within the same session.

**Session protocol:**

1. When the Governor makes a decision, the AI writes the decision entry to `governor-decisions.md` first.
2. Then the AI modifies the OD to reflect the decision, noting the decision reference (e.g., "DEC-14") in context.
3. For bulk authoring (initial OD creation, major restructuring), the AI notes "GOV-session-N" as the authorization source rather than creating individual decision entries for each element.
4. For automatic adjustments (allocation renormalization after a kill, guardrail recovery), the AI notes "SYSTEM-renormalize" or "SYSTEM-recovery" and logs the adjustment in the session log.

**Cross-session context gap mitigation:** At Tier 0, the most common traceability issue is context gaps — the AI in a new session may not have full history of prior sessions. The reconciliation check at strategy review (§12.7 item 7) catches these gaps. When the AI finds an OD element without a traceable authorization, it asks the Governor to confirm rather than assuming error.

### 12.9 OD State Versioning (from GOSTA §8.3) `[ROBUST]`

At Tier 0, the OD is a markdown file. There is no database versioning or event sourcing. State versioning is achieved through two lightweight mechanisms:

**1. Decision context snapshots.** When the AI writes a decision entry to `governor-decisions.md`, it includes a `Context Snapshot` section capturing the OD parameters evaluated for the decision. For kill decisions: the tactic's kill condition, current metric values, signal references with their values, parent strategy WMBT status. For pivots: same plus the proposed new spec. For rebalances: all allocation weights before and after. The snapshot makes each decision entry self-contained — a reader can understand the decision without reconstructing prior OD state.

**Template addition to decision entry:**
```
### DEC-[N] | [date]
... [existing fields] ...
- **Context Snapshot:**
  - Target spec at decision time: [relevant fields from the target element — kill condition, hypothesis, allocation, etc.]
  - Prior authorized_by: [the authorized_by value that was on this element before this decision]
  - Key signals: [signal IDs with their values at decision time]
  - Environmental context: [active environmental signals, if any]
```

**2. Cross-session edit detection.** At session end (Step 5 — Update Bootstrap), the AI records an `od_fingerprint` in the bootstrap: count of active goals, objectives, strategies, tactics, total allocation weight sum, and guardrail count. At session start (Step 1 — Orient), the AI recomputes the fingerprint and compares. If they differ: "The Operating Document has been modified since session [N]. [Describe detected changes]. No decision entry covers these changes. Governor: were these intentional edits?" If the Governor confirms, the AI creates a retroactive `GOV-session-[N]` authorization entry.

### 12.10 Causal Context at Kill Decisions `[CORE]` (from GOSTA §8.4)

When the AI recommends killing a tactic, it must surface known confounders before presenting the recommendation. This prevents automatic attribution of underperformance to hypothesis failure when other factors may explain the metrics.

**Confounder checklist (run before every kill recommendation):**

1. **Environmental change:** Has any environmental watch list entry (§7.14) changed during this tactic's active period? If yes, note the change and its potential metric impact.
2. **Sibling tactic interference:** Does another active tactic under the same strategy target overlapping metrics or audiences? If yes, note the overlap.
3. **Input starvation:** Did the tactic receive fewer human creative inputs than its declared estimate? If yes, note the shortfall and whether fully-resourced cycles showed different results.
4. **Data quality:** Are any signals feeding the kill assessment flagged `[PROVENANCE-INCOMPLETE]` or `[STALE]`? If yes, note which signals and how they affect the assessment.
5. **Bootstrap insufficiency:** Has the tactic completed fewer post-bootstrap cycles than the minimum evidence floor (2 cycles per §4.2)? If yes, note that the kill assessment may be premature.
6. **Allocation change:** Was the tactic's resource allocation modified during the assessment period (e.g., rebalance after a sibling kill)? If yes, note the old vs. new allocation and whether performance decline correlates with the change.

**Presentation:** The AI presents confounders *before* the kill recommendation, not as an afterthought:

"TAC-3's kill condition is met (engagement < 2% for 3 cycles). Before recommending kill, I note:
- ENV-003 (market contraction) occurred during TAC-3's active period — market dropped 15%.
- TAC-3 received 2 of 4 expected human inputs per cycle.
- No sibling overlap, no data quality issues, bootstrap complete.

Confounder assessment: Environmental factor is real but TAC-4 outperformed 2.1x under same conditions. Input shortfall is moderate but fully-resourced cycles (Week 3, Week 5) showed no improvement.

Recommendation: kill. Confounders noted but do not explain the performance gap."

**Recording:** The Governor's response to each confounder is recorded in the decision entry's `Confounders` section (dismissed with reason, acknowledged, or not applicable). This creates an auditable record of the causal reasoning behind the kill.

**Extension to other decisions `[ROBUST]`:** At `[ROBUST]` complexity, the confounder surface also applies to pivots, strategy kills (WMBT falsification), and A/B winner declarations. At `[CORE]`, only kill decisions trigger confounder assessment.

### 12.11 Cross-Boundary Claim Propagation (from GOSTA §14.3.10) `[ROBUST]`

When claims cross agent trust boundaries — during deliberation synthesis, cross-session context loading, or multi-agent coordination — grounding status can degrade silently. This section operationalizes the propagation tracking that prevents "claim laundering," where `[UNGROUNDED]` flags get stripped as claims move between agents or sessions.

**Propagation failure modes:**

1. **Flag stripping:** An agent receives a claim tagged `[UNGROUNDED]` from a position paper and incorporates it into its synthesis without the flag. The claim now appears grounded.
2. **Authority accumulation:** A claim cited by multiple agents in separate position papers gains apparent consensus weight, even though all agents derived it from the same ungrounded source.
3. **Cross-session persistence:** A claim marked `[UNGROUNDED]` in session N appears in session N+1's bootstrap without the flag, because the bootstrap summary didn't preserve grounding metadata.

**Grounding provenance flags (from Framework §14.3.10):**

| Flag | Meaning | When Applied |
|------|---------|--------------|
| `[GROUNDED]` | Claim traces to a domain model concept with supporting evidence | Default for properly grounded claims |
| `[UNGROUNDED]` | Claim lacks domain model support or evidence | Applied by §12.2 checks |
| `[PARTIALLY-UNGROUNDED]` | Some sub-claims are grounded, others are not | Applied when compound claims have mixed grounding |
| `[PROPAGATED-UNGROUNDED: agent-id, round]` | Claim was received ungrounded from another agent | Applied during synthesis when incorporating cross-boundary claims |
| `[CROSS-DOMAIN: source-model, concept]` | Claim originates from a different domain model than the current agent's | Applied when domain agents cite concepts outside their assigned model |

**Propagation rules:**

1. **Flag preservation:** When incorporating a claim from another agent's output, the receiving agent must preserve the original grounding flag. If the original flag is `[UNGROUNDED]`, the receiving agent may upgrade it to `[GROUNDED]` only by providing independent evidence from its own domain model.
2. **Source attribution:** Claims crossing a trust boundary must carry `[PROPAGATED-UNGROUNDED: agent-id, round]` if their source was ungrounded. The Coordinator must not strip this flag during synthesis.
3. **Consensus independence:** Multiple agents citing the same ungrounded claim does not make it grounded. The Coordinator must trace citation chains — if all paths lead to the same ungrounded source, the synthesized finding retains `[UNGROUNDED]`.
4. **Cross-session propagation:** Bootstrap files and session logs must preserve grounding flags for any claims carried forward. The AI must not summarize away grounding metadata.

**Trust boundary types (from Framework §14.3.10):**

| Boundary Type | Description | Primary Risk |
|---------------|-------------|-------------|
| Identity | Between distinct agent instances | Flag stripping during handoff |
| Planning | Between strategic and tactical reasoning | Ungrounded strategy claims inherited as grounded tactic assumptions |
| Communication | Between position papers and synthesis | Authority accumulation through repeated citation |
| Memory | Between sessions or context windows | Flag loss during summarization |
| Retrieval | Between stored knowledge and active reasoning | Stale grounding status on retrieved claims |
| Execution | Between plan specification and action execution | Capability claims assumed without validation |
| Oversight | Between AI reasoning and Governor review | Ungrounded recommendations presented without grounding metadata |

**Tier implementation:**

- **Tier 0:** The AI self-checks propagation at two points: (a) during deliberation synthesis (§12.5), verify that all cross-agent claims preserve grounding flags; (b) at session start (Step 1), verify that bootstrap claims carry grounding metadata from prior sessions. Violations are logged as `claim_propagation` signals (§6.2).
- **Tier 1:** System-enforced flag preservation — the orchestrator rejects synthesis outputs that reference claims without grounding flags. Automated cross-session grounding metadata in bootstrap files.
- **Tier 2+:** Automated propagation audit across all trust boundaries. Claims crossing more than two boundaries without independent grounding are auto-flagged for Governor review.

**Interaction with §12.5 (Synthesis Verification):** Propagation tracking complements synthesis verification. §12.5 checks whether the Coordinator faithfully represented agent positions; §12.11 checks whether grounding status was preserved across the boundary. A synthesis can be faithful (accurately representing what agents said) but still propagate ungrounded claims if the agents themselves had ungrounded inputs.

### 12.12 Frame Integrity Validation (from GOSTA §9.2 AFC) `[CORE]`

**Frame declaration.** Before producing deliverable content, the deliverable agent states its frame interpretation at the top of the deliverable draft:

```
<!-- FRAME DECLARATION
Task interpretation: [1 sentence — what I understand my task to be]
Analytical stance: [who is the reader, what is their relationship to the subject]
Output answers the question: [the question this deliverable answers]
-->
```

In AFC-enabled sessions, the frame declaration is mechanically compared against AFC fields before drafting proceeds:
- Task interpretation must align with AFC Output Verb.
- Analytical stance must match AFC Stance.
- Output question must avoid AFC Prohibited Frame.

If any mismatch is detected, the agent corrects its interpretation before drafting. The declaration remains in the deliverable as an HTML comment (invisible to readers, visible in source) for post-session audit.

**Non-AFC sessions:** The frame declaration is still produced (it costs 3 lines) but is not mechanically validated — it serves as an audit trail only.

When the OD declares an Analytical Frame Contract (§4.1a), the deliverable agent performs three content-level checks at deliverable authoring time:

1. **Output verb match:** Deliverable section verbs and framing match the AFC Output Verb. A dependency-exposure AFC should produce sections that "expose," "surface," or "identify" — not sections that "recommend," "evaluate for adoption," or "advise on procurement." If the OD declares a Verdict Vocabulary, check verdict terms against the declared vocabulary (e.g., "LOW EXPOSURE" not "VIABLE").
2. **Stance reader match:** Recommended actions, postures, or conclusions address the AFC Stance's reader. A dependency-exposure deliverable addresses "organizations depending on [target]" — not "customers evaluating [target] for purchase." A regulatory-mapping deliverable addresses "policy makers assessing coverage" — not "vendors seeking compliance certification."
3. **Failure mode alignment:** Risk characterization aligns with the AFC Failure Mode. A dependency-exposure deliverable characterizes "dependency risk" and "exposure severity" — not "purchase risk" or "adoption suitability." A roadmap-sequencing deliverable characterizes "sequencing constraints" and "strategic misdirection risk" — not "vendor selection risk."

**Annotation:** Sections failing any check receive `[FRAME-DRIFT]` annotation. Severity: MATERIAL — requires revision before Governor acceptance. The deliverable agent must revise annotated sections to align with the AFC before presenting the deliverable for Governor review.

**Relationship to existing guardrails:** §12.12 supplements, not replaces, existing guardrail attestation. G-1 (or any session-specific guardrail like "no purchase recommendation") continues to operate — the deliverable agent self-attests compliance. §12.12 adds a second, independent check that is AFC-aware and content-level. In a session with an AFC, both checks run: G-1 attestation catches what the agent recognizes as a violation; §12.12 catches what the agent misses because its training-data default matches the Prohibited Frame. If a session has no AFC, §12.12 does not apply and G-1 attestation is the sole frame check.

**Revision trail.** When a deliverable fails §12.12 checks or Governor review and requires revision, the pre-revision version is preserved before edits are applied. Preservation method by tier:
- *Tier 0:* Before applying revisions, copy the deliverable file to `deliverables/[name]-rev-[N].md` (where N is the revision number, starting at 0 for the original). The revision entry in the session log (see template) records: what triggered the revision, which sections changed, and the nature of the frame correction.
- *Tier 1+:* Version-controlled deliverable store handles this automatically.

The final accepted deliverable retains its original filename. Revision copies are retained for post-session analysis but are not promoted to evidence archive.

### 12.13 Guardrail Attestation Log `[CORE]`

When the deliverable agent performs guardrail self-attestation (hard guardrails G-1 through G-N), the attestation is recorded in the session log's Guardrail Attestation section (see session-log template). For each guardrail attested:

1. **What was checked:** Which deliverable sections were evaluated for this guardrail.
2. **Check method:** `mechanical` (pattern scan for prohibited phrases) or `interpretive` (semantic evaluation of intent).
3. **Supporting evidence:** A verbatim quote from the checked content that the attestor relied on to conclude compliance. Maximum 2 sentences per guardrail.
4. **Conclusion:** `pass` or `fail — [action taken]`.

For AFC-enabled sessions, §12.12 Frame Integrity Validation results are also recorded in this section — they are a second independent check layer.

**Rationale:** Self-attestation without a trail is unauditable. The attestation log makes the attestor's reasoning visible to the Governor at review time without requiring debug logging.

### 12.14 Pre-Flight Validation Gates Operationalization (from GOSTA §8.7) `[CORE]`

Beyond specification coherence (§12.7) and contract validation at handoffs (§14 interface contracts), the AI verifies that declared structures (artifacts, retrieval contracts, runtime tools, capture-mode flags, inherited domain models) are operationally true at every lifecycle boundary they cross. This catches the operational-truth gap class — declarations that pass §12.1 schema validation and §12.7 semantic coherence but fail at runtime because the declared structure was never empirically exercised.

**At bootstrap entry:**

1. **Runtime import verification (V5).** For each declared tool, the AI runs an actual import test against the runtime path: `python3 -c "from <runtime_modules> import <symbols>"`. File-presence checks against model files or comparison to documented dep lists do NOT satisfy V5. Failure: BLOCK with the missing modules and fix command surfaced to Governor inline.

2. **Inherited-artifact vertical-fit (V7).** For each inherited domain model, scope decision, deliberation roster, or template, the AI extracts the new session's declared concept set (from scope objectives + OD strategies + deliberation roster) and runs a concept-coverage grep against the inherited artifact. Default threshold: ≥70% of declared concepts have at least one matching reference. Below threshold: WARN with three response options surfaced (extend / accept-with-acknowledgment / substitute).

**At Phase 1 entry:**

3. **Decision spine consistency (V3).** The AI runs a cross-document key-set comparison between OD and scope: every STR-N appears in both, every guardrail referenced in scope exists in OD, every scope deliverable maps to an OD strategy ID, every OD TAC-N references a scope strategy or signal. This is a mechanical key-set comparison, not a strategic-alignment judgment. Failure: BLOCK at Phase 1 entry on non-empty symmetric difference.

**At every phase entry that consumes per-unit retrieval:**

4. **Retrieval contract validation (V1).** Before any phase running per-unit queries at scale, the AI runs the actual operational queries (not topic-vocabulary probes) against each declared pool and tabulates outcomes per (unit, pool) cell: VALIDATED / CORPUS-FIT-GAP / VOCABULARY-MISMATCH / ESCALATE. Failure: BLOCK on unresolved ESCALATE; WARN on CORPUS-FIT-GAP or VOCABULARY-MISMATCH cells without explicit Governor disposition. Cell-by-cell results are surfaced with the three mitigation paths from §8.7.3 V1.

**After every artifact-producing build:**

5. **Build artifact shape verification (V2).** After any pool, index, or embedding build, the AI inspects the produced artifact's shape: `numpy.load('<embeddings>.npy').shape`, file count, byte count. If `N_embeddings == N_input_files` for non-trivial inputs (default threshold 20-50KB plain-text), the AI flags as suspicious and verifies the build subcommand was the intended one. Failure: WARN; BLOCK if downstream depends on chunk-level discrimination.

**At every phase exit:**

6. **Continuous-capture coverage (V4).** For each active continuous-capture mode flag (Debug + Shortfall Reporting, framework feedback, episodic session logging), the AI runs `wc -l` against the corresponding artifact and compares to friction signals observed during the phase. If friction observed and capture is empty without explicit "no capture-class observations apply" confirmation, the gate fails. The AI either backfills entries before phase exit or logs the explicit confirmation.

7. **Declared artifact existence (V6).** For every artifact named in CLAUDE.md, OD §Decision History, or scope as a phase deliverable, the AI runs `test -s <path>`. Missing-or-empty artifacts BLOCK phase exit unless explicitly deferred with a Governor-acknowledged reason in OD §Decision History. The Governor sees the missing-artifact list and chooses per artifact: create-now / defer-with-reason / remove-from-declaration.

**What the AI does NOT do:** suppress gate failures, paraphrase verification from memory, or treat declared structure as operationally true without a mechanical test. Pre-flight gates surface failures to the Governor with explicit fix paths; the Governor decides on resolution. The AI's role is the mechanical verification, not interpretive judgment about whether the failure matters. A gate that fails without surfacing to the Governor is itself a §8.7 violation.

**Phase-gate request integration.** §5.1 Phase Gate Enforcement Protocol's structured Phase Gate Request includes a mandatory "Pre-Flight Validation Gate Results (from GOSTA §8.7)" field listing per-V-invariant outcome at the boundary. BLOCK rows prevent gate advancement; WARN rows require explicit Governor acknowledgment in the gate response.

---

## 13. Closing a Scope

### 13.1 Finite Scope Closure

1. Final Governor decision: `accept_deliverable`
2. Write final health report summarizing the session
3. Run Mandatory Retrospective (§5.4) — populate learnings.md and gosta-framework-feedback.md
4. Write final session log
5. Update bootstrap: status = completed

### 13.2 Ongoing Scope Conclusion

1. Governor decision: `conclude_scope` with reasoning
2. Run final strategy and goal reviews
3. Produce scope conclusion report
4. Run Mandatory Retrospective (§5.4)
5. Update bootstrap: status = completed

---

## 14. Agent Failure and Safe Defaults (from GOSTA §7.7)

AI sessions fail — API errors, context overflow, malformed responses, mid-session crashes.

### 14.1 Failure Modes and Responses

| Failure | Response | Signal |
|---|---|---|
| AI fails to generate plan or deliverable | Use safe defaults: repeat last session's approach with conservative scope | Emit `agent_degradation` with `fallback: safe_defaults` |
| AI produces unparseable or incoherent output | Governor discards output, logs the failure, retries in next message/session | Emit `agent_degradation` with `fallback: parse_failure` |
| AI returns invalid entity references (e.g., kills non-existent tactic) | Reject the invalid decision, continue processing valid ones | Emit `agent_degradation` with `fallback: invalid_reference` |
| Session crashes mid-execution (Code mode) | State in files is safe (append-only signals, versioned OD). Resume from bootstrap next session | Emit `agent_degradation` at next session start |
| AI enters a repetitive loop (same recommendation 3+ times with no new evidence) | Governor intervenes: either provide new input or kill the current tactic | Emit `agent_degradation` with `fallback: harmful_repetition` |

### 14.2 Safe Defaults

Safe defaults are conservative actions that keep the session operational without AI reasoning:
- Never violate any guardrail in the chain
- Preserve current state rather than optimizing
- In Code mode: do not commit, push, or delete files during recovery
- In Cowork mode: present the failure clearly and ask Governor for direction

### 14.3 State Protection

All file operations must be all-or-nothing:
- Signal files are append-only — a crash mid-append leaves a partial entry that can be cleaned up
- The OD is never partially updated — draft changes in conversation, apply atomically
- Bootstrap is the last file written in a session — if the session crashes before Step 5, the previous bootstrap remains valid

### 14.4 Failure Resilience (from GOSTA §7.13)

Beyond individual agent failures (§14.1), four systemic failure modes apply at Tier 0:

**Signal freshness check (§7.13.1).** At session start, the AI checks the recency of signals for each active tactic. If the most recent signal for any active tactic is older than expected (based on the tactic's action cycle), the AI flags it: "TAC-2 last signal was 12 days ago (expected cadence: weekly). Either no action was taken, or signal collection failed. Please confirm: is the metrics source still active?" If >50% of active tactics have stale signals, the AI announces it is operating on potentially stale data and appends a staleness warning to any health computation. If no new signals exist for any tactic, the AI halts autonomous decisions until the Governor confirms the signal state.

**Recovery verification (§7.13.2).** When a previously-flagged issue is resolved (data source back online, grounding restored), the AI does not immediately return to full normal operation. It maintains the constraint for 2 additional sessions: "Data source X back online as of this session. Maintaining Stage [N-1] approval requirements for 2 more sessions to verify stability." The Governor can accelerate verification by confirming they've independently validated the fix. If the same issue recurs within 5 sessions after recovery, the AI doubles the stability window and flags chronic instability.

**Context and memory integrity (§7.13.3).** At session start, before any substantive work, the AI runs integrity checks on loaded state:
1. Bootstrap validation: all required fields present, dates parseable, referenced entities exist in OD.
2. Temporal consistency: bootstrap's "last session" date matches most recent session log date.
3. Learnings coherence: no contradictory entries about the same entity.
4. Cross-file references: entities in bootstrap and learnings exist in OD (or are marked historical/killed).

If any check fails, the AI reports the issue before doing session work. Bootstrap corruption is blocking — the AI attempts reconstruction from the most recent valid session log + current OD and asks Governor to confirm before proceeding. Other failures are flagged but non-blocking for unrelated session work.

**Context capacity management (§7.13.4).** The AI monitors approximate context utilization during loading. Content is loaded in priority order: (1) OD + active guardrails + kill conditions — never shed; (2) domain models for active tactics + current signals + bootstrap — shed last; (3) historical session logs and completed tactic specs — shed when needed; (4) inactive domain models and old decision records — shed first. If utilization exceeds 75% after Priority 1-2 content, the AI announces: "Context at ~75%. Loaded: [list]. NOT loaded: [list]. Ask me to swap if you need something I didn't load." If Priority 1 content alone exceeds 90%, the AI escalates that the scope may need complexity reduction or Tier 1 upgrade.

**Governor decision validation (§7.13.6).** After receiving a Governor decision and before applying it, the AI checks for semantic inconsistencies: persevering with a tactic whose kill condition is met, continuing a strategy whose WMBT condition is falsified, budget allocations exceeding available funds, guardrails that contradict each other, deadlines already past. Inconsistencies are flagged conversationally: "Before I apply this — I notice TAC-3's kill condition has been met for 4 cycles. You chose to persevere. Is that intentional, or would you like to revisit?" Budget incoherence and graduation-authority violations are blocking — the Governor must resolve before the AI applies the decision. All other flags are informational; the Governor can override with confirmation.

**Interface contract validation (§8.6).** The validations above implement specific interface contracts from Framework §8.6. At Tier 0, the AI performs these checks conversationally; at Tier 1+, they are automated. The full contract set covers 8 boundaries: signal emission (§8.6.1 — schema + attribution before writing signals), health computation (§8.6.2 — completeness + freshness + cross-signal consistency before computing health), decision-to-OD (§8.6.3 — state transition legality + prerequisite satisfaction before applying mutations), OD-to-work-plan (§8.6.4 — invariant checks + dependency resolution before generating actions), memory loading (§8.6.5 — bootstrap parse + cross-source consistency at session start), learning routing (§8.6.6 — kill reason presence + vector correctness before structural memory transfer), environmental monitoring (§8.6.7 — liveness + staleness checks), and deliberation output (§8.6.8 — attribution + agreement map fidelity). When a contract check fails, the AI flags the failure before proceeding — not after.

---

## 15. Governor Succession (from GOSTA §6.1)

When the Governor role transfers to a different person:

### 15.1 Succession Protocol

1. **Outgoing Governor** records a `governor_succession` decision in governor-decisions.md:
   - Reason for succession
   - What the incoming Governor needs to know (strategic intent, key tensions, pending decisions)
   - Current graduation stage (does NOT transfer — resets to Stage 1)

2. **Read-in session:** The AI runs a special session for the incoming Governor:
   - Present: OD summary, active strategies, tactic health, pending decisions, unresolved tensions
   - The incoming Governor reviews and may modify anything at any level
   - Graduation resets to Stage 1 — the new Governor must re-earn trust

3. **Domain models are preserved.** Governor succession does not change the domain model store. The incoming Governor may update domain models through normal approval channels.

### 15.1.1 Governance Feature Implementation by Tier (from §6.1)

**Tier 0 (conversational):**
- **Succession:** Outgoing Governor briefs incoming Governor conversationally. AI facilitates handoff by summarizing OD state, pending decisions, and active tensions.
- **Capacity validation:** AI periodically asks "are you keeping up with the review load?" and flags when projected reviews/week exceeds declared capacity. Mental check, no automation.
- **Delegated reviewers:** Governor tags specific decisions in the decision log as "delegated to [name]" with scope boundaries. AI enforces scope by flagging out-of-scope delegated decisions.
- **Informed override:** When Governor overrides AI recommendation, AI logs the override reason conversationally and notes it in the next health report.

**Tier 1 (system-enforced):**
- **Succession:** System event triggers handoff workflow. Incoming Governor receives structured read-in package (OD snapshot, decision backlog, tension queue).
- **Capacity validation:** Automated blocking — when review queue exceeds declared capacity threshold, system batches lower-priority reviews and surfaces only critical items. Unblocks when capacity freed.
- **Delegated reviewers:** Scoped permissions system — delegated reviewers can only approve/modify within their declared scope. System rejects out-of-scope actions.
- **Informed override:** API-enforced — overrides require structured justification field. System tracks override frequency and flags patterns (e.g., >3 overrides on same mechanism).

**Tier 2+ (predictive):**
- **Succession:** Transition risk assessment — system evaluates in-flight decisions, pending deadlines, and active recovery cycles to recommend optimal succession timing. Flags high-risk transition windows.
- **Capacity validation:** Predictive projection — system models upcoming review load based on tactic cadences, pending decisions, and historical patterns. Warns before capacity breach, not after.
- **Delegated reviewers:** Anomaly detection — system flags delegated decisions that deviate from historical patterns (unusual scope, frequency, or severity). Alerts Governor for review.
- **Informed override:** Contradiction detection — system correlates overrides against prior decisions and framework constraints. Flags when an override contradicts a previous Governor decision or guardrail.

### 15.2 Rotating Governors

For team sessions where the Governor role rotates (e.g., weekly rotation):
- The bootstrap file must always state who the current Governor is
- Each rotation triggers a lightweight read-in (abbreviated from §15.1 — skip OD re-review, just update pending items)
- Graduation stage is locked at Stage 2 maximum for rotating-Governor sessions (no autonomous execution without stable authority)

---

## 16. Protocol Self-Update Mechanism

### 16.1 Version Check

At session start (Step 1 — Orient), the AI should check:
- What protocol version is this session using? (stated in `gosta-cowork-protocol.md` header)
- What GOSTA framework version is this session using? (stated in the specification file header)
- If the AI is aware of a newer GOSTA version, flag it: "This session uses [protocol version] with [framework version]. A newer version is available. Some mechanisms may be outdated."

### 16.2 Feedback-to-Protocol Pipeline

When `gosta-framework-feedback.md` accumulates 3+ entries:
1. The AI surfaces a recommendation at the next review: "Framework feedback has accumulated [N] entries. Recommend a protocol update session."
2. If the Governor approves, the AI drafts amendments to the protocol and presents them for approval.
3. Approved amendments are applied to the session's local copy of `gosta-cowork-protocol.md`. Amendments may also target template files and CLAUDE.md — the AI should identify which files are affected by each amendment.
4. The version is incremented (e.g., v3.6 → v3.6.1 for session-local patches).
5. **Global propagation:** When a session-local patch is approved, the Governor should also apply it to the canonical `cowork/gosta-cowork-protocol.md` (and templates/CLAUDE.md if affected). The AI should surface this reminder when applying any local patch: "This fix should also be applied to the canonical cowork/ directory so future sessions inherit it."

### 16.3 Cross-Session Learning Transfer

When bootstrapping a new session from `cowork/`:
1. Check if any sibling sessions (in the repo's `sessions/` and `sessions/` folders) have `learnings.md` or `gosta-framework-feedback.md` files
2. Surface relevant learnings: "Prior session [name] discovered: [pattern]. Consider whether this applies here."
3. The Governor decides whether to incorporate the learning into the new session's OD or domain models

This closes the recursion loop: session discovers improvement → feedback recorded → Governor approves → protocol/templates updated → next session inherits the improvement.

---

## 17. Parallelism Rules (from GOSTA §7.12)

When work can be forked into parallel streams:

### 17.1 Validity Criteria

Work may be parallelized when:
- Inputs are independent (no shared state between parallel streams)
- Outputs don't conflict (parallel streams produce additive results, not competing ones)
- Each stream can be evaluated independently

### 17.2 Fork/Merge Protocol

1. **Fork:** Declare parallel streams with: stream ID, inputs, expected outputs, independence justification
2. **Execute:** Complete each stream. In Code mode, this can use multiple agent invocations. In Cowork mode, this means sequential execution with explicit "switching to Stream B" markers.
3. **Merge:** Consolidate outputs. Surface any conflicts as tensions (§5.1 Step 3b). If conflicts exist, the Governor resolves them.

### 17.3 When to Parallelize

- Multi-domain scoring (Level 2/3 independence — §7.5)
- Independent research tasks that don't share conclusions
- Deliverable production for unrelated phase outputs

### 17.4 When NOT to Parallelize

- Tasks where one output informs another (use sequential instead)
- Tasks that modify shared state (OD, signals, decisions)
- Tasks where conflict resolution would be more expensive than sequential execution

---

## 18. Claude Code Mode Specifics

When running this protocol in Claude Code (or similar tool-based AI), the following adaptations apply:

### 18.1 File Operations

- The AI reads files directly using Read tool — no need for the Governor to paste content
- The AI writes files directly using Write/Edit tools — no need for the Governor to copy output
- The AI should read `00-BOOTSTRAP.md` at the start of every session automatically
- **Git:** The AI should commit meaningful checkpoints (end of phase, after Governor decisions) but NOT push without Governor approval

### 18.2 Bootstrap Automation

In Code mode, Step 1 (Orient) and Step 2 (Load Context) can be automated:

```
1. Read 00-BOOTSTRAP.md
2. Read files listed in "Context Loading Order"
3. Check OD staleness triggers
4. Report current state to Governor
5. Ask: "What would you like to work on this session?"
```

### 18.3 CLAUDE.md Integration

When working in a GOSTA session directory in Claude Code, the session's `CLAUDE.md` (if present) should reference this protocol:

```markdown
# CLAUDE.md — [Session Name]

## GOSTA Session

This directory is a GOSTA session. Follow the GOSTA-Cowork Protocol.

### Session Start
1. Read 00-BOOTSTRAP.md first
2. Follow the Context Loading Order specified there
3. Check OD staleness triggers (§4)
4. Report status and ask what the Governor wants this session

### Key Rules
- Never modify the OD without Governor approval
- Signal-first execution: write signal stub before each action, update after (§6.3)
- Use Phase Gate Enforcement Protocol at every phase transition
- Kill-before-pivot when kill conditions are formally met (§7.1)
- Log framework feedback when you notice spec gaps
- Reference pool agent: if pool > 50 items, use `cowork/tools/pool-agent.py query` — do NOT load full YAML into context (§18.5)

### Reference Pool (if applicable)
```bash
# Retrieve relevant articles — returns JSON with RP-IDs, scores, excerpts, file paths
python3 ../../cowork/tools/pool-agent.py query \
    "your analytical question" \
    --store [path/to/pool-store/] \
    --top 20 --json
```
Score thresholds: ≥0.58 read full article | 0.50–0.57 excerpt only | <0.50 ignore
```

### 18.4 Validation Scripts

In Code mode, the AI can write and run validation scripts for:
- OD structural integrity checks (§12.1) — schema validation for all framework objects
- Dependency DAG validation (§7.7)
- Signal attribution verification (§12.4) — every signal traces to a valid OD element
- Signal provenance verification (§12.3) — every signal has a populated provenance field
- Domain model grounding audit (§12.2) — scan deliverables for `[UNGROUNDED]` flags, report count and percentage
- Guardrail calibration checks (are any guardrails set below current baseline?)

### 18.5 Reference Pool Consumption

Reference pools above a size threshold cannot be loaded into Tier 0 context directly. Two modes apply based on pool size. The pool-agent tool handles retrieval for large pools via semantic search; the YAML itself is never loaded into context for pools above the threshold.

**Threshold:**
- **≤50 items:** Load the YAML directly into context. No agent required.
- **>50 items:** Use the pool-agent for all retrieval. Do NOT load the full YAML into context.

---

#### Pool-Agent Tool

Location: `cowork/tools/pool-agent.py`
Model: `cowork/tools/pool-agent/models/` (all-MiniLM-L6-v2, ONNX quantized, ~22MB — no torch, no API calls)
Dependencies (install once): `pip install numpy pyyaml onnxruntime tokenizers huggingface-hub`
First-time model setup: `python3 cowork/tools/pool-agent.py setup-model` (downloads from Hugging Face + quantizes to qint8)

The agent uses semantic embeddings — not tag matching — so queries like "hospital cybersecurity incidents" and "healthcare cyber incidents" return equivalent results. Tag taxonomy quality does not affect retrieval accuracy.

**Pre-session build (run once after pool creation or update):**
```bash
python3 cowork/tools/pool-agent.py build \
    --pool path/to/reference-pool.yaml \
    --articles path/to/articles/base/ \
    --store path/to/pool-store/
```

This embeds all items and saves a vector store (`embeddings.npy`, `metadata.json`, `pool-info.json`). Rebuild only when the pool changes.

**Session invocation:**
```bash
python3 cowork/tools/pool-agent.py query \
    "your analytical question in natural language" \
    --store path/to/pool-store/ \
    --top 20 --json
```

Output is a JSON array (~3K tokens for 10 results) with RP-IDs, scores, titles, tags, excerpts, and file paths. This replaces loading the full YAML.

**Score thresholds (mandatory):**

| Score | Action |
|-------|--------|
| ≥ 0.58 | Read the full article file via `sourceDir/sourceFile` path |
| 0.50 – 0.57 | Use excerpt from JSON output only — do not read full article |
| < 0.50 | Ignore — not sufficiently relevant |

The threshold is a protocol rule, not a suggestion. Do not read full articles for scores below 0.58 unless the Governor explicitly overrides.

**Citation rule:** Always cite by RP-ID. Never cite an article that has not been read (full or excerpt per threshold). An RP-ID cited from agent output alone without reading the source is an ungrounded citation.

**OD declaration:** When a scope uses a pool of >50 items, the OD's Reference Materials section must include:
```
pool_agent_store: [path to pool-store/]
pool_consumption: semantic-agent
pool_size: [N]
score_threshold_full_read: 0.58
score_threshold_excerpt: 0.50
```

---

#### Single-Document Indexing (large reference documents)

Some reference materials are single large documents (specifications, regulatory texts, long-form guides) rather than collections of items. These cannot be meaningfully represented as a single pool item — they contain dozens of distinct topics — and loading them fully into context exceeds token budgets.

The pool-agent's `index-doc` command handles this case by segmenting a markdown document by heading level, embedding each section independently, and producing a standard vector store. The existing `query` command then works unchanged against the resulting store.

**Pre-session build:**
```bash
python3 cowork/tools/pool-agent.py index-doc \
    --doc path/to/large-document.md \
    --store path/to/doc-store/ \
    --heading-level 2
```

This segments the document at `##` headings (configurable with `--heading-level`), embeds each section, and saves the same store format (`embeddings.npy`, `metadata.json`, `pool-info.json`). Metadata entries include `section_range` (line numbers) for precise retrieval.

**Session invocation:** Identical to pool-based queries:
```bash
python3 cowork/tools/pool-agent.py query \
    "governance decision authority" \
    --store path/to/doc-store/ \
    --top 10 --json
```

Results return section IDs (e.g., `SEC-001`), headings, excerpts, and line ranges. Use `section_range` to read only the relevant portion of the source document.

**Score thresholds:** Same as pool-based queries (§18.5):
- ≥ 0.58: Read the full section from the source document using the `section_range` line numbers.
- 0.50 – 0.57: Use excerpt from JSON output only.
- < 0.50: Ignore.

**When to use `index-doc` vs `build`:**

| Scenario | Command |
|----------|---------|
| Collection of items (articles, blog posts, research papers) described in a YAML pool | `build` |
| Single large markdown document (spec, regulatory text, long guide) | `index-doc` |
| Multiple large documents | Run `index-doc` once per document, each to its own store |

**OD declaration:** When a scope uses an indexed document, the OD's Reference Materials section must include:
```
doc_store: [path to doc-store/]
doc_consumption: section-search
source_document: [document name/path]
heading_level: [level used for segmentation]
section_count: [N]
score_threshold_full_read: 0.58
score_threshold_excerpt: 0.50
```

---

#### Fallback: Index-First (no pool-store available)

If no pool-store has been built yet and the pool exceeds 50 items, apply the index-first protocol as a fallback until the build is run:

1. **Index scan:** Load only metadata (tags, excerpts, titles) — not full article content.
2. **Metadata classification:** Map items to tactic requirements using metadata fields only.
3. **Selective deep read:** Read full content only for ambiguous items, counter-evidence candidates, and direct citation candidates.
4. **Checkpoint before narrative:** Write a structured summary (counts, key RP-IDs) to file before writing deliverable prose. This survives context compression.

Build the pool-store and switch to semantic-agent mode at the earliest opportunity.

### 18.6 Multi-Agent Parallelism

In Code mode with agent capabilities, Level 3 Multi-Domain Assessment (§7.5) uses the Deliberation Protocol for structured multi-agent evaluation. Each Domain Agent receives the §8.5 three-element framing (protocol context, Governor oversight, domain scope boundary) plus its assigned domain model and the items to evaluate. The Coordinator (which may be the orchestrator itself or a separate agent) manages the round structure per the Deliberation Protocol.

For simple scoring (no deliberation needed), Level 3 can still use direct parallel agent invocations where each agent receives only its assigned domain model and items to score, with results merged in the parent context. The distinction: direct parallelism is for isolated scoring; Deliberation Protocol is for decisions requiring disagreement resolution.

---

## 19. Agent Debug Logging

When debug logging is enabled (Group 1 toggle), the orchestrator and all dispatched agents produce incremental execution traces. Debug logging is observational — it does not affect session outputs, scoring, or governance decisions. Its purpose is post-session analysis: diagnosing agent behavior, identifying inefficiencies, and improving future runs.

### 19.1 Storage Structure

All trace files live in `sessions/[SESSION_NAME]/debug-logs/`:

```
debug-logs/
  orchestrator-trace.md          ← Orchestrator's own actions + all dispatch records
  [AGENT-ID].trace.md            ← Child agent's self-reported execution trace
  ...
```

File naming: child traces use the agent's ID as filename (e.g., `COLL-1-financial.trace.md`, `DELIB-advocate.trace.md`, `COORD-1.trace.md`). The orchestrator specifies the exact filename in the dispatch prompt.

### 19.2 Orchestrator Trace Format

The orchestrator logs two categories of entries to `orchestrator-trace.md`, interleaved chronologically:

**Own actions** — every tool call the orchestrator makes directly (web searches, file reads, file writes, reasoning decisions):

```markdown
## [timestamp] Action: [action type]
- Tool: [tool name]
- Input: [query, file path, or parameters]
- Result: [summary — hit count, file size, key finding]
- Decision: [what the orchestrator decided based on this result]
```

**Dispatch records** — every agent dispatch and its outcome:

```markdown
## [timestamp] Dispatch: [AGENT-ID]
- Role: [agent role description]
- Prompt: [full dispatch prompt text — or if >500 words: first 200 words + "... [truncated, N words total]"]
- Context injected: [list of files/artifacts passed to agent]
- Files writable: [list of paths the agent can write to]
- Debug logging block: injected [yes/no]

## [timestamp] Return: [AGENT-ID]
- Duration: [time elapsed]
- Output summary: [1-3 sentence summary of what the agent returned]
- Files written by agent: [list of files the agent created/modified]
- Trace file: debug-logs/[AGENT-ID].trace.md
- Trace integrity: [N actions logged in trace vs N items/files in output — note discrepancies]
```

**Trace integrity check.** After each agent returns, the orchestrator opens the agent's trace file and compares: (a) number of logged actions against the agent's claimed output (e.g., 12 evidence items but only 4 search actions logged = discrepancy), (b) whether the trace file exists at all (agent may have skipped logging). Discrepancies are noted in the dispatch record — they indicate the trace is incomplete, not that the agent's output is wrong.

### 19.3 Child Agent Trace Format

Child agents write their own trace incrementally during execution. The dispatch prompt includes a standard logging block (§19.4) that instructs the agent to log before moving to each next action.

**Child trace file format:**

```markdown
# Agent Trace: [AGENT-ID]
**Task received:** [agent's interpretation of its assignment — 1-3 sentences]
**Started:** [timestamp]

## Step 1: [action type]
- Detail: [search query, file path, or decision description]
- Result: [what came back — hit count, key findings, or "no useful results"]
- Selected: [what the agent chose to use and why]
- Rejected/skipped: [what was discarded and why — dead ends, irrelevant results]
- Decision: [what the agent decided to do next based on this result]

## Step 2: [action type]
...

## Output Summary
- Items/artifacts produced: [count and brief description]
- Confidence: [agent's self-assessed confidence in its output]
- Gaps identified: [what the agent couldn't find or resolve]
- Dead ends: [searches or approaches that produced nothing useful]

**Ended:** [timestamp]
```

**Action types** used in step headers: `Web search`, `File read`, `File write`, `Evidence synthesis`, `Scoring`, `Analysis`, `Decision point`, `Dead end pivot`.

### 19.4 Standard Debug Logging Injection Block

When debug logging is enabled, the orchestrator appends the following block to every agent dispatch prompt. This block is defined here as a protocol-level standard — the orchestrator copies it verbatim, substituting only `[AGENT-ID]` and `[SESSION_PATH]`.

```markdown
<!-- DEBUG LOGGING — protocol §19 -->
## Execution Trace Requirement

You MUST write an incremental execution trace to:
  [SESSION_PATH]/debug-logs/[AGENT-ID].trace.md

Trace format (follow exactly):
1. Begin the file with: `# Agent Trace: [AGENT-ID]` followed by your interpreted task and start timestamp.
2. Before each tool call or major decision, append a step entry:
   ```
   ## Step N: [action type]
   - Detail: [what you're doing]
   - Result: [what came back]
   - Selected: [what you kept and why]
   - Rejected/skipped: [what you discarded and why]
   - Decision: [what you'll do next]
   ```
3. Write each step IMMEDIATELY — do not reconstruct the trace from memory at the end.
4. After completing your task, append an Output Summary section with items produced, confidence, gaps, and dead ends.
5. End with your completion timestamp.

Action types for step headers: Web search, File read, File write, Evidence synthesis, Scoring, Analysis, Decision point, Dead end pivot.

This trace is for post-session analysis only. It does not affect your task or output quality. Prioritize your primary task — if context is critically constrained, you may abbreviate step entries, but never skip them entirely.
<!-- END DEBUG LOGGING -->
```

**Injection rule:** The orchestrator appends this block to the end of every dispatch prompt when debug logging is enabled. It is not included when debug logging is disabled. The block is self-contained — agents need no other context to produce a valid trace.

### 19.5 Orchestrator Self-Logging

The orchestrator's own actions are logged via protocol discipline, not an injection block (the orchestrator cannot inject prompts into itself). The protocol instruction is:

**When debug logging is enabled:** Before each tool call (web search, file read, file write) and after each significant reasoning decision, append an entry to `debug-logs/orchestrator-trace.md` using the §19.2 "Own actions" format. Before each agent dispatch, append a "Dispatch" entry. After each agent returns, append a "Return" entry with the trace integrity check.

**Timing:** Log entries are appended in real-time during execution. The orchestrator does not reconstruct the trace post-hoc. If the orchestrator forgets to log an action (context pressure, complex reasoning chains), the gap is acceptable — the trace is best-effort for the orchestrator, mandatory for dispatched agents (who receive explicit instructions).

**Minimum checkpoint obligation.** Regardless of real-time logging fidelity, the orchestrator MUST write a phase-transition entry to `orchestrator-trace.md` at every phase gate. Format:

```
## Phase [N] checkpoint — [timestamp]
- Agents dispatched this phase: [count] ([IDs])
- Key orchestration decisions: [1-3 sentence summary]
- Files written: [list]
- Dispatch anomalies: [none | list]
- Dispatch Verification Check results: [all passed | failures: list]
```

The Phase Gate Enforcement Protocol (§7.4) verifies this entry exists via the Session Lifecycle Compliance field before the gate request is presented to the Governor. Real-time per-action entries remain best-effort; the checkpoint entry is mandatory.

### 19.6 Interaction with Other Session Features

- **Shortfall logging:** Independent toggle. A session can have both shortfall logging and debug logging enabled. Shortfall entries go to `session-shortfall-log.md`; debug entries go to `debug-logs/`. If a shortfall is discovered via debug log analysis, it is recorded in the shortfall log with a cross-reference to the relevant trace file.
- **Evidence collection:** When debug logging is enabled during evidence collection, each COLL agent receives the logging block and writes its own trace. The orchestrator's dispatch records capture the full prompt sent to each collection agent, enabling prompt-to-output analysis.
- **Deliberation:** When debug logging is enabled during deliberation, each domain agent and the coordinator receive the logging block. This captures each agent's reasoning path through its domain model, not just the final position paper.
- **Phase gates:** Debug log content is not reviewed at phase gates (it is diagnostic, not a governance artifact). However, the Session Lifecycle Compliance field in the Phase Gate Request (§7.4) reports orchestrator trace entry count when debug logging is enabled. An empty trace triggers the minimum checkpoint obligation (§19.5) — the orchestrator writes at least a phase-transition summary entry before the gate can be presented. Phase Gate 0→1 additionally checks that `debug-logs/` was scaffolded and `orchestrator-trace.md` contains at least a Phase 0 checkpoint entry.
- **Closeout:** Debug logs are retained in the session directory after closeout. They are not promoted to the evidence archive or any cross-session artifact.

### 19.7 Automatic Logging (Claude Code Hooks)

When running in Claude Code with debug logging enabled, the session can use hooks to automatically capture dispatch events without relying on model self-logging. This provides a mechanical floor — dispatches and returns are always captured, regardless of model attention allocation under context pressure.

**Components:**

- **`cowork/hooks/log-dispatch.sh`** — Triggered by PreToolUse, PostToolUse, and SubagentStop on the Task tool. Appends §19.2-format entries to `orchestrator-trace.md` with timestamps, prompt text (truncated per §19.2 if >500 words), duration (correlated across Pre/Post pairs), and result summaries. All hook-generated entries carry a `[HOOK-GENERATED]` marker to distinguish them from model-written entries.
- **`cowork/hooks/audit-closeout.sh`** — Triggered by SessionEnd. Walks the session directory and checks every `.md` file for template stub indicators (unresolved bracket placeholders). Writes a compliance report to `debug-logs/closeout-audit.md` listing each file's status (populated / stub / empty) with a summary count and compliance verdict. This implements a mechanical version of the §5.5 Closeout File Audit.
- **`cowork/templates/hooks-settings.json`** — Configuration template for `.claude/settings.json`. Points hooks to the scripts in `cowork/hooks/`. Copied or merged into the session's settings during bootstrap (Step 2).

**Relationship to §19.5 self-logging:** Hooks capture the mechanical facts — that a dispatch happened, what prompt was sent, what came back, how long it took. Self-logging (§19.5) captures the semantic layer — reasoning decisions, context injected, files writable, trace integrity checks. The two are complementary. Hooks ensure the trace is never empty; self-logging enriches it when the model complies. If both are active, the trace contains interleaved `[HOOK-GENERATED]` entries (automatic) and unmarked entries (model-written).

**Scope limitations:** Hooks fire on Task tool dispatches only. In single-session-sequential mode (where the model role-plays multiple agents in a single context rather than dispatching subagents), there are no Task calls to intercept and hooks provide no dispatch logging. The closeout audit hook works in all modes. If a session uses single-session-sequential mode with debug logging enabled, the trace depends entirely on §19.5 self-logging for dispatch records.

**Not a replacement for protocol compliance:** Hooks address one failure mode (model forgetting to log). They do not address: session-status.md population during execution, deliberation-status.md updates between rounds, shortfall log entries, or any other mid-execution obligation. Those remain model responsibilities enforced at Phase Gates (§7.4 Session Lifecycle Compliance).

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-16 | Initial version — created during product roadmap session bootstrap |
| 1.1 | 2026-03-17 | Deliberation enforcement (Step 3b), multi-domain assessment (§7.5), phase compression warning |
| 1.2 | 2026-03-17 | Tension severity, independence levels, Phase Gate Enforcement Protocol, Mandatory Retrospective |
| 2.0 | 2026-03-17 | Dual-mode support (Cowork + Code). Backported v5.7: OD staleness triggers (§4), scoring protocol (§7.6), dependency validation (§7.7), parallelism rules. Added: domain model authoring guidance (§3.1), kill-vs-pivot precedence (§7.1), pivot_override decision type (§8.2), guardrail calibration check (§12.1), Claude Code specifics (§18). |
| 2.1 | 2026-03-17 | Closes 6 structural gaps: guardrail architecture (§4.1), signal taxonomy (§6.2), health computation formulas (§7.1-7.3), agent failure/safe defaults (§14), Governor succession (§15), self-update mechanism (§16). |
| 2.2 | 2026-03-17 | 23 fixes from six-dimension assessment. Tactic template (17 fields), A/B testing (§7.8), domain model + health report templates, guardrail check in Step 3, 3 integrity rules, blocker+knowledge_flag signals, global propagation, cross-session feedback. |
| 2.3 | 2026-03-17 | 9 fixes from geopolitical-sim session. PA-1: signal triage mechanism (§6.4). PA-2: compound signal model. PB-1: narrative_assessment signal type. PB-2: analytical guardrails (quality criteria type). PB-3: guardrail evaluation timing (per-phase vs deliverable). PB-4: composite score normalization formula (90/70/40/10). PB-5: source credibility modifiers + temporal validity fields. PC-1: partial exit criteria guidance. PC-2: deliverable naming convention. References updated to GOSTA v6.1. |
| 2.4 | 2026-03-20 | Deliberation Protocol integration. §7.5: Three-level escalation model (Level 1 inline, Level 2 sequential isolation, Level 3 multi-agent deliberation) with explicit escalation triggers and Cowork/Code mode details. §18.5: Distinguished direct scoring parallelism from Deliberation Protocol rounds. All references updated to GOSTA Framework v6.0 and Deliberation Protocol v0.4. |
| 2.5 | 2026-03-20 | Grounding architecture operationalized. §12 restructured from 3 thin subsections to 5 enforcement-backed grounding components (from Framework §14.3). §12.1: Schema validation with enforcement at bootstrap and phase gates. §12.2: Domain model grounding with `[UNGROUNDED]` flag protocol, scoring grounding, anti-pattern detection. §12.3: Signal provenance requirements by source type with `[PROVENANCE-INCOMPLETE]` flag and 50% weighting rule. §12.4: Attribution validation — signals without attribution rejected. §12.5: Synthesis verification for Level 3 (cross-ref to Deliberation Protocol §9.3). §5.1 Steps 3 and 4 gain inline grounding checkpoints. §6.1 signal format gains Provenance field. §18.4 validation scripts expanded for grounding audit. |
| 2.6 | 2026-03-20 | Attribution enforcement in health computation. §7.1 gains Attribution Validation step before health computation: OD reference check, orphan detection (`[ORPHANED]` flag), orphan exclusion from composite scores, provenance cross-check with §12.3. Orphaned signals (referencing killed tactics or removed strategies) are excluded by default — Governor can reclassify with updated attribution. |
| 2.7 | 2026-03-21 | Feedback architecture completeness. §6.2: `environmental` signal type added to taxonomy (from Framework §7.14). §7.3: Goal health computation rewritten from basic objective-progress to full §20.12 computation (objective portfolio assessment, environmental alignment, goal health composite with maintain/investigate/reassess recommendations). Health report template: goal health section updated to §20.12 format, computation trace section added (from Framework §20.1). OD template: environmental watch list section added (from Framework §7.14.1). Signal-entry template: `environmental` type added. |
| 2.8 | 2026-03-21 | Integrity architecture. §12.7: Semantic Coherence Validation operationalized — kill condition evaluability (C1, blocking), allocation arithmetic (C2), temporal ordering (C3), hypothesis-domain coherence (R1), WMBT-objective alignment (R2), guardrail consistency (R3/R4), reconciliation check (§8.2.3). §12.8: Decision-to-State Traceability operationalized — decision-first write protocol, authorization sources (DEC/GOV/SYSTEM), cross-session gap mitigation. Health report template: Semantic Coherence section added. Decision entry template: Authorization field added. Bootstrap: kill condition evaluability in Session-Start Integrity. |
| 2.9 | 2026-03-21 | Integrity cross-document consistency. §5.1: Step 3c added — coherence check at authoring time (C1-C3 at creation, R1-R4 + reconciliation at strategy review). §12.1: added §12.7 relationship paragraph (structural vs semantic validation complement). Session-log template: Semantic Coherence section added. Learnings template: Coherence Validation Patterns subsection added. OD template: `authorized_by` field added to strategy and tactic sections. |
| 3.0 | 2026-03-21 | Attribution architecture. §12.9: OD State Versioning — decision context snapshots (target spec, prior_authorized_by, key signals, environmental context at decision time), cross-session edit detection via OD fingerprint in bootstrap. §12.10: Causal Context at Kill Decisions — 6-point confounder checklist (environmental change, sibling interference, input starvation, data quality, bootstrap insufficiency, allocation change), confounder recording in decision entries, extension to pivots/strategy kills at ROBUST. Decision-entry template: context snapshot and confounders sections added. Bootstrap template: OD fingerprint field added. |
| 3.1 | 2026-03-22 | Reasoning depth validation. §12.2.1: Reasoning Depth Validation operationalized from Framework §14.3.7 `[ROBUST]`. Three self-checks at decision points: depth check (concept engagement vs decoration), coverage check (relevant concept scan with `considered_not_material` audit trail), chain integrity check (inferential completeness). `[SHALLOW]` flag for insufficient engagement. Interaction with tension surfacing documented. §12 intro updated: six → seven grounding components, reasoning corruption category added. |
| 3.2 | 2026-03-22 | Ecosystem consistency for P2/P3 production readiness. §15.1.1: Governance feature implementation by tier added — Governor succession, capacity validation, delegated reviewers, informed override operationalized at Tier 0 (conversational), Tier 1 (system-enforced), Tier 2+ (predictive). From Framework §6.1 tier guidance. |
| 3.3 | 2026-03-22 | Live session dashboard. §3: `session-status.md` added to file structure as overwrite-only live dashboard. §5.1 Step 6b: session-status update triggers defined (session start/end, phase gates, decisions, health computations, deliberation rounds, signal batches). File convention updated: bootstrap and session-status are the two overwrite-only files. Template: `cowork/templates/session-status.md` with scope state, active tactics, pending Governor actions, signal pipeline, deliberation status, next reviews, resource utilization. |
| 3.4 | 2026-03-22 | Field complexity determination. §4: Added field complexity determination step before OD template population. AI must check scope's adopted features (deliberation, A/B testing, domain model stacking, dependency tracking) to determine which conditional field sections ([CORE]/[ROBUST]/[ADVANCED]) to include. Inapplicable fields within an included level use N/A rather than omission. Closes gap where §4 said "use the template" but never instructed the AI to evaluate the template's conditional field markers against scope configuration. |
| 3.5 | 2026-03-22 | Mirror-derived enhancements (Finding Classification). §7.1-7.3: Health recommendations carry epistemic classification (confirmed/information_gap/conditional) per Framework §14.3.8. Kill recommendations classified as `information_gap` block autonomous execution at Stage 3+. §12.5: Finding Classification verification added to Governor synthesis review obligations. §4.1: Mechanical guardrails evaluated first, always receive `confirmed` classification. Health report template: Classification column added. Computation Trace: Classification Justification field. References updated to Framework v6.0. |
| 3.6 | 2026-03-23 | Sycophancy Detection operationalization (Framework §14.3.9).
| 3.9 | 2026-03-25 | Shortfall fixes from roadmap-analysis-2 (FG-001, PG-002, PG-003). §5.1 Phase Gate Enforcement Protocol: Item 8 (Dependency Amendment Gate) — synthesis-derived dependency graph amendments must be registered as DEP-AMEND-NNN, presented as named decision items at phase gate, and explicitly accepted/rejected by Governor before sequencing begins. Item 9 (Cross-Phase Consistency Check, CPCC) — mechanical circular dependency detection across merged dependency graph + agent prerequisite registry constraint sets; constraint application blocked until any CD-NNN is resolved. startup.md Step 9: G-6 Deliberation Calibration block — traceability guardrail threshold must equal agent roster size (N) when deliberation is enabled; §14.7 minimum of ≥3 superseded. startup.md Step 6: Narrative Options-Universe Gate — when options-universe document lacks a discrete numbered list, AI must derive, present, and get Governor confirmation of item list before scoring begins. |
| 3.8 | 2026-03-24 | Reference pool semantic agent. §18.5 rewritten: semantic pool-agent replaces index-first approach for pools >50 items. Tool at `cowork/tools/pool-agent.py` (all-MiniLM-L6-v2 ONNX, no torch, no API). Score thresholds: ≥0.58 full read / 0.50–0.57 excerpt / <0.50 ignore. Fallback index-first retained for pools without a built store. OD template: Reference Materials section added with `pool_consumption` and `pool_agent_store` fields. §18.3 session CLAUDE.md snippet: pool-agent invocation pattern and score thresholds added. CLAUDE.md Core Rules: pool-agent rule added. |
| 3.7 | 2026-03-23 | Evidence pool and scoring robustness (from product-value-validation session feedback FB-001 through FB-006). Signal-first execution pattern and compressed signal format (from stress-test report Gap 1.2). OD template scope-type branching for analytical objectives (from stress-test report Gap 1.3). §18.5: Reference Pool Consumption Strategy — index-first protocol for pools >50 items, OD `pool_consumption_strategy` field, checkpoint-before-narrative pattern. §18.5→§18.6 renumbering (Multi-Agent Parallelism). §5.2 Bootstrap Session: Guardrail feasibility check — verify guardrails referencing evidence can be enforced given actual inputs, `feasibility-limited` flag for structurally unsupported guardrails. Phase Gate Enforcement Protocol item 7: Kill condition discriminating power check — assess whether kill conditions could plausibly trigger given known inputs, `non-discriminating` flag with recalibration recommendation. §7.6: Per-domain anchoring for multi-domain scoring — 3 reference anchors per domain, mid-pass consistency check for >30 scoring decisions. OD template: Evidence Blind Spots field in tactic template — declare items where pool structurally cannot observe failure modes, alternative evidence sources, `[BLIND-SPOT]` annotation. OD template: Domain Model Adaptations section — per-concept applicability mapping (applies/does-not-apply/requires-interpretation) when reusing models across analytical contexts. | §6.2: Signal integrity check — narrative-quantitative divergence detection with `[DIVERGENCE]` tag. §7.1: Kill Proximity Alerting (20% threshold, consecutive cycle tracking), Signal-Recommendation Consistency Check (flag when signals trend negative but persevere recommended), Signal Integrity Check (discard qualitative framing for divergence-tagged signals). §7.1 Output: Mandatory non-empty Risk Factors section with sycophancy self-check. Sycophancy self-check timing specified: after Signal Integrity Check, before output generation, with previous cycle comparison. §5.1 Step 1b: Bootstrap state conflict resolution protocol added — decision log authoritative for decisions, OD for structure, bootstrap is summary. `bootstrap_anomaly` signal on conflict. §7.5: Cross-deliberation dissent frequency tracking (`low_dissent_frequency` flag). §12.5: Sycophancy verification in Governor synthesis review (Coordinator framing bias check). CLAUDE.md: Core Rules for risk surfacing and alignment checking. Templates updated: health-report.md (Risk Factors section, Signal-Recommendation Alignment fields, Sycophancy Indicators), signal-entry.md (Signal Integrity Check), session-log.md (Sycophancy Flags field), operating-document.md (kill proximity threshold), learnings.md (Dissent Frequency Tracking), deliberation-status.md (Independence Assessment). |
| 3.11 | 2026-03-26 | Consistency audit fixes (cowork ↔ deliberation protocol ↔ spec). §7.6: Scoring scale bands aligned to spec §20.10 (5 bands: 1-2 Absent, 3-4 Weak, 5-6 Moderate, 7-8 Strong, 9-10 Exceptional — was 4 bands). §7.5: Min Rounds hard floor cross-referenced from Deliberation Protocol §5.1; role-bleed warning expanded with mitigation actions; convergence probe cross-referenced from §4.5. §3 File Structure: deliberation/ directory added. §4: OD Deliberation section requirements specified with cross-reference to Deliberation Protocol §2.1. §6.1: Agent Source field added to signal format (deliberation-mode only). §12.5: Extended grounding obligations paragraph added referencing Deliberation Protocol §10.5. §3.1: Domain model authoring protocol cross-reference added. §3.1.1: First-cycle correction-derived domain model creation (operationalizes Framework §21.11). §4 replacement protocol: four concrete replacement options with routing to authoring procedures. §6.3 triage threshold and §12.2 UNGROUNDED flag: routing to domain model creation procedures. |
| 3.12 | 2026-03-30 | Cross-Boundary Claim Propagation (Framework §14.3.10). §6.2: `claim_propagation` signal type added — emitted when claims cross agent trust boundaries during deliberation, with grounding status metadata (source_agent_id, grounding_status, boundary_crossed, propagation_flag). §12 intro updated: seven → eight grounding components, claim laundering (continuity corruption) added. §12.11: Cross-Boundary Claim Propagation operationalized — three propagation failure modes (flag stripping, authority accumulation, cross-session persistence), grounding provenance flags table (`[GROUNDED]`, `[UNGROUNDED]`, `[PARTIALLY-UNGROUNDED]`, `[PROPAGATED-UNGROUNDED]`, `[CROSS-DOMAIN]`), four propagation rules, seven trust boundary types table, tier implementation (0/1/2+), interaction with §12.5 Synthesis Verification. OD template: Agent Roster gains Trust Boundaries column with per-role boundary declarations. Deliberation Protocol updated to v0.9 (position paper cross-boundary claims, synthesis propagation audit, roster trust boundaries, coordinator propagation tracking). |
| 3.13 | 2026-04-18 | Agent Debug Logging (§19). New section: two-way parent-child execution tracing. §19.1: Storage structure (`debug-logs/` directory). §19.2: Orchestrator trace format — own actions + dispatch records with trace integrity check. §19.3: Child agent trace format — incremental step-by-step execution log. §19.4: Standard debug logging injection block — protocol-level template appended to all dispatch prompts when enabled. §19.5: Orchestrator self-logging discipline. §19.6: Interaction with shortfall logging, evidence collection, deliberation, phase gates, closeout. startup.md: Group 1 toggle, Phase 2 summary field, Step 2 scaffold, Phase Gate 0→1 criterion. |
| 3.14 | 2026-04-19 | AFC integration, logging compliance (SFL-008), evidence context management. §4.1a: Analytical Frame Contract — stance, output verb, failure mode, prohibited frame, verdict vocabulary (operationalizes Framework §9.2). §7.5: Dispatch Preamble gains AFC constraint as injectable prompt element; evidence loading strategy row added (direct load vs. pool-agent retrieval per evidence-collection-protocol §6.4); dispatch verification check extended to 4 steps with evidence loading confirmation. §12.12: Frame Integrity Validation — per-section frame drift check against AFC fields at deliverable completion. §12.13: Guardrail attestation log — structured per-guardrail compliance record at deliverable and phase gate. §5.1: OD mutation journal added to session log — cascade check recording for OD changes. Phase Gate Enforcement Protocol: lifecycle compliance field added. §19.5: Orchestrator trace minimum checkpoint obligation — trace entries required at phase gates, dispatch, and completion events. startup.md: Group 2A AFC derivation, F-16 fidelity checkpoint, AFC-to-OD propagation rule, domain model frame audit, goal correction procedure, SFL-001 domain model adaptation intent gate, SFL-002 scaffold verification step, evidence context management (§5.3 build/consumption split, §6.4 pre-dispatch content estimation, per-domain loading threshold in Group 3B and evidence-collection-config template). |
| 3.15 | 2026-04-19 | Phase Gate enforcement hardening, closeout audit, and automatic logging (SFL-009 through SFL-015 + hooks). Phase Gate: Item 8 Input fidelity attestation (0→1 only, F-16 pass/fail, blocking if not run); Synthesis Verification field (when deliberation completed); session-status.md and deliberation-status.md currency fields in lifecycle compliance; orchestrator trace strengthened to dispatch-count verification; Shortfall Cross-Check field cross-referencing lifecycle corrections against shortfall entries; items 9-11 renumbered (was 8-10). §5.5 Closeout: structured compliance table (step 8) listing all scaffolded files with disposition, blocking on unresolved stubs. §19.7: Automatic Logging via Claude Code hooks — `cowork/hooks/log-dispatch.sh` captures Task dispatches/returns to orchestrator-trace.md without model cooperation; `cowork/hooks/audit-closeout.sh` detects template stubs at SessionEnd; `cowork/templates/hooks-settings.json` configuration template; startup.md Step 2 hook setup integration. |
