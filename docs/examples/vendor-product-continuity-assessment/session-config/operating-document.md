# Operating Document: Vendor-Product Continuity Assessment

**Version:** 2 | **Date:** [Session Date] | **Governor:** [Your Name]
**Scope Type:** finite | **Graduation Stage:** 1

## Goal

Assess whether continued dependency on [Target Vendor] / [Target Product] represents material third-party risk. Produce a six-signal viability assessment covering business model exposure, contractual position, and dependency exposure — with dual-level scoring (vendor and product independently) across 8 analytical domains, a risk determination with timeline, and mitigation recommendations grounded in cross-domain findings.

### Analytical Frame Contract

| Field | Value |
|---|---|
| **Stance** | Dependent organization (existing customer of [Target Product]) |
| **Output Verb** | Assess (surface exposure, not recommend alternatives) |
| **Failure Mode** | Unmanaged dependency — continued reliance on a vendor/product whose viability trajectory is deteriorating without organizational awareness or contingency |
| **Prohibited Frame** | Vendor sales evaluation, competitive comparison, migration planning, procurement advisory |
| **Verdict Vocabulary** | VIABLE / AT RISK / STRUCTURALLY PRESSURED (vendor and product viability); HIGH EXPOSURE / MATERIAL EXPOSURE / LOW EXPOSURE (third-party risk level) |

### Six Signals Framework

The assessment is organized around six observable vendor viability signals, grouped into three categories. This framework defines what the session must produce — every signal must receive an evidence-grounded assessment.

**Category 1 — Business Model Signals** (Is the vendor structurally viable?)

| Signal | Question | Domain Coverage |
|---|---|---|
| **(1) Revenue model exposure** | Is the vendor pricing per-seat for capabilities that AI can now automate, or pricing on domain-specific intelligence and operational outcomes that remain differentiated? | SAAS-1 (Pricing Model Vulnerability) + ECON-1 (SaaS Financial Metrics) |
| **(2) Domain depth vs. feature breadth** | Does the vendor operate on your organization's own data (contracts, configurations, vendor relationships) or on publicly available knowledge? Products built on public knowledge face direct substitution risk from AI foundation model providers. | DISP-1 (Data Moat: Customer-Specific vs. Public Knowledge) |
| **(3) Financial sustainability and consolidation positioning** | Is the vendor a consolidation winner or an acquisition target? Is capital concentrating toward or away from their category? | ECON-1 (Revenue Trajectory, Financial Runway, Consolidation Positioning) |

**Category 2 — Contractual Position** (Are you protected if they fail?)

| Signal | Question | Domain Coverage |
|---|---|---|
| **(4) Exit strategy provisions** | Does your contract include data portability, transition assistance periods, and source code escrow? Can you extract your data and transition without losing operational continuity? | REG-1 (Exit Provision Requirements) |
| **(5) Regulatory embedding depth** | Is the vendor embedded in your regulatory workflows (audit trails, compliance evidence, notification chains) or providing capabilities outside your compliance-critical path? | REG-1 (Compliance Workflow Embedding, Regulatory Switching Costs) |

**Category 3 — Dependency Exposure** (How much operational risk do you carry?)

| Signal | Question | Domain Coverage |
|---|---|---|
| **(6) Vendor stickiness vs. viability** | If this vendor ceased operations, how long are you stuck? High stickiness combined with low viability is the maximum-risk combination. | STICK-1 (Stickiness-Viability Combination Matrix) |

**Leading Indicators** (domains that predict viability deterioration before the six signals manifest):

| Domain | Role |
|---|---|
| TAL-1 (Talent & Workforce) | Talent departures and workforce capacity decline precede financial metric deterioration by 2-4 quarters. Key engineering and security staff leaving is an early indicator of service quality degradation before it shows up in the product. |
| GOV-1 (Governance & Strategic Coherence) | Leadership instability, strategic pivots, and organizational restructuring predict operational deterioration 12-18 months before financial metrics show it. |
| ADAPT-1 (Adaptation Capacity) | Assesses the vendor's ability to respond to the pressures the six signals detect — R&D investment trajectory, product investment vs. neglect, pivot capacity. |

