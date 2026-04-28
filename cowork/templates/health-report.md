# Health Report — [Date]
**Type:** [tactic | strategy | goal | phase_gate]
**Session:** [NNN]
**Scope:** [Session name]
*Valid values for all status fields, decision types, and signal types: see Framework Appendix B.*

---

## Tactic Health (per active tactic)

### TAC-[ID]: [Name]
- **Status:** [active | bootstrap (N/M cycles) | killing (§8.5.3 — intermediate state during cross-strategy kill sequence) | killed | killed_winding_down | completed | graduated (§7.8 — tactic→permanent operations) | exhausted | paused]
- **Metric Status:**
  | Metric | Current | Target | Kill Threshold | Status |
  |---|---|---|---|---|
  | [metric] | [value] | [target] | [threshold] | exceeded / on_track / at_risk / failing |
- **Kill Condition:** [safe | approaching (within 20%) | met | suspended (prerequisite gap)]
  - Kill condition type: [metric-based | completion-based (§8.1.1 execution-only default) | deadline-based | qualitative (§3.6 — must pass: observable state ✓/✗, observation point ✓/✗, binary outcome ✓/✗)]
- **Hypothesis Status:** [holding | weakening | falsified]
- **Human Creative Input Rate:** [N/M cycles with input] (if applicable)
- **Composite Health Score:** [0-100]
- **Tournament Status (if applicable):** [not_active | in_progress (N of M candidates generated) | completed (winner: [deliverable_ref], cell: [assignment])]
  - Health computed on selected deliverable only. Cross-cell score patterns inform the health narrative but do not change the computation formula.
- **Pivot Count:** [N] (if >0, note: 2+ pivots with no improvement → kill per §7.1)
- **Recommendation:** [kill | pivot | persevere] | **Classification:** [confirmed | information_gap | conditional]
- **Classification Basis:** [For confirmed: cite signals and attribution. For information_gap: specify missing data. For conditional: specify assumption and test.]
- **Signal-Recommendation Alignment (§14.3.9):** [aligned | divergence: justification required]
  - If divergence: **Divergence Justification:** [specific countervailing evidence — signal IDs, sources, reasoning]

---

## Strategy Health (per active strategy)

### STR-[ID]: [Name]
- **WMBT Status:**
  | Condition | Status | Evidence | Classification |
  |---|---|---|---|
  | [WMBT 1] | assumed / holding / at_risk / falsified | [signal reference] | [confirmed / information_gap / conditional] |
- **Approach Validation:** [confirmed | uncertain | disproven]
- **Tactic Portfolio:** [N healthy, N at_risk, N killed, N pending]
- **Child Scope Status (§4.3)** `[ADVANCED]`**:** [none | child scope [name] internal kill: TAC-[child-ID] killed → parent TAC-[N] receives `at_risk` signal, NOT auto-kill. Governor evaluates at next parent review.]
- **Cross-Domain Conflicts:** [None | Conflict: description]
  - If conflict involves 3+ domains AND deliberation mode is enabled in OD: flag for Deliberation Protocol escalation per Framework §14.7 Level 3.
- **Recommendation:** [kill | pivot | persevere] | **Classification:** [confirmed | information_gap | conditional]
- **Classification Basis:** [For confirmed: cite signals and attribution. For information_gap: specify missing data. For conditional: specify assumption and test.]
- **Signal-Recommendation Alignment (§14.3.9):** [aligned | divergence: justification required]
  - If divergence: **Divergence Justification:** [specific countervailing evidence — signal IDs, sources, reasoning]
- **Cross-Strategy Kill Batch (§8.5.3):** [none | batch: TAC-[N] (STR-X), TAC-[M] (STR-Y) — present jointly to Governor. Combined resource impact: [description]. Tactics in `killing` state pending batch resolution.]

---

## Goal Health (from GOSTA §20.12, computed at goal review)

