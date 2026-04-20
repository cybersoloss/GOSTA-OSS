# Level 4 — Full GOSTA Multi-Domain Deliberation

**Method:** 8 domain models + evidence collection from reference pool + 8-agent deliberation (4 rounds) + Governor governance with operating document, guardrails, independence level 2, and kill conditions.
**Prompt (Operating Document goal):** "Produce a multi-domain continuity risk assessment for [Target Vendor]'s [Target Product] that separates vendor-level from product-level risk, surfaces cross-domain tensions, and determines material risk exposure with traceable evidence chains."
**Agents:** FIN-1 (SaaS Financial Health), MKT-1 (Market & Competitive Dynamics), PROD-1 (Product Viability), OPS-1 (Operational Dependency & Stickiness), DISP-1 (Displacement & Migration), REG-1 (Regulatory & Compliance), GOV-1 (Vendor Governance & Transparency), TAL-1 (Talent & Workforce). Coordinator: COORD-1.

---

## Executive Summary

**Risk Level: MATERIAL EXPOSURE**

[Target Product] occupies the critical quadrant of the stickiness-viability matrix: high operational stickiness (7.8/10) combined with declining product viability (4.2/10) and a displacement timeline exceeding 12 months. [Target Vendor]'s financial position (5.1/10) masks near-term product risk — the vendor is stable enough to continue operating but under sufficient pressure to deprioritize [Target Product] relative to higher-growth product lines.

The deliberation surfaced a key structural finding: **stickiness is masking viability risk.** Because [Target Product] is deeply embedded and operationally functional today, internal stakeholders perceive low risk. The financial and market indicators suggest a 18–30 month window before product degradation becomes operationally visible — but the displacement timeline is 12–15 months, leaving a narrow margin for planned migration if viability continues to decline.

**Confidence: MODERATE** (5 of 8 agents converged on MATERIAL EXPOSURE; 2 rated ELEVATED RISK; 1 rated MANAGEABLE RISK with conditions. See unresolved tensions VT-01 and VT-02.)

---

## Score Matrix

| Agent | Domain | Vendor Score | Product Score | Verdict |
|-------|--------|-------------|---------------|---------|
| FIN-1 | SaaS Financial Health | 5.1 | — | ELEVATED |
| MKT-1 | Market & Competitive | 4.8 | 4.5 | MATERIAL |
| PROD-1 | Product Viability | — | 4.2 | MATERIAL |
| OPS-1 | Stickiness & Dependency | — | 7.8 (stickiness) | MATERIAL |
| DISP-1 | Displacement & Migration | — | 6.9 (difficulty) | ELEVATED |
| REG-1 | Regulatory & Compliance | 6.2 | 5.5 | ELEVATED |
| GOV-1 | Governance & Transparency | 4.4 | 3.8 | MATERIAL |
| TAL-1 | Talent & Workforce | 3.9 | 3.5 | MATERIAL |

**Consensus Vendor Score: 5.1/10** (confidence: moderate — FIN-1 and MKT-1 disagreed on revenue trajectory interpretation, resolved Round 3)
**Consensus Product Score: 4.2/10** (confidence: high — 7 of 8 agents within 0.8 points after Round 3)
**Stickiness Score: 7.8/10** (confidence: high — OPS-1 methodology unchallenged)
**Displacement Timeline: 12–15 months** (confidence: moderate — DISP-1 estimate contested by OPS-1, see VT-02)

---

## Vendor-Level Agreed Findings

**VF-01: Financial pressure is real but not acute.**
[Target Vendor]'s Rule of 40 score has declined from [X] to [X] over three reporting periods. NRR remains above 100% but trending downward. Burn multiple is within acceptable range. The [FAILURE-TRAJECTORY] flag is not triggered, but the trajectory toward the flag threshold is measurable.
*Attribution chain: FIN-1 (Round 1 position) → MKT-1 challenge (Round 2: revenue growth declining faster than margin improving) → FIN-1 revised assessment (Round 3: acknowledged trajectory concern, maintained non-flag status) → Counter-factual test: "What if NRR drops below 100% next quarter?" — FIN-1 and MKT-1 agree this triggers the flag and moves vendor score to 3.8.*

**VF-02: Market share loss is structural, not cyclical.**
[Target Vendor] is losing share in [Target Product]'s segment to competitors with [specific competitive advantage]. MKT-1's analysis distinguishes cyclical share fluctuation from structural displacement. Three indicators suggest structural: (a) new customer acquisition rate declining while existing customer expansion stalls, (b) competitive wins concentrated in a specific buyer segment that was previously [Target Vendor]'s core, (c) analyst positioning moved from "Leader" to "Challenger" or equivalent.
*Attribution chain: MKT-1 (Round 1) → PROD-1 challenge (Round 2: market share loss could reflect segment contraction, not vendor weakness) → MKT-1 rebuttal with evidence (Round 2: segment is growing, vendor share is shrinking) → PROD-1 conceded (Round 3).*