### Guardrails

- **G-1:** AFC Prohibited Frame Guard — the assessment evaluates dependency risk from an existing customer perspective; it must NOT drift into procurement recommendation, vendor advocacy, competitive comparison, or migration planning | Severity: hard | Evaluation: interpretive | Threshold: zero instances of prohibited-frame content in deliverable
- **G-2:** Six-Signal Coverage — all six signals must appear in the final deliverable with substantive, evidence-grounded assessment; no signal may be omitted or reduced to a placeholder | Severity: hard | Evaluation: mechanical | Threshold: 6 signal assessments present with ≥2 evidence citations each | Timing: deliverable
- **G-3:** Multi-Domain Coverage — all 8 domain models must contribute to the assessment; no domain may be omitted | Severity: hard | Evaluation: mechanical | Threshold: 8 domains referenced with substantive findings | Timing: deliverable
- **G-4:** Evidence-First Scoring — every domain score must cite specific evidence item IDs before applying domain model concepts; no score shall be justified by domain model logic alone | Severity: hard | Evaluation: interpretive | Threshold: zero scores without evidence ID citation
- **G-5:** No Single-Source Extreme Scores — extreme scores (1-3 or 8-10 on a 10-point scale) require corroboration from 2+ independent Tier 1 or Tier 2 sources | Severity: soft | Evaluation: mechanical | Threshold: zero single-source extreme scores
  - Recovery: Downgrade extreme score to moderate range (4 or 7) and flag for Governor review with available evidence
- **G-6:** Directional Balance Check — if >70% of Tier 1/Tier 2 evidence items support a single directional frame (all "risk" or all "stable"), halt scoring and present evidence distribution to Governor before proceeding | Severity: hard | Evaluation: mechanical | Threshold: directional ratio ≤70/30 across Tier 1/2 items
- **G-7:** Deliberation Traceability — every claim in the synthesis report must trace to a specific domain agent position from the deliberation transcript | Severity: soft | Evaluation: interpretive | Threshold: zero untraceable synthesis claims
  - Recovery: Add traceability annotation to untraceable claims or remove them from synthesis
- **G-8:** Dual-Level Discrimination — vendor viability and product viability must be scored independently wherever evidence supports divergence; conflating vendor-level and product-level assessment is a structural error | Severity: hard | Evaluation: interpretive | Threshold: zero conflated vendor/product scores where evidence shows divergence
- **G-9:** Analytical Relevance — each signal and domain assessment must contain at least one claim that directly addresses the dependency risk question; descriptions that characterize a topic without linking to viability or risk are flagged as disconnected | Severity: soft | Evaluation: interpretive | Threshold: zero disconnected assessments | Timing: deliverable
  - Recovery: Add explicit dependency-risk linkage to disconnected section

## Objectives

### OBJ-1: Business Model Viability Assessment (Signals 1-3)

- **Analytical Question:** Is [Target Vendor]'s business model structurally viable given AI-era competitive dynamics? Specifically: is the revenue model exposed to AI automation (Signal 1), does the product operate on defensible customer-specific data or substitutable public knowledge (Signal 2), and is the vendor positioned as a consolidation winner or acquisition target (Signal 3)?
- **Acceptance Criteria:** Signals 1-3 scored at both vendor and product levels with evidence citations; revenue model exposure classified; data moat assessed; consolidation positioning determined
- **Deliverable:** Business model viability section with per-signal scoring, evidence citations, and cross-signal tension analysis
- **Quality Standard:** Every signal score cites ≥2 evidence items; vendor-level and product-level assessments explicitly distinguished where they diverge
- **Domain Coverage:** ECON-1 (primary), DISP-1 (primary), SAAS-1 (supporting), ADAPT-1 (supporting — adaptation capacity contextualizes whether the vendor can respond to business model pressure)
- **Priority:** critical

### OBJ-2: Contractual Position Assessment (Signals 4-5)