### GOAL-[ID]: [Name]
- **Objective Portfolio:**
  | Objective | Metric Progress | Portfolio Health | Status |
  |---|---|---|---|
  | [objective] | [current] → [target] = [N%] | strong / moderate / weak | on_track / at_risk / failing / exceeded / partially_achieved (§3.1) |
- **Portfolio Assessment:** [strong | moderate | weak]
- **Environmental Alignment:** [aligned | drifting | misaligned]
  - Environmental inputs: [list sources checked — Governor report, environmental signals, knowledge flags]
  - Watch list changes since last goal review: [none | list condition_id changes with severity]
- **Goal Health:** [healthy | at_risk | reassess]
- **Recommendation:** [maintain | investigate | reassess] | **Classification:** [confirmed | information_gap | conditional]
- **Reasoning:** [Why this assessment — cite specific objectives and environmental factors]

**Multi-Goal Scope Aggregation (§20.12)** `[ROBUST]` — *Include when scope has 2+ goals.*
- **Scope Health:** [worst-goal-drives-scope: if any goal is `reassess` → scope `reassess`; if any goal `at_risk` → scope at minimum `at_risk`; scope `healthy` only when ALL goals `healthy`]
- **Priority-Driven Escalation:** [any critical-priority goal at `at_risk` → immediate scope-level review per §7.9 | standard-priority goals at `at_risk` → next scheduled goal review]

---

## Cross-Objective Tradeoff Assessment (from GOSTA §20.12) `[ROBUST]`

*Include when scope has 2+ objectives under the same goal. Omit for single-objective scopes.*

- **Tradeoff Detected:** [yes | no]
- **Objectives Involved:** [OBJ-X improving while OBJ-Y declining — describe temporal correlation]
- **Correlation Window:** [N cycles of inverse movement]
- **Hypothesized Mechanism:** [shared resource pool / shared customer base / operational capacity conflict / other]
- **Resolution Status:** [new — first detection | unresolved — detected N consecutive reviews | resolved — DEC-N]
- **Resolution Options (Governor decides):**
  - [ ] `accept_tradeoff` — gains worth losses; adjust declining objective via `revise_objective`
  - [ ] `constrain_improvement` — add guardrail to limit interference mechanism
  - [ ] `rebalance_portfolio` — shift resources via `portfolio_rebalance`
  - [ ] `decompose_metric` — separate shared factor for independent optimization
- **Governor Decision:** [pending | DEC-N with `decision_type: cross_objective_tradeoff`]

*Escalation: unresolved after 2 consecutive strategy reviews → flag `unresolved_cross_objective_tradeoff` in scope health.*

---

## Phase Gate Assessment (finite scopes)

### Phase [N] → Phase [N+1]
- **Exit Criteria:**
  | Criterion | Status | Evidence |
  |---|---|---|
  | [criterion] | met / partially_met / not_met | [reference] |
- **Recommendation:** [advance | iterate | restructure]

### Pre-Flight Validation Gate Results (per spec §8.7)

Per-invariant test outcomes at this phase boundary. PASS / WARN / BLOCK per row; BLOCK rows must be resolved before phase advances.

| Invariant | Test | Outcome | Notes |
|---|---|---|---|
| V1 Retrieval Contract | per-unit query matrix vs declared pools | PASS / WARN / BLOCK | Cell distribution: VALIDATED / CORPUS-FIT-GAP / VOCABULARY-MISMATCH / ESCALATE |
| V2 Build Artifact Shape | embeddings.npy shape vs expected chunking | PASS / WARN / BLOCK | Shape observed; expected ratio |
| V3 Decision Spine | OD ↔ scope key-set symmetric difference | PASS / BLOCK | (Phase 1 entry only) |
| V4 Continuous Capture | capture entries vs friction signals | PASS / WARN | Capture artifact line counts |
| V5 Runtime Imports | tool import-test results | PASS / BLOCK | (First-call per session only) |
| V6 Declared Artifact Existence | `test -s` per declared artifact | PASS / BLOCK | Missing-or-empty list |
| V7 Vertical-Fit | concept-coverage on inherited artifacts | PASS / WARN | (Phase 1 entry only) |

