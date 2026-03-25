# Position Paper: REG-1 (Regulatory Compliance)
**Deliberation:** DELIB-001 | **Round:** 1 | **Date:** 2026-03-19
**Domain Model:** regulatory-compliance | **Evaluation Target:** 12 candidate features (F-01 through F-12)

---

## Domain Concepts Applied

| Concept | Definition (from model) | How It Applies |
|---------|------------------------|----------------|
| Enforcement Probability Gradient | Not all regulations carry equal enforcement risk — priority should map to actual enforcement patterns | F-02 (DSAR) addresses the #1 GDPR enforcement trigger for SaaS providers. F-01 (EU Residency) addresses data sovereignty requirements with active enforcement post-Schrems II. F-08 (AI Act Transparency) addresses obligations with phased enforcement starting August 2025. |
| Data Flow Sovereignty | Where data is processed determines which regulations apply — assessed per-feature | F-01 directly addresses this. F-05 (AI Code Review), F-07 (Analytics), F-12 (Real-Time Collab) all process personal data and inherit data flow sovereignty requirements. Without F-01, every feature processing EU personal data carries jurisdictional risk. |
| Compliance Prerequisite Chain | Some features cannot be compliant without other capabilities existing first | F-05 → F-08 (AI Code Review requires AI Act Transparency Layer). F-07 → lawful basis mechanism (Analytics Dashboard requires consent/legitimate interest documentation). F-01 is a prerequisite for ALL features processing EU personal data at enterprise compliance level. |
| Regulatory Change Velocity | EU regulatory landscape 2024-2027 is high-velocity — features should be assessed for regulatory durability | AI Act enforcement phases: Feb 2025 (prohibited practices), Aug 2025 (GPAI), Feb 2027 (high-risk systems, Article 52 transparency). NIS2 implementation ongoing. Data Act adoption 2025-2026. Features built now must remain compliant through at least 2028. |

## Feature Scores (1-10 scale, regulatory urgency — higher = more urgent from compliance perspective)

| Feature | Score | Regulation(s) | Enforcement Risk | Rationale |
|---------|-------|---------------|-----------------|-----------|
| F-01: EU Data Residency | **10** | GDPR Ch. V (transfers), Schrems II | CRITICAL | Data Flow Sovereignty: without EU residency, every feature processing EU personal data operates on a legal risk basis. Post-Schrems II enforcement is active — DPAs are issuing orders. This is not a feature; it is a compliance prerequisite for the entire EU product. Enforcement Probability: HIGH (active DPA investigations of US-processed EU data). |
| F-02: Automated DSAR Pipeline | **9** | GDPR Art. 15-20 (data subject rights) | HIGH | Enforcement Probability Gradient: DSAR non-compliance is the #1 enforcement trigger for SaaS providers in 2025-2026. Current manual process risks deadline violations (30-day requirement). Three DPAs have issued fines >€1M for systematic DSAR failures in 2025. |
| F-03: In-App Templates | **1** | None directly | NONE | No regulatory implications. Templates don't process personal data, don't create new compliance obligations. Regulatory score is not relevant to this feature's prioritization. |
| F-04: Slack Integration | **2** | GDPR Art. 28 (processor obligations) | LOW | Minor: data shared with Slack creates a sub-processor relationship requiring DPA update. Standard contractual coverage. No enforcement risk if DPA is in place. |
| F-05: AI Code Review | **8** | EU AI Act Art. 52 (transparency), GDPR Art. 22 (automated decisions) | HIGH | Compliance Prerequisite Chain: CANNOT ship to EU without F-08 (AI Act Transparency Layer). Article 52 transparency obligations become enforceable February 2027, but enterprise customers will require compliance documentation before that date. If F-05 ships without F-08, it is legally non-compliant for EU deployment. Regulatory Change Velocity: AI Act enforcement is phasing in — building F-05 without transparency architecture encodes assumptions that upcoming enforcement will invalidate. |
| F-06: RBAC | **4** | GDPR Art. 25 (data protection by design), Art. 32 (security) | MEDIUM-LOW | RBAC supports data protection by design (access minimization). Not a direct enforcement target, but strengthens overall compliance posture. NIS2 access control requirements apply if product is classified as essential/important service. |
| F-07: Usage Analytics | **6** | GDPR Art. 6 (lawful basis), ePrivacy | MEDIUM | Compliance Prerequisite Chain: analytics processing EU personal data requires a lawful basis mechanism (consent or legitimate interest assessment). If analytics tracks individual user behavior, GDPR applies. If it uses cookies or similar tracking, ePrivacy applies. Without a lawful basis mechanism, the feature creates enforcement risk. |
| F-08: AI Act Transparency | **9** | EU AI Act Art. 52 | HIGH | Regulatory Change Velocity: Article 52 enforcement begins February 2027. This feature is a compliance prerequisite for F-05 and any future AI-powered features. Building it now provides regulatory durability — all AI features built on top of it will inherit compliance. NOT building it blocks the entire AI feature roadmap for EU. |
| F-09: Custom Workflows | **3** | GDPR Art. 22 (if workflows make automated decisions about individuals) | LOW | Low enforcement probability. Workflows processing personal data need documented logic but this is a minor compliance burden, not an enforcement risk. |
| F-10: SSO/SAML | **5** | NIS2 Art. 21 (security measures), GDPR Art. 32 | MEDIUM | SSO strengthens authentication security (NIS2 compliance). Not a direct enforcement target but supports security audit posture. Enterprise customers increasingly require SSO for their own NIS2 compliance. |
| F-11: Bulk Data Export | **4** | GDPR Art. 20 (data portability) | LOW | Enforcement Probability Gradient: Article 20 has seen minimal enforcement action. Theoretically required, practically unenforced. Low regulatory urgency despite being a GDPR obligation. |
| F-12: Real-Time Collaboration | **3** | GDPR Art. 25, 32 (security of processing) | LOW | Real-time data processing creates data flow complexity but no specific enforcement risk beyond standard GDPR obligations. Security of the real-time channel must be adequate (encryption in transit) but this is standard engineering practice. |

