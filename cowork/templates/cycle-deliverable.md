# Cycle Deliverable — Consumer-Legibility Template

**Purpose.** Optional template for cycle deliverables in ongoing-scope sessions. Structures a deliverable so the Governor's actionable content is reachable at the top while framework discipline (multi-model evaluation, attribution chains, V-gate metadata, audit artifacts) remains preserved in an appendix. The template is non-mandatory: sessions that do not adopt it produce deliverables that satisfy all framework discipline checks. The template's value is operational legibility for Governors who consume deliverables at high cadence.

**When to use.** Ongoing-scope sessions whose cycle deliverables run >150 lines or whose Governor consumption pattern is "weekly review against many deliverables." When the deliverable is short (<60 lines) or the Governor reads it linearly, the template's body/appendix split adds friction without benefit; skip.

**Empirical anchor.** Pilot-stage cycle deliverables that fully satisfied framework grounding (cite-then-apply, multi-model evaluation, evidence attribution) measured ~14% decision-relevant content per body line; most actionable content surfaced past line 300 of 350-line deliverables. After adopting this template's structure pattern: ~70-75% body compression with identical underlying analysis (apparatus moved to appendix; the multi-model machinery operates on appendix data unchanged).

**Cross-reference.** Sessions using this template typically declare the discipline in their OD under a `§Deliverable Presentation Discipline` section (or equivalent) so the template's structural choices are auditable. The cowork-protocol references this template as the recommended-default structure for ongoing-scope deliverables at high Governor-consumption cadence.

---

## Section structure (body first, apparatus in appendix)

### `## Executive Summary` (mandatory; top placement)

≤200 words. Plain English. Required content:

- **What changed in the source since last cycle** — 1 sentence.
- **What surfaced this cycle** — ≤3 bullets, each ≤1 sentence.
- **What the Governor should act on this week** — ≤3 bullets, each ≤1 sentence.

Forbidden in the Executive Summary (move to appendix or omit): pattern catalog ID citations, spec section references (§X.Y), multi-model evaluation tables, V-gate metadata, evidence-scope tables. The Executive Summary reads cleanly without the OD open, or it has failed its purpose.

### `## Actions Required` (mandatory; second placement)

Immediately after the Executive Summary. Bulleted list of Governor-directed asks. Each item:

- Explicit verb (ratify / defer / route / decide / schedule / investigate / acknowledge), AND
- Short description, AND
- Landing artifact (file path or decision channel).

Each item fits one line. If the cycle produces no Governor-pending asks, retain the section with an explicit "No Actions Required this cycle" placeholder so the structure is consistent across deliverables.

### Per-candidate / per-finding body sections (adaptive depth)

For sessions evaluating items (candidates, findings, change-events, etc.) against a multi-model or multi-criterion framework:

- **High-verdict-tier items** (e.g., items the framework treats as "proceed to next stage"): full per-model or per-criterion body presentation.
- **Mid-tier items** (e.g., conditional, partial-fit, ambiguous): summary body presentation citing top N models or criteria; remaining model/criterion outputs as one-line summary references.
- **Low-tier items** (e.g., not-viable, rejected, irrelevant): single-line convergence note in body; first-rejecting model or criterion verdict in body.

**Critical discipline:** the framework's evaluation machinery (e.g., variance metric, kill condition, cross-model agreement check) operates on the *appendix data*, not on the body's adaptive presentation. Body presentation is consumer-legibility scaffolding; statistical or correctness machinery runs on the full data the appendix preserves. The body presentation choice is presentation-only scope; it does not mutate evaluation discipline.

### `## "What This Means" — per-item directive` (optional but recommended)

For each item presented in the body, a ≤80-word paragraph in plain directive language: *"Don't pursue [item] until [gate]; in the interim, [action]; reconsider when [revival condition fires]."* Translates verdict labels (e.g., "VIABLE", "INFRASTRUCTURE-ONLY", "ADJACENT-NOT-VIABLE") into action language the Governor can apply without consulting the verdict taxonomy.

### `## Outbound Observations` (optional)

