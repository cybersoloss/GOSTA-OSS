# Session Status — [scope-name]
**Updated:** [timestamp — overwrite at every major checkpoint]

## Scope State
- **Cycle:** [N] | **Phase/Step:** [current phase or step name]
- **Graduation Stage:** [1-5]
- **Scope Health:** [healthy | degraded: [reason] | critical: [reason]]
- **Mode:** [cowork | code] | **Independence:** [1 | 2 | 3]

## Active Tactics
| ID | Name | Health | Status | Last Signal | Next Review |
|---|---|---|---|---|---|
| TAC-1 | [name] | [score or healthy/degraded/critical] | [active | bootstrap | paused | killing] | [date] | [date] |

*At Tier 0: health is a qualitative assessment (healthy/degraded/critical). At Tier 1+: numeric health score from computation.*

## Pending Governor Actions
- [DEC-N: description — awaiting approval | "None — no actions pending"]

*Items appear here when: decisions require Governor approval, phase gates await advance, deliberation synthesis awaits review, guardrail deviations need acknowledgment.*

## Signal Pipeline
- **Signals this cycle:** [N]
- **Freshness:** [all current | tactic_gap: TAC-N last signal [date] | pipeline_degradation: M of T stale | pipeline_failure: no signals for N cycles]
- **Pipeline status:** [normal | degraded | failure]

## Deliberation Status
- **Current:** [none | DELIB-N in progress — Round M of max K, [N] agents responding]
- **Last completed:** [DELIB-N: [outcome] on [date] | none]

## Next Reviews Due
- **Action cycle:** [date]
- **Tactic review:** [date] — [TAC-N, TAC-M]
- **Strategy review:** [date] — [STR-N]
- **Goal review:** [date]

## Resource Utilization
- **Governor review load:** [N decisions this cycle / capacity N/week] — [sustainable | approaching | exceeded]
- **Context utilization:** [~N% | shed: [list] | no shedding required]

---
*This file is overwrite-only. Updated at: phase gates, decision points, health computations, deliberation rounds, signal batches, and session start/end. For historical records, see session-logs/.*
