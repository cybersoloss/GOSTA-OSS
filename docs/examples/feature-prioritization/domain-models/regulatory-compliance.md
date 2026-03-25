# Domain Model: Regulatory Compliance (EU SaaS)

**Source:** Domain expertise — synthesized from GDPR enforcement patterns (2018–2026), EU AI Act requirements (Regulation 2024/1689), and NIS2 Directive obligations for SaaS providers
**Application Context:** Evaluating regulatory risk and compliance requirements for features serving EU enterprise customers
**Created:** 2026-03-25
**Purpose:** Grounds AI agent reasoning in regulatory reality when scoring features — prevents market and technical domains from deprioritizing compliance requirements that carry enforcement risk

---

## 1. Core Concepts

### Enforcement Probability Gradient

Not all regulatory requirements carry equal enforcement risk. GDPR's data subject access rights are actively enforced with €multi-million fines. NIS2's incident reporting obligations have specific deadlines with defined penalties. The EU AI Act's requirements phase in between August 2025 and August 2027 with enforcement varying by risk classification. Features should be scored against the enforcement probability of the specific requirement they address, not against "regulatory compliance" as a generic category.

**Boundary:** Enforcement probability covers the likelihood of regulatory action for non-compliance. It does NOT cover contractual compliance (customer DPA requirements, SOC 2 audit expectations), which are business obligations with different consequences.

**Common misapplication:** Treating all GDPR requirements as equally urgent. Article 17 (right to erasure) is actively enforced; Article 20 (data portability) has seen minimal enforcement action. Prioritizing both equally wastes resources.

### Data Flow Sovereignty

Where user data is processed, stored, and transmitted determines which regulations apply. EU data residency requirements mean that a feature processing EU personal data on US infrastructure may be non-compliant regardless of its functionality. Data flow sovereignty must be assessed per-feature, not per-product — a single feature that routes data through a non-compliant jurisdiction can create liability for the entire product.

**Boundary:** Data flow sovereignty covers the geographic and jurisdictional path of personal data. It does NOT cover data classification, retention, or access controls, which are separate compliance domains.

### Compliance Prerequisite Chain

Some features cannot be compliant without other capabilities existing first. You cannot offer GDPR-compliant analytics without a lawful basis mechanism. You cannot offer AI Act-compliant model outputs without a transparency layer. Compliance prerequisites create hard dependencies that override market-driven sequencing — if the prerequisite isn't built, the feature is unlawful regardless of customer demand.

**Boundary:** Compliance prerequisite chains cover regulatory dependencies. They do NOT cover technical dependencies (those belong in the technical feasibility domain). A feature can be technically buildable but legally unshippable.

### Regulatory Change Velocity

The EU regulatory landscape for SaaS is in a high-velocity period (2024–2027): AI Act enforcement phasing, NIS2 implementation, Data Act adoption, eIDAS 2.0 rollout. Features built for today's regulatory state may need modification within 12–18 months. Features should be assessed for regulatory durability — will this implementation still be compliant in 18 months, or does it encode assumptions that known regulatory changes will invalidate?

**Boundary:** Regulatory change velocity covers formal legislative and regulatory changes. It does NOT cover industry standard evolution (SOC 2 criteria updates, ISO certification changes), which are voluntary.

---

## 2. Concept Relationships

**Prerequisites:** Data Flow Sovereignty must be mapped before Enforcement Probability Gradient can be accurately assessed — the applicable regulations depend on where data flows. Compliance Prerequisite Chains must be mapped before feature sequencing is valid — a feature sequenced before its compliance prerequisite is unshippable on delivery.

**Tensions:** Enforcement Probability Gradient (prioritize highest-risk requirements) creates tension with market-domain priorities — the highest enforcement risk may not be the highest market opportunity. Regulatory Change Velocity creates tension with technical domain's desire for architectural stability — building for regulatory durability may require more flexible (more complex) architectures. Data Flow Sovereignty requirements create tension with technical scalability — data residency constraints limit infrastructure optimization options.

**Amplifiers:** Compliance Prerequisite Chains amplify Enforcement Probability — a feature that is both high-enforcement-risk AND missing its compliance prerequisite is doubly urgent. High Regulatory Change Velocity amplifies the value of Reversibility (from the technical domain) — in fast-changing regulatory environments, features that can be modified cheaply are strategically superior.

---

## 3. Quality Principles

- **QP-1:** Regulatory risk claims must cite specific articles, sections, or recitals of the applicable regulation — not "GDPR compliance" as a category. Ungrounded regulatory claims are as dangerous as no assessment at all.
- **QP-2:** Enforcement probability assessments must reference actual enforcement actions (fines, orders, investigations) from the relevant DPA or authority. "This could be enforced" without evidence of actual enforcement patterns is speculative.
- **QP-3:** Data flow maps must trace the complete path of personal data for each feature — ingestion, processing, storage, transmission, deletion. Incomplete maps create hidden compliance gaps.
- **QP-4:** Regulatory change velocity assessments must cite specific upcoming regulations with effective dates. "The regulatory landscape is changing" without specifics is not actionable.

---

## 4. Anti-Patterns

- **AP-1:** Compliance theater — Implementing the visible aspects of compliance (privacy policy, cookie banner) without addressing the substantive requirements (data flow controls, access rights automation, deletion pipelines). Detect by checking whether compliance investments map to specific enforcement-risk requirements or to user-visible compliance signaling.
- **AP-2:** Regulation-by-panic — Deprioritizing all other work when a new regulation is announced, without assessing enforcement timeline or applicability. Creates whiplash in roadmap priorities. Detect by checking whether regulatory responses include an enforcement probability assessment or are pure urgency reactions.
- **AP-3:** Compliance isolation — Treating regulatory compliance as a separate workstream disconnected from feature development. This creates duplicate work and gaps. Detect by checking whether compliance requirements are integrated into feature specifications or maintained in a separate document that nobody reads.

---

## 5. Hypothesis Library

- **HL-1:** "If we ship the data residency feature (EU hosting) before July 2026, then we unblock 8 enterprise prospects worth €400K ARR currently blocked by data sovereignty requirements, because Data Flow Sovereignty predicts that these prospects cannot purchase without EU data residency guarantees."
- **HL-2:** "If we build the automated DSAR pipeline (data subject access request fulfillment under 30 days), then GDPR enforcement risk for our highest-probability requirement drops from HIGH to LOW, because Enforcement Probability Gradient shows DSAR non-compliance is the #1 enforcement trigger for SaaS providers in 2025–2026."
- **HL-3:** "If we implement the AI Act transparency layer before February 2027, then all AI-powered features remain shippable to EU customers, because Regulatory Change Velocity indicates Article 52 transparency obligations become enforceable on that date."

---

## 6. Guardrail Vocabulary

- **GV-1:** Compliance prerequisite enforcement — Severity: hard — No feature may be shipped to EU customers if its compliance prerequisite chain contains an unbuilt component. Market demand does not override legal requirements. Violation consequence: feature recall, potential regulatory notification.
- **GV-2:** Data sovereignty verification — Severity: hard — Every feature that processes personal data must have a verified data flow map showing all jurisdictions where data is processed or stored. Features without verified data flow maps are blocked from EU deployment.
- **GV-3:** Regulatory horizon scan — Severity: soft — Features with >12-month expected lifetime must include a regulatory durability assessment against known upcoming regulations. Features without this assessment may be approved but carry flagged regulatory change risk.
