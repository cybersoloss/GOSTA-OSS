# Diff Agent Protocol (Minimal Interface Spec)

**Version:** 0.1 (minimal interface)
**Derives from:** Framework §7.14 (Environmental Signal Architecture), §7.14.2 (Environmental Signal Processing); Cowork Protocol §6 (Signal Format); references `cowork/cycle-runner-protocol.md` Step 5.
**Purpose:** Specify the minimal input/output contract for an agent that watches an environmental source on behalf of a GOSTA session, detects change since last cycle, and emits a change-set the session consumes as environmental signals.

---

## 1. Scope

This is a **minimal interface spec**, not a full protocol. Per Governor decision (verifier verdict SIMPLIFY on GOSTA-Watch Plan Gap 5.2), the scope is intentionally bounded to the input contract, the output contract, and the failure-signal mapping. Source-type adapter abstraction, full failure-mode taxonomy, and the relationship to `cowork/evidence-collection-protocol.md` §14.8 evidence-item schema are explicitly deferred until empirical observation exists.

**This minimal interface covers:**
- The input contract a Cycle Runner (or other invoker) passes to a Diff Agent when invoking it.
- The output contract a Diff Agent produces: a change-set consisting of environmental signals conforming to spec §7.14.2's signal schema and severity vocabulary.
- The failure-signal mapping for three primary failure classes.

**It does NOT cover (deferred):**
- Source-type adapter abstraction (git, filesystem, REST API, document store, app-export, web, RSS, etc.).
- Comprehensive failure-mode taxonomy beyond the three primary classes named in §5 below.
- Resolution of the Diff Agent's relationship to `cowork/evidence-collection-protocol.md` §14.8 evidence-item schema.
- Hybrid runtime patterns (pure subagent / pure script / hybrid script+subagent).
- Specific change-detection algorithms (semantic diff, structural diff, hash diff, etc.).

These are tracked as deferred sections in §8 below with an explicit unlock trigger.

---

## 2. Activation Conditions

A session uses a Diff Agent when **all** of the following hold:

