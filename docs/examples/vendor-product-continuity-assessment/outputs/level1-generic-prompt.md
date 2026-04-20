# Level 1 — Generic Prompt (Zero Context)

**Method:** Single prompt to any capable LLM, no domain knowledge, no structure, no scoring framework.
**Prompt:** "Assess whether [Target Vendor]'s [Target Product] represents a material third-party risk for our organization."

---

## Output

### Third-Party Risk Assessment: [Target Vendor] — [Target Product]

**1. Financial Health**
[Target Vendor]'s financial stability should be evaluated through publicly available indicators such as revenue trends, profitability, and funding status. A vendor experiencing financial distress may reduce investment in product development or fail to meet contractual obligations.

**2. Market Position**
Consider [Target Vendor]'s competitive positioning within its market segment. A strong market position generally indicates sustained investment in the product, while declining market share may signal future product deprecation or acquisition risk.

**3. Technology Risk**
Evaluate the technical architecture of [Target Product], including update frequency, integration capabilities, and dependency on proprietary standards. Products with infrequent updates or closed ecosystems present higher switching costs.

**4. Compliance and Regulatory**
Assess whether [Target Product] meets your organization's regulatory requirements (GDPR, SOC 2, ISO 27001, etc.). Verify that [Target Vendor] can provide evidence of compliance certifications relevant to your jurisdiction.

**5. Operational Dependency**
Determine how deeply [Target Product] is embedded in your workflows. High operational dependency combined with limited alternatives increases business continuity risk.

**6. Data Security**
Review [Target Vendor]'s data handling practices, encryption standards, incident response history, and breach notification procedures. Consider whether your data residency requirements are met.

**7. Contractual Protections**
Ensure contractual terms include SLA guarantees, data portability provisions, termination assistance, and liability caps appropriate to the level of dependency.

**8. Vendor Concentration**
If your organization relies on [Target Vendor] for multiple products or services, concentration risk multiplies. Consider the aggregate impact of a single vendor failure across all touchpoints.

**Recommendation:** Conduct a structured vendor risk assessment using an industry-standard framework and assign a risk rating based on the findings above.

---

## What This Level Demonstrates

- **Generic categories from training data.** The eight risk areas (financial, market, technology, compliance, operational, security, contractual, concentration) are pulled from general TPRM knowledge. They apply equally to any vendor in any industry — nothing is specific to [Target Vendor] or [Target Product].
- **No scoring framework.** No numeric scores, no thresholds, no definitions of what constitutes "material" risk. The word "material" from the prompt is not operationalized.
- **No evidence requirements.** Every statement is advisory ("should be evaluated," "consider," "review") without specifying what data sources, metrics, or evidence would ground the assessment.
- **No vendor/product distinction.** Vendor-level risk (financial health, market position) and product-level risk (technology architecture, operational dependency) are mixed without separation. A vendor can be stable while a specific product is being sunset — this analysis cannot surface that.
- **No analytical frame control.** The model chose its own categories, sequencing, and depth. A different model or a different day might produce a different set of categories with no way to compare.
- **No cross-domain tension detection.** Financial pressure might drive product changes that affect technology risk, which compounds operational dependency — these interactions are invisible in a flat list.
- **The output looks plausible but is context-agnostic.** A risk committee receiving this would learn nothing about [Target Vendor] or [Target Product] specifically. It is a template, not an assessment.
