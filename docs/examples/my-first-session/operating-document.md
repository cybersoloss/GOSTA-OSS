# Operating Document: my-first-session

**Version:** 1 | **Date:** 2026-03-25 (refreshed 2026-05-03 to current framework state) | **Governor:** Murat
**Scope Type:** finite | **Graduation Stage:** 1
**Framework Version:** v6.1 | **Cowork Protocol:** v3.34 | **Mode:** cowork | **Independence:** 2 | **Deliberation:** disabled

## Analytical Frame Contract (AFC)

N/A — operational scope (feature prioritization with no analytical question to answer). Group 2A of the bootstrapper does not fire for non-analytical scopes. AFC field is populated by the OD only when the deliverable answers a question rather than produces a prioritization artifact. See `cowork/startup.md` Group 2A for the AFC derivation procedure used in analytical scopes.

## Goal

Determine which three of five candidate features should be built next quarter based on explicit evaluation of user value and engineering cost, with all guardrails satisfied.

### Guardrails

- **G-1:** 12-week budget constraint | Severity: hard | Evaluation: mechanical | Threshold: Total estimated weeks across top 3 features ≤ 12 weeks
  - Recovery (soft only): N/A

- **G-2:** Single developer — no parallelization in effort estimates | Severity: hard | Evaluation: interpretive | Threshold: All effort estimates assume sequential execution of selected features, not parallel
  - Recovery (soft only): N/A

- **G-3:** No breaking changes to public API | Severity: hard | Evaluation: mechanical | Threshold: 0 breaking changes to public API surface
  - Recovery (soft only): N/A

- **G-4:** Governor sign-off required before any feature is committed to roadmap | Severity: hard | Evaluation: interpretive | Threshold: DEC-001 signed by Murat before features move to implementation
  - Recovery (soft only): N/A

- **G-5:** All scoring must cite domain model concepts (anti-sycophancy) | Severity: hard | Evaluation: interpretive | Threshold: Every feature score across both domain models must trace to at least one explicit concept from user-value.md or engineering-cost.md
  - Recovery (soft only): N/A

## Objectives

### OBJ-1: Feature Prioritization Decision

- **Analytical Question:** Which three of five candidate features maximize combined user value and engineering feasibility within a 12-week, single-developer constraint?
- **Acceptance Criteria:** All five features assessed against six user-value concepts and six engineering-cost concepts, with per-feature totals computed; cross-domain trade-off tensions identified; Governor hypothesis HL-4 (dark mode distraction hypothesis) tested explicitly; top three features and deferred rationale documented
- **Deliverable:** feature-ranking.md with scored matrix, tensional analysis, and ranked recommendation
- **Quality Standard:** Every verdict cites specific domain model concepts; every trade-off mentions where user-value and engineering-cost compete; deferred features have explicit rationale referencing domain models, not vague dismissals; HL-4 result clearly stated as confirmed/refuted
- **Priority:** critical

## Strategies

### STR-1: Multi-domain sequential assessment

- **Rationale:** Evaluating features against user value first (without cost constraint), then engineering cost, then synthesizing cross-domain tensions, prevents the analysis from being dominated by whichever domain is discussed first
- **What Must Be True (WMBT):** Both domain models are loaded and understood before scoring begins; scoring templates cite concepts explicitly; synthesis phase identifies genuine tensions, not just differences
- **Not Doing:** Not performing a single-domain assessment; not relying on intuition without domain model grounding
- **Kill Signal:** If scoring cannot cite domain model concepts or if top-ranked feature violates guardrails G-1 through G-5
- **Relationship to sibling strategies:** N/A (single strategy)
- **Authorized By:** GOV-session-1

## Tactics

### TAC-1: Score all five features against user-value domain model

**[CORE — required for any GOSTA implementation]**

- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1
- **Hypothesis:** If we apply the six user-value concepts (Activation Distance, Retention Signal, Perceived Complexity, WTP Indicator, Segment Reach, Habit Formation Potential) to each feature with cite-then-apply structure, we will produce defensible per-feature user-value totals
- **Kill Condition:** If any feature cannot be scored (insufficient user data to assess two or more concepts), kill the tactic and escalate to Governor for decision on how to proceed (external user research, defer scoring, substitute domain model)
- **Success Metrics:** All five features scored 1-10 on each of six concepts; per-feature user-value total computed (sum of six concept scores); onboarding wizard scores ~48/60 (8.0 avg), dark mode scores ~18/60 (3.0 avg), confirming hypothesis HL-4
- **Guardrails (inherited):** G-5 (all scores cite concepts)
- **Guardrails (own):** None
- **Timeline:** Start 2026-03-25 — End 2026-03-26
- **Bootstrap Cycles:** 0 (no cycling, assessment completes once)
- **Seed Actions:** Load user-value.md; review all feature descriptions; identify which features have explicit user research vs. estimates only
- **Owner:** AI
- **Approach:** For each feature, for each concept: state the concept name and definition from domain model; explain how it applies to this specific feature; assign a score 1-10 with justification; repeat for all six concepts; sum the six scores to produce feature total
- **Dependencies:** execution (AI can do this)
- **Domain Model Dependencies:** user-value (all six concepts: Activation Distance, Retention Signal, Perceived Complexity, WTP Indicator, Segment Reach, Habit Formation Potential)
- **Review Date:** 2026-03-26

### TAC-2: Score all five features against engineering-cost domain model

**[CORE]**

- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1
- **Hypothesis:** If we apply the six engineering-cost concepts (Effort Estimate Confidence, Dependency Chain Length, Reversibility, Maintenance Burden, Technical Debt Multiplier, Integration Surface Area) to each feature, we will produce effort estimates and identify which features create long-term cost (debt multiplier) vs. short-term cost (effort)
- **Kill Condition:** If any feature has Dependency Chain Length > 3 or Technical Debt Multiplier > 1.5 with no clear mitigation path, escalate to Governor (may defer feature or redesign approach)
- **Success Metrics:** All five features scored 1-10 on each of six concepts; per-feature engineering-cost total computed; effort estimates in weeks provided; onboarding wizard 3 weeks, dark mode 1.5 weeks, audit logging 9 weeks, confirming that audit logging deferred
- **Guardrails (inherited):** G-5 (all scores cite concepts)
- **Guardrails (own):** None
- **Timeline:** Start 2026-03-26 — End 2026-03-27
- **Bootstrap Cycles:** 0
- **Seed Actions:** Load engineering-cost.md; review technical architecture to assess integration surface areas; gather historical effort estimates if available
- **Owner:** AI
- **Approach:** For each feature, for each concept: cite the concept definition; explain domain-specific implications for this feature; assess current state (e.g., "Effort Estimate Confidence: high — we've built similar onboarding flows"); assign score 1-10; include effort estimate in weeks alongside score
- **Dependencies:** execution
- **Domain Model Dependencies:** engineering-cost (all six concepts: Effort Estimate Confidence, Dependency Chain Length, Reversibility, Maintenance Burden, Technical Debt Multiplier, Integration Surface Area)
- **Review Date:** 2026-03-27

### TAC-3: Synthesize cross-domain assessment and produce feature ranking

**[CORE]**

- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1
- **Hypothesis:** If we compare per-feature user-value totals against per-feature engineering-cost totals and effort estimates, we can identify which features offer best value-per-week spent, and where user-value and engineering-cost compete
- **Kill Condition:** If no feature combination satisfies guardrail G-1 (≤12 weeks), or if Governor rejects the ranking, escalate for decision on how to modify scope
- **Success Metrics:** Ranked list of top three features with combined effort ≤12 weeks; per-feature trade-offs documented (e.g., "onboarding: highest user-value, moderate cost; dark mode: lowest user-value, lowest cost"); deferred features with rationale; HL-4 result (dark mode hypothesis) confirmed or refuted
- **Guardrails (inherited):** G-1 (12-week budget), G-3 (no breaking changes), G-4 (Governor sign-off), G-5 (domain model grounding)
- **Guardrails (own):** None
- **Timeline:** Start 2026-03-27 — End 2026-03-28
- **Bootstrap Cycles:** 0
- **Seed Actions:** Load TAC-1 and TAC-2 scoring results; identify three-feature combinations that fit 12-week budget; compute value-per-week for each feature
- **Owner:** AI
- **Approach:** For each possible three-feature combination that fits 12-week budget: compute combined user-value and effort; identify cross-domain tensions (e.g., "feature X high user-value, high effort cost"); select top combination based on value-per-week and feature portfolio balance; document why deferred features were not selected (e.g., "audit logging 9 weeks exceeds budget in any three-feature combination"); explicitly test HL-4 by comparing dark mode's user-value score to other features
- **Dependencies:** execution
- **Domain Model Dependencies:** user-value (for weighting), engineering-cost (for effort estimates)
- **Review Date:** 2026-03-28

## Actions (Current Cycle)

[For finite scopes: this section references Phase 1 actions — assessment phase]

### ACT-1: Load domain models and feature descriptions

- **Assignee:** AI
- **Deliverable:** Session ready with both domain models understood and all five feature descriptions reviewed
- **Deadline:** 2026-03-25
- **Dependency Type:** execution

### ACT-2: Execute TAC-1 (score user-value)

- **Assignee:** AI
- **Deliverable:** scoring-user-value.md with all five features scored against all six user-value concepts
- **Deadline:** 2026-03-26
- **Dependency Type:** execution

### ACT-3: Execute TAC-2 (score engineering-cost)

- **Assignee:** AI
- **Deliverable:** scoring-engineering-cost.md with all five features scored against all six engineering-cost concepts and effort estimates
- **Deadline:** 2026-03-27
- **Dependency Type:** execution

### ACT-4: Execute TAC-3 (synthesize and rank)

- **Assignee:** AI
- **Deliverable:** feature-ranking.md with top three features ranked, trade-off analysis, and deferred rationale
- **Deadline:** 2026-03-28
- **Dependency Type:** execution

## Review Cadences

**Finite scope:** Review at each phase gate

---

## Phases (finite scopes only)

### Phase 1: Assessment

- **Objective:** Score all five features against both domain models, identify tensions, and produce ranked recommendation
- **Entry Criteria:** Domain models loaded, operating document approved by Governor, TAC-1, TAC-2, TAC-3 defined
- **Exit Criteria:** All five features scored in both domains; feature-ranking.md produced with top three and deferred rationale
- **Actions:** ACT-1, ACT-2, ACT-3, ACT-4

### Phase 2: Governor Decision

- **Objective:** Present recommendation to Governor, resolve any tensions, obtain sign-off
- **Entry Criteria:** Phase 1 complete, feature-ranking.md ready
- **Exit Criteria:** Governor approves or rejects recommendation, documented in DEC-001
- **Actions:** Present ranking to Governor; answer clarifying questions; apply Governor feedback if any; obtain sign-off

---

## Autonomy Safeguards (from GOSTA §6.7)

### Magnitude Thresholds

- **Resource cost:** not set
- **Timeline impact:** not set
- **Stakeholder visibility:** not set
- **External commitment:** not set

### Autonomy Conditions

None.

### Failure Resilience Thresholds

Not applicable (finite scope with no ongoing metrics).

### Governor Attention Capacity

- **Reviews per Week:** 1 (single ranking review at end of assessment)
- **Role:** part_time
- **Sustainability Flag:** Sustainable

### Execution Cost Tracking

No metered resources.

### Environmental Watch List

Not applicable (finite scope, no external conditions to monitor).

## Reference Materials

None.

## Domain Models Referenced

