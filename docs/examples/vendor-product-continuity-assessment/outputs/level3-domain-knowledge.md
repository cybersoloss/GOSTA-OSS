# Level 3 — Domain Model Grounding

**Method:** Single prompt + 8 domain model files loaded as context. No multi-agent deliberation, no evidence collection, no governance.
**Prompt:** "Assess whether [Target Vendor]'s [Target Product] represents a material third-party risk for our organization."
**Domain models loaded:** SaaS Financial Health, Product Viability Indicators, Operational Dependency & Stickiness, Displacement & Migration, Regulatory & Compliance Exposure, Market & Competitive Dynamics, Vendor Governance & Transparency, Talent & Workforce.

---

## Output

### Third-Party Continuity Risk Assessment: [Target Vendor] — [Target Product]

#### Scoring Framework

Each dimension scored 1–10 using domain-anchored thresholds. Vendor-level and product-level scores separated.

---

#### Vendor-Level Assessment

**V1. Financial Health — Score: [X]/10**
Applying SaaS Financial Health model: Rule of 40 status (revenue growth % + profit margin % ≥ 40), net revenue retention (NRR) relative to 120% benchmark, gross margin trajectory, and customer concentration (top-10 customers as % of ARR). **[FAILURE-TRAJECTORY] flag criteria:** NRR < 100% for two consecutive quarters, or Rule of 40 score declining >10 points year-over-year while burn multiple exceeds 2.0x.

**V2. Market & Competitive Position — Score: [X]/10**
Market segment growth rate vs. [Target Vendor]'s growth rate (share gain/loss). Competitive moat assessment: switching cost depth, network effects, data gravity, regulatory moat (compliance certifications that competitors lack). Analyst positioning trajectory (improving, stable, declining across major analyst firms).

**V3. Governance & Transparency — Score: [X]/10**
Incident disclosure history (proactive vs. reactive, time-to-disclosure). Roadmap visibility (public roadmap, customer advisory board, NDA-only). Financial transparency (public filings, SOC 2 Type II, independent audit availability). Executive stability (C-suite and VP-Engineering tenure, recent departures).

**V4. Talent & Workforce — Score: [X]/10**
Applying Talent & Workforce model: key personnel stability (VP-Engineering and product leadership tenure, departure clustering), engineering retention rate relative to industry benchmarks, and workforce capacity trajectory (hiring velocity in [Target Product] teams vs. overall headcount growth). **[LEADING-INDICATOR] flag criteria:** engineering attrition >20% annualized in [Target Product] team, or key personnel departures clustered within two quarters, or workforce capacity declining while product roadmap commitments remain unchanged.

**Vendor Composite: [X]/10**

---

#### Product-Level Assessment

**P1. Product Viability — Score: [X]/10**
Release cadence (major releases/year, patch frequency). Feature velocity vs. competitive parity. Technical debt indicators: API versioning practices, deprecation policy, backward compatibility track record. **Product revenue share:** estimated % of [Target Vendor]'s total revenue. Products below 15% of vendor revenue are divestiture candidates regardless of vendor health.

**P2. Operational Dependency (Stickiness) — Score: [X]/10**
Using Operational Dependency & Stickiness model: integration depth (API calls/day, data volume, workflow criticality), user penetration (% of organization using [Target Product] daily), data lock-in (proprietary formats, export completeness, schema portability). **Stickiness score** = f(integration depth, user penetration, data lock-in). High stickiness amplifies all other risk dimensions.

**P3. Displacement Timeline — Score: [X]/10**
Using Displacement & Migration model: functionally equivalent alternatives available (count, maturity), estimated migration duration (months), migration cost as % of annual contract value, data migration completeness achievable (%). **Displacement timeline score** = calendar months to full operational replacement assuming parallel-run approach. Scores: <3 months = low risk, 3–9 months = moderate, 9–18 months = high, >18 months = critical.

**P4. Regulatory Exposure — Score: [X]/10**
Data classification level processed by [Target Product]. Regulatory regimes applicable (GDPR, NIS2, DORA, sector-specific). Vendor compliance certification coverage vs. your regulatory obligations. **Regulatory moat assessment:** does [Target Vendor]'s compliance posture create competitive advantage (hard to replicate certifications) or regulatory dependency (your compliance relies on their attestations)?

**Product Composite: [X]/10**

---

#### Stickiness-Viability Matrix

|                     | Product Viability HIGH | Product Viability LOW |
|---------------------|------------------------|----------------------|
| **Stickiness HIGH** | Monitor — stable but locked in | **CRITICAL** — high dependency on declining product |
| **Stickiness LOW**  | Comfortable — viable and replaceable | Manageable — declining but easy to exit |

**[Target Product] position:** [Quadrant placement based on P1 and P2 scores]

**Risk Determination:** The stickiness-viability matrix position, combined with the vendor composite and displacement timeline, determines the overall risk level:
- **MATERIAL EXPOSURE:** Stickiness HIGH + Viability LOW + Displacement >9 months
- **ELEVATED RISK:** Any two of (Stickiness HIGH, Viability LOW, Displacement >6 months)
- **MANAGEABLE RISK:** Stickiness LOW or (Viability HIGH + Displacement <6 months)
- **LOW RISK:** Stickiness LOW + Viability HIGH + Displacement <3 months

---

## What This Level Demonstrates

- **Domain models constrain and sharpen the analysis.** Instead of generic "financial health" advice, the output uses Rule of 40, NRR benchmarks, burn multiples, and talent retention indicators — domain-specific thresholds that distinguish SaaS vendor risk from general corporate risk.
- **[FAILURE-TRAJECTORY] flags operationalize "material."** The prompt asked about "material risk" but Level 1 and Level 2 never defined it. Domain models provide specific flag criteria (NRR < 100% for two consecutive quarters) that convert a vague question into testable conditions.
- **Vendor vs. product scores are separated.** The stickiness-viability matrix produces a 2x2 assessment that Level 1 and Level 2 cannot — a healthy vendor with a declining product is a different risk from a struggling vendor with a strong product.
- **Displacement timeline scoring adds time dimension.** Calendar-month estimates for replacement convert abstract "switching cost" into actionable planning data.
- **Stickiness-viability matrix produces risk determination.** The combination of stickiness and viability produces four distinct risk postures with different response strategies. Single-category analysis misses the interaction: high stickiness is not inherently bad (it is bad only when viability is low).
- **Still lacks forced cross-domain disagreement.** The financial health model and the market position model may imply different conclusions — a vendor losing market share but maintaining strong financials, or vice versa. A single analyst resolves this silently. No tension is surfaced or tested.
- **No evidence citation.** Scores are framework-ready but not grounded in specific evidence. The [X]/10 placeholders indicate where evidence would go but the analysis cannot fill them without a reference pool.
- **No governance guardrails.** Nothing prevents the analyst from overweighting one domain (e.g., strong financials masking product-level decline) or from resolving tensions in favor of the most comfortable conclusion.
- **No tension resolution mechanics.** When stickiness is high and displacement is long but financial health is strong, what is the net risk? The matrix provides quadrants but not the reasoning for edge cases where indicators conflict across domains.
