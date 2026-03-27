# Governor Decisions

Append-only. Do not edit existing entries. *Valid decision types, kill reasons, and all other enums: see Framework Appendix B.*

---

### DEC-[sequential-number] | [date]
- **Session:** [session number]
- **Type:** [kill | pivot | pivot_override | persevere | approve | reject | promote | phase_advance | iterate | restructure | accept_deliverable | scope_change | rebalance | pause | resume | revise_objective | conclude_scope | cross_objective_tradeoff | informed_override | guardrail_reclassify | wmbt_refinement | portfolio_rebalance | decision_reversal | resolve_conflict | tournament_selection]
- **Target:** [Which tactic/strategy/objective/phase — use IDs like TAC-1, STR-2, OBJ-1]
- **Decision:** [What was decided — one sentence]
- **Kill Reason (kill decisions only):** [hypothesis_falsified | kill_condition_met | exhaustion | external_constraint (§7.8 — force majeure, routes to Vector 3 external learning) | strategy_kill_cascade | governor_override]
- **Reasoning:** [Why — referencing signals, domain model concepts, Governor judgment]
- **Domain Models Referenced:** [Which domain model concepts informed this]
- **Impact on OD:** [What changes in the operating document, if any]
- **Authorization:** [This decision authorizes the OD changes listed above. OD elements modified by this decision reference DEC-[this-number] as their `authorized_by` source. For bulk authoring: GOV-session-[N]. For automatic adjustments: SYSTEM-[mechanism].]
- **Context Snapshot:** `[ROBUST]` [Captures OD parameters evaluated for this decision. Makes the entry self-contained for post-mortem audit.]
  - Target spec at decision time: [For kill/pivot/persevere: hypothesis, kill condition, success metrics, allocation weight. For rebalance: all affected allocation weights. For revise_objective: old metric/target/deadline.]
  - Prior authorized_by: [The `authorized_by` value on the target element before this decision. Creates backward-linked authorization chain. For new elements: "N/A — creation".]
  - Key signals: [Signal IDs referenced with their values at decision time. Example: "SIG-42 (engagement rate: 1.8%), SIG-43 (conversion: 0.3%)"]
  - Environmental context: [Active environmental signals during target's active period, if any. "None" if no environmental changes.]
- **Confounders:** `[CORE for kill decisions, ROBUST for pivots/strategy kills/A/B]` [Present only for kill, pivot, strategy_kill, and A/B winner decisions. For each applicable confounder:]
  - Environmental change: [present/absent — if present: description + disposition: dismissed (reason) | acknowledged]
  - Sibling interference: [present/absent — if present: which tactic + overlap description + disposition]
  - Input starvation: [present/absent — if present: expected vs actual inputs + disposition]
  - Data quality: [present/absent — if present: which signals flagged + disposition]
  - Bootstrap insufficiency: [present/absent — if present: cycles completed vs minimum]
  - Allocation change: [present/absent — if present: old vs new allocation + disposition]
  - External dependency strain: [present/absent — if present: which dependencies + exit_cost + notice period impact + disposition: terminate | transfer | renegotiate]
  - Cost overrun: [present/absent — if present: category + budget vs actual + disposition: accepted_overage | pivot | kill]
- **Tournament Selection (tournament_selection decisions only):**
  - Tournament mode: [sampling | constrained]
  - Selected candidate: [deliverable_ref]
  - Behavior cell (constrained): [cell assignment of winner]
  - Comparative scores:
    | Candidate | Cell | [Model 1] | [Model 2] | ... | Mean |
    |---|---|---|---|---|---|
    | [ref] | [cell] | [score] | [score] | ... | [mean] |
  - Selection rationale: [why this candidate — strategic, not just highest score]
  - Structural memory note: [design principle revealed, if any — e.g., "evidence-first entry outperforms problem-first for this audience"]
