# Level 2 — Extended Reasoning (Thinking Mode)

**Method:** Single prompt with extended reasoning / thinking mode enabled, no domain knowledge, no structure provided.
**Prompt:** "Assess whether [Target Vendor]'s [Target Product] represents a material third-party risk for our organization."

---

## Output

### Third-Party Risk Assessment: [Target Vendor] — [Target Product]

#### Assessment Framework

Before evaluating individual risk areas, I need to establish what "material" means in this context. A third-party risk is material when disruption, degradation, or failure of the vendor relationship would impair a critical business function or trigger regulatory consequences that exceed the organization's stated risk appetite.

#### 1. Financial Viability (Vendor-Level)

[Target Vendor]'s financial trajectory determines the product's long-term availability. Key indicators: revenue growth vs. burn rate, customer concentration, funding runway (if private), and debt-to-equity ratio. **Reasoning chain:** Financial distress → reduced R&D investment → product stagnation → competitive alternatives emerge → customer migration pressure → further revenue decline. This is a compounding cycle — early financial signals predict product-level consequences 12–18 months later.

**Preliminary score: Cannot assess without data.** Flag for evidence collection.

#### 2. Product Viability (Product-Level)

Distinct from vendor health: a profitable vendor may deprecate a specific product line. Indicators: release cadence, roadmap visibility, feature parity with competitors, customer growth for this specific product. **Reasoning chain:** If [Target Product] represents <15% of [Target Vendor]'s revenue, it is a candidate for divestiture even if the vendor is healthy.

**Preliminary score: Cannot assess without data.**

#### 3. Operational Dependency Depth

How deeply is [Target Product] embedded? Consider: number of business processes dependent on it, data volumes stored within it, integration points with other systems, and whether the product sits in the critical path of revenue-generating workflows. **Reasoning chain:** Operational dependency amplifies all other risks — a product with low dependency and high replaceability has low materiality regardless of vendor financial health.

#### 4. Displacement Feasibility

If [Target Product] became unavailable, what would replacement look like? Key factors: migration complexity, data portability, availability of functionally equivalent alternatives, and time-to-replacement. **Reasoning chain:** Displacement feasibility determines the severity function — high dependency with easy replacement is lower risk than moderate dependency with no viable alternatives.

**Connection to (3):** Dependency depth and displacement feasibility together define the "lock-in envelope." High dependency + difficult displacement = material risk even from a financially stable vendor.

#### 5. Regulatory Exposure

Does [Target Product] process, store, or transmit data subject to regulatory requirements? If the vendor fails to maintain compliance certifications, does your organization inherit regulatory liability? **Reasoning chain:** Regulatory risk compounds operational risk — a vendor compliance failure may require immediate migration under regulatory pressure, collapsing the displacement timeline from planned (months) to forced (weeks).

#### Risk Compounding Sequence

These risks are not independent. The compounding sequence is:
1. **Financial distress** (leading indicator, 12–18 month horizon)
2. **Product investment decline** (lagging indicator of financial distress)
3. **Operational disruption** (consequence of product degradation)
4. **Forced displacement** (triggered when disruption exceeds tolerance)
5. **Regulatory exposure** (amplifier that compresses timelines)

**Overall Assessment:** Material risk determination requires evidence for items 1–5. The compounding sequence suggests that financial viability is the highest-priority data point because it is the leading indicator.

---

## What This Level Demonstrates

- **Reasoning chains improve structure.** The thinking mode produces causal sequences ("financial distress leads to reduced R&D leads to product stagnation") rather than flat lists. This is a genuine improvement over Level 1.
- **Cross-category connections emerge.** The output links operational dependency to displacement feasibility and identifies regulatory exposure as a timeline compressor. These connections are absent in Level 1.
- **Vendor vs. product distinction begins to appear.** The output separates vendor financial health (1) from product viability (2) and notes they can diverge. This is a real analytical improvement.
- **Preliminary scoring is attempted but ungrounded.** The output recognizes it cannot score without data and flags items for evidence collection. This is honest but does not operationalize what data or what thresholds would be sufficient.
- **Still uses generic categories.** The five areas are standard TPRM categories, not informed by domain-specific frameworks. What counts as "financial distress" for a SaaS vendor is different from a hardware supplier — the analysis does not distinguish.
- **No domain-specific failure thresholds.** The output mentions "burn rate" and "revenue growth" but does not specify what ratios signal danger (e.g., Rule of 40, net revenue retention below 100%). Without domain-anchored thresholds, the reasoning chains describe plausible stories rather than testable conditions.
- **Cannot distinguish vendor-level from product-level risk with precision.** The separation is noted but not operationalized — there is no framework for scoring vendor health and product health independently and then combining them.
- **No forced disagreement.** A single reasoning thread resolves tensions before they reach the page. The "compounding sequence" looks insightful but was never challenged by an alternative sequencing argument.