Any BLOCK row prevents phase advancement. WARN rows require explicit Governor acknowledgment in the phase gate request.

---

## Guardrail Status

| Guardrail | Severity | Evaluation | Threshold | Current | Status | Classification |
|---|---|---|---|---|---|---|
| [guardrail] | hard/soft | mechanical/interpretive | [value] | [value] | safe / near-violation / violated | [confirmed / information_gap / conditional] |

---

## External Dependency Viability (from GOSTA §4.3) `[ROBUST]`

*Include for any tactic with non-empty `dependencies` field in OD. Omit if no tactics have external dependencies.*

| Tactic | Dependency | Type | Exit Cost | Notice Period | Status | Kill Timing Impact |
|---|---|---|---|---|---|---|
| [TAC-N] | [entity] | [contract/partner/regulatory/infrastructure] | [low/medium/high] | [duration] | [active / strained / at_risk] | [immediate / must honor notice / cost to exit] |

- **Pre-kill recommendation (if kill pending):** [kill now | defer N cycles for notice period | renegotiate exit terms | transfer dependency to TAC-N]
- **Undeclared dependency flag:** [none | TAC-N references [external party] in actions but has empty dependency field]

---

## Execution Cost Status (from GOSTA §13.3) `[ROBUST]`

*Include when scope declares `execution_costs` in OD. Omit if no cost categories declared.*

### Per-Tactic Cost Tracking

| Tactic | Category | Budget | Consumed | Remaining | Status |
|---|---|---|---|---|---|
| [TAC-N] | [category] | [budget] | [actual] | [remaining] | [on_track / approaching / exceeded] |

- **Cost Guardrail Flags:** [none | `cost_exceeded`: TAC-N [category] at [actual] vs [budget] | `cost_data_missing`: TAC-N [category] — actions not reporting cost metadata]
- **Scope-Level Cost Summary:** [total across all tactics by category — enables Governor cost-effectiveness assessment]

---

## Deliberation Summary (when deliberation was triggered this review period)

Include this section only when a deliberation cycle was executed as part of this review.

### Deliberation Cycle [DELIB-NNN]
- **Trigger:** [what triggered this deliberation — signal threshold, Governor request, schedule]
- **Agents:** [list of Agent IDs that participated]
- **Rounds:** [N of max]
- **Outcome:** [full_consensus | strong_consensus | weak_consensus | split]
- **Recommendation:** [the synthesized recommendation — 1-2 sentences]
- **Unresolved Disagreements:** [N — list DIS-IDs if any, with 1-line summary each]
- **Agent Coverage:** [all agents completed normally / N agents required fallback / N agents excluded. If any fallback: list agent IDs, fallback type (reduced_model / proxy / excluded), and coverage impact. See Deliberation Protocol §1.1.]
- **Finding Classification:** [N confirmed, N information_gap, N conditional. Information gaps requiring data collection: list. Conditions requiring monitoring: list.]
- **Pre-Deliberation Review:** [completed (N updates made) | no changes needed | not performed]
- **Domain Model Feedback:** [any domain model calibrations, gaps, or prune candidates discovered during this deliberation. Reference Deliberation Protocol §12.4. "None" if no feedback signals detected.]
- **Governor Decision:** [accept | modify | override | remand] — DEC-[NNN]
- **Verification:** [passed | failed | pending — reference deliberation/DELIB-NNN/verification.md]
- **Cost:** [agents dispatched, rounds executed, estimated token consumption]

*Full synthesis report:* `deliberation/[DELIB-NNN]/synthesis-report.md`

---

## System Health (from GOSTA §7.13)