- **Analytical Question:** Is the dependent organization contractually protected if [Target Vendor] fails or deteriorates? Specifically: do exit provisions provide actionable data portability and transition assistance (Signal 4), and how deeply is [Target Product] embedded in the organization's regulatory compliance workflows (Signal 5)?
- **Acceptance Criteria:** Exit provisions evaluated against DORA Article 28 requirements; regulatory embedding depth classified; switching cost implications assessed
- **Deliverable:** Contractual position section with exit provision analysis, regulatory embedding assessment, and switching cost implications
- **Quality Standard:** Specific regulatory references (DORA, NIS2) where applicable; exit provision assessment distinguishes documented provisions from tested provisions
- **Domain Coverage:** REG-1 (primary)
- **Priority:** critical

### OBJ-3: Dependency Exposure Assessment (Signal 6)

- **Analytical Question:** What is the operational exposure if [Target Vendor] / [Target Product] ceases operations or undergoes material deterioration? Specifically: what is the migration complexity, how long is the organization stuck, and does the stickiness-viability combination indicate maximum risk?
- **Acceptance Criteria:** Migration complexity scored; stickiness-viability matrix position determined; exposure timeline estimated
- **Deliverable:** Dependency exposure section with stickiness scoring, viability-stickiness combination assessment, and exposure timeline
- **Quality Standard:** Migration timeline estimates grounded in evidence (industry benchmarks: 3-6 months standard, 12+ months complex); stickiness-viability combination explicitly classified
- **Domain Coverage:** STICK-1 (primary), ECON-1 + DISP-1 (viability inputs to the combination matrix)
- **Priority:** critical

### OBJ-4: Cross-Domain Risk Determination with Leading Indicators

- **Analytical Question:** Given the six-signal assessment from OBJ-1 through OBJ-3, what is the overall third-party risk determination, and do leading indicators (governance quality, talent trajectory, adaptation capacity) confirm or contradict the signal-based assessment?
- **Acceptance Criteria:** Risk level verdict applied per AFC vocabulary; exposure timeline estimated; leading indicator assessment identifies confirming or contradicting signals; mitigation recommendations framed as risk postures (not migration plans)
- **Deliverable:** Third-party risk determination with exposure timeline, leading indicator analysis, and mitigation posture recommendations
- **Quality Standard:** Risk determination traces to signal scores from OBJ-1 through OBJ-3; leading indicators explicitly compared against signal-based findings; mitigation postures actionable without violating AFC prohibited frame
- **Domain Coverage:** GOV-1 (primary), TAL-1 (primary), ADAPT-1 (primary), all domains (synthesis)
- **Priority:** critical

## Strategies

### STR-1: Six-Signal Evidence-Grounded Assessment → serves OBJ-1, OBJ-2, OBJ-3

- **Rationale:** Talk-2's thesis is that vendor viability is a distinct third-party risk category requiring its own assessment methodology. The six signals provide the observable framework; the 8 domain models provide analytical depth behind each signal. Structured assessment across all signals with evidence grounding prevents single-dimension bias.
- **What Must Be True (WMBT):** Sufficient public evidence exists across the six signals to score meaningfully. Domain models are rich enough to distinguish vendor-level from product-level viability signals.
- **Not Doing:** Competitive benchmarking, market share analysis for procurement, technology evaluation for feature comparison.
- **Kill Signal:** Fewer than 4 of the 6 signals produce evidence-supported scores (insufficient public information to assess).
- **Relationship to sibling strategies:** sequential — STR-2 depends on STR-1 output
- **Authorized By:** GOV-session-1

### STR-2: Viability-Stickiness Risk Synthesis with Leading Indicators → serves OBJ-4

- **Rationale:** Third-party risk is the interaction between viability trajectory and dependency depth (stickiness). Signal 6 explicitly models this interaction. Leading indicators (GOV-1, TAL-1, ADAPT-1) provide forward-looking signals that either confirm or contradict the six-signal assessment — a vendor with stable financials but deteriorating talent trajectory is on a declining path that financial metrics will eventually confirm.
- **What Must Be True (WMBT):** STR-1 has produced scored signal assessments. Leading indicator evidence is available to contextualize the signal scores.
- **Not Doing:** Migration cost estimation, alternative vendor evaluation, procurement scoring.
- **Kill Signal:** STR-1 output does not differentiate viability trajectory from current state — all scores are static snapshots with no directional indicators.
- **Relationship to sibling strategies:** depends on STR-1
- **Authorized By:** GOV-session-1

