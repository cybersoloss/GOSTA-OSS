# Operating Document: [Scope Name]
**Version:** 1 | **Date:** [YYYY-MM-DD] | **Governor:** [Name]
**Scope Type:** [finite | ongoing] | **Graduation Stage:** 1

## Goal
[Broad statement of strategic intent]

### Guardrails
Each guardrail must declare severity and (for soft) a recovery specification.
Guardrails must be set ABOVE current baseline (for worse-is-higher metrics) or BELOW (for worse-is-lower). They prevent deterioration, not mandate targets.

- **G-1:** [Constraint description] | Severity: [hard | soft] | Evaluation: [mechanical | interpretive] | Threshold: [value]
  - Recovery (soft only): [Concrete, executable recovery action]
- **G-2:** [Constraint description] | Severity: [hard | soft] | Evaluation: [mechanical | interpretive] | Threshold: [value]

**Severity guidance:**
- `hard` = violation requires immediate stop. All in-flight actions halt. Governor must approve resumption. Use for: legal prohibitions, ethical boundaries, irreversible damage thresholds, budget caps.
- `soft` = violation is flagged and the recovery action executes. Execution continues while recovering. If recovery fails or the metric does not improve within the recovery window, escalate to Governor. Use for: quality thresholds, timeline targets, operational limits where degradation is tolerable short-term.

**Evaluation mode guidance:** `mechanical` = numeric threshold checkable by direct comparison (budget, timeline, rate). `interpretive` = requires judgment (compliance, quality, appropriateness). Default: `interpretive`.

## Objectives

**[Ongoing scope — use this form]**
### OBJ-1: [Measurable target with deadline]
- **Metric:** [What is measured]
- **Baseline:** [Current value — guardrails must be calibrated relative to this]
- **Target:** [Success threshold]
- **Deadline:** [Date]
- **Priority:** `[ROBUST]` [critical | high | standard] — default: critical if undeclared. Critical+at_risk triggers immediate scope review (§20.12). Multi-goal scopes: worst-goal-drives-scope-status.

**[Finite scope — use this form instead]**
### OBJ-1: [Name]
- **Analytical Question:** [The specific question this scope answers]
- **Acceptance Criteria:** [What "good enough to decide from" looks like — e.g., "all features assessed with ≥3 evidence items each"]
- **Deliverable:** [The artifact produced — e.g., "feature-evidence matrix with per-feature verdicts"]
- **Quality Standard:** [How the deliverable is evaluated — e.g., "every verdict cites specific evidence by ID and specific domain model concepts"]
- **Priority:** `[ROBUST]` [critical | high | standard] — default: critical if undeclared.

## Strategies
### STR-1: [Named approach] → serves OBJ-1
- **Rationale:** [Why this approach]
- **What Must Be True (WMBT):** [Assumptions that must hold]
- **Not Doing:** [What this strategy deliberately excludes]
- **Kill Signal:** [What falsifies this strategy]
- **Relationship to sibling strategies:** [competing | complementary]
- **Authorized By:** `[ROBUST]` [GOV-session-1 | DEC-N — reference to the decision that created or last modified this strategy. For initial OD authoring: GOV-session-1. For subsequent modifications: DEC-N referencing the specific decision entry.]