**VF-03: Governance opacity correlates with product deprioritization.**
[Target Vendor]'s roadmap visibility for [Target Product] has decreased: public roadmap updates are less frequent, customer advisory board meetings for this product line have been reduced, and engineering leadership for the product has turned over. GOV-1 identifies this pattern as consistent with internal deprioritization.
*Attribution chain: GOV-1 (Round 1) → FIN-1 supporting evidence (Round 2: R&D allocation shift visible in financial disclosures) → PROD-1 corroboration (Round 2: release cadence decline aligns with governance signals) → 3-agent convergence (Round 3).*

**VF-04: Regulatory compliance posture is currently adequate but maintenance-dependent.**
[Target Vendor] holds relevant compliance certifications. REG-1 assesses that current certifications are valid but renewal depends on continued investment. If [Target Product] is deprioritized (VF-03), compliance maintenance for this specific product may lag.
*Attribution chain: REG-1 (Round 1) → GOV-1 linkage (Round 2: deprioritization pattern predicts compliance investment decline) → REG-1 conditional assessment (Round 3: "adequate if maintained, at risk if VF-03 trajectory continues").*

**VF-05: Talent signals are a leading indicator of product deprioritization.**
TAL-1 identifies engineering attrition in [Target Product] teams exceeding vendor-wide attrition by a significant margin, with key personnel departures clustering in recent quarters. This pattern historically precedes measurable product quality decline by 6–12 months. TAL-1's workforce capacity trajectory analysis shows hiring velocity for [Target Product] teams declining while overall vendor headcount grows — consistent with internal resource reallocation away from this product line.
*Attribution chain: TAL-1 (Round 1 position) → GOV-1 corroboration (Round 2: talent signals align with governance opacity pattern from VF-03) → FIN-1 supporting evidence (Round 2: R&D reallocation visible in segment-level disclosures) → 3-agent convergence (Round 3). TAL-1's talent trajectory preceded GOV-1's governance signals by approximately two quarters, establishing talent as the earliest observable indicator of deprioritization.*

---

## Unresolved Tensions

**VT-01: Financial stability vs. product trajectory — divergent time horizons.**
FIN-1 rates vendor risk as ELEVATED (not MATERIAL) because financial indicators show 18–24 months of operational runway. PROD-1 and MKT-1 rate product risk as MATERIAL because product-level decline is already measurable. The tension: vendor-level stability can coexist with product-level decline for an extended period, but the stickiness score means the organization is exposed to the product trajectory, not the vendor trajectory.
*Round 4 resolution attempt: FIN-1 acknowledged that vendor stability does not protect against product deprioritization (VF-03 linkage). Tension remains because FIN-1's scoring framework weights vendor solvency, while OPS-1's framework weights product functionality — both are legitimate but produce different risk determinations. Governor adjudication recommended.*

**VT-02: Displacement timeline estimate — OPS-1 vs. DISP-1 disagreement.**
DISP-1 estimates 12–15 months for full displacement based on migration complexity analysis. OPS-1 argues the estimate is optimistic because it does not account for organizational change management, parallel-run resource requirements, and the informal workflows built around [Target Product] that are not captured in integration audits. OPS-1's revised estimate: 15–21 months.
*Round 4 resolution attempt: Counter-factual tested — "What if displacement takes 21 months instead of 15?" Impact: the migration window narrows from comfortable (start now, complete before projected viability degradation) to critical (migration overlaps with period of expected product quality decline). Governor adjudication recommended with pilot migration data.*

---

## Product-Level Findings

**PF-01: Stickiness is masking viability risk — the central finding.**
OPS-1's stickiness analysis (7.8/10) reveals deep operational embedding: [X] integration points, [X]% daily active user penetration, [X] TB of data with limited export fidelity. This embedding creates a perception of stability ("it works, so it's fine") that masks the viability trajectory identified by PROD-1, MKT-1, and GOV-1. The stickiness-viability combination places [Target Product] in the CRITICAL quadrant.
*This finding emerged from deliberation. In Round 1, OPS-1 initially rated overall risk as MANAGEABLE because the product is operationally functional. PROD-1's Round 2 challenge ("operational functionality today does not predict functionality in 18 months given the viability trajectory") forced OPS-1 to revise its overall assessment in Round 3 while maintaining its stickiness score. The revision — "high stickiness with declining viability is worse than low stickiness with declining viability" — is the insight that single-perspective analysis misses.*

