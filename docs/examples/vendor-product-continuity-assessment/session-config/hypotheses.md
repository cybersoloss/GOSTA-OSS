# Session Hypotheses: Vendor-Product Continuity Assessment

These hypotheses test Talk-2's core claims when applied to a specific vendor. Each hypothesis maps to one or more of the six signals and is testable within the session through evidence collection and deliberation.

---

## H-1: Revenue Model Exposure Under AI Automation (Signal 1)

**Hypothesis:** [Target Vendor]'s revenue model is structurally exposed if its core pricing is per-seat for capabilities that AI foundation model providers can now automate at near-zero marginal cost. Vendors still dependent on seat-based revenue for commoditizing capabilities face structural margin pressure — IDC forecasts 70% of software vendors will refactor away from pure per-seat pricing by 2028.

**Test:** Does evidence show [Target Vendor] pricing per-seat for capabilities where AI alternatives exist or are shipping? Does the SAAS-1 + ECON-1 assessment identify pricing model vulnerability? If the vendor has shifted to outcome-based or platform pricing, the hypothesis is falsified for this vendor.

**Signals:** 1 (Revenue model exposure)
**Domains:** SAAS-1, ECON-1

---

## H-2: Data Moat as Displacement Discriminator (Signal 2)

**Hypothesis:** [Target Product]'s defensibility against AI displacement depends primarily on whether it operates on customer-specific operational data or publicly available knowledge. Products built on public knowledge (common vulnerability databases, standard compliance frameworks, general threat intelligence) face direct substitution risk from foundation model providers who can replicate the analytical capability without customer environment access. Products operating on the customer's own data (contracts, configurations, internal processes) retain a structural moat.

**Test:** Classify [Target Product] on the data moat spectrum. If the product primarily operates on public knowledge, does evidence show foundation model providers shipping competing capabilities? If it operates on customer-specific data, is the vendor deepening its integration into customer workflows (extending the moat) or standing still (allowing erosion)?

**Signals:** 2 (Domain depth vs. feature breadth)
**Domains:** DISP-1

---

## H-3: Consolidation Positioning Determines Survival Trajectory (Signal 3)

**Hypothesis:** In a market with $76-96B in cybersecurity M&A in 2025 alone, [Target Vendor]'s position as a consolidation winner (platform, acquirer) or consolidation target (point solution, acquisition candidate) is the strongest predictor of 2-5 year survival trajectory. Point solutions without platform positioning face the most acute viability risk — not because they fail immediately, but because capital concentration toward platforms starves them of growth capital and acquisition premium.

**Test:** Does evidence show [Target Vendor] positioned as a platform or a point solution? Is funding concentrating toward or away from their category? Does the ECON-1 assessment of consolidation positioning align with or contradict the DISP-1 assessment of competitive pressure?

**Signals:** 3 (Financial sustainability and consolidation)
**Domains:** ECON-1, DISP-1

---

## H-4: Stickiness-Viability Maximum Risk Combination (Signal 6)

**Hypothesis:** High structural stickiness (deep integration, data gravity, workflow dependency) combined with declining viability is the maximum-risk scenario for the dependent organization. Stickiness creates a false sense of security — the organization interprets high switching costs as evidence that [Target Vendor] "cannot be replaced" and therefore "must be fine," when stickiness and viability are independent dimensions. Standard enterprise migrations take 3-6 months; complex integrations take 12+ months. 61% exceed planned timelines by 40-100%.

**Test:** Score stickiness and viability independently using STICK-1 and ECON-1 + DISP-1. Does the stickiness-viability combination matrix place [Target Vendor] / [Target Product] in the maximum-risk quadrant (high stickiness + low viability)? Does Agent C (Dependency Exposure) challenge any instance where stickiness is cited as evidence of vendor stability?

**Signals:** 6 (Vendor stickiness vs. viability)
**Domains:** STICK-1, ECON-1, DISP-1

---

## H-5: Regulatory Moat — Protection Floor with Erosion Conditions (Signals 4-5)

**Hypothesis:** Regulatory demand for [Target Product]'s category creates a viability floor — [Target Vendor] has a minimum sustainable revenue base as long as the regulatory requirement exists. DORA Article 28 requires exit strategies for critical ICT third-party service providers. NIS2 Article 21(2)(d) requires supply chain security assessment. However, regulatory embedding is a double-edged sword: it protects vendor demand but amplifies exit costs for the dependent organization. If the vendor fails, the organization's regulatory compliance is disrupted — the vendor's failure becomes a compliance event, not just an operational one.

**Test:** How deeply is [Target Product] embedded in the dependent organization's regulatory workflows? Does the contract include DORA Article 28-compliant exit provisions? Has the organization tested whether data portability actually works? Does the REG-1 assessment identify both the viability floor and the erosion conditions?

**Signals:** 4 (Exit strategy provisions), 5 (Regulatory embedding depth)
**Domains:** REG-1, STICK-1

---

## H-6: Talent Trajectory as Viability Leading Indicator

**Hypothesis:** Talent departures and workforce capacity decline precede financial metric deterioration by 2-4 quarters. A vendor with stable financials but deteriorating talent trajectory (key personnel departures, engineering hiring freeze, shift to maintenance hiring) is on a declining path that financial metrics will eventually confirm. Key engineering and security staff leaving is an early indicator of service quality degradation before it shows up in the product.

**Test:** If TAL-1 and ECON-1 assessments diverge (ECON-1 shows stable financials but TAL-1 shows declining talent trajectory), the divergence itself is the finding — it predicts future financial deterioration. If both align (both stable or both declining), the leading indicator confirms rather than contradicts.

**Signals:** Leading indicator (supports all signals)
**Domains:** TAL-1, ECON-1

---

## H-7: Governance Quality as Strategic Early Warning

**Hypothesis:** Leadership instability (executive turnover, strategic pivots, organizational restructuring) at [Target Vendor] predicts operational deterioration 12-18 months before financial metrics show it. Governance and talent together form the organizational health picture that either confirms or contradicts the business model and competitive assessments from Signals 1-3.

**Test:** Does the GOV-1 assessment identify governance signals that contradict or temper the six-signal assessment? When GOV-1 and TAL-1 diverge (governance projects stability while talent signals decline, or vice versa), which signal is the more reliable predictor?

**Signals:** Leading indicator (supports all signals)
**Domains:** GOV-1, TAL-1

---

## H-8: Adaptation Capacity Under Financial Pressure

**Hypothesis:** When [Target Vendor] is under financial stress (declining revenue, margin compression, capital constraints), R&D investment is cut disproportionately relative to other cost centers, reducing adaptation capacity faster than financial metrics alone would suggest. This means product viability deteriorates before vendor viability does — the vendor survives by cutting the product's future.

**Test:** Does evidence show R&D investment ratio declining faster than revenue? Does the ADAPT-1 product-level score diverge from the ECON-1 vendor-level score? If the vendor is cutting R&D while maintaining revenue, the hypothesis is supported.

**Signals:** Supports Signals 1-3 (business model viability)
**Domains:** ADAPT-1, ECON-1
