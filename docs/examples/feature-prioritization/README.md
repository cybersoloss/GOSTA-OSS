# Feature Prioritization — GOSTA Deliberation Example

> **Framework state — version-stamped 2026-05-03.** This example was authored against an earlier framework state (Cowork Protocol ~v3.15) and demonstrates the conceptual structure of multi-agent deliberation accurately. The framework has since added deliverable-time disciplines that this example does NOT show: Verdict Strength Annotation `[cluster-confirmation: N, tier-floor: TX]` per verdict (Plan #8), §12.12 Frame Integrity Validation section in synthesis report (Plan #19), §12.15 Coverage Limitations Disclosure when coverage is sub-threshold (Plan #7), Evidence Channel Disclosure for Party-X-reception claims (Plan #11'), `[VERDICT-SPLIT-CARRIED]` annotation when intra-cluster splits are carried unresolved (Plan #13), and formula-based per-deliverable caps (Plans #17/#20). See `cowork/sync-manifest.md` C201–C217 for the change record. Conceptual structure shown here remains accurate for understanding deliberation mechanics. For a fully current example, see [`my-first-session/`](../my-first-session/) (refreshed 2026-05-03 to current framework state).

A completed example of a moderate-complexity GOSTA session: 3 domain models + 1 scoped specialist agent (UX-1, scoped to activation-distance concerns), four-agent deliberation, and a phased two-quarter roadmap. Demonstrates how multi-agent deliberation surfaces cross-domain tensions that single-perspective analysis misses.

## Reproducibility Notes

A user re-executing this session today against current framework state will produce artifacts with the same conceptual structure but several visible differences from what this example shows:

**Bootstrap-time differences:**
- Group 1 of `cowork/startup.md` asks 10 questions, including 4 flags not in this session's original execution: shortfall logging, assessment target, debug logging, evidence collection mode. For a feature-prioritization scope, all four typically answer "no/none."
- Group 2A may fire the AFC derivation — feature prioritization sits at the analytical/operational borderline. Current `cowork/startup.md` Group 2A heuristic would likely classify this as operational and skip the AFC. If the heuristic fires AFC derivation, the bootstrapper presents Stance/Output Verb/Failure Mode/Prohibited Frame for Governor confirmation.
- Group 3A (Deliberation Configuration) fires because this session uses deliberation. The Governor would specify topology, max rounds, convergence definition, sub-coordinator structure.
- Pre-Flight Validation Gates V1–V9 appear in bootstrap output. V8 fires if subagent dispatch declared (likely yes for code-mode deliberation); V9 SKIP if no inheritance.

**Deliberation-time differences:**
- Position papers would use **formula-based per-deliverable caps** (`base=4kb + 1.0kb × evidence_items_assigned`) per Plans #17 and #20, instead of the fixed cap this example used. Sessions using formula caps must include `evidence_items_assigned: <count>` in YAML front matter for the M3 hook to resolve correctly.
- Round 2+ may invoke **sub-coordinator re-engagement** per Plan #24 if deliberation grows to cluster-then-synthesize topology with 3+ agents in any cluster.
- Round 3+ termination is now **verdict-split-aware** per Plan #13: if any intra-cluster verdict-band split exceeding the convergence threshold remains open, deliberation cannot terminate without targeted re-dispatch OR Governor override carrying the split with `[VERDICT-SPLIT-CARRIED]` annotation. Original execution predates this discipline.

**Synthesis report differences:**
- Synthesis report would include `## Frame Integrity Validation` section if AFC declared (Plan #19 scope extension).
- Each verdict in synthesis report carries **Verdict Strength Annotation** `[cluster-confirmation: N, tier-floor: T<X>]` per Plan #8.
- If coverage came in below the session's threshold, synthesis report would include `## Coverage Limitations Disclosure` section per Plan #7.

**Deliverable-time differences:**
- Deliverables (`scored-feature-matrix.md`, `phased-roadmap.md`) would include `## Frame Integrity Validation` section if AFC declared. M4 hook fires WARN on deliverables without it (when AFC is in scope).
- If deliverables make Party-X-reception claims (e.g., "users will adopt X"), an **Evidence Channel Disclosure** would declare which channels (analyst-consumed / empirically-validated / AI-domain-agent reasoning) supported the claim per Plan #11'.
- Verdict Strength Annotations propagate from synthesis report to deliverable verdicts.

**Hooks (when installed at `.claude/settings.local.json`):**
- M1 fires PreToolUse Task — verifies signal stub before agent dispatch.
- M3 fires PostToolUse Write|Edit — checks per-deliverable cap. Resolves formula caps if YAML front matter has `evidence_items_assigned`.
- M4 fires PostToolUse Write|Edit on deliverable / synthesis-report / phase-gate files — checks AFC section presence.
- M5 reports hook-availability at bootstrap.
- log-dispatch + audit-closeout fire on Task lifecycle events.

**What's the same:**
- Conceptual structure of multi-agent deliberation (independent positions → tensions → synthesis → Governor decisions)
- 6-component domain model structure
- Cross-domain tension surfacing as the deliberation's value
- Convergence Probe protocol on unanimous Round 1 results
- 5-step graduated fallback for agent failures

For a fully current-state example, see [`my-first-session/`](../my-first-session/) (refreshed 2026-05-03; simpler scope, no deliberation, no AFC, but demonstrates current Per-Deliverable Caps, Validation Manifest, Hooks reference, U1 reviewer reference).

## What This Session Does

Prioritizes 12 candidate features for an EU developer tools SaaS product across Q2–Q3 2026. Four domain agents — market fit, technical feasibility, regulatory compliance, and UX/activation — independently score each feature, then deliberate to resolve conflicts. The Governor reviews the synthesis, applies guardrails (capacity budget, compliance prerequisites, activation distance), and commits a phased roadmap.

## Structure

```
00-BOOTSTRAP.md                ← Session orientation — start here
operating-document.md          ← Goal, guardrails (G-1 through G-6), objectives, strategies
01-scope-definition.md         ← Initial scope negotiation

domain-models/
  market-fit.md                ← Market demand, competitive positioning, segment analysis
  technical-feasibility.md     ← Engineering effort, dependencies, tech debt multipliers
  regulatory-compliance.md     ← EU regulatory requirements (AI Act, GDPR, NIS2)

deliberation/DELIB-001/
  position-MKT-1.md            ← Market agent's independent assessment
  position-TECH-1.md           ← Technical agent's independent assessment
  position-REG-1.md            ← Regulatory agent's independent assessment
  position-UX-1.md             ← UX/activation agent's independent assessment
  interim-assessment-R1.md     ← Round 1 interim synthesis
  synthesis-report.md          ← Final synthesis after two rounds
  verification.md              ← Deliberation quality verification

health-reports/HR-001.md       ← Session health assessment
decisions/DEC-001.md           ← Governor's final decision
deliverables/
  scored-feature-matrix.md     ← Cross-domain feature scores with verdicts
  phased-roadmap.md            ← Two-quarter implementation sequence
```

## How to Read This Example

Start with `00-BOOTSTRAP.md` for orientation. Then read the operating document to understand the goal and guardrails. The most instructive part is the deliberation: read the four position papers (`position-*.md`) to see how each agent independently scores the same features, then read the synthesis to see how tensions were resolved. Finish with the deliverables to see the output.

This example is a snapshot of a completed session, not a template to execute. To run your own feature prioritization, start a GOSTA session with `Read cowork/startup.md and start a new session.` and adapt the domain models for your context.

## What to Notice

- **Cross-domain tensions change the ranking.** Features that score well in one domain may rank poorly overall once regulatory prerequisites and tech debt multipliers are applied. The synthesis report documents which tensions shifted rankings and why.
- **The UX agent was added mid-session** (OD v2, G-5 added by Governor). GOSTA sessions can evolve — domain models and agents can be added when the Governor identifies analytical gaps.
- **Guardrail G-1 (compliance prerequisites)** prevents sequencing features before their regulatory dependencies are met, regardless of market demand score. This is a structural constraint, not a tie-breaker.
- **Every verdict traces to specific domain model concepts.** The scored feature matrix cites which concepts from which domains drove each score.

## Related

- [All Examples](../) — examples index
- [My First Session](../my-first-session/) — simpler version (2 domains, no deliberation)
- [Vendor-Product Continuity Assessment](../vendor-product-continuity-assessment/) — complex session (8 domains, evidence collection, six-signal framework)
- [GOSTA Walkthrough](../../walkthrough.md) — step-by-step guide to running your own session
