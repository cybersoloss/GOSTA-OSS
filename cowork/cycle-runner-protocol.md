# Cycle Runner Protocol

**Version:** 0.1
**Derives from:** Framework §7.2 (Orchestrator Execution Loop), §8.7 (Pre-Flight Validation Gates), §6.1 (Governor non-response), §7.7 (escalation protocol), §7.13 (Failure Resilience); Cowork Protocol §5 (Session Lifecycle), §6 (Signal Format).
**Purpose:** Specify how an already-bootstrapped ongoing-scope GOSTA session runs **one Action Cycle** without a Governor in the conversation — woken by a scheduler, executing per the existing operating document, exiting cleanly.

---

## 1. Scope

This protocol governs the **non-interactive execution path** for an already-bootstrapped ongoing-scope session. It is the scheduler-driven counterpart to the conversational entry paths in `cowork/startup.md` (bootstrap) and `cowork/gosta-cowork-protocol.md` §5.2 (interactive execution session).

**It covers:**
- Scheduler-triggered execution of one Action Cycle per invocation against an already-ratified operating document.
- Reading inter-cycle Governor input (the inter-cycle input surface).
- Writing Governor-bound escalations (the escalation surface) when Blocking tensions or V-gate failures occur.
- Pre-cycle and post-cycle Pre-Flight Validation Gate (§8.7) handling adapted to non-interactive operation.
- State updates (signals, decisions, bootstrap, deliverables) per the standard cowork-protocol artifacts.

**It does NOT cover:**
- Bootstrap or session authoring — see `cowork/startup.md` (interactive scaffold) for first-session entry.
- OD authoring or mutation — non-interactive cycles treat the OD as ratified. OD changes are Blocking tensions; the cycle escalates and does not mutate the OD.
- Tactic Cycle or Strategy Cycle review — non-interactive execution runs the Action Cycle only. Review cycles (tactic, strategy) surface Governor decisions and remain interactive in Tier 0 unless the Governor explicitly authorizes review-cycle automation under Stage 3+ autonomy (§6.3, §7.2 STEP 5).
- Conversational lifecycle — see `cowork/gosta-cowork-protocol.md` §5 for Governor-present operation.

---

## 2. Activation Conditions

A session may use this protocol when **all** of the following hold:

1. The session is an **ongoing operational scope** per Cowork Protocol §2.2. Finite scopes do not iterate; this protocol does not apply.
2. The session has completed bootstrap and has a Governor-ratified operating document.
3. The session's operating document declares non-interactive cycle execution as authorized — either implicitly via scope type (`ongoing` with cadence ≥1/day) or explicitly via an `automation_mode: scheduler_triggered` flag declared at OD authoring time.
4. The session declares two file surfaces (abstract roles; runtime names are an implementation choice):
   - **Inter-cycle input surface** — a known file the Cycle Runner reads at the start of each cycle for Governor input accumulated since the prior cycle.
   - **Escalation surface** — a known file the Cycle Runner writes to when Blocking tensions or V-gate failures occur, for Governor attention before the next cycle.
5. The Governor has acknowledged the constraint that the Cycle Runner cannot decide non-delegable items (§6.1, §6.3 Stage 1 non-delegable list). Any tension classified as Blocking surfaces to the escalation surface and the cycle terminates without resolving it.

**Anti-pattern:** Running a Cycle Runner on a session whose OD has not been ratified. The protocol assumes the OD is the source of truth; without ratification it cannot be. Pre-flight V3 (decision-spine consistency) detects this at invocation.

---

## 3. Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Session directory | Yes | Path to an already-bootstrapped ongoing-scope session per Cowork Protocol §3. |
| Operating document | Yes | Governor-ratified, present in the session directory. |
| Bootstrap file | Yes | `00-BOOTSTRAP.md` reflects the state at the end of the prior cycle (or post-bootstrap state for the first non-interactive cycle). |
| Inter-cycle input surface | Yes | The file declared at OD authoring time for Governor input between cycles. May be empty (no input). |
| Escalation surface | Yes | The file declared at OD authoring time for Governor-bound escalations. The Cycle Runner appends to it; never overwrites. |
| Domain models | Yes when the OD declares any | Same loading semantics as Cowork Protocol §5.1 Step 2. |
| Signals from prior cycles | Yes | Read for state assessment per §7.2 Step 1 (Action Cycle LOAD CONTEXT). |
| Trigger-time metadata | Optional | Scheduler may pass invocation-time data (e.g., a Diff Agent change-set per `cowork/diff-agent-protocol.md`). Treated as additional input signals to the cycle. |

---