- **Signal Pipeline:** [normal | degradation: [N of M tactics stale] | failure: no new signals for [N] cycles]
- **Recovery Status:** [no active recoveries | recovering: [component] — cycle [N of M] stability window | chronically unstable: [component]]
- **Kill Timer Status (§7.7):** [no active kill timers | active: TAC-[N] mode: [pause — suspended, no execution, timer frozen | infrastructure_outage — extended by outage duration, execution continues with data gap | recovery — continues, tactic still executing] deadline: [date] remaining: [N cycles]]
- **Context Utilization:** [~N% | shed content: [list] | no shedding required]
- **Governor Decision Validations:** [none this cycle | flagged: [list] — [overridden | corrected]]
- **Governor Review Load (§6.1):** [N decision points this cycle / declared capacity N/week] — [sustainable | approaching limit | exceeded. If exceeded: recommend cadence adjustment, review batching, or tactic consolidation]
- **Recovery Oscillation (§7.13.2):** [none | [component]: [N] relapses — stability window cycle [N of M] | chronic: [component] — exceeded 3 relapse threshold, Governor escalation required]
- **Silent Failure Detection (§7.7):** [none | TAC-[N] action type [X]: [N] consecutive silent completions (completed with no signal) — [informational (1st) | significant (2nd) | critical (3rd+): tactic `data_quality: degraded`]]
- **Sycophancy Indicators (§14.3.9):** [none this cycle | flagged: [list flags with brief context — e.g., "recommendation_divergence: TAC-2 persevere recommendation despite 3/4 signals negative" | "generic_risk_section: Risk Factors section has been boilerplate for 3 consecutive reports" | "kill_proximity_silent: TAC-3 metric within 15% of kill threshold not addressed in recommendation" | "narrative_quantitative_divergence: N signals flagged"]]
- **A/B Test Confound Flags (§8.5):** [none | TAC-[N] vs TAC-[M]: confound detected — [type: environmental_change | resource_shift | timeline_overlap | guardrail_interaction] — comparative metrics marked unreliable until confound resolved]
- **Interface Contract Violations (§8.6, §8.6.9):** [none | list: signal_conflict: {signal_ids, metric} | health_status: data_insufficient for TAC-[N] | health_status: stale_data for TAC-[N] | state_drift: {entity, bootstrap_status, od_status} | monitoring_gap: {watch_item} | coverage_gap: {tactic_id} | other: {description}]
  - *Tier 0:* Validate cognitively — check each contract by reviewing whether signal→health→decision→OD data flows are consistent. Report violations found through manual inspection.
  - *Tier 1:* Validate programmatically — JSON Schema on signal payloads, state machine assertions on OD transitions, automated reconciliation between bootstrap and OD state. Report violations from automated checks.
  - *Tier 2+:* Continuous validation — cross-contract correlation (e.g., signal emission rate vs. health computation freshness), predictive monitoring for contract drift, scale safety checks on concurrent state access. Report violations from monitoring dashboards.

---

## Semantic Coherence (from GOSTA §8.1, §8.2) `[ROBUST]`

**Invariant checks this cycle:**
- **Kill condition evaluability (C1):** [all evaluable | flagged: TAC-[N] — metric [X] has no confirmed data source | flagged: TAC-[N] — execution-only tactic with Kill Condition: N/A (§8.1.1 violation, apply completion-based default)]
- **Allocation arithmetic (C2):** [all balanced | corrected: STR-[N] renormalized after [event]]
- **Temporal ordering (C3):** [all ordered | flagged: TAC-[N] completion [date] exceeds STR-[N] review [date]]
- **Hypothesis coherence (R1):** [all current | flagged: TAC-[N] cites [concept] removed/modified in domain model v[X]]
- **WMBT-objective alignment (R2):** [STR-[N]: alignment [strong | moderate | weak | unclear] — [reasoning]]
- **Guardrail consistency (R3, R4):** [no contradictions | flagged: [guardrail X] vs [guardrail Y] — [detail]]

**Decision-state reconciliation (§8.2.3):**
- Decisions since last review: [N]
- All applied correctly: [yes | no — [details]]
- Unauthorized OD elements found: [none | [list with resolution: confirmed | pending | removed]]