## Tactics
### TAC-1: [Named tactic] → serves STR-1
**[CORE — required for any GOSTA implementation]**
- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1
- **Hypothesis:** [If we do X, we expect Y]
- **Kill Condition:** [If metric hasn't reached threshold by date, kill. For execution-only tactics (deliverables, builds, analyses): use completion-based form — default: "deliverable not accepted after 3 revision cycles". Other forms: deadline_exceeded, cost_exceeded, scope_exceeded. `Kill Condition: N/A` is a C1 violation — every tactic must have an evaluable kill condition (§8.1.1). **Qualitative kill conditions (§3.6)** must pass three checks: (1) observable state — references a state that can be observed, not just inferred; (2) observation point — specifies where/when the state is observed; (3) binary outcome — produces a yes/no assessment, not a spectrum. Example passing: "If Governor rates deliverable quality below 'acceptable' after reviewing final draft." Example failing: "If results are disappointing" (no observation point, no binary threshold).]
- **Success Metrics:** [What we measure — list all]
- **Guardrails (inherited):** [Accumulated from Goal + Objective + Strategy levels]
- **Guardrails (own):** [Additional tactic-specific guardrails, if any]
- **Timeline:** [Start — End]
- **Bootstrap Cycles:** [N — kill assessment suspended during bootstrap]
- **Seed Actions:** [Initial actions for bootstrap period — what to do before signals exist]
- **Evidence Blind Spots:** [Optional. Declare specific items, features, or problem domains where the reference pool cannot observe relevant failure modes — e.g., pre-incident features evaluated against a post-incident evidence pool. For each blind spot: (1) identify the item/feature affected, (2) explain why the pool structurally cannot evidence it, (3) declare the alternative evidence source (regulatory mandate, structural reasoning, external research, Governor-supplied data). Blind spot items receive modified scoring: alternative evidence substitutes for pool evidence, with explicit documentation that pool-based validation was impossible. Scores derived from alternative evidence carry a `[BLIND-SPOT]` annotation in deliverables. If no blind spots exist, omit this field.]
- **Authorized By:** `[ROBUST]` [GOV-session-1 | DEC-N — reference to the decision that created or last modified this tactic. At Stage 3+, autonomous tactic creation by the orchestrator uses DEC-N referencing the autonomous decision entry per §8.2.2. For SYSTEM-triggered changes (e.g., allocation renormalization per §4.3): SYSTEM-renormalization.]

**[ROBUST — include when adopting A/B testing, domain model stacking, deliberation, or detailed dependency tracking]**
- **Owner:** [Who is responsible — Governor, AI, or named person]
- **Approach:** [How the hypothesis will be tested — description of the method]
- **Dependencies:** [execution: AI can do it | external: needs third party | human_creative: needs Governor input]
- **External Dependencies (§4.3):** [For tactics with external parties — list as: `{entity: [name], type: contract|partner|regulatory|infrastructure, exit_cost: low|medium|high, exit_notice: [duration]}`. Empty if no external dependencies. Orchestrator flags tactics referencing external parties in actions but with empty dependency field.]
- **Domain Model Dependencies:** [Which domain models this tactic's hypothesis and kill condition rely on. Used for failure-to-model-feedback traceability — when a tactic is killed, these models are candidates for calibration per Deliberation Protocol §12.4. Format: model-name (concepts: X, Y, Z)]
- **Human Creative Input Estimate:** [N inputs per cycle expected from Governor]
- **Review Date:** [When the next tactic review is scheduled]
- **A/B Variant:** [If this tactic is part of an A/B test, which variant and what's it compared against]

**[ESSENTIAL — include when adopting tournament execution for this tactic]**
- **Tournament Mode:** [sampling | constrained] — enables tournament execution (§4.6). Omit if standard single-run.
- **Tournament Runs:** [2-8] — number of competing deliverables. For constrained: should equal behavior space cell count.
- **Tournament Behavior Space (constrained only):**
  | Dimension | Values | Source | Rationale |
  |---|---|---|---|
  | [dimension] | [value-1, value-2, ...] | [domain model tension / guardrail pair / reference pool / trade-off] | [why this dimension produces structural differentiation] |
  Produced via Dimension Elicitation Protocol (§4.6): AI proposes candidates from session context → Governor curates and declares.
- **Tournament Cell Assignments (constrained, partial coverage only):** [which cells to populate if runs < cells]
- **Tournament Selection:** governor_choice (default). At [ROBUST]: highest_mean | highest_minimum also available.

- **Tactic Dependencies (§3.6):** [For sequential or dependent tactics — `depends_on: TAC-N (exit_criteria: [condition])`. If TAC-N fails or is killed, orchestrator assesses cascading failure impact on this tactic. Empty if independent.]
- **Guardrail Calibration (§3.6):** [For first-time guardrails with no baseline data — `calibration: first_use`. Guardrail operates in observation mode during first assessment cycle (flags but doesn't enforce). Default: `calibrated` (normal enforcement).]
- **Preconditions (§7.2):** [Conditions that must hold before tactic execution proceeds — e.g., "API key provisioned", "baseline data collected". Format: `{condition: [description], status: met|unmet|deferred, deferred_since: [date], override: none|governor_approved}`. Tier 0: AI evaluates conversationally and tracks deferral count. Tier 1: programmatic timeout triggers escalation after N cycles deferred. Tier 2+: predictive estimation of resolution timeline.]
- **Resource Ceiling (§7.2):** [Maximum Governor-hours or AI-hours this tactic may consume per cycle. Format: `{governor_hours: [N]/cycle, ai_hours: [N]/cycle, current_utilization: [N%]}`. When total across tactics exceeds Governor declared capacity (§6.1), orchestrator trims lowest-priority tactics. Tier 0: AI estimates conversationally. Tier 1: automated field summation. Tier 2+: predictive projection of workload spikes.]
- **Allocation Rebalancing Trigger (§7.2):** [Conditions under which this tactic's resource allocation should be reviewed — e.g., "if health drops below 40%" or "if sibling tactic killed". Tier 0: AI proposes rebalanced weights conversationally. Tier 1: programmatic computation with draft decision. Tier 2+: impact simulation with historical performance projections.]

**[ADVANCED — include for metric lag modeling, metric prerequisites, or production-level traceability]**
- **Related Function:** [If this tactic maps to a code function/module in the implementation]
- **Metric Prerequisites:** [Conditions that must be true before kill assessment begins — beyond bootstrap]

## Actions (Current Cycle)
[For finite scopes: this section references the actions from the CURRENTLY ACTIVE Phase (see Phases section below). When Phase 1 is active, list Phase 1's actions here. When transitioning to Phase 2, replace with Phase 2's actions. This section answers "what should the AI do RIGHT NOW?" — the Phases section answers "what's the full plan across all phases?" Both must exist for finite scopes.]

### ACT-1: [Task] → serves TAC-1
- **Assignee:** [Governor | AI]
- **Deliverable:** [What is produced]
- **Deadline:** [Date]
- **Dependency Type:** [execution | external | human_creative]

## Review Cadences
- **Finite scope:** Review at each phase gate
- **Ongoing scope:** Action cycle [frequency], Tactic review [frequency], Strategy review [frequency]

## Decision History
[Append-only log of OD changes with date, what changed, why]

---

## Phases (finite scopes only)

### Phase 1: [Name]
- **Objective:** [What this phase produces]
- **Entry Criteria:** [What must be true to start]
- **Exit Criteria:** [What must be true to advance]
- **Actions:** [List]

### Phase 2: [Name]
...

---

## Autonomy Safeguards (from GOSTA §6.7)

### Magnitude Thresholds
Decisions exceeding any threshold require Governor approval regardless of graduation stage.
- **Resource cost:** [e.g., "$5,000 committed spend" | not set]
- **Timeline impact:** [e.g., "delays objective deadline by >2 weeks" | not set]
- **Stakeholder visibility:** [e.g., "visible to customers or partners" | not set]
- **External commitment:** [e.g., "creates or terminates external commitments" | not set]

### Autonomy Conditions
Time-bounded, event-triggered, or metric-triggered constraints on autonomy. Remove section if none.
- **COND-1:** [Trigger description] | Scope: [which tactics/strategies affected] | Reversion: [Stage N] | Expiry: [when condition becomes irrelevant]

### Failure Resilience Thresholds (from GOSTA §7.13)
Optional. Configure if scope has graduated to Stage 3+ or if signal reliability is a concern.
- **Signal freshness cadence:** [per-tactic expected cadence, or default to shortest review cadence]
- **Recovery stability window:** [N cycles — recommend 2 for pipeline, 1 for agent]
- **Chronic instability threshold:** [N relapses before permanent degradation declared — recommend 3]
- **Governor review capacity:** [max non-trivial decisions per review session — triggers batching if exceeded]
- **Kill proximity alert threshold:** [N% — default 20%. Metrics within this distance of kill threshold are prominently surfaced in health report Risk Factors section.]

### Governor Attention Capacity (from GOSTA §6.1) `[ROBUST]`
- **Reviews per Week:** [N — total tactic + strategy reviews. Compute: sum(1 / cadence_days × 7) across all active tactics and strategies]
- **Role:** [part_time | full_time] — part_time default threshold: 5 reviews/week, full_time: 15/week
- **Sustainability Flag:** [If projected reviews/week exceeds threshold, note here. Orchestrator flags at tactic creation and strategy review.]

### Execution Cost Tracking (from GOSTA §13.3) `[ROBUST]`
Declare cost categories relevant to this scope. Empty if no metered resources apply.

| Category | Unit | Budget per Cycle | Notes |
|---|---|---|---|
| [api_calls / compute_time / search_queries / external_data / other] | [unit] | [threshold] | [e.g., "shared across all tactics" or "per-tactic"] |

Orchestrator tracks per-tactic cost accumulation and flags `cost_exceeded` when any tactic exceeds its budget. `cost_data_missing` flagged when actions don't report cost metadata for declared categories.

### Environmental Watch List (from GOSTA §7.14)
External conditions whose change would materially affect this scope. Check at each strategy review (Tier 0) or continuously (Tier 2+).

| ID | Condition | Relevance | Monitoring Method | Check Cadence | Change Threshold |
|---|---|---|---|---|---|
| ENV-1 | [external condition to monitor] | [which goal/strategy/WMBT it affects] | [manual_governor / automated_api / scheduled_search] | [strategy review / weekly / daily] | [what level of change warrants a signal] |

## Reference Materials

*Omit this section if the scope has no reference pool.*

| File | Path | Role | Notes |
|---|---|---|---|
| [pool name] | `[path/to/reference-pool.yaml]` | context | [N]-item index. Do NOT load into context directly if N > 50 — use pool-agent. |
| [article dir] | `[path/to/articles/]` | context | Full article content. Read on demand via sourceDir/sourceFile fields. |

**Pool consumption configuration** *(required if pool > 50 items)*:
```
pool_agent_store: [path/to/pool-store/]
pool_consumption: semantic-agent
pool_size: [N]
score_threshold_full_read: 0.58
score_threshold_excerpt: 0.50
```

*If pool ≤ 50 items, set `pool_consumption: direct-yaml` and omit the remaining fields.*

## Domain Models Referenced
- [domain-model-name] — [which aspects are relevant to this scope]

## Domain Model Adaptations

When reusing a domain model written for a different analytical context (e.g., a model built for roadmap sequencing applied to a value validation scope), a single-line context note is insufficient to prevent scoring drift. Instead, complete this adaptation table for each reused model. This section is optional — omit if all domain models were authored specifically for this scope.

| Domain Model | Original Context | This Scope's Context | Adaptation |
|---|---|---|---|
| [model name] | [what the model was written for] | [how it's used in this scope] | See table below |

**Per-concept applicability mapping (one per adapted model):**

| Concept ID | Concept | Applicability | Notes |
|---|---|---|---|
| [QP-1] | [concept name] | applies / does-not-apply / requires-interpretation | [If requires-interpretation: explain what the concept means in this scope vs. its original scope] |
| [AP-1] | [concept name] | applies / does-not-apply / requires-interpretation | |
| [GV-1] | [concept name] | applies / does-not-apply / requires-interpretation | |

Concepts marked `does-not-apply` are excluded from scoring. Concepts marked `requires-interpretation` must include a one-line reframing in the Notes column. During TAC-2 scoring, the AI references this table — not the original model's framing — to prevent semantic drift between the original context and this scope's context.

## Multi-Domain Assessment
- **Independence Level:** [1 | 2 | 3] (default: 2 — Sequential Isolation)
  - Level 1: Ask before each action (maximum oversight)
  - Level 2: Sequential isolation — domains assessed independently, then synthesized (default)
  - Level 3: Multi-agent deliberation — Deliberation Protocol invoked for high-stakes decisions (requires 3+ domain models)
- **Deliberation Mode:** [enabled | disabled] (default: disabled)
  - If enabled: high-stakes decisions (strategy kill/pivot, feature sequencing, cross-domain conflicts) trigger the Deliberation Protocol (cowork/deliberation-protocol.md). One Domain Agent per domain model, Coordinator synthesizes, Governor resolves dissents.
  - If disabled: standard sequential assessment per §14.7 Level 1-2.

## Deliberation (when Deliberation Mode = enabled)

This section is required when Deliberation Mode is enabled above. It configures the multi-agent deliberation per Deliberation Protocol §2.1. Remove or leave as stub when deliberation is disabled.

### Agent Roster

| Agent ID | Domain Model | Role | Model/Provider | Trust Boundaries Crossed | Notes |
|----------|-------------|------|----------------|--------------------------|-------|
| [XX-1] | [Domain Name] | domain_agent | default | identity, communication | |
| [XX-2] | [Domain Name] | domain_agent | default | identity, communication | |
| [XX-3] | [Domain Name] | domain_agent | default | identity, communication | |
| COORD-1 | — | coordinator | default | identity, communication, planning, oversight | No domain model |

**Trust boundaries** (from Framework §14.3.10): Each agent role crosses specific trust boundaries where grounding status can degrade. Domain agents cross identity (separate agent instance) and communication (position paper → synthesis) boundaries. The Coordinator additionally crosses planning (strategic synthesis) and oversight (presenting to Governor) boundaries. For boundary type definitions, see Cowork Protocol §12.11.

**Roster rules:** One agent per domain model. Coordinator mandatory. Minimum 3 domain agents (below 3, use standard sequential assessment). Recommended 5-7 for full analytical depth; 8-10 viable with 4+ rounds; >10 use cluster-then-synthesize (see Deliberation Protocol §2.2). Agent IDs are stable for the scope's lifetime.

**G-6 Traceability Calibration** *(required — see startup.md Step 9 and Framework §21.8)*:
- **N (domain agents):** [count — auto-derived from roster above, excluding COORD-1]
- **Tolerated Fallback Proxies:** [0 | N] (default: 0 — Governor must specify if agent failures are acceptable. A value of 1 means one agent may fail and be replaced by a Coordinator proxy without triggering a G-6 violation.)
- **G-6 Threshold:** [= N − Tolerated Fallback Proxies] ← This value MUST be entered in the G-6 guardrail at the Goal level. It overrides the §14.7 multi-domain minimum of ≥3.

### Deliberation Cadence
- **Trigger:** [on_signal | on_schedule | on_governor_request | on_phase_gate]
- **Max Rounds:** [N] (finite default: 5, ongoing default: 2)
- **New Argument Gate (Round 4+):** [enabled | disabled] (default: enabled)
- **Governor Interaction:** [at_synthesis | mid_deliberation]
- **Agent Timeout:** [duration] (default: 5 min for Code mode, 1 session for Cowork)
- **Cost Budget:** [optional — max tokens or cost per deliberation cycle]
- **Pre-Deliberation Review:** [required | optional] (default: required)

### Deliberation Isolation Mode (Cowork mode only)
- **Isolation:** [single_session_sequential | multi_session]
  - `single_session_sequential` (default): All agents run sequentially in one conversation. Cowork Protocol Level 2 Sequential Isolation — complete one agent's position paper before starting the next. No back-revision.
  - `multi_session`: Each agent runs in a separate conversation session for true Level 3 isolation. Position papers written to files. Coordinator runs in a subsequent session. Expensive (N+2 sessions for N agents + coordinator + synthesis) but maximum isolation.

### Termination Thresholds
- **Convergence Definition:** [What counts as convergence — when can the Coordinator declare agents have agreed? See Deliberation Protocol §2.1 calibration guidance. For 3 agents, a 3-point confidence spread may still indicate convergence if recommendations align. For 5-7 agents, use a 2-point spread.]
- **New Argument Definition:** [What counts as a genuinely new argument vs. restatement? Default: introduces a domain concept not previously cited, or applies an existing concept to a scenario not previously analyzed. Reframing with different emphasis does NOT count.]
- **Stall Definition:** [What counts as a stall — how many rounds of zero progress before termination? Default: 2 consecutive rounds for rich domains, 1 round for thin domains (<5 concepts per model).]

### Role-Switching Protocol (single_session_sequential only)

In single-session sequential mode, the AI Session plays multiple deliberation roles within one conversation. To prevent role bleed (Coordinator bias from having just written domain positions, or domain agents being influenced by prior agents' positions), follow this protocol:

**Entering deliberation:**
The AI Session suspends its Orchestrator/Executor role. Announce: "Deliberation DELIB-[NNN] triggered. Suspending normal execution. Entering deliberation mode."

**Role transitions (Round 1 — domain agents):**
For each domain agent, explicitly announce the role switch and declare the context boundary:
```
--- ROLE: [Agent ID] ([Domain Name]) | Round 1 ---
Domain model: [domain model name]
Shared context: [OD version, evaluation target, relevant signals]
Instruction: Produce position paper from [domain] perspective ONLY.
Do not reference or incorporate reasoning from any prior agent's position.
Cite-then-apply: For each domain concept cited, state its definition from the domain model
before applying it. The "How It Applies" column in Domain Concepts Applied must be
traceable to the concept as defined — not a narrowed, broadened, or drifted version (§14.3.2).
---
```
Complete the position paper. Then announce: `--- END [Agent ID] Round 1 ---`

**Role transition (Coordinator — Interim Assessment):**
```
--- ROLE: COORD-1 (Coordinator) | After Round [N] ---
Position papers received: [list Agent IDs]
Instruction: Identify agreements, soft disagreements, hard disagreements, novel arguments.
Do NOT advocate for any domain position. Map the landscape only.
Check retrieval faithfulness: flag any agent whose concept application appears inconsistent
with the concept's domain model definition as [CONCEPT-DISTORTED] (§14.3.2, §10.5).
---
```

**Role transitions (Round 2+ — domain agents responding):**
Each responding agent receives ONLY:
- Its own prior position/response paper
- The Coordinator's Interim Assessment (the targeted prompt directed at this agent)
- NOT the full text of other agents' position papers (to prevent contamination — the Coordinator's summary is sufficient)

**Exiting deliberation:**
After the Coordinator produces the Synthesis Report, announce: "Deliberation DELIB-[NNN] complete. Synthesis report produced. Resuming Orchestrator role. Awaiting Governor decision on synthesis."

**Agent failure during role-switching:** If the AI Session fails to produce a valid position paper while acting as a Domain Agent (empty reasoning, no domain model citations, or content refusal), apply the graduated fallback sequence from Deliberation Protocol §1.1 while remaining in that agent's role:
1. Retry with clarified prompt (still as the same agent)
2. If retry fails: switch to reduced domain model (top 5 concepts) and retry
3. If reduced model fails: switch to Coordinator role and produce a proxy position statement from the domain model's Quality Principles and Anti-Patterns, clearly labeled `[PROXY]`
4. If all fail: log exclusion, switch to next agent
Do not switch to another Domain Agent's role while troubleshooting — complete or exclude the current agent first.

**Back-revision prohibition:** Once a position paper or response paper is written, it cannot be modified. If the AI notices an error in a prior agent's paper while writing a subsequent agent's paper, the error stands — it may surface naturally as a disagreement in the Coordinator's assessment. This is by design: back-revision destroys the independence guarantee.

### Deliberation File Structure
```
deliberation/
├── [DELIB-NNN]/                  ← One directory per deliberation cycle
│   ├── position-[AGENT-ID].md    ← Round 1 position papers
│   ├── interim-assessment-R[N].md ← Coordinator assessment after each round
│   ├── response-[AGENT-ID].md    ← Round 2+ response papers
│   ├── synthesis-report.md       ← Final coordinator synthesis
│   ├── cost-report.md            ← Token/cost tracking for the cycle
│   └── verification.md           ← Governor's synthesis verification checklist (from template)
```
Deliberation artifacts are append-only within a cycle. No artifact is modified after creation. The verification checklist is completed by the Governor after receiving the synthesis report — it is the Governor's audit artifact, not the Coordinator's.