Findings the cycle surfaces that don't bind to a candidate/finding but warrant Governor awareness (cross-source signals, environmental shifts, framework-feedback candidates).

### `## Closure Summary` (mandatory final body section)

One-paragraph cycle close note: what the cycle accomplished, what remains pending, the cycle's exit state per the Cycle Runner's exit signal vocabulary (clean / completed_with_post_block / escalated_and_halted).

### `---` divider

Visually separates body from appendix.

### `## Appendix — Framework Apparatus`

Below the divider, retain in the appendix (preserved for audit; not gating Governor reading):

- Cycle status report
- Survey scope / evidence scope tables
- Multi-model scoring tables / per-criterion evaluation tables
- Cross-domain synthesis tables
- Guardrail evaluation walks
- Viability-trail / dependency-trail completeness checks
- Attribution chains and citations (full per §14.3.3 / §14.3.4)
- V-gate execution records (per §8.7)
- Signal references emitted by this cycle

A Governor reading only the body must reach a complete operational understanding of the cycle; a reviewer reading the appendix must reach a complete framework-discipline audit. The body and appendix are complementary, not redundant.

---

## Length guidance by cycle delta size

Length caps apply to body content (above the appendix divider). Appendix is uncapped.

- **Substantive cycle** (≥1 candidate / finding evaluated): body ≤150 lines; appendix unlimited.
- **Thin cycle** (process work, framework feedback, OD-mutation proposal, no candidate evaluation): body ≤60 lines; appendix unlimited.
- **Null-delta cycle** (no input, no process work, no Governor-pending surface): body ≤30 lines; appendix ≤50 lines.

The session may override these caps in its OD with a documented rationale (e.g., for cycles producing a multi-candidate cross-section that needs side-by-side body presentation).

---

## Pattern catalog discipline (body vs appendix)

Pattern catalog codes (domain-model concept IDs, quality principle IDs, anti-pattern IDs, etc.) appearing in body sections require parenthetical inline expansion at first mention per deliverable. Example: *"Capability Audit Before Scoring (QP-3) indicates >70% reuse."* Or omit the code and use plain language: *"Capability audit indicates >70% reuse."*

In appendix sections, pattern codes may appear without inline expansion — the auditor is expected to consult the OD.

---

## Relationship to existing framework discipline

This template does **not** override or weaken any framework discipline. It re-organizes a discipline-complete deliverable for consumer legibility:

- Spec §14 grounding architecture (cite-then-apply per §14.3.2; data grounding per §14.3.3; attribution per §14.3.4; multi-domain consultation per §14.7; evidence collection per §14.8): all preserved in appendix where audit is the consumer.
- Spec §14.3.9 sycophancy detection: applies unchanged to the body's adaptive presentation — the body cannot omit risk factors or signal-recommendation contradictions; those must surface in Executive Summary or Outbound Observations.
- Spec §14.3.11 verification checks (Checks 1-9): operate on appendix data; body presentation is downstream of check execution.
- Cowork-protocol §5.5 closeout audit: deliverables remain V6-mandated under the same population-floor and audit-trail-union semantics.
- Independent reviewer (U1) dispatch (cowork-protocol §5.1 step 2a / §5.5): U1 sees both body and appendix; adversarial enumeration applies to both.

---

## Adoption pattern

Sessions adopt this template by:

1. Declaring `§Deliverable Presentation Discipline` (or equivalent) in their OD with the template references (DPD-1.1..1.N or session-specific identifiers).
2. Referencing the OD's discipline section in `00-BOOTSTRAP.md` Context Loading Order.
3. Authoring cycle deliverables to the structure pattern from the OD-ratification cycle forward. Pre-adoption cycle deliverables are retained as-is for audit-trail consistency; a cross-reference note in the candidate-/finding-backlog directs consumers to the new format for actionable extraction.

The cowork-protocol does not enforce template adoption. Sessions may produce framework-discipline-complete deliverables in any structural layout. The template is recommended-default for ongoing-scope sessions whose Governor-consumption pattern empirically benefits from the body/appendix split.