## Key Regulatory Tensions

1. **F-01 is a compliance prerequisite for the entire EU product, not just one feature.** Data Flow Sovereignty is clear: without EU data residency, every feature processing EU personal data inherits jurisdictional risk. The market domain may see F-01 as one of 12 features to prioritize. The regulatory domain sees it as the foundation that makes EU business legally sustainable. This is a hard tension — the market can choose to accept the risk, but it cannot eliminate the risk by deferring F-01.

2. **F-08 creates a compliance prerequisite chain that the market domain may not see.** F-08 (AI Act Transparency) scores 3 in market demand. It scores 9 in regulatory urgency. Without F-08, F-05 (AI Code Review, market score 6) is legally unshippable to EU customers. The market will want to defer F-08 — the regulatory domain requires it before any AI feature. This is a Compliance Prerequisite Chain enforcement (GV-1 from regulatory model): hard guardrail, no override.

3. **F-02 scores 5 in market demand but 9 in regulatory urgency.** Customers don't ask for DSAR compliance — they assume it exists. The absence of customer demand masks the enforcement risk. If we are fined for DSAR non-compliance, the fine (potentially €10M+ under GDPR Art. 83) dwarfs the revenue from any single feature. This is the AP-1 (compliance theater) anti-pattern risk: visible features get prioritized over substantive compliance infrastructure.

4. **Regulatory Change Velocity demands F-08 be built before February 2027.** Given typical development and deployment cycles, a Q2 2026 start is necessary for Q4 2026 deployment. Deferring F-08 to Q3 creates unacceptable schedule risk against the regulatory deadline.

## Recommended Priority (Regulatory Domain Only)

**Tier 1 (compliance-critical — must build immediately):** F-01, F-02, F-08
**Tier 2 (compliance-important — build in 2026):** F-05 (after F-08), F-07 (with lawful basis mechanism)
**Tier 3 (compliance-relevant but low enforcement risk):** F-06, F-10, F-11
**Tier 4 (no significant regulatory dimension):** F-03, F-04, F-09, F-12

**Hard constraints (Compliance Prerequisite Chain — GV-1):**
- F-05 MUST NOT ship to EU before F-08 is deployed
- F-07 MUST NOT ship without lawful basis mechanism
- F-01 is structurally prerequisite for full EU compliance of any feature processing personal data