## Tactics

### TAC-1: Evidence Collection → serves STR-1

- **Parent Strategy:** STR-1
- **Parent Objective:** OBJ-1, OBJ-2, OBJ-3
- **Hypothesis:** If we collect and tier-classify public evidence across all six signals and 8 analytical domains for [Target Vendor] and [Target Product], then we will have sufficient grounded material to produce evidence-first viability scores that resist single-source bias.
- **Kill Condition:** Fewer than 15 total Tier 1/Tier 2 evidence items collected across all domains after exhausting available sources.
- **Success Metrics:** (a) Total evidence items collected (target: ≥30), (b) Signal coverage (target: ≥2 items per signal for all 6 signals), (c) Domain coverage (target: ≥3 items per domain for 6+ domains), (d) Tier distribution (target: ≥40% Tier 1/2)
- **Guardrails (inherited):** G-4, G-5, G-6
- **Guardrails (own):** None
- **Timeline:** [Session Date]
- **Bootstrap Cycles:** 0 (finite)
- **Seed Actions:** Parallel dispatch across 8 evidence collection domains; G-6 directional balance check after collection
- **Owner:** AI
- **Approach:** Parallel evidence collection using reference pool queries and web search across all 8 domains. Evidence items classified by tier (1-3) and tagged with both domain relevance and signal relevance (which of the 6 signals each evidence item informs). Directional balance check (G-6) applied before proceeding to scoring.
- **Dependencies:** execution
- **Domain Model Dependencies:** ECON-1, DISP-1, ADAPT-1, SAAS-1, STICK-1, REG-1, GOV-1, TAL-1
- **Human Creative Input Estimate:** 0

### TAC-2: Six-Signal Deliberation + Risk Synthesis → serves STR-1, STR-2

- **Parent Strategy:** STR-1, STR-2
- **Parent Objective:** OBJ-1, OBJ-2, OBJ-3, OBJ-4
- **Hypothesis:** If we run multi-agent deliberation where each domain agent independently covers its assigned Talk-2 signal categories with forced cross-domain tension identification, then viability-stickiness interactions and leading-indicator divergences will surface that single-signal scoring would miss — producing a risk determination that accounts for dependency depth, not just vendor health.
- **Kill Condition:** Deliverable not accepted after 3 revision cycles.
- **Success Metrics:** (a) All 6 signals scored with evidence citations, (b) Cross-domain tensions identified (target: ≥4), (c) Vendor vs. product viability divergences surfaced (target: ≥2), (d) Leading indicator confirmation or contradiction documented, (e) Governor assessment of risk determination usefulness
- **Guardrails (inherited):** G-1 through G-9
- **Guardrails (own):** None
- **Timeline:** [Session Date]
- **Bootstrap Cycles:** 0 (finite)
- **Seed Actions:** Execute deliberation per deliberation-config.md; synthesize risk determination
- **Owner:** AI
- **Approach:** Eight-agent deliberation with one agent per domain model, aligned to Talk-2 signal categories per deliberation-config.md. Independence Level 2. 3 rounds + synthesis. Risk synthesis combines signal scores with stickiness assessment and leading indicator analysis to produce third-party risk determination.
- **Dependencies:** execution (depends on TAC-1 output)
- **Domain Model Dependencies:** All 8 domain models (ECON-1, DISP-1, ADAPT-1, SAAS-1, STICK-1, REG-1, GOV-1, TAL-1)
- **Human Creative Input Estimate:** 1 (Governor review of final risk determination)

## Actions (Current Cycle)

### ACT-1: Collect and classify evidence across 6 signals and 8 domains → serves TAC-1
- **Assignee:** AI
- **Deliverable:** Evidence manifest with tier classifications, domain tags, and signal tags
- **Deadline:** [Session Date]
- **Dependency Type:** execution

### ACT-2: Execute eight-agent deliberation → serves TAC-2
- **Assignee:** AI
- **Deliverable:** Deliberation transcript with per-agent positions, signal assessments, and tension identification
- **Deadline:** [Session Date]
- **Dependency Type:** execution

