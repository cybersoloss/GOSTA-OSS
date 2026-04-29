# Signal Log — [Date Range]

Append-only. Do not edit existing entries. *Valid signal types and severity values: see Framework Appendix B.3.*
*When a health assessment identifies an `information_gap` finding (Cowork Protocol §7.1), the missing data specification becomes a signal collection target. Emit a `knowledge_flag` signal when the gap is resolved.*

---

## Signal Triage Summary

| Domain | Raw Sources | Passed Triage | Ratio | Notes |
|---|---|---|---|---|
| [domain] | [N] | [N] | [%] | [Why sources were filtered: low tier, stale, irrelevant, duplicate] |

**Triage criteria applied:** relevance to active tactic, source tier minimum, temporal currency, deduplication.

---

## Action Signal Stubs (signal-first pattern — Protocol §6.3)

Write a stub BEFORE starting each action. Update to completed/failed AFTER.

| SIG-ID | ACT-ID | Status | Deliverable Ref | Timestamp | Notes |
|---|---|---|---|---|---|
| SIG-[N] | [ACT-ID] | in_progress | — | [timestamp] | |
| SIG-[N] | [ACT-ID] | completed | [path/to/deliverable] | [timestamp] | |

This table is the `[MINIMAL]` compressed format. Always acceptable. Use the full format below when context permits.

---

## Signals (full format)

### SIG-[sequential-number] | [date]
- **Source:** [execution | governor | external | computation]
- **Type:** [action_completion | metric_value | guardrail_violation | guardrail_interpretation | guardrail_recovery | kill_condition | market_event | governor_decision | agent_degradation | signal_pipeline_degradation | signal_pipeline_failure | environmental | milestone | blocker | knowledge_flag | narrative_assessment | cost_exceeded | cost_data_missing | validation_failure (§8.7 — sub-types: V1-retrieval-contract / V2-build-shape / V3-decision-spine / V4-capture-coverage / V5-runtime-import / V6-declared-artifact (Layer A existence / Layer B population) / V7-vertical-fit / V8-subagent-dispatch-smoke / V9-inheritance-residue; severity per invariant failure mode: BLOCK = high, WARN = medium, LOG = low) | absence (§7.4 `[ROBUST]`) | stakeholder_interaction (§7.4 `[ROBUST]`) | claim_propagation (§14.3.10 `[ROBUST]`) | tournament_selection (§4.6 `[ESSENTIAL]`)]
- **Attribution:** [Goal] > [Objective] > [Strategy] > [Tactic] > [Action]
- **Data:** [The actual signal — for simple signals: numeric value, status, or observation text]
- **Confidence:** [complete | partial | estimated]
- **Source Tier:** [1-6] with optional modifier [-neutral | -belligerent | -pro-X | -mediator]
- **Temporal Validity:** [hours | days | weeks | structural]
- **Notes:** [Optional context]

#### Signal Integrity Check (from GOSTA §14.3.9) — applied at signal recording

When a signal contains both quantitative data (metric values, counts, percentages) and qualitative assessment (narrative text in Data or Notes fields):
- **Direction check:** Does the qualitative assessment match the quantitative direction?
  - Quantitative declining + qualitative positive = `narrative_quantitative_divergence` flag
  - Quantitative improving + qualitative negative = no flag (conservative framing is not sycophantic)
  - Quantitative stable + qualitative positive = review — may be legitimate or may be baseline drift
- **If flagged:** Add `[DIVERGENCE]` tag to signal Notes field. Health computation treats the qualitative assessment as unreliable — use quantitative data only for this signal.
  - Format example: `Notes: [DIVERGENCE] Narrative claims "strong engagement" but click-through rate declined 15% week-over-week. Using quantitative data only.`

#### Compound Signal Format (when a single source contains multiple distinct claims)

### SIG-[N] | [date] (compound)
- **Source:** [as above]
- **Type:** [as above]
- **Attribution:** [as above]
- **Source Tier:** [tier for the source overall]
- **Claims:**
  1. [claim text] | Confidence: [complete/partial/estimated] | Validity: [window]
  2. [claim text] | Confidence: [complete/partial/estimated] | Validity: [window]
  3. [claim text] | Confidence: [complete/partial/estimated] | Validity: [window]
- **Notes:** [Optional context]