- user-value.md — Evaluates six user-value concepts (Activation Distance, Retention Signal, Perceived Complexity, WTP Indicator, Segment Reach, Habit Formation Potential)
- engineering-cost.md — Evaluates six engineering-cost concepts (Effort Estimate Confidence, Dependency Chain Length, Reversibility, Maintenance Burden, Technical Debt Multiplier, Integration Surface Area)

## Multi-Domain Assessment

- **Independence Level:** 2 (Sequential Isolation) — domains assessed independently, then synthesized
- **Deliberation Mode:** disabled

## Per-Deliverable Caps

| Artifact | Cap | Notes |
|---|---|---|
| `signals/scoring-user-value.md` | 8 KB | 5 features × 6 concepts with cite-then-apply structure |
| `signals/scoring-engineering-cost.md` | 8 KB | Same scope as user-value scoring |
| `health-reports/HR-001.md` | 6 KB | Single-tactic scope, simple aggregation |
| `decisions/DEC-001.md` | 4 KB | Single decision with rationale |
| `deliverables/feature-ranking.md` | 6 KB | Ranked list of 3 + deferred rationale |

Formula caps (`base=N kb + M kb × VAR`) are recommended for content-density-variable artifacts in deliberation-enabled sessions (see `cowork/templates/operating-document.md` § Formula-Based Caps). For this simple non-deliberation session, fixed caps are appropriate. The M3 hook (`cowork/hooks/check-cap-overage.sh`) fires WARN when an artifact exceeds 1.0× its cap.

## Validation Manifest (from GOSTA §8.7)

| Gate | Boundary | Mechanical Test | Failure Mode |
|---|---|---|---|
| V3 — Cross-doc consistency | Phase 1 entry | Every guardrail referenced in OD exists in scope; every deliverable maps to a strategy | BLOCK |
| V6 — Declared artifact existence + population | Every phase exit + closeout | Layer A: `test -s` on each declared artifact; Layer B: `grep -c "\[POPULATE:"` returns 0 + per-section word floor ≥20 | BLOCK |
| V7 — Inheritance vertical fit | Phase 1 entry (declared in scope) | N/A — no inheritance in this session | SKIP |
| V8 — Subagent dispatch capability | Bootstrap entry (declared in scope) | N/A — no subagent dispatch declared (deliberation disabled) | SKIP |
| V9 — Inheritance framework-residue audit | Phase 1 entry (declared in scope) | N/A — no inheritance | SKIP |

V1, V2, V4, V5 not applicable to this session (no retrieval contracts, no pool builds, no continuous-capture mode, no orchestrator runtime imports beyond AI model itself).

## Hooks (Optional — Claude Code Mechanizable-Discipline Layer)

If running this session in Claude Code with `~/.claude/settings.local.json` (or per-project `.claude/settings.local.json`) configured per `cowork/templates/hooks-settings.json`:

- **M1 — `check-signal-first.sh`** fires PreToolUse on Task — verifies signal stub exists before agent dispatch
- **M3 — `check-cap-overage.sh`** fires PostToolUse on Write|Edit — checks per-deliverable cap overage
- **M4 — `check-afc-section.sh`** fires PostToolUse on Write|Edit on deliverable / synthesis-report / phase-gate files — checks AFC section presence (silent here since AFC is N/A)
- **`log-dispatch.sh`** fires PreToolUse + PostToolUse on Task + SubagentStop — logs all dispatches
- **`audit-closeout.sh`** fires SessionEnd — runs closeout audit per protocol §5.5

Hooks are advisory at write-time and structural at closeout. M5 hook-availability check at bootstrap warns if hooks are not configured.

## U1 Independent Reviewer (Optional)

For sessions with deliberation or analytical scopes, a U1 independent-reviewer subagent can be dispatched at phase-gate decision support and at closeout per `cowork/templates/independent-reviewer-prompt.md`. This simple session does not require U1 since it has no deliberation or analytical scope, but the pattern is available if you want an audit of file-grounding integrity, sycophancy patterns, or signal-recommendation alignment before closeout.

