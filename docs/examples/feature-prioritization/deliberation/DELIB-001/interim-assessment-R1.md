# Interim Assessment — Round 1
**Deliberation:** DELIB-001 | **Coordinator:** COORD-1 | **Date:** 2026-03-19
**Position Papers Received:** MKT-1, TECH-1, REG-1, UX-1

---

## Score Overview

| Feature | MKT-1 | TECH-1 | REG-1 | UX-1 | Range | Status |
|---------|-------|--------|-------|------|-------|--------|
| F-01: EU Data Residency | 9 | 3 | 10 | 1 | **9** | HARD DISAGREEMENT |
| F-02: Automated DSAR Pipeline | 5 | 5 | 9 | 1 | **8** | HARD DISAGREEMENT |
| F-03: In-App Templates | 8 | 9 | 1 | 10 | **9** | SOFT DISAGREEMENT |
| F-04: Slack Integration | 7 | 8 | 2 | 3 | **6** | SOFT DISAGREEMENT |
| F-05: AI Code Review | 6 | 5 | 8 | 4 | **4** | MODERATE SPREAD |
| F-06: RBAC | 7 | 4 | 4 | -2 | **9** | HARD DISAGREEMENT |
| F-07: Usage Analytics | 4 | 5 | 6 | 2 | **4** | CONVERGENT |
| F-08: AI Act Transparency | 3 | 7 | 9 | 0 | **9** | HARD DISAGREEMENT |
| F-09: Custom Workflows | 6 | 4 | 3 | -1 | **7** | HARD DISAGREEMENT |
| F-10: SSO/SAML | 7 | 4 | 5 | 5 | **3** | CONVERGENT |
| F-11: Bulk Data Export | 3 | 7 | 4 | 1 | **6** | SOFT DISAGREEMENT |
| F-12: Real-Time Collaboration | 8 | 2 | 3 | 7 | **6** | HARD DISAGREEMENT |

**Convergent (range ≤3):** F-07, F-10
**Soft Disagreement (range 4-6):** F-03, F-04, F-05, F-11, F-12
**Hard Disagreement (range ≥7):** F-01, F-02, F-06, F-08, F-09

## Agreements

1. **F-03 (In-App Templates) is high-priority across 3 of 4 domains.** MKT-1 (8), TECH-1 (9), UX-1 (10) all rank it highly. REG-1 scores it 1 (no regulatory dimension), which is a "not relevant" signal, not opposition. This feature has cross-domain consensus for priority.

2. **F-07 (Usage Analytics) and F-10 (SSO/SAML) show convergent scores** with moderate priority. Neither is a top priority in any domain, but none opposes them strongly. They are "solid middle" features.

3. **F-12 (Real-Time Collaboration) is desired by market and UX but technically infeasible in the near term.** MKT-1 (8) and UX-1 (7) want it; TECH-1 (2) says it's the highest-risk feature. This is not a disagreement about value — it's a feasibility constraint on a valued feature.

## Hard Disagreements

### HD-1: F-01 (EU Data Residency) — Market/Regulatory vs. Technical
- **MKT-1 (9) + REG-1 (10):** Strongest market signal (€400K ARR blocked) and highest regulatory urgency (compliance foundation for EU business). Both argue it is the single most important feature.
- **TECH-1 (3):** Infrastructure migration project, not an application feature. 12-16 FTE-weeks, low reversibility, cloud provider coordination risk. Technically the second-hardest feature after F-12.
- **Nature of disagreement:** Value vs. feasibility. All domains agree on its importance — the disagreement is whether it can be done within G-3 effort constraints alongside other priorities.
- **Resolution path:** This cannot be resolved by scoring — it requires a resource allocation decision. If F-01 consumes 12-16 FTE-weeks of the 24 FTE-week ceiling (G-3), it constrains everything else.

### HD-2: F-08 (AI Act Transparency) — Regulatory vs. Market
- **REG-1 (9):** Compliance prerequisite for F-05 and all future AI features. Regulatory deadline February 2027 creates hard scheduling constraint.
- **MKT-1 (3):** Zero customer demand. No revenue signal.
- **TECH-1 (7):** Technically straightforward (3-4 weeks, isolated module).
- **Nature of disagreement:** Direct conflict between market demand signal and regulatory obligation. This is exactly the tension the Compliance Prerequisite Chain concept (GV-1, hard guardrail) is designed to address.
- **Resolution path:** GV-1 enforces: F-08 MUST precede F-05 regardless of market priority. The question is whether to build F-08 at all if F-05 is deferred. REG-1 argues yes (regulatory durability for future AI features). MKT-1 argues defer both.