*At Tier 0, report only the checks that surfaced findings. If all checks pass: "Coherence checks: all passed, no flags."*

---

## Grounding Status

- **Stale Signals (temporal):** [N signals older than 2 review cycles without refresh. List SIG-IDs if any. Governor action: refresh, accept, or discard per §14.3.3.]
- **Retrieval Faithfulness Flags (domain):** [N concept distortion flags raised during this review period. List agent ID + concept name if any. See §14.3.2.]
- **Capability Flags (feasibility):** [N actions flagged as infeasible against current capabilities. List action IDs if any. Governor action: reformulate, confirm capability, or defer. See §14.3.6.]
- **Calibration Notes (signal quality):** [Any observed miscalibration between declared signal confidence and actual outcomes. "None observed" if N/A. Recorded in learnings.md Calibrated Norms at strategy review per §14.6.]
- **Reasoning Depth Flags (§14.3.7)** `[ROBUST]`**:** [none | `[SHALLOW]`: recommendation for [entity] cites [concept] without substantive engagement — Governor may request deeper analysis | concepts `considered_not_material`: [concept, reason] (audit trail for deliberate omissions) | coverage gap: [N relevant domain concepts not addressed]]

---

## Computation Trace (from GOSTA §20.1) `[ROBUST]`

For each tactic/strategy/goal health assessment in this report:
- **Signals Included:** [SIG-IDs used as input, with values]
- **Signals Excluded:** [SIG-IDs excluded, with reason: stale / below confidence / triaged]
- **Thresholds Applied:** [kill thresholds, normalization values, decision boundaries used]
- **Recommendation Basis:** [which specific intermediate result drove the recommendation]
- **Classification Justification:** [Why the epistemic classification was assigned — which signals were missing, stale, or conditional]

*At Tier 0, this section IS the AI's reasoning made visible. It is required, not optional — without it, the Governor cannot answer "why did the system recommend kill?" and must ask the AI to reconstruct reasoning post-hoc (risking rationalization). A brief note suffices ("kill recommended because metric X at 1.8% vs 2% threshold for 4 cycles") — the goal is traceability, not exhaustive logging.*

---

## Risk Factors and Negative Signals (from GOSTA §14.3.9) `[ROBUST]`

*This section is REQUIRED and must be non-empty. Generic dismissals ("no significant risks") are flagged as potential sycophancy.*

### Per-Tactic Risk Assessment
| Tactic | Risk Factor | Signal Evidence | Severity | Trajectory |
|---|---|---|---|---|
| TAC-[N] | [specific risk — what is going wrong or could go wrong] | SIG-[N] | [low / medium / high] | [new / stable / worsening / improving] |

### Kill Proximity Alerts
| Tactic | Metric | Current | Kill Threshold | Distance | Cycles at This Distance |
|---|---|---|---|---|---|
| TAC-[N] | [metric] | [value] | [threshold] | [N%] | [N cycles — trend: approaching / stable / receding] |

*Proximity threshold: [N%] (configurable in OD Failure Resilience Thresholds section, default: 20%)*
*Any metric listed here with `approaching` trajectory for 2+ cycles must be explicitly addressed in the Recommendation section.*

### Negative Signal Summary
- **Signals trending negative:** [list SIG-IDs with direction — even if overall recommendation is persevere]
- **Divergence-tagged signals:** [N signals flagged `[DIVERGENCE]` for narrative-quantitative mismatch — qualitative framing discounted for these signals]
- **Information gaps affecting this assessment:** [list — cross-reference §14.3.8 classification]

### Sycophancy Self-Check
- **Risk section completeness:** [substantive | generic_flag — if orchestrator cannot identify any risk factors, it must state: "No risk factors identified. Governor should verify: is this genuinely risk-free, or am I failing to surface risks?"]
- **Recommendation-signal alignment:** [aligned | divergence_detected — see per-tactic/strategy Signal-Recommendation Alignment fields above]

---

## Signals Referenced
[List SIG-numbers used in this report]
