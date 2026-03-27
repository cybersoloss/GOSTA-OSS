# Learnings — [Session Name]

## Validated Patterns
- [What worked and why — with signal evidence]

## Anti-Patterns Discovered
- [What failed and why — with signal evidence]

## Calibrated Norms
- [Baseline expectations adjusted by experience — e.g., "feature scoring
  against Sales domain model consistently over-weights Risk Reversal
  relative to actual purchase behavior"]

### Confidence Calibration (populated at strategy review or after 3+ tactic review cycles per §14.6)
| Confidence Level | Signals Declared | Signals Accurate | Accuracy Rate | Notes |
|---|---|---|---|---|
| complete | [N] | [N] | [%] | [e.g., "2 of 8 'complete' signals on engagement metrics were off by >30% — source API returns cached data, not real-time"] |
| partial | [N] | [N] | [%] | |
| estimated | [N] | [N] | [%] | |

Action items from calibration review:
- [e.g., "Downgrade engagement metric confidence to 'partial' until API caching issue resolved"]
- [e.g., "Agent systematically overestimates conversion rate confidence — add a provenance note requiring A/B sample size disclosure"]

### Summary Fidelity Audit (populated at strategy review per §18.2.6 Meta-Memory)
Governor picks 1-2 recent tactic episode summaries and compares against the full health reports.

| Summary (session/tactic) | Information Present in Full Report | Present in Summary? | Impact if Missing |
|---|---|---|---|
| [e.g., session-005 / TAC-2] | [e.g., "engagement quality declining despite volume increase"] | [yes / no] | [e.g., "leading indicator for next kill/pivot decision — omission could delay kill by 1 cycle"] |

Systematic omission patterns found:
- [e.g., "Summaries never mention human creative input rate for marketing tactics — add as required summary field"]
- [e.g., "Blocker status consistently absent from tactic summaries — blockers only appear in full reports"]

## External Constraint Learnings (Vector 3 — from GOSTA §7.8)
*Populated when a tactic or strategy is killed with `kill_reason: external_constraint`. These are force majeure events — factors outside the system's control that terminated execution. Learning is about environmental awareness, not execution improvement.*

| Kill Decision | External Constraint | Impact | Environmental Watch List Update |
|---|---|---|---|
| [DEC-N] | [description of external event] | [what was lost — progress, resources, commitments] | [new ENV-N entry to monitor, or existing ENV-N threshold adjusted, or "no actionable monitoring possible"] |

## Cross-Domain Insights
- [Interactions between domain models not predicted by their stacking notes]

## Tournament Execution Patterns (when tournament mode was active)

Populated at scope conclusion or after 3+ tournament cycles. Governor reviews entries before they become structural memory.

### Behavior Space Effectiveness
| Tactic | Dimension 1 | Dimension 2 | Cells Covered | Winning Cell | Score Delta (best vs worst) | Structural Insight |
|---|---|---|---|---|---|---|
| [TAC-N] | [dim name: values] | [dim name: values] | [N of M] | [cell assignment] | [N pts] | [design principle discovered — e.g., "evidence-first consistently outperforms problem-first for technical audiences"] |

### Dimension Source Effectiveness
| Context Source | Dimensions Proposed | Dimensions Selected | Produced Score Swings? | Notes |
|---|---|---|---|---|
| Domain model tensions | [N] | [N] | [yes/no — magnitude] | [e.g., "Cross-model divergence between compliance and usability models reliably produces high-impact dimensions"] |
| Guardrail pair analysis | [N] | [N] | [yes/no — magnitude] | |
| Reference pool clustering | [N] | [N] | [yes/no — magnitude] | |
| Deliverable trade-off analysis | [N] | [N] | [yes/no — magnitude] | |

### Tournament Calibration Summary
- **Optimal run count observed:** [N — did additional runs beyond N add selection value?]
- **Structural vs content dimensions:** [which dimension types produced meaningful differentiation?]
- **Generic fallback usage:** [were generic dimensions used? Did they produce sufficient differentiation?]
- **Anti-patterns discovered:** [cell combinations that consistently produced low scores — e.g., "vision-led + quantitative evidence is structurally incoherent"]

## Deliberation Patterns (when deliberation mode was active)

Populated by the Coordinator at scope conclusion or after 3+ deliberation cycles — whichever comes first. Governor reviews and approves entries before they become structural memory.

### Agent Behavioral Patterns
- [Per-agent tendencies observed across deliberation cycles. Examples:
  "Agent NIS2-1 consistently rates compliance risk higher than business agents find actionable — calibrate by weighting NIS2-1 confidence at 0.8x for prioritization decisions."
  "Agent VC-1 concedes too quickly in Round 2 when challenged by regulatory agents — position papers show strong reasoning that gets abandoned without new evidence."]

### Recurring Disagreement Patterns
- [Disagreements that recur across cycles with the same structure. Examples:
  "VC-1 vs VD-1 on feature complexity: recurred in DELIB-001, DELIB-003, DELIB-005. Root cause: Value Creation model weights market differentiation; Value Delivery model weights implementation cost. Governor resolved the same way each time (favor VD-1 when delivery timeline < 3 months). Consider encoding as a guardrail."
  "Circular disagreement between MKT-1 and SL-1 on channel priority: stalled in 2 of 3 deliberations. Domain models may have overlapping scope — consider merging or adding boundary clause."]

### Deliberation Effectiveness
- [What worked and didn't work about the deliberation configuration. Examples:
  "2-round max was sufficient for 3-agent finite scope — Round 2 resolved all hard disagreements."
  "single_session_sequential produced noticeable role bleed in DELIB-002 — Coordinator synthesis echoed the last domain agent's framing. Governor caught it via spot-check."
  "Cost per deliberation averaged ~X tokens. Round 2 accounted for 60% of cost but only shifted 1 of 4 recommendations."]

### Retrieval Faithfulness Observations
- [Concept distortion patterns observed during deliberation. Examples:
  "VC-1 consistently narrowed 'Risk Reversal' to money-back guarantees — the full concept includes free trials, proof-of-concept, and performance guarantees. Coordinator flagged in DELIB-002 and DELIB-004. Consider adding application examples to the domain model concept definition."
  "MKT-1 broadened 'Probable Purchaser' criteria in DELIB-003, applying it to an audience meeting 1 of 4 criteria. Governor caught via position paper review. Domain model definition was ambiguous — tightened definition added to model v1.2."]

### Sycophancy Indicators (from GOSTA §14.3.9)

#### Dissent Frequency Tracking
| Deliberation Cycle | Round 1 Unanimity? | Hard Disagreements | Convergence Probe Triggered? | Probe Result |
|---|---|---|---|---|
| DELIB-[NNN] | [yes/no] | [N] | [yes/no/N/A] | [substantive_dissent / weak_dissent / genuine_alignment / N/A] |

**Running statistics:**
- **Round 1 unanimity rate:** [N of M deliberations] — if >60% across 3+ cycles, flag `low_dissent_frequency`
- **Mean hard disagreements per cycle:** [N] — if <1.0 across 3+ cycles, deliberation may not be adding value
- **Convergence probe hit rate:** [N probes triggered / N unanimity flags] — tracks whether probes surface genuine disagreement

**Interpretation guidance:**
- High unanimity + high dissent frequency = healthy deliberation with convergent domain models
- High unanimity + low dissent frequency = possible sycophancy or domain model redundancy
- Low unanimity = healthy deliberation

### Threshold Calibration
- [Adjustments to termination thresholds based on experience. Examples:
  "Convergence threshold of 3 points was too loose for our 3-agent setup — agents converged on recommendation but 3-point confidence spread masked a substantive concern from VD-1."
  "Stall definition of 1 round worked for thin models (<5 concepts) — no false terminations observed."]

## Domain Model Feedback (when deliberation mode was active)

Populated from deliberation outcomes per Deliberation Protocol §12.4. Governor reviews and approves each entry before the domain model is updated.

| Domain Model | Proposed Change | Evidence | Type | Governor Decision |
|---|---|---|---|---|
| [model name] | [add concept / calibrate weight / add boundary condition / prune unused concept] | [DELIB cycle IDs, Governor override pattern, concession pattern] | [calibration / gap / prune] | [apply / defer / reject] |

## Failure Resilience Observations (from GOSTA §7.13)

### Signal Pipeline Health
- [Signal freshness issues, pipeline degradation events, recovery timing. Examples:
  "Session 12: TAC-2 signals stale for 2 weeks — Governor confirmed metrics source was migrated. Updated data source reference."
  "Session 18: pipeline degradation detected (3 of 5 tactics stale). Root cause: API key expired. Resolved session 19."]

### Recovery Patterns
- [Components that failed and recovered, relapse patterns, stability window outcomes. Examples:
  "Data grounding source X failed and recovered 3 times in sessions 8-15. Declared chronically unstable in session 16. Switched to alternative source."
  "Agent recovery after context overflow in session 10 — verified stable after 1 cycle."]

### Memory/Context Issues
- [Bootstrap corruption repairs, learnings contradictions found, context shedding incidents. Examples:
  "Session 7: bootstrap had stale 'What Is Pending' — missed session 6 due to crash. Reconstructed from session-log-006."
  "Session 14: learnings contained contradictory entries about Strategy A. Governor resolved in favor of session 12 assessment."]

### Governor Decision Consistency
- [Frequency of semantic inconsistency flags, which checks most relevant, override patterns. Examples:
  "Kill condition consistency check flagged 3 times across sessions 10-20. Governor overrode twice (had information not in signals), corrected once."
  "Budget coherence check blocked once — Governor had approved tactics totaling 120% of budget. Resolved by deferring TAC-5."]

### Cadence Calibration (from GOSTA §6.4.4)
- [Review cycle effectiveness observations — were cadences too fast, too slow, or well-matched to domain velocity? Examples:
  "Action cycle weekly — signals arrived faster than review cadence. Signal-to-review ratio hit 3.2 by session 8. Governor shortened to twice-weekly."
  "Tactic review every 4 weeks caught TAC-3's inflection point 1 cycle late. Recommend 2-week tactic reviews for high-velocity tactics."
  "Strategy review monthly was appropriate — WMBT conditions moved slowly. No cadence change needed."
  "Event-triggered reviews fired 3 times in 2 weeks during market disruption. Ratio >1.0 sustained — Governor temporarily shortened strategy review cadence."]

### Coherence Validation Patterns (from GOSTA §8.1)
- [Recurring semantic coherence issues and their resolution. Examples:
  "C1 (kill condition evaluability) flagged 3 times across sessions 10-20 — all were metric source changes that invalidated existing kill conditions. Recommend adding metric availability check to tactic creation checklist."
  "R2 (WMBT-objective alignment) consistently flags for Strategy B — WMBT references 'organic growth' but objective metric is total revenue including paid. Governor confirmed alignment both times — consider tightening WMBT wording."
  "Reconciliation found 2 unauthorized state changes in session 14 — traced to cross-session gap (session 13 crashed). Resolved by Governor retroactive approval."
  "R3 (guardrail consistency) never flags — guardrail set is small and non-overlapping. Check may become relevant if guardrail count exceeds 5."]

### Epistemic Classification Patterns
- **Information gap frequency:** [How often did recommendations carry `information_gap`? If >50%, signal pipeline may be under-instrumented.]
- **Conditional assumptions resolved:** [Which conditional findings were later confirmed or disconfirmed? Track prediction accuracy.]
- **Classification-driven Governor actions:** [Did the Governor collect data for information gaps? Did conditional findings get monitored?]

## Technical Decisions
- [Architecture, tooling, or process choices made and their rationale]