1. The session is an ongoing operational scope (per Cowork Protocol §2.2) running per `cowork/cycle-runner-protocol.md` or an equivalent non-interactive execution path.
2. The session declares an environmental watch list per spec §7.14.1.
3. The session's operating document declares a Diff Agent for one or more watch list entries.
4. The invoker has access to a persisted last-seen state for each watched source (commit SHA / timestamp / hash / equivalent — the choice is the invoker's implementation concern).

If any of (1)–(4) does not hold, the Diff Agent is not invoked; environmental signals fall back to the reactive paths described in spec §7.14 (Governor reports at reviews, executor discovery, milestone events).

---

## 3. Input Contract

The invoker passes the following input to the Diff Agent on each invocation:

| Field | Type | Description |
|-------|------|-------------|
| `source_state.location` | string | The source location reference (URL, file path, repository identifier — opaque to this protocol). |
| `source_state.last_seen` | opaque | The persisted last-seen state from the prior cycle (commit SHA / timestamp / hash / nothing-if-first-cycle). The Diff Agent does not interpret this beyond passing it back through; the invoker is responsible for its persistence and shape. |
| `watch_list` | list | The subset of the OD's environmental watch list entries (per §7.14.1) that apply to this source. Each entry carries `condition`, `relevance` (goal/strategy/WMBT IDs), `change_threshold`. |
| `monitor_identity.session_id` | string | The originating session identifier. Travels with every emitted signal as the `source` field's anchor. |
| `monitor_identity.scope_id` | string | The OD's declared scope identifier. Distinguishes signals from different scopes when multiple sessions share infrastructure. |

The `source_state.location` and `source_state.last_seen` together fully describe what to compare against; the Diff Agent does not retain state between invocations.

---

## 4. Output Contract

The Diff Agent produces a **change-set** on every invocation. A change-set is a list of zero or more environmental signals plus an updated last-seen state.

### 4.1 Change-set top-level shape

```yaml
change_set:
  invocation_id: <opaque identifier — invoker-assigned>
  source_location: <echoed from input>
  last_seen_updated: <new last-seen state value to persist for the next invocation>
  signals:
    - <environmental signal entry — schema below>
    - ...
  invocation_status: VALIDATED | PARTIAL | FAILED  # see §5
  failure_class: <one of the failure-signal mapping classes when invocation_status != VALIDATED; null otherwise>
```

### 4.2 Per-signal schema (conforms to spec §7.14.2)

Each entry in `change_set.signals` is an environmental signal per spec §7.14.2's exact field set:

| Field | Value |
|-------|-------|
| `signal_type` | `environmental` |
| `condition_id` | The watch list entry identifier that this change satisfies |
| `previous_state` | The relevant slice of the prior `source_state.last_seen` |
| `current_state` | The relevant slice of the new observation |
| `source` | `diff_agent:<monitor_identity.session_id>:<source_location>` — preserves provenance per §14.3.3 / §14.3.4 |
| `affected_entities` | The `relevance` field from the watch list entry (goal/strategy/WMBT IDs) |
| `severity` | `informational` | `significant` | `critical` — per §7.14.2 vocabulary |

The Diff Agent assigns `severity` per the watch list entry's `change_threshold` field plus §7.14.2's classification rules:

- **`informational`** — change detected but within normal variance / below `change_threshold`.
- **`significant`** — change exceeds `change_threshold` and affects an active strategy's WMBT or a guardrail-viability condition.
- **`critical`** — change directly falsifies a WMBT, renders a guardrail untenable, or triggers a goal-level reassessment per §7.14.2.

Severity classification is the Diff Agent's responsibility; the invoker does not re-classify. If the Diff Agent cannot classify (e.g., the threshold is qualitative and the change is borderline), it assigns `informational` and adds an `unclassified_severity` flag to the signal entry. The next-cycle Cycle Runner or Governor disposition surfaces the unclassified case.

### 4.3 Empty change-set (no change)

If the source is reachable and no watch list condition changed beyond its threshold, the change-set is:

```yaml
change_set:
  invocation_id: <...>
  source_location: <...>
  last_seen_updated: <updated tracking metadata — possibly identical to input>
  signals: []
  invocation_status: VALIDATED
  failure_class: null
```

The invoker still persists `last_seen_updated` even when no signals were produced — last-seen metadata may include tracking fields (e.g., last poll timestamp) that update on every invocation.

---

## 5. Failure-Signal Mapping (the three primary classes)

The Diff Agent maps three primary failure classes to specific output behavior:

| Failure class | Cause | `invocation_status` | Signal emitted | Severity | Invoker disposition |
|---------------|-------|---------------------|----------------|----------|---------------------|
| **Source unreachable** | The source endpoint cannot be reached (network failure, authentication failure, source decommissioned). | `FAILED` | One signal with `condition_id: diff_agent_source_unreachable`, `current_state: <error description>` | `informational` | Cycle continues; the cycle's status report notes the failed Diff Agent invocation. Repeated source-unreachable failures across N cycles (configured at OD authoring time, default N=3) escalate to Governor as a Blocking tension. |
| **Partial diff** | The source is reachable but the comparison against last-seen state is incomplete (some watch list entries evaluated, others not — e.g., a subset of paths inaccessible). | `PARTIAL` | One signal per successfully-evaluated entry per the schema above, plus one signal with `condition_id: diff_agent_partial_evaluation`, `current_state: <list of unevaluated entries + reasons>` | `significant` (the partial-evaluation signal); per-condition signals carry their per-condition severity | Cycle continues; the cycle's status report notes the partial evaluation. The unevaluated entries are re-tried at next cycle. |
| **Corrupt last-seen state** | The persisted `source_state.last_seen` is malformed, schema-violated, or otherwise unusable for comparison against the current source. | `FAILED` | One signal with `condition_id: diff_agent_corrupt_last_seen`, `current_state: <description of corruption>` | (not severity-classified; this maps to Blocking escalation) | **Blocking escalation.** The Cycle Runner's Step 8 treats this as a Blocking tension: writes to the Governor-bound escalation surface, exits the cycle, subsequent cycles HOLD until the Governor disposes (typically: reset last-seen state or substitute a known-good value). |

Other failure modes (ambiguous change, source schema changed, watch list entry not satisfiable, etc.) are explicitly deferred to the full failure-mode taxonomy — see §8 below. The Diff Agent treats unrecognized failure classes as `PARTIAL` with an explanatory signal at `significant` severity until the taxonomy is authored.

---

## 6. Invocation Within a Cycle Runner Cycle

The Diff Agent is invoked by the Cycle Runner during Step 5 (Run one Action Cycle) — specifically, before §7.2 STEP 4 GENERATE WORK PLAN, so the change-set is available as input to work plan generation. The exact invocation point inside Step 5 is documented in `cowork/cycle-runner-protocol.md` §10 Relationship.

The Cycle Runner consumes the change-set as follows:

- **Signals are appended to `signals/`** per Cowork Protocol §6 (append-only discipline). Each signal's `source` field carries the Diff Agent provenance.
- **`last_seen_updated` is persisted** wherever the invoker chose to persist last-seen state (file system, database, etc. — implementation concern).
- **`invocation_status: FAILED` with `failure_class: corrupt_last_seen` triggers Blocking escalation** per the Cycle Runner protocol Step 8.
- **`invocation_status: FAILED` with `failure_class: source_unreachable` accumulates** per the Cycle Runner protocol's cumulative-WARN-becomes-BLOCK rule (default 3 consecutive failures → escalation).
- **`invocation_status: PARTIAL` is treated as Material tension** with the cycle's declared default (proceed with the partially-evaluated change-set; note the gap in the status report).

The Diff Agent does NOT write to `signals/`, `decisions/`, `deliverables/`, or the escalation surface directly. It returns the change-set; the Cycle Runner is the I/O boundary.

---

## 7. Open Design Questions (Intentionally Retained)

Per Governor decision and verifier guidance, the following question remains explicitly open and is NOT resolved at v0.1:

**Relationship to `cowork/evidence-collection-protocol.md` §14.8 evidence-item schema.** The Diff Agent emits signals conforming to spec §7.14.2 (environmental signal schema). The evidence-collection-protocol operates on §14.8 evidence-item schema (with attribution tiers, provenance fields, claim-evidence pairs). Both ingest external content with provenance. The following remain unresolved:

- Is a Diff Agent signal also an evidence item (and if so, which §14.8 attribution tier applies to environmental observation)?
- Should a Diff Agent invocation produce both an environmental signal AND an evidence-collection evidence item for the same observed change, or only one?
- When a session runs both periodic Diff Agent invocations and a single-phase evidence-collection phase, do they share a manifest? A pool? Separate stores?

These are real interaction-design questions; resolving them speculatively without empirical patterns invites the wrong architecture per `cowork/verification-patterns.md` Pattern 4 (anchor in observation). They will be addressed when ≥1 Monitor has completed ≥2 cycles AND at least one observation surfaces the dual-emission question concretely. Until then, the Diff Agent emits §7.14.2 environmental signals only; sessions that need evidence-item provenance for an observed change invoke evidence-collection separately within the same cycle.

---

## 8. Deferred Sections (with unlock trigger)

The following sections are intentionally NOT authored at v0.1. They unlock when **≥1 Monitor has completed ≥2 Action Cycles** with the v0.1 interface, AND the empirical observations indicate which extensions are needed:

1. **Source-type adapter abstraction.** A generalized adapter interface per source type (git, filesystem, REST API, document store, app-export, web, RSS, etc.) with per-source-type extension hooks. Defer rationale: the right adapter abstraction depends on which source types are actually used and which sharing patterns emerge. Authoring abstractly before observation risks the wrong factoring.

2. **Full failure-mode taxonomy.** Beyond the three primary classes in §5: ambiguous change (informational vs. significant boundary cases), source schema changed (the source's data model evolved between invocations), watch list entry not satisfiable (the entry references concepts no longer present in the source), authentication degradation (partial-credential failure), rate-limit failure (source reachable but rate-limited). Defer rationale: each failure mode wants a specific signal mapping and Cycle Runner disposition; authoring them speculatively risks designing for cases that don't occur.

3. **Evidence-collection-protocol relationship resolution.** See §7 above. Defer rationale: empirical evidence required to choose the right integration shape.

4. **Hybrid runtime accommodation.** Pure-subagent / pure-script / hybrid patterns with per-pattern guarantees about determinism, cost, and failure semantics. Defer rationale: runtime pattern choice is currently the invoker's concern; framework guidance would over-constrain implementations without an observed need.

5. **Change-detection algorithm guidance.** Semantic diff (LLM-classified) vs. structural diff (path/key/field-level) vs. hash diff (binary identity). Defer rationale: source-type-specific; tied to deferred section 1.

**Unlock trigger restated:** ≥1 Monitor × ≥2 cycles with the v0.1 interface, AND empirical observations of specific friction in one or more deferred areas. When the trigger fires, the relevant deferred section is re-proposed to GOSTA-DEV with the empirical anchor.

---

## 9. Relationship to Other Protocols

- **`cowork/cycle-runner-protocol.md`** — invoker. The Cycle Runner invokes the Diff Agent during Step 5 of its cycle and consumes the change-set output. The two protocols are tightly coupled at the invocation contract but not at the implementation: the Cycle Runner does not depend on a specific Diff Agent runtime pattern.
- **`cowork/evidence-collection-protocol.md`** — separate concern. Evidence collection is single-phase deep investigation; Diff Agent is per-cycle change detection. Both ingest external content with provenance; the protocol-level relationship is intentionally unresolved (§7).
- **Spec §7.14 Environmental Signal Architecture** — the source of the schema and severity vocabulary the Diff Agent emits. This protocol does not modify §7.14; it operationalizes the agent that §7.14.3 describes only conceptually at each tier.
- **`cowork/verification-patterns.md`** — Patterns 4 (anchor in observation), 13 (scope extension justified), 14 (session-need vs framework-need) all informed the SIMPLIFY decision that produced this minimal scope.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-06-02 | Initial minimal interface spec per Governor SIMPLIFY decision on GOSTA-Watch Plan Gap 5.2. Input contract, output contract (change-set schema using §7.14.2 vocabulary), three-primary-failure-class signal mapping, invocation point within Cycle Runner cycle. Source-type adapter abstraction, full failure-mode taxonomy, evidence-collection relationship, hybrid runtime patterns, change-detection algorithm guidance — all explicitly deferred to a future v0.2+ pending empirical observation (≥1 Monitor × ≥2 cycles). |