### HD-3: F-02 (Automated DSAR Pipeline) — Regulatory vs. Market/UX
- **REG-1 (9):** #1 GDPR enforcement trigger. €multi-million fine risk from systematic failures.
- **MKT-1 (5):** Low customer demand (customers assume compliance exists).
- **Nature of disagreement:** Invisible-to-customer compliance work vs. visible-to-customer features. REG-1 explicitly flags AP-1 (compliance theater): prioritizing visible features over substantive compliance infrastructure.
- **Resolution path:** Governor must weigh enforcement probability against opportunity cost. This is a risk management decision, not a scoring problem.

### HD-4: F-06 (RBAC) — Market vs. UX/Technical
- **MKT-1 (7):** Enterprise demand, expansion deals contingent on it.
- **UX-1 (-2):** INCREASES activation distance. Violates G-2 unless designed with zero-config defaults.
- **TECH-1 (4):** High-debt identity service, 12-18 effective weeks with multiplier.
- **Nature of disagreement:** Market demand for a feature that harms activation and is technically expensive. Three-way tension.
- **Resolution path:** If built, requires design constraints (UX-1) and pairs with F-10 to amortize identity refactor (TECH-1). Governor decision on whether enterprise demand justifies the cost + activation risk.

### HD-5: F-09 (Custom Workflows) — Market vs. UX/Technical/Regulatory
- **MKT-1 (6):** High switching cost asymmetry potential.
- **UX-1 (-1), TECH-1 (4), REG-1 (3):** Activation risk, large scope (workflow engine underestimation AP), minor regulatory concerns.
- **Nature of disagreement:** Long-term strategic value (switching cost) vs. short-term execution risk.
- **Resolution path:** Strong candidate for deferral to Q4 or later. No time pressure, no regulatory deadline, high execution risk.

## Soft Disagreements

### SD-1: F-03 (In-App Templates) — Priority Level
All non-regulatory domains rate highly, but the question is whether F-03 is Q2-priority or "must build but can sequence flexibly." Given TECH-1's score of 9 (most feasible feature) and UX-1's score of 10 (highest activation impact), this appears to be a low-risk, high-reward Q2 candidate. REG-1's score of 1 is domain-irrelevant, not opposition.

### SD-2: F-12 (Real-Time Collaboration) — Desire vs. Reality
Market (8) and UX (7) want it. Technical (2) says it's the hardest feature. This is a sequencing question: should we invest in a proof-of-concept in Q2 (TECH-1 suggests 2-3 week POC) to derisk a Q3 or Q4 full build?

## Novel Arguments Detected

1. **UX-1 raised G-2 violations** for F-06 and F-09 that no other agent identified. Activation distance regression is a hard guardrail and creates design constraints that affect effort estimates (TECH-1 should account for this).

2. **REG-1 argued F-01 is not one feature among twelve but a compliance foundation** for all EU features. This reframes the prioritization: F-01 is not competing with other features — it is enabling them. This structural argument changes the nature of the resource allocation decision.

3. **TECH-1 identified the F-06/F-10 pairing opportunity** — shared identity service refactor means building one without the other wastes investment. This is a sequencing constraint that should inform roadmap construction.

## Concept Distortion Check

No [CONCEPT-DISTORTED] flags. All agents applied domain model concepts consistently with their definitions. Specific checks:

- MKT-1's use of "Switching Cost Asymmetry" for F-09 (Custom Workflows) is consistent with the model's definition (outbound switching cost increases when customers build workflows). ✓
- TECH-1's use of "Technical Debt Load" with 1.5x multiplier for identity service is consistent with QP-1 (debt-load multiplier 1.5x-3x). ✓
- REG-1's use of "Enforcement Probability Gradient" distinguishing Art. 17 (active) from Art. 20 (minimal) enforcement is directly from the model's common misapplication warning. ✓
- UX-1's activation distance scores including negative values for features that increase distance is a legitimate interpretation — the model says features that increase activation distance should be flagged (GV-1 from market-fit model: no feature may increase activation distance without Governor approval). ✓

## Recommended Round 2 Prompts

Given the number and severity of disagreements, Round 2 should focus on the three hardest tensions:

1. **To TECH-1:** Given REG-1's argument that F-01 is a compliance foundation (not just one feature), assess: if F-01 is sequenced first, what is the realistic impact on the remaining G-3 budget, and which features become unfeasible?
2. **To MKT-1:** Given REG-1's enforcement probability data for F-02 (DSAR) and the compliance prerequisite chain for F-08→F-05, reassess whether your Tier 3/4 placement of F-02 and F-08 accounts for the risk of regulatory enforcement vs. the opportunity cost of market features.
3. **To UX-1:** Given TECH-1's assessment that F-12 is 16-24 FTE-weeks, assess whether the team activation path (2-step) justifies a proof-of-concept investment in Q2, or whether F-03 alone provides sufficient activation improvement for both quarters.

Coordinator recommends proceeding to synthesis after Round 2 responses, as the disagreements are structural (value vs. feasibility, market vs. regulatory) and additional rounds are unlikely to produce convergence — these are Governor decisions.
