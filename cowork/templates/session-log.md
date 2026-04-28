# Session [NNN] — [Date]
**Type:** [bootstrap | execution | review | decision | deliberation | ad-hoc]
**Mode:** [cowork | code]
**Duration:** [approximate]

## Summary
[3-5 sentences: what was the purpose, what was accomplished]

## Domain Models Consulted
- [Which models and which specific concepts were used]

## Signals Emitted
- [Summary of signals produced this session]

## Decisions Made
- [Summary of Governor decisions]

## Deliberation Activity (if type = deliberation or deliberation occurred during session)
- **Cycle:** DELIB-[NNN]
- **Agents Dispatched:** [N] | **Completed Normally:** [N] | **Fallback Used:** [N] | **Excluded:** [N]
- **Fallback Details:** [if any — Agent ID, fallback type (reduced_model / proxy), coverage impact. "None" if all agents completed normally.]
- **Rounds Executed:** [N of max]
- **Outcome:** [full_consensus | strong_consensus | weak_consensus | split]
- **Artifacts Produced:** [list — position papers, response papers, interim assessments, synthesis report, verification checklist]
- **Domain Model Feedback:** [any calibration/gap/prune signals discovered — "None" if none]
- **Governor Action:** [accept | modify | override | remand]

## System Resilience (from GOSTA §7.13)
- **Integrity Checks:** [all pass | failures: [list]]
- **Signal Freshness:** [all current | stale: [tactics] | pipeline degradation | pipeline failure]
- **Recovery Status:** [no active recoveries | recovering: [component] — cycle [N/M] | chronic: [component]]
- **Context Utilization:** [~N% | shed: [list] | no shedding required]
- **Governor Decision Validations:** [none | flagged: [checks] — [overridden/corrected]]
- **Sycophancy Flags (§14.3.9):** [none | list: generic_risk_section / recommendation_divergence / kill_proximity_silent / round1_unanimity / low_dissent_frequency / narrative_quantitative_divergence — with brief context]

## Semantic Coherence (from GOSTA §8.1, §8.2)
- **Authoring-time checks:** [all pass | flags: C1 [details] | C2 [auto-corrected: details] | C3 [flag: details] | C4 [flag: details]]
- **Review-time checks (if strategy review session):** [R1-R4 results | not applicable — not a review session]
- **Reconciliation (if strategy review session):** [forward: N decisions checked, M applied | reverse: N elements checked, M unauthorized | parameter drift: [none | details]]

## Pre-Flight Validation Gate Results (from GOSTA §8.7)

V1-V7 invariant results at this session's phase boundaries. Compact form: list any BLOCK or WARN outcomes with (a) which invariant fired, (b) what the test observed, (c) how it was resolved.

If no validation gates fired this session, state: "All §8.7 invariants PASS at the boundaries crossed this session."

## OD Mutations (post-bootstrap edits) — omit section if no post-bootstrap OD edits occurred
| Timestamp | Field Changed | Old → New | Cascade Checked | Cascade Skipped | Downstream Changes |
|---|---|---|---|---|---|
| [time] | [field] | [old] → [new] | [section IDs reviewed] | [section IDs not reviewed + rationale] | [changes applied] |

## Guardrail Attestation (from Cowork Protocol §12.13)
| Guardrail | Sections Checked | Method | Supporting Quote | Result |
|---|---|---|---|---|
| [G-N: name] | [deliverable sections] | [mechanical / interpretive] | "[verbatim quote supporting compliance conclusion]" | [pass / fail — action taken] |

**AFC Frame Integrity (if AFC enabled):**
- Output verb match: [pass / FRAME-DRIFT — details]
- Stance reader match: [pass / FRAME-DRIFT — details]
- Failure mode alignment: [pass / FRAME-DRIFT — details]

## Deliverables Produced
- [Files created or modified]

### Revision Trail — omit subsection if deliverable accepted without revision
| Rev | Trigger | Sections Changed | Frame Correction | Snapshot |
|---|---|---|---|---|
| [0→1] | [Governor feedback / §12.12 FRAME-DRIFT / G-N violation] | [sections] | [what changed in analytical framing] | [deliverables/name-rev-0.md] |

## Open Items
- [What wasn't finished, what needs follow-up]

## Framework Feedback
- [Any GOSTA shortfalls or observations — reference gosta-framework-feedback.md]