**PF-02: Regulatory moat creates displacement friction independent of product quality.**
REG-1 identifies that [Target Product] holds compliance certifications that are difficult to replicate (sector-specific or jurisdiction-specific). Any replacement product must achieve equivalent certifications before migration can complete. This adds 3–6 months to displacement timelines beyond the technical migration estimate.
*Attribution chain: REG-1 (Round 2, in response to DISP-1's timeline) → DISP-1 revised estimate (Round 3: incorporated compliance re-certification into timeline) → OPS-1 amplification (Round 3: regulatory friction compounds organizational change management friction from VT-02).*

---

## Risk Mitigation Recommendations

**RM-01: Establish viability monitoring cadence (immediate).**
Implement quarterly viability reviews using PROD-1 and GOV-1 indicators: release cadence, roadmap visibility, engineering leadership stability, and NRR trend. Define trigger thresholds that initiate migration planning. *Grounded in: VF-03 (governance opacity), VF-01 (financial trajectory), PROD-1 viability framework.*

**RM-02: Conduct displacement pilot (within 90 days).**
Migrate a non-critical workflow to the leading alternative to validate DISP-1's 12–15 month estimate and OPS-1's concerns about informal workflow dependencies (VT-02). Pilot data resolves the displacement timeline tension with evidence rather than competing estimates. *Grounded in: VT-02 (timeline disagreement), PF-01 (stickiness masking risk), DISP-1 migration model.*

**RM-03: Negotiate contractual protections tied to viability indicators (next renewal).**
At the next contract renewal, negotiate provisions triggered by measurable viability indicators: source code escrow activation if [FAILURE-TRAJECTORY] flag triggers, data portability SLA with defined export formats and completeness guarantees, and termination assistance obligations with timeline commitments. *Grounded in: VF-01 (financial trajectory), VF-04 (compliance maintenance dependency), FIN-1 and REG-1 joint recommendation.*

**RM-04: Map and document informal workflows (within 60 days).**
OPS-1's analysis revealed that integration audits undercount actual dependency because informal workflows (manual processes, workarounds, team-specific configurations) are not captured in system-level assessments. Document these to refine the stickiness score and displacement timeline. *Grounded in: VT-02 (OPS-1 challenge to DISP-1 estimate), PF-01 (stickiness assessment).*

---

## What This Level Demonstrates

- **Multi-agent deliberation forces cross-domain tension surfacing.** VT-01 (financial stability vs. product trajectory) exists because FIN-1 and PROD-1 have legitimately different time horizons. A single analyst resolves this silently — the deliberation structure forces it onto the page with both perspectives and their evidence chains preserved.
- **Stickiness masking viability risk is the emergent finding.** No single domain model produces this insight. It emerges when OPS-1's stickiness analysis (product is deeply embedded and currently functional) collides with PROD-1's viability analysis (product is on a declining trajectory). OPS-1's Round 3 revision — "high stickiness with declining viability is worse, not better" — is the analytical insight that changes the risk determination. Level 3 placed [Target Product] on the matrix; Level 4 explained why the CRITICAL quadrant is worse than it appears.
- **Evidence grounding prevents speculation.** Every finding carries an attribution chain tracing it through rounds, challenges, and evidence. VF-02 (structural market share loss) was challenged by PROD-1 as potentially cyclical — MKT-1 defended with three specific indicators. This challenge-and-defend cycle produces higher-confidence conclusions than single-pass assertion.
- **Governance guardrails prevent frame drift.** The operating document defined the vendor/product separation, the stickiness-viability matrix as the combination framework, and the [FAILURE-TRAJECTORY] flag criteria before deliberation began. Agents operated within this frame rather than each inventing their own assessment structure.
- **Unresolved tensions are preserved, not hidden.** VT-01 and VT-02 are presented to the Governor with both positions intact rather than silently resolved. This is structurally impossible in single-pass analysis — a single analyst must choose one position. The deliberation preserves the disagreement as decision-relevant information.
- **Recommendations are grounded in multiple domains.** RM-02 (displacement pilot) addresses VT-02 (timeline disagreement) and PF-01 (stickiness assessment) simultaneously. RM-03 (contractual protections) bridges FIN-1 and REG-1 findings. Single-domain recommendations address one risk; multi-domain recommendations address risk interactions.
- **The stickiness-viability combination matrix produces risk determination that single-perspective analysis misses.** The MATERIAL EXPOSURE determination depends on the interaction of stickiness (OPS-1), viability (PROD-1), displacement timeline (DISP-1), and financial trajectory (FIN-1). Remove any one perspective and the determination changes — high stickiness alone is not alarming, declining viability alone is manageable, long displacement alone is plannable. The combination is what makes it material.