## 4. Procedure

The Cycle Runner executes the following steps in order. Each step has a defined failure behavior — V-gate failures, state conflicts, and Blocking tensions all map to escalation-then-exit rather than to interactive resolution.

### Step 1 — Orient

Read `00-BOOTSTRAP.md`. Determine: what cycle is this? When did the prior cycle complete? What did the prior cycle leave pending? Has the Governor disposed of any prior-cycle escalations between then and now?

If the bootstrap file is missing, malformed, or references a phase the OD does not name: this is a V-gate violation (V3 decision-spine consistency or V6 declared-artifact existence). Surface to the escalation surface with the specific anomaly and exit. Do not attempt repair.

### Step 1b — State conflict resolution (per Cowork Protocol §5.1 Step 1b)

Cross-check bootstrap state against authoritative sources before proceeding:

1. **Decision log is authoritative for decisions.** Apply any decision-log entries not yet reflected in the bootstrap before continuing.
2. **OD is authoritative for structure.** If the bootstrap references entities not in the OD, the bootstrap is stale — regenerate it from OD + decision log before continuing.
3. **Health reports are derived artifacts.** Stale health reports are noted; not blocking.
4. **Conflicts → `bootstrap_anomaly` signal.** Emit the signal with each conflict + its resolution. If a conflict is ambiguous (e.g., two contradictory decision log entries), this is a Blocking tension — surface to the escalation surface and exit. Do not guess.

### Step 2 — Read the inter-cycle input surface

Read the inter-cycle input surface declared at OD authoring time. Process its content as if the Governor had said it during a conversational session at this point in the lifecycle:

- **OD-mutation requests** (e.g., "kill TAC-3", "add guardrail X", "revise objective Y threshold"): non-mutable in this cycle. The Cycle Runner does not change the OD without a Governor in the loop. Record the request as a Blocking tension, surface to the escalation surface, exit.
- **Action-level direction** (e.g., "prioritize feature investigation for source X this cycle"): apply as input to Step 5 work plan generation. The Cycle Runner may bias the work plan within the OD's existing scope; it may not exceed the OD's scope.
- **Acknowledgments** (e.g., "I've reviewed the prior escalation; proceed"): clear the corresponding HOLD state from the bootstrap before continuing.
- **Information** (context, observations, references): note in the cycle's session log; not blocking.