### ACT-3: Synthesize six-signal risk determination → serves TAC-2
- **Assignee:** AI
- **Deliverable:** Third-party risk determination structured as: (1) Business model viability (Signals 1-3), (2) Contractual position (Signals 4-5), (3) Dependency exposure (Signal 6), (4) Leading indicator assessment, (5) Overall risk verdict with timeline, (6) Mitigation postures
- **Deadline:** [Session Date]
- **Dependency Type:** execution

### ACT-4: Governor review and acceptance → serves TAC-2
- **Assignee:** Governor
- **Deliverable:** Acceptance or revision request
- **Deadline:** [Session Date]
- **Dependency Type:** human_creative

## Review Cadences
- **Finite scope:** Review at each phase gate

## Decision History
- **[Session Date] — OD-v1 created:** Initial operating document for vendor-product continuity assessment. 8 domain models, 6 observable signals.
- **[Session Date] — OD-v2 created:** Restructured to align with Talk-2 six-signal framework. Objectives mapped to Talk-2's three signal categories (business model, contractual position, dependency exposure) plus leading indicators. Agent naming aligned. Signal-to-domain mapping made explicit.

---

## Phases (finite scopes only)

### Phase 1: Evidence Collection
- **Objective:** Collect, classify, and balance-check evidence across 6 signals and 8 domains for [Target Vendor] and [Target Product]
- **Entry Criteria:** Domain models loaded; evidence sources identified
- **Exit Criteria:** ≥15 Tier 1/2 evidence items collected; all 6 signals have ≥2 evidence items; G-6 directional balance check passed; Governor confirms evidence adequacy

### Phase 2: Six-Signal Deliberation
- **Objective:** Execute 3-round deliberation to produce six-signal viability assessment with cross-domain tension identification and leading indicator analysis
- **Entry Criteria:** Phase 1 exit criteria met
- **Exit Criteria:** Deliberation complete; all 6 signals scored at vendor and product levels; all 8 domains contributed; tension map produced; leading indicators assessed

### Phase 3: Risk Synthesis and Governor Review
- **Objective:** Synthesize third-party risk determination from signal scores, stickiness assessment, and leading indicators; Governor acceptance
- **Entry Criteria:** Phase 2 exit criteria met
- **Exit Criteria:** Governor accepts deliverable or requests revision (max 3 cycles per TAC-2 kill condition)

---

## Deliverable Structure

The final deliverable follows Talk-2's analytical structure:

### 1. Executive Summary
- Overall risk verdict (per AFC vocabulary)
- Exposure timeline
- Key finding (1-2 sentences)

### 2. Business Model Signals (OBJ-1)
- **Signal 1: Revenue Model Exposure** — pricing vulnerability assessment, AI automation exposure
- **Signal 2: Domain Depth vs. Feature Breadth** — data moat classification (customer-specific vs. public knowledge), substitution risk
- **Signal 3: Financial Sustainability and Consolidation** — revenue trajectory, market positioning, consolidation winner/target determination

### 3. Contractual Position (OBJ-2)
- **Signal 4: Exit Strategy Provisions** — data portability, transition assistance, escrow, DORA Article 28 compliance
- **Signal 5: Regulatory Embedding Depth** — compliance workflow dependency, regulatory switching costs

### 4. Dependency Exposure (OBJ-3)
- **Signal 6: Vendor Stickiness vs. Viability** — migration complexity, exposure timeline, stickiness-viability combination matrix position

### 5. Leading Indicators (OBJ-4)
- Talent trajectory (TAL-1) — confirming or contradicting?
- Governance quality (GOV-1) — confirming or contradicting?
- Adaptation capacity (ADAPT-1) — can the vendor respond to identified pressures?

### 6. Cross-Domain Tensions
- Agreed findings with attribution chains
- Unresolved tensions with evidence gaps

### 7. Risk Determination
- Verdict with timeline
- Mitigation postures (not migration plans)

### 8. Evidence Index
- All cited evidence with tier classifications and source URLs