After processing, the inter-cycle input surface is left in place (it is the Governor's surface; the Cycle Runner does not delete its content) but the bootstrap records which entries were consumed and how, to prevent double-application on subsequent cycles.

### Step 3 — Load context

Per Cowork Protocol §5.1 Step 2: read the operating document, relevant domain models, signals since last cycle, last 5 decision log entries, latest tactic episode summaries. The §7.2 Action Cycle STEP 1 load specification governs the minimum read set.

### Step 4 — Pre-cycle V-gate verification

Apply the applicable Pre-Flight Validation Gate invariants from spec §8.7.3 before producing work. The invariant set that applies at non-interactive cycle entry:

- **V3 Decision Spine Consistency** — OD ↔ scope ↔ bootstrap key-set comparison. BLOCK on symmetric-difference non-empty.
- **V6 Layer A Declared Artifact Existence** — every artifact named in the OD or bootstrap as a steady-state expectation must exist with non-zero content. BLOCK on missing.
- **V6 Layer B Continuous-Capture** — if continuous-capture mode flags are active (debug, shortfall logging, framework feedback), prior-cycle artifacts must be non-empty proportional to prior-cycle friction. WARN-only at cycle entry (not BLOCK); the consumer Monitor is responsible for capture coverage during execution, not at entry.
- **V5 Runtime Import Verification** — first invocation per session of any runtime-dependent tool (pool-agent, embedding tools) requires the import test from Cowork Protocol §"Verification Discipline" rule 5. BLOCK on import failure.
- **V1 Retrieval Contract Validation** — applies only if the cycle will run per-unit queries (typically not in Action Cycle execution — V1 is a phase-entry gate, not an action-cycle gate). Skip unless explicitly invoked.

**V-gate failure handling in non-interactive mode** (the load-bearing rule of this protocol):

| Failure | Disposition |
|---------|-------------|
| BLOCK | Write a structured escalation entry to the escalation surface naming the failing invariant, the specific test result, the operational state observed, and at least two mitigation paths drawn from the §8.7.2 escalation menu. Exit cleanly. Subsequent cycles HOLD (do not run the OD's action-cycle work) until the Governor disposes of the escalation via the inter-cycle input surface. |
| WARN | Log the warning in the cycle's session log; continue to Step 5. Cumulative WARN across N cycles (default N=3) escalates to BLOCK behavior — the cycle treats sustained capture failures as Blocking even if individually they only WARN. |
| PASS | Continue to Step 5. |
| N/A | Skip the invariant; record the skip with reason. |

**HOLD semantics.** When subsequent cycles run while a prior BLOCK is outstanding: the cycle reads the escalation surface and bootstrap, observes the unresolved BLOCK, writes a "cycle skipped — prior BLOCK unresolved" signal, and exits. The Governor disposes of the BLOCK via the inter-cycle input surface (Step 2 next cycle). The cycle does NOT silently retry the failing V-gate hoping the operational state has changed.

### Step 5 — Run one Action Cycle

Execute the spec §7.2 Action Cycle steps 1–6 against the loaded context. Non-interactive specifics:

- **STEP 1 LOAD CONTEXT, STEP 2 ACTIVATION SCHEDULE, STEP 3 ASSESS CURRENT STATE** — execute as specified. Trigger-time metadata (e.g., a Diff Agent change-set) is treated as additional signal input.
- **STEP 3 guardrail processing** — hard guardrail violation is a Blocking tension; escalate and exit per Step 8 below. Soft guardrail at Stage 1–2 is also a Blocking tension. Soft guardrail at Stage 3+ with declared recovery spec applies the recovery via normal action dispatch and continues, per §7.2 STEP 3 sub-step (d).
- **STEP 3 event-triggered review conditions (§7.9)** — if a trigger condition is met (critical environmental signal, kill condition deadline approaching, etc.), the event triggers a *recommendation* in the cycle output; the Cycle Runner does not enter a Tactic or Strategy Review without a Governor. The event-triggered review is a Blocking tension if it requires non-delegable decisions; otherwise it surfaces as a recommendation in the next cycle's status report.
- **STEP 4 GENERATE WORK PLAN, STEP 4b CAPACITY CEILING** — execute as specified. Cycle-level work plan production is autonomous within the OD's existing scope. If Step 4b capacity-ceiling trim would defer items the Governor previously prioritized via the inter-cycle input surface: surface as a Material tension; default = honor the capacity ceiling (the operationally safe action), note the trim in the cycle's session log, continue.
- **STEP 5 STATUS REPORT** — generate the report as specified, but the report is written to the session's standard `health-reports/` or `session-logs/` artifacts; it is not interactively presented. Material tensions are recorded with their applied defaults per the OD's `material_tension_defaults` (or, if undeclared, the §6.1 Section A defaults). Blocking tensions surface to the escalation surface.
- **STEP 6 DISPATCH AND WRITE** — dispatch executors per the work plan, signal stubs before dispatch (Cowork Protocol §6.3), signals updated to `completed` or `failed` after each executor returns. Write episode summaries, status report, and any escalations as specified.

### Step 6 — Process cycle outputs

Per Cowork Protocol §5.1 Steps 4–5:
- Write all signals (append-only) to `signals/`.
- Append decisions made autonomously per the stage's autonomy table to `decisions/governor-decisions.md` with `decision_source: orchestrator_autonomous` and the cycle identifier.
- Write deliverables produced this cycle to `deliverables/`.
- Update `00-BOOTSTRAP.md` to reflect the cycle's outcome: current state, what was completed, what is pending, what is escalated to the Governor (with reference to the escalation surface entry IDs).

### Step 7 — Post-cycle V-gate verification

At cycle exit, apply the post-cycle subset of §8.7.3 invariants:

- **V4 Continuous Capture Operationalization** — for each active continuous-capture mode flag, verify the corresponding artifact received cycle-proportional entries. Empty captures with observed friction WARN; sustained-empty across N cycles escalates per §4 above.
- **V6 Layer A** — every artifact the OD or bootstrap declares as a cycle deliverable must exist with non-zero content. BLOCK if missing; cycle treated as failed-after-execution; escalate.
- **V2 Build Artifact Shape Verification** — applies only if the cycle produced a pool/embedding build. Skip otherwise.

Post-cycle BLOCK semantics differ from pre-cycle BLOCK: the cycle has already executed and produced state, so post-cycle BLOCK means escalation surface receives a "cycle completed but post-validation failed; outputs may be inconsistent" notification with the specific failure. Bootstrap records the cycle as `completed_with_post_block`; the Governor disposes whether to roll forward or roll back via the inter-cycle input surface.

### Step 8 — Handle Blocking tensions and escalations

For every Blocking tension surfaced during the cycle (whether from V-gate failure, hard guardrail, OD-mutation request, ambiguous state conflict, or non-delegable decision required):

1. Append a structured escalation entry to the escalation surface with: tension type, originating step, operational state observed, at least two mitigation paths drawn from the relevant spec/protocol sections, and the cycle identifier.
2. Record the escalation in the bootstrap's "What Is Pending" section.
3. Continue executing the rest of the cycle steps **only if** the tension does not invalidate downstream state. V-gate BLOCKs at Step 4 invalidate downstream state and exit immediately. Hard guardrail violations at Step 5 invalidate the violating action only — the rest of the work plan continues if no other action depends on the halted action.
4. Material tensions apply the OD's declared defaults (or the §6.1 generic defaults) and continue. They are logged in the cycle's status report but do not write to the escalation surface.
5. Informational tensions are logged in the cycle's session log; no escalation surface write.

### Step 9 — Exit cleanly

Write the final cycle exit signal: `cycle_completed | cycle_id | exit_state: clean | completed_with_post_block | escalated_and_halted`. Update `session-status.md` per Cowork Protocol §5.1 Step 6b. Exit the runtime.

The runtime exit is the cycle's terminal action. The Cycle Runner does not retain state between cycles beyond what is written to session artifacts. Each cycle re-orients from the bootstrap.

---

## 5. V-Gate Handling in Non-Interactive Mode (Summary)

The load-bearing design choice of this protocol is the mapping from §8.7 V-gate failures (originally specified for Governor-present escalation) to non-interactive escalation-and-exit:

| V-gate scope in §8.7 | Non-interactive mapping |
|----------------------|--------------------------|
| BLOCK with Governor-presented mitigation paths | Escalation surface entry with mitigation paths drawn from §8.7.2; cycle exits; HOLD until Governor disposes |
| WARN with Governor acknowledgment | Logged in session log; cycle continues; cumulative WARN across N cycles → BLOCK behavior |
| Mid-cycle event-triggered escalation | Status report records; if event requires non-delegable decision → Blocking tension → escalation surface |
| Hard guardrail violation | Blocking tension; halt violating action; escalation surface entry; rest of work plan continues if independent |
| Soft guardrail Stage 1–2 violation | Blocking tension; escalation surface entry; halt violating action |
| Soft guardrail Stage 3+ violation with declared recovery | Apply recovery per §7.2 STEP 3 (d); continue; recovery logged |
| Soft guardrail Stage 3+ violation with blocked recovery | Treat as hard per §7.2 STEP 3 (d) fallback; escalation surface entry; halt |

The Governor non-response default (§6.1 / §7.7) does not apply to V-gate BLOCKs in non-interactive mode. V-gate BLOCKs always HOLD until disposed — there is no "safe default" for operational-truth failures because the failure itself indicates the operational state is not safe.

---

## 6. Blocking Tension Handling

Blocking tensions in non-interactive mode are categorically different from Blocking tensions in conversational mode. In conversation, the Governor responds in the same session. Here, the response is at least one cycle delayed.

**The default disposition for any non-delegable decision encountered mid-cycle is escalate-and-halt.** The Cycle Runner does not attempt graceful continuation past a Blocking tension because the cycle's downstream work may depend on the Governor's disposition.

**Exceptions** — cycles may continue past a Blocking tension in two specific cases:

1. The Blocking tension applies to a tactic the rest of the work plan does not depend on. In this case the affected tactic's actions halt; other tactics' actions proceed; bootstrap records the partial completion.
2. The Blocking tension is an event-triggered review recommendation (not a halt-now condition). The recommendation surfaces in the cycle's status report and on the escalation surface; cycle work proceeds for the current cycle; next cycle HOLDs if the Governor has not disposed.

These exceptions are documented in the cycle's session log with the specific reasoning. Operational-truth gaps (V-gate BLOCK, hard guardrail, ambiguous state conflict) do not qualify for graceful continuation.

---

## 7. Material Tension Handling

Material tensions apply the OD's declared `material_tension_defaults`. If the OD does not declare per-tension defaults, the §6.1 generic default applies: the AI states its default recommendation and proceeds unless the Governor overrides via the inter-cycle input surface on a subsequent cycle.

Material tensions are logged in the cycle's status report with the applied default and the rationale. They are not written to the escalation surface (the surface is reserved for Blocking).

A Governor override arriving on the inter-cycle input surface after the default has been applied is honored on the subsequent cycle's Step 2 processing. The Cycle Runner does not retroactively reverse a default-applied decision unless the OD declares reversal semantics for the specific tension class.

---

## 8. Constraints

- **The Cycle Runner is not a Governor.** It cannot make decisions in the §6.3 Stage 1 non-delegable list. Any such decision required mid-cycle is a Blocking tension.
- **The OD is treated as ratified.** No OD authoring or mutation. Any OD change request is a Blocking tension.
- **Each cycle is one Action Cycle.** Tactic and Strategy Review cycles are not run non-interactively unless explicitly authorized in the OD with Stage 3+ autonomy declared.
- **Append-only discipline holds.** Signals, decisions, deliverables, escalation surface are append-only. The bootstrap and `session-status.md` are the only files the Cycle Runner overwrites.
- **No mid-cycle V-gate retry.** A V-gate BLOCK at Step 4 exits; the next cycle re-runs the gate from scratch with whatever operational state exists then. The Cycle Runner does not loop on a failing gate within a single cycle.
- **Capture discipline applies.** If continuous-capture mode flags are active, the Cycle Runner produces capture entries proportional to observed friction per Cowork Protocol §"Verification Discipline" rule 10. Empty captures with observed friction WARN at post-cycle V4.

---

## 9. Open Design Questions

These remain unresolved at v0.1 and are subject to Governor disposition or empirical observation:

1. **Tactic and Strategy Review cycle automation.** At Stage 4+ autonomy, the spec authorizes the orchestrator to make tactic-level decisions autonomously. Whether the Cycle Runner extends to run Tactic Cycle (and Strategy Cycle) non-interactively at high autonomy stages is deferred. This protocol covers Action Cycle only; Tactic Cycle non-interactive execution requires an extension, with new V-gate handling for the heavier decisions involved.

2. **Cross-cycle HOLD propagation across sessions.** When ≥2 ongoing-scope sessions are running non-interactively and one HOLDs on an outstanding BLOCK, whether the HOLD propagates to related sessions (e.g., sessions whose work depends on signals from the held session) is not specified. The current default: HOLD is per-session; cross-session dependencies surface as `precondition_not_met` signals on the dependent session, handled by §7.2 STEP 4 precondition deferral.

3. **Recovery-spec validation at cycle-entry.** §7.2 STEP 3 sub-step (d) validates a soft-guardrail recovery against inherited hard constraints at the moment of violation. Whether recovery specs should also be validated at cycle-entry (V-gate-like, before the cycle begins) is deferred until empirical observation indicates whether recovery-spec drift is a real failure mode.

4. **Trigger-time metadata schema.** The protocol accepts arbitrary trigger-time metadata as input but does not specify a schema. When `cowork/diff-agent-protocol.md` (forthcoming, minimal interface) lands, this protocol will reference its change-set schema as the canonical trigger-time metadata format. Until then, scheduler-passed metadata is treated as opaque input signals.

---

## 10. Relationship to Other Protocols

- **`cowork/gosta-cowork-protocol.md`** — the conversational counterpart. §5 Session Lifecycle covers Governor-present operation. This protocol is its non-interactive variant for Action Cycle execution. The two are mutually exclusive within a single cycle but compose within a session lifetime: a session may interleave conversational and non-interactive cycles.
- **`cowork/startup.md`** — the bootstrap entry point. Sessions enter this protocol only after a Governor-present bootstrap has produced a ratified OD.
- **`cowork/diff-agent-protocol.md`** (v0.1 minimal interface spec) — when a Monitor declares a Diff Agent, the Cycle Runner invokes it during Step 5, before §7.2 STEP 4 work plan generation. The Diff Agent's change-set output is treated as additional signal input to STEP 4. The input contract, output contract, and failure-signal mapping (including the `corrupt_last_seen` Blocking escalation that fires at Step 8 of this protocol) are specified in the Diff Agent protocol.
- **`cowork/evidence-collection-protocol.md`** — single-phase deep investigation. The Cycle Runner does NOT invoke evidence-collection per-cycle. Sessions requiring periodic deep investigation declare it in the OD as a periodic phase; this protocol's relationship to multi-phase evidence collection in ongoing scopes is deferred (cf. `cowork/startup.md` line 56's acknowledgment of the same gap at the evidence-collection layer).
- **`cowork/verification-patterns.md`** — Pattern 4 (anchor in observation), Pattern 14 (session-need vs framework-need): this protocol is framework-general (any ongoing-scope session on a schedule), not session-specific. The mechanism is reusable across all GOSTA implementations of Tier 1+ scheduler-triggered execution.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-06-02 | Initial version. Codifies non-interactive Action Cycle execution from Framework §7.2 + Cowork Protocol §5. Maps Pre-Flight Validation Gates (§8.7) to non-interactive escalation. Defers Tactic/Strategy Cycle automation and trigger-time metadata schema until empirical observation. |
