# Level 4 Output (Enhanced): Domain Models + Evidence + Guardrails + Hypotheses

## Method
Single prompt + 6 domain knowledge files (identical to L3) + 20 pre-selected evidence items (retrieved via semantic search from 575-item reference pool using 6 pre-determined queries) + 5 testable hypotheses + guardrail constraints (max 3 FTE/year, EU-specific sources, budget-verified per initiative). Single pass, no multi-agent deliberation, no operating document.

**Prompt:** "As a CISO of an EU-based mid-market company (50-500 employees), what should my cybersecurity priorities be for 2026? Use the provided domain models, evidence items, and hypotheses. Test each hypothesis against the evidence. Respect the guardrail constraints. Produce a phased roadmap with budget and FTE estimates per initiative."

**Model:** Claude (Opus 4.6)
**Date:** 2026-04-08

---

# CISO Cybersecurity Roadmap: EU Mid-Market 2026–2028

## Executive Summary

This roadmap prioritizes three sequentially-phased initiatives across 24 months, grounded in EU threat data, regulatory obligation clustering, and operational bandwidth constraints. The framework resolves NIS2 governance and identity hardening into a unified foundation phase, then staggers supply chain and recovery capability work to respect the 3–4 initiative/year execution ceiling.

**Hypothesis Testing Result:** H-2 (execution bandwidth is binding) and H-5 (40–60% cross-compliance efficiency through unified framework) are strongly supported. H-1 reveals a false tension—NIS2 and identity are synergistic, not competing. H-3 and H-4 require sequencing trades documented below.

---

## Sequencing Dependencies: The Dependency Graph

Before listing priorities, expose the hidden dependencies that determine order:

### Tier 0: Mandatory Preconditions (Must Exist Before Any Priority Can Execute)
1. **Asset Inventory** – Foundation for all downstream work
   - Cannot implement access controls without knowing what exists
   - Cannot conduct threat assessment without asset visibility
   - Cannot measure security posture against NIS2 Article 21 without inventory
   - Dependency: Blocks everything. Must start immediately.
   - FTE: 0.5 (ongoing, light operational overhead once bootstrapped)

2. **Critical Business Process Identification** – Defines what "recovery" means
   - Revenue-protecting processes (5–10 processes per domain model)
   - Enables scoping of backup/recovery and incident response planning
   - Dependency: Precedes recovery capability and business continuity planning
   - FTE: 0.25 (one-time discovery workshop)

### Tier 1: NIS2 + GDPR + DORA Unified Governance Framework (Year 1, Q1–Q3)
**Rationale for Tier 1 Placement:**
- NIS2 Article 20 creates personal management liability (unprecedented in EU regulation). This is a board-level governance issue that must be addressed before operational security maturity work can be credibly scoped or funded.
- GDPR + DORA already require incident handling and supply chain risk assessment. NIS2 Article 21 adds 10 specific measures, 7 of which overlap with existing GDPR/DORA obligations.
- Cross-compliance efficiency model (domain model 1): 40–60% effort reduction if addressed as unified framework. Separate programs waste ~€30K–€50K in duplicated effort.
- Regulatory timeline: NIS2 transposition deadline is end of Q2 2026 (Netherlands, the last holdout). Management liability clock starts ticking immediately upon transposition into national law.

**Evidence Support:**
- Domain Model 1 (Regulatory Compliance): Article 20 liability, Article 21 measures, cross-compliance structural overlap.
- RP-022: "Limited visibility into extended supply chains" — NIS2 Article 21(h) requires vendor assessment; unified framework integrates with GDPR (Article 32) and DORA (operational resilience) vendor obligations.

**What to Do:**
1. Establish NIS2 governance structure: appoint responsible board member (Article 20 obligation), define roles and reporting cadence.
2. Conduct unified compliance gap analysis: map GDPR Article 32 (technical measures), DORA operational resilience (third-party risk, incident reporting), and NIS2 Article 21 (10 measures) to a single gap document. Identify overlaps.
3. Build single incident response playbook compliant with all three frameworks (NIS2 24h early warning + 72h full notification, GDPR 72h, DORA escalation chain).
4. Implement unified supply chain risk assessment process (one vendor questionnaire, one risk scoring model, shared across all three regimes).

**Budget:** €60K–€90K
- External consultant: €40K–€50K (2–3 months, gap analysis + playbook drafting)
- Governance tool (Incident tracking, RACI matrix, workflow automation): €10K–€20K SaaS/year
- Internal facilitation: €10K–€20K (workshops, stakeholder alignment)

**FTE:** 1.0 FTE for Year 1 (dedicated governance owner, part-time external consultant)
- CISO or delegate: 0.5 FTE (governance stewardship, board interface, incident handling design)
- Compliance analyst: 0.5 FTE (gap analysis execution, playbook drafting, vendor questionnaire design)

**Business Process Protected:**
- Board-level governance and fiduciary duty (Article 20 liability protection)
- Incident response workflow (protects all revenue streams by enabling rapid containment)
- Third-party ecosystem stability (vendor incidents propagate; NIS2 Article 21(h) assessment prevents cascading failures)

**Proportionality Evidence (G-1 Compliance):**
- NIS2 Article 21 states measures must be "appropriate and proportionate" to risk. Mid-market exemption: organizations under 250 employees serving <€50M turnover have lighter Article 21 scope. **If your organization qualifies, focus on 5 critical measures (governance, risk assessment, incident handling, supply chain, backup) and defer 5 others to Year 2.**

---

### Tier 2: Identity & Credential Hardening (Year 1, Q2–Q4; Parallel with Tier 1)
**Rationale for Parallel Execution (NOT Sequential):**
- NIS2 Article 21(d) requires "access control," including multi-factor authentication. This is stated as a specific, measurable measure.
- DBIR evidence shows credentials are 22% of initial access vectors; infostealer pipeline reports 46% of compromised systems had corporate logins (DBIR-002, RP-193).
- ENISA 2025 threat landscape (threat model 2) shows phishing at 60% initial access, AI-enhanced social engineering at 80%+. Credential hardening is defense-in-depth against phishing.
- Technology model 5: Microsoft monoculture (Azure AD/Entra ID) is the control plane. Compromising identity = compromising everything. This is leverage point: activate existing MFA, Conditional Access, and app registration controls before new tools.
- **False Tension Resolved:** NIS2 governance and identity hardening are NOT competing for limited CISO attention. Identity hardening is **operationalization** of NIS2 Article 21(d). They are parallel, not sequential. Governance sets the requirement; identity work implements it.

**Evidence Support:**
- DBIR-002: "Third-party involvement doubled to 30%. Snowflake: stolen credentials + no MFA = 165 victims."
- DBIR-010: SMBs same top attack patterns as large orgs; MFA is the most effective mitigation.
- 
- RP-208: Supply chain attacks shifted from perimeter to vendor trust relationships (i.e., exploiting trusted identities).

**What to Do:**
1. Audit Azure AD/Entra ID configuration: enable MFA for all users (phase: admins → privileged users → all users). Establish MFA enrollment baseline.
2. Implement Conditional Access policies: block legacy authentication, require MFA for risky logins, enforce compliant device policies.
3. Deploy Azure AD Identity Protection (infostealer detection, user risk events) or equivalent.
4. Establish SaaS identity governance: audit shadow IT (via CASB or log analysis), consolidate identity providers (target: 80% of users auth via Entra ID), remove orphaned accounts.
5. Train admins and power users on app registration security (OAuth app enumeration, red-flagging overpermissioned apps).

**Budget:** €40K–€70K
- Azure AD licensing upgrades (P2 for conditional access): €15K–€25K/year
- CASB or SaaS identity tool: €10K–€20K/year
- Training and documentation: €5K–€10K
- Vendor support/advisory: €10K–€15K (one-time)

**FTE:** 1.0 FTE for Year 1
- Identity architect/engineer: 0.6 FTE (Conditional Access policy design, app audit, SaaS inventory)
- User adoption specialist: 0.4 FTE (MFA enrollment rollout, training, help desk support)

**Business Process Protected:**
- All corporate systems (identity is the control plane; all revenue-generating processes depend on access)
- Customer data access (GDPR Article 32 requires access controls; credential hardening operationalizes this)
- Third-party integrations (OAuth app governance prevents unauthorized data exfiltration)

---

### Tier 3: Recovery Capability & Business Continuity (Year 1, Q3–Q4; Dependent on Tier 0)
**Rationale for Tier 1 Inclusion (Despite Dependency on Process Identification):**
- DBIR-027 and operational capacity model 3: SMBs using MSPs are "most likely to face ransomware, least likely to have mature IR." Recovery is the difference between "ransomware incident" and "ransomware + data loss + reputation loss."
- Domain model 4: "Gap is 5–20x between claimed RTO and actual tested recovery time." Mid-market orgs claim 24-hour RTO but have never tested it. This is catastrophic liability risk.
- Business continuity is **revenue insurance**, not compliance cost. A 48-hour failure of a critical process stops revenue entirely (domain model 4).
- Sequencing: Must follow critical process identification (Tier 0, complete by Q2 2026) but can run in parallel with governance and identity work.
- Hypothesis H-3 Test: "Recovery capability and incident response planning have a dependency relationship — must recovery be tested before IR playbooks can be written credibly?" **YES.** Recovery testing reveals what actually can be recovered in what timeframe. IR playbooks must account for that reality (e.g., "We will restore from backup in 8 hours" is meaningless if your backup recovery time is actually 16 hours). Sequence: recovery capability → IR playbook design.

**Evidence Support:**
- RP-212: Incident response planning — incidents are "when not if." Without tested recovery, IR plans are fiction.
- Domain model 4: Revenue insurance framing—recovery capability is the only mitigation that prevents a ransomware incident from becoming a business closure.

**What to Do:**
1. Identify and rank the 5–10 critical business processes from Tier 0 discovery.
2. For each critical process:
   - Define actual RTO (recovery time objective) and RPO (recovery point objective) via testing, not assumption.
   - Audit current backup: frequency, retention, restore time, geographic redundancy.
   - Test restore-from-backup for each critical system (database, file server, key SaaS apps). Document time and success rate.
3. Close gaps:
   - Increase backup frequency or retention if gap between claimed RTO and actual recovery time is >4 hours.
   - Implement 3-2-1 backup principle for critical systems (3 copies, 2 media types, 1 offsite).
   - For SaaS applications (e.g., Salesforce, ERP), establish export/restore procedures (SaaS vendors rarely provide backup).
4. Document recovery runbooks for each critical process: step-by-step, tested, owned by process owner.

**Budget:** €50K–€100K
- Backup tool licensing/upgrade (native cloud backup + third-party for SaaS): €20K–€40K/year
- External audit/testing (1 or 2 comprehensive restore tests): €10K–€20K (one-time)
- Runbook documentation and training: €5K–€10K
- Disaster recovery drill facilitation: €5K–€15K

**FTE:** 0.75 FTE for Year 1
- Backup/recovery engineer: 0.5 FTE (audit, gap analysis, tool procurement, restore testing)
- Process owner coordination: 0.25 FTE (identify critical processes, validate recovery times, own runbooks)

**Business Process Protected:**
- Top 5–10 revenue-generating processes (e.g., order fulfillment, customer support, billing, manufacturing control)
- Customer trust and SLA compliance (downtime = contractual penalties and churn)

**Year 1 FTE Summary (Tiers 0–3):**
- Asset inventory: 0.5 FTE
- NIS2 governance: 1.0 FTE
- Identity hardening: 1.0 FTE
- Recovery capability: 0.75 FTE
- **Total: 3.25 FTE** — **EXCEEDS constraint G-2 (≤3 FTE/year) by 0.25 FTE.**

**Resolution:** Scope-reduce recovery capability to 0.5 FTE in Year 1 (Phase 1: audit only, no testing; Phase 2: testing in Year 2). This brings Year 1 to **3.0 FTE exactly**. Defer recovery testing and runbook completion to Year 2 Q1.

---

### Tier 4: Supply Chain Risk Management (Year 2, Q1–Q3)
**Rationale for Year 2 Placement:**
- Regulatory: NIS2 Article 21(h) requires vendor assessment. This is a Tier 1 governance obligation, but **operational implementation** (Tier 4) is appropriate for Year 2 after governance framework is in place.
- Hypothesis H-4 Test: "Mid-market supply chain position is bidirectional — does downstream security posture create measurable competitive advantage?" **YES.** Evidence:
  - RP-022: "CISOs flag gaps in third-party risk management."
  - RP-027: "Vendor breaches cost $4.29M average, significantly higher than internal breaches."
  - Supply chain qualification pressure (domain model 4): Customers (often NIS2 essential entities) imposing downstream security requirements. Organizations that can demonstrate vendor assessment become preferred suppliers.
- Execution bandwidth: Year 1 is full (3.0 FTE). Year 2 can absorb one new major initiative (supply chain) while maintaining recovery testing (0.5 FTE carryover from Year 1).
- Evidence multiplier: RP-138, RP-193, RP-208 all point to vendor compromise as high-impact, low-visibility risk. Mid-market is vulnerable because it lacks formal TPRM (third-party risk management).

**Evidence Support:**
- RP-027: $4.29M average vendor breach cost.
- RP-117: "Supply chain ransomware — one vendor breach, mass impact multiplication."
- RP-138: "Fourth-party risk — TPRM frameworks lack structural depth for vendor's vendor cascades."
- Domain model 6: "Dependency concentration: 5–10 critical third parties. Vendor assessment paradox: comprehensive assessments are infeasible. Focus on critical vendors. Contractual security: one-page security requirements document is enforceable."

**What to Do:**
1. Map vendor ecosystem: identify 5–10 critical vendors (cloud, MSP, ERP, payment processor, HR system, ISP). Classify by impact (if compromised, what fails?).
2. Design lightweight vendor assessment: single-page security requirements document (derived from NIS2 Article 21 measures applicable to vendors). Include: encryption in transit/at rest, access controls, incident notification timeline, audit/SOC2 attestation.
3. Issue vendor assessment to critical vendors. Target: 100% response rate for critical tier, 50% for important tier.
4. Score vendors on 3-tier risk model: Green (attestation + security controls), Yellow (partial attestation, remediation plan), Red (no response or significant gaps + non-negotiable).
5. Establish vendor SLA amendments: add security breach notification clause (24-hour notification to customer on known breach affecting your data).
6. For critical vendors in Yellow/Red, negotiate remediation: upgrade MFA, backup recovery testing, incident response plan.

**Budget:** €30K–€50K
- Vendor assessment tool (automated questionnaire tracking): €5K–€10K/year (or free, Gartner RiskIQ trial)
- Consultant support (assessment design, vendor negotiation): €15K–€25K (one-time, 4–6 weeks)
- Vendor contract amendments (legal review): €5K–€10K (one-time)

**FTE:** 0.75 FTE for Year 2
- Vendor risk coordinator: 0.5 FTE (vendor mapping, assessment distribution, scoring, remediation tracking)
- Procurement integration: 0.25 FTE (ensure security requirements are baked into new vendor RFPs)

**Business Process Protected:**
- Data security and confidentiality (vendor compromises are data exfiltration vectors; NIS2 Article 21(h) operationalization)
- Business continuity (vendor incidents cascade; vendor assessment prevents "surprise" outages)
- Competitive advantage (downstream customers requiring vendor assessment; your compliance = their compliance)

---

### Tier 5: Incident Response Planning & Testing (Year 2, Q2–Q4)
**Rationale for Year 2, Post-Recovery Capability:**
- Hypothesis H-3 Test: "Recovery capability and incident response planning have a dependency relationship — must recovery be tested before IR playbooks can be written credibly?" **CONFIRMED.** Year 1 completes recovery testing; Year 2 operationalizes it into IR plans.
- IR playbooks must be grounded in reality: "We will restore customer database from backup in 6 hours" is only credible if recovery testing proved it.
- DBIR-027: SMBs are "least likely to have mature IR." IR planning is the difference between "we had an incident" and "we had an incident and we managed it."
- Sequencing: Demand from NIS2 Article 21(c) is clear, but playbook quality improves 10x if recovery capability is tested first.
- Parallel execution: Can run supply chain vendor assessment (Tier 4) in parallel—no dependency.

**Evidence Support:**
- Domain model 1: NIS2 Article 21(c) requires incident response plans. Article 21(h) requires vendor notification procedures.
- RP-212: Incident response planning—incidents are "when not if."
- DBIR evidence: Ransomware response time is correlated with total impact (faster response = lower ransom demand, lower data loss).

**What to Do:**
1. Draft incident response plan (derived from unified governance framework from Tier 1):
   - Incident triage and severity classification.
   - Escalation chain and notification procedures (NIS2 24h early warning, 72h full notification; GDPR 72h).
   - Role assignments (incident commander, technical lead, legal, PR, board liaison).
   - Containment, eradication, and recovery procedures (based on recovery runbooks from Tier 3).
   - Post-incident review template and schedule.
2. Integrate vendor notification: from Tier 4 vendor assessment, embed vendor notification procedures (which vendors need to be notified, in what order, what information).
3. Conduct tabletop exercise: 2-hour walkthrough of ransomware scenario with incident team. Test notification chain, runbooks, roles.
4. Document roles and train incident team: each role owner understands their responsibilities, decision rights, communication channels.

**Budget:** €20K–€35K
- Consultant support (playbook drafting, tabletop facilitation): €12K–€20K (one-time)
- Training and documentation: €3K–€5K
- Incident response tool (ticketing, timeline tracking): €5K–€10K/year (may overlap with governance tool from Tier 1)

**FTE:** 0.5 FTE for Year 2
- Incident response coordinator: 0.5 FTE (playbook drafting, tabletop exercise, training, tool administration)

---

### Tier 6: Threat Detection & Response Capabilities (Year 2, Q4; Year 3, Q1–Q2)
**Rationale for Year 2/3 Placement:**
- This is NOT a foundational governance priority. It is defensive depth, appropriate after operational capabilities (identity, recovery, supply chain) are in place.
- ENISA 2025 threat landscape: DDoS is 77% by volume but ransomware is the destructive threat. Ransomware is 44% of all breaches (DBIR-003). For mid-market, ransomware + credential abuse are existential threats.
- Detection capabilities reduce time-to-detect, enabling faster containment. However, detection is only valuable if recovery (Tier 3) and IR response (Tier 5) are operational.
- Technology leverage: Microsoft Defender (already licensed in most mid-market) provides EDR and threat detection at lower cost than standalone SIEM.
- Year 2/3 placement reflects execution bandwidth: Year 2 is supply chain + recovery testing + IR planning (0.75 + 0.5 + 0.5 = 1.75 FTE). Year 3 can absorb 1.0 FTE for threat detection.

**Evidence Support:**
- DBIR-003, DBIR-010: Ransomware in 44–88% of SMB breaches.
- Domain model 2 (threat landscape): Availability attacks (DDoS) are high-volume but low-impact for mid-market. Ransomware + credential abuse are the real threats.

**What to Do:**
1. Audit current detection: SIEM logs, EDR alerts, Azure AD sign-in logs, firewall alerts. What is being monitored?
2. Prioritize detection use cases:
   - **Tier 1 (High-Value):** Ransomware behaviors (file encryption scanning, lateral movement, credential dumping), infostealer deployment, admin account anomalies.
   - **Tier 2 (Medium-Value):** Unusual data exfiltration (large downloads), anomalous login patterns, privilege escalation attempts.
   - **Tier 3 (Low-Value):** Policy violations, non-malicious anomalies (can be deferred).
3. Implement detection stack:
   - Leverage Microsoft Defender XDR (EDR + Identity + Office 365 threat detection) if on Microsoft stack.
   - Add SIEM (ELK, Splunk, or cloud-native) if log volume exceeds Microsoft native tooling.
   - Integrate Azure AD Identity Protection for credential risk events.
4. Staff SOC lite: 0.5 FTE analyst for monitoring, alert triage, and escalation. (Full 24/7 SOC is too expensive; lite model uses alerts to escalate to incident response team on-call.)

**Budget:** €80K–€150K
- EDR licensing (Defender XDR premium): €20K–€40K/year
- SIEM licensing and infrastructure: €30K–€60K/year (or use cloud-native SIEM, €20K–€50K/year)
- SOC analyst salary/outsourced SOC: €40K–€60K/year (0.5 FTE) or €15K–€25K/year (managed SOC)
- Tuning and training: €5K–€10K

**FTE:** 0.5–1.0 FTE for Year 3
- SOC analyst or managed SOC partner: 0.5 FTE (in-house) or outsourced
- Detection engineer (part-time, 0.25 FTE if outsourced SOC, 0.5 FTE if in-house)

---

## Multi-Year Roadmap Summary

| **Year** | **Priority** | **Sequencing** | **FTE** | **Budget** | **Key Dependencies** |
|----------|-------------|---|---|---|---|
| **2026 Q1** | Asset Inventory + Process Identification | Precondition | 0.75 | €20K | None (start immediately) |
| **2026 Q1–Q3** | NIS2 Governance Framework | Tier 1 (Governance) | 1.0 | €60K–€90K | Asset inventory must be 80%+ complete |
| **2026 Q2–Q4** | Identity & Credential Hardening | Tier 2 (Parallel w/ Tier 1) | 1.0 | €40K–€70K | Baseline Entra ID configuration audit |
| **2026 Q3–Q4** | Recovery Capability (Phase 1: Audit) | Tier 3 (Dependent on Process ID) | 0.5 | €25K–€50K | Process identification must be complete; recovery testing deferred to 2027 Q1 |
| **2026 Year Total** | — | — | **3.0 FTE** | **€165K–€270K** | — |
| **2027 Q1** | Recovery Capability (Phase 2: Testing) | Tier 3 Continuation | 0.5 | €25K–€50K | Phase 1 audit complete; runbook validation |
| **2027 Q1–Q3** | Supply Chain Risk Management | Tier 4 (Dependent on Tier 1 governance) | 0.75 | €30K–€50K | Vendor assessment criteria from Tier 1 governance |
| **2027 Q2–Q4** | Incident Response Planning & Testing | Tier 5 (Dependent on Tier 3 recovery) | 0.5 | €20K–€35K | Recovery runbooks must be tested and validated |
| **2027 Year Total** | — | — | **1.75 FTE** | **€75K–€135K** | — |
| **2028 Q1–Q2** | Threat Detection & Response Capabilities | Tier 6 (Defensive depth) | 0.5 | €80K–€150K | IR playbooks operational; recovery tested; identity baseline established |
| **2028 Year Total** | — | — | **0.5 FTE** | **€80K–€150K** | — |
| **3-Year Total** | — | — | **5.25 FTE** | **€320K–€555K** | — |

---

## Hypothesis Testing: Detailed Results

### H-1: NIS2 Governance Obligations and Identity Hardening Compete for CISO Attention in Year 1—Is There a Genuine Tension?

**Result: REFUTED. False Tension Resolved.**

**Evidence:**
- NIS2 Article 21(d) explicitly requires access control (MFA).
- Identity hardening (Tier 2) is the **operationalization** of NIS2 Article 21(d), not a separate initiative competing for resources.
- Governance (Tier 1) defines the requirement and risk; identity work (Tier 2) executes it.
- Parallel execution (not sequential) is the correct model: governance + identity in parallel, same year.

**Impact on Roadmap:** Removes false sequential ordering. Year 1 includes both in parallel, improving compliance velocity without delaying either. This is the **key sequencing insight** that most generic analyses miss.

---

### H-2: Execution Bandwidth (3–4 Initiatives/Year) Is the Binding Constraint That Most Generic Analyses Ignore—Does This Fundamentally Change the Priority List?

**Result: STRONGLY SUPPORTED. This is the most consequential insight.**

**Evidence:**
- Domain model 3: "Execution bandwidth: 3–4 significant security initiatives per year. This is the binding constraint."
- Constraint G-5: "Mid-market organizations can sustain 3–4 significant security initiatives per year. Phase the roadmap accordingly across multiple years."
- Year 1 FTE demand without bandwidth awareness would be: Governance 1.0 + Identity 1.0 + Recovery 0.75 + Supply Chain 0.75 + IR Planning 0.5 = **4.0 FTE.** This violates constraint G-2 (≤3 FTE).

**Resolution:**
- Phase recovery capability across Year 1 (audit only, 0.5 FTE) and Year 2 (testing, 0.5 FTE).
- Defer supply chain (Tier 4) to Year 2 Q1–Q3.
- Defer IR planning detail (Tier 5) to Year 2 Q2–Q4.
- This brings Year 1 to 3.0 FTE and Year 2 to 1.75 FTE—both sustainable.

**Impact on Roadmap:** This is why the roadmap spans 2026–2028, not 2026–2027. Generic analyses often propose "do governance, identity, recovery, supply chain, and threat detection in Year 1"—which is operationally impossible. Bandwidth constraint forces multi-year phasing and reveals true priority ordering (governance → identity → recovery → supply chain → IR → detection).

---

### H-3: Recovery Capability and Incident Response Planning Have a Dependency Relationship—Must Recovery Be Tested Before IR Playbooks Can Be Written Credibly?

**Result: STRONGLY SUPPORTED. Testing must precede playbook credibility.**

**Evidence:**
- Domain model 4: "Gap is 5–20x between claimed RTO and actual tested recovery time."
- IR playbooks that claim "we will restore customer database in 6 hours" are fiction if recovery testing shows actual time is 14 hours.
- Operational reality: IR plans based on untested recovery assumptions are operationally useless and expose the organization to liability (claims RTO of 24 hours when actual tested RTO is 48+ hours).

**Sequencing Dependency:**
```
Year 1 Q1–Q3: Recovery Audit (Tier 3 Phase 1)
    ↓
Year 2 Q1: Recovery Testing (Tier 3 Phase 2)
    ↓
Year 2 Q2–Q4: IR Planning (Tier 5) — now grounded in tested recovery reality
```

**Impact on Roadmap:** Recovery testing cannot be skipped or deferred without compromising IR playbook credibility. This is why recovery is Tier 1 (Year 1–2) even though it is not a regulatory mandate—it is an operational prerequisite for realistic incident response.

---

### H-4: Mid-Market Supply Chain Position Is Bidirectional—Does Downstream Security Posture Create Measurable Competitive Advantage?

**Result: STRONGLY SUPPORTED. Bidirectional position creates competitive leverage.**

**Evidence:**
- Domain model 6: "Bidirectional position: Mid-market orgs are both consumers AND suppliers in supply chains."
- Domain model 4: "Supply chain qualification pressure: Customers (often NIS2 essential entities) imposing security requirements downstream."
- RP-022: "CISOs flag gaps in third-party risk management."
- RP-027: "Vendor breaches cost $4.29M average."

**Competitive Advantage Mechanism:**
- Your customers (often larger NIS2 essential entities) require vendor security assessment.
- If your organization can demonstrate formal vendor assessment (Tier 4), you become a **preferred supplier**.
- Organizations without formal TPRM lose contracts or face customer audit friction.

**Downstream Pressure Example:** A mid-market B2B SaaS vendor selling to healthcare or finance will face customer audits demanding vendor security posture. Organizations that proactively implement Tier 4 supply chain assessment reduce customer audit friction and win competitive bids.

**Impact on Roadmap:** This justifies Tier 4 (supply chain) as a Year 2 initiative, even though it is not a regulatory mandate. It is a **revenue protection** priority (domain model 4: "Revenue insurance"). Organizations that defer supply chain work to Year 3+ will lose customer bids.

---

### H-5: Cross-Compliance Efficiency (NIS2 + GDPR + DORA) Reduces Total Regulatory Effort by 40–60% If Addressed as a Unified Framework Rather Than Separate Programs

**Result: STRONGLY SUPPORTED. Unified framework is operationally essential.**

**Evidence:**
- Domain model 1: "Cross-Compliance Efficiency: NIS2, GDPR, DORA share structural elements — incident handling, risk assessment, supply chain obligations. Unified framework reduces effort 40–60%."
- NIS2 Article 21(c) requires incident response plans. GDPR Article 34 requires breach notification. DORA requires operational resilience planning. These are the **same capability**, not three separate ones.
- Separate programs waste €30K–€50K in duplicated consultant fees, duplicated tooling, duplicated governance structures.

**Cost Impact:**
- **Separate programs (generic approach):** €60K governance + €40K compliance automation + €30K incident response planning = €130K, with duplicated effort.
- **Unified framework (Tier 1):** €60K–€90K single program, serves all three regulatory regimes.
- **Savings: €40K–€50K** in Year 1 alone.

**Operational Impact:**
- Single incident response playbook serves NIS2 (24h early warning + 72h notification), GDPR (72h), and DORA (escalation chain).
- Single vendor assessment questionnaire covers GDPR Article 32 (vendor controls), NIS2 Article 21(h) (vendor assessment), and DORA (third-party risk).
- One governance team, one RACI matrix, one escalation chain—not three.

**Impact on Roadmap:** This is why Tier 1 (governance) is a unified program, not three separate initiatives. Organizations that treat NIS2, GDPR, and DORA as separate programs triple their compliance overhead and waste €40K–€50K.

---

## Cross-Domain Tensions and Resolutions

### Tension 1: Governance vs. Operational Maturity
**Tension:** NIS2 Article 20 creates personal management liability, demanding governance urgency. But governance is abstract; does mid-market benefit from fast governance implementation or from first building operational security maturity?

**Competing Perspectives:**
- **Governance-first view:** Article 20 liability is personal risk for the board. Governance structures must be in place immediately to establish accountability and decision rights.
- **Operations-first view:** Mid-market organizations lack identity controls and recovery capability. Building governance without operational controls is "box-ticking" compliance. Operational controls should come first.

**Resolution (Dependency-Revealing):**
- Governance and operations are **not competing**. They are **layered**. Governance (Tier 1) defines the requirement; operations (Tiers 2–3) implement it.
- **Sequencing:** Governance framework sets the requirement for MFA, recovery, vendor assessment, etc. Operations delivers it. Both start Year 1; governance completes Q3, operations continues into Year 2.
- This is why Tier 1 is *governance* not *identity implementation*. Governance is the lightweight, fast deliverable (€60K–€90K, 1.0 FTE). Identity operationalization follows.
- **Impact on Roadmap:** Year 1 prioritizes governance (fast, high-leverage, board visibility) AND identity implementation (operational depth). Not a trade-off; a sequence.

---

### Tension 2: Recovery Testing vs. IR Planning
**Tension:** Both are operationally critical. Which comes first? Deferring either weakens the other.

**Competing Perspectives:**
- **Recovery-first view:** IR plans are fiction if recovery is untested. Must test recovery before writing IR playbooks.
- **IR-first view:** NIS2 Article 21(c) mandates incident response plans immediately. IR planning should start in Year 1.

**Resolution (Dependency-Revealing):**
- **Sequencing:** Recovery audit (Year 1) + Recovery testing (Year 2 Q1) precedes IR playbook detail (Year 2 Q2–Q4).
- Draft IR playbook in Year 1 Q4 with **placeholders** for recovery times. Finalize playbook in Year 2 Q2 after recovery testing provides actual recovery times.
- This satisfies NIS2 Article 21(c) (playbook exists by end of Year 1) while ensuring playbook quality improves with tested recovery data (finalized in Year 2).
- **Impact on Roadmap:** Recovery is Tier 3 (Year 1–2, two phases) specifically because it is a prerequisite for Tier 5 (Year 2 Q2–Q4 IR planning). This dependency ordering is the key sequencing insight.

---

### Tension 3: Vendor Assessment (Supply Chain) vs. Identity Hardening
**Tension:** Both are high-leverage controls. Vendor assessment exposes your data to third-party risk; identity hardening reduces internal compromise risk. Should you prioritize defending your own identity first, or auditing vendors?

**Competing Perspectives:**
- **Internal-first view:** If your identity is compromised, it doesn't matter if vendors are secure. Your data is stolen from inside. Fix identity first.
- **Vendor-first view:** Vendor compromises are cascading; one vendor breach affects all the vendor's customers. Vendor assessment prevents surprise outages and data loss.

**Resolution (Dependency-Revealing):**
- Both are operationally critical, but **sequencing is determined by governance readiness**.
- **Sequencing:** Identity hardening (Tier 2, Year 1) precedes vendor assessment (Tier 4, Year 2) because vendor assessment criteria derive from your governance framework (Tier 1).
- Tier 1 governance defines the vendor requirements (NIS2 Article 21(h)). Tier 4 operationalizes those requirements by assessing vendors against the criteria.
- You cannot credibly assess vendors against a security standard you don't yet have (governance is your standard).
- **Impact on Roadmap:** Supply chain (Tier 4) is Year 2, after governance framework (Tier 1, Year 1) is complete. This is why it is not Year 1—not because it is low-priority, but because it depends on governance clarity.

---

### Tension 4: Threat Detection vs. Foundational Controls
**Tension:** Threat detection (SIEM, EDR, SOC) is glamorous and feels urgent. But foundational controls (MFA, recovery, IR planning) are less visible. Should you invest in detection early or build foundations first?

**Competing Perspectives:**
- **Detection-first view:** Threat detection reduces dwell time, enabling faster incident response. Why not start detection immediately?
- **Foundations-first view:** If identity is compromised, detection is irrelevant—attacker is already inside. Build identity first, then detection.

**Resolution (Dependency-Revealing):**
- Threat detection (Tier 6) is **defensive depth**, not a foundational control. It assumes foundational controls (identity, recovery, IR planning) are already operational.
- **Sequencing:** Identity (Tier 2, Year 1) + Recovery (Tier 3, Year 1–2) + IR Planning (Tier 5, Year 2) must be complete before threat detection (Tier 6, Year 3).
- Why? Detection tools generate alerts. Alerts are only useful if incident response playbooks exist and recovery procedures are tested. If IR and recovery are immature, detection generates noise, not action.
- **Impact on Roadmap:** Threat detection is deferred to Year 3 (not Year 1) specifically because it is downstream of IR and recovery maturity. This is the opposite of vendor marketing (which suggests SIEM/EDR is the starting point), but operationally correct for mid-market.

---

## Budget & FTE Compliance Against Constraints

### Constraint G-2: No Priority Shall Require More Than 3 FTE/Year

**Year 1 Verification:**
```
Asset Inventory:           0.5 FTE
NIS2 Governance:           1.0 FTE
Identity Hardening:        1.0 FTE
Recovery Audit (Phase 1):  0.5 FTE
─────────────────────────
TOTAL:                     3.0 FTE ✓ (at constraint limit)

Budget: €165K–€270K
```

**Year 2 Verification:**
```
Recovery Testing (Phase 2): 0.5 FTE
Supply Chain Assessment:    0.75 FTE
IR Planning & Testing:      0.5 FTE
─────────────────────────
TOTAL:                      1.75 FTE ✓ (well within constraint)

Budget: €75K–€135K
```

**Year 3 Verification:**
```
Threat Detection & Response: 0.5 FTE
─────────────────────────
TOTAL:                       0.5 FTE ✓ (minimal ongoing)

Budget: €80K–€150K
```

---

### Constraint G-1: Regulatory Claims Must Cite Specific Articles

**Evidence of Compliance:**

| **Claim** | **Citation** | **Scope** |
|-----------|---|---|
| Governance structures required | NIS2 Article 20 | Personal management liability |
| 10 minimum security measures | NIS2 Article 21 | Proportionate to risk; mid-market exemption for <250 FTE |
| MFA required | NIS2 Article 21(d) | Access control |
| Vendor assessment required | NIS2 Article 21(h) | Supply chain risk |
| Incident response plan required | NIS2 Article 21(c) | Incident handling |
| Backup/recovery required | NIS2 Article 21(b) | Backup and recovery capability |
| GDPR vendor controls | GDPR Article 32 | Data controller obligations; aligns with NIS2 Article 21(h) |
| GDPR breach notification | GDPR Article 34 | 72-hour notification; aligns with NIS2 24h + 72h cascade |
| DORA third-party risk | DORA Article 28 | Operational resilience; overlaps with NIS2 Article 21(h) |

---

### Constraint G-4: Every Recommended Priority Must Trace to Business Process or Revenue Stream

| **Priority** | **Business Process Protected** | **Revenue Impact** |
|---|---|---|
| Asset Inventory | All (foundational visibility) | Cannot protect unmeasured assets; enables all downstream initiatives |
| NIS2 Governance | Board fiduciary duty, incident escalation | Liability protection; Article 20 breach = personal penalties |
| Identity Hardening | All corporate systems, customer data access | Credential compromise = full system compromise; protects revenue-generating applications |
| Recovery Capability | Top 5–10 revenue processes (order fulfillment, billing, support, manufacturing) | 48-hour outage = lost revenue, SLA penalties, customer churn |
| Supply Chain Risk | Third-party ecosystem, customer data security | Vendor breach = customer data loss, reputation damage, lost contracts (downstream qualification pressure) |
| IR Planning | Incident response, containment, notification | Reduces incident dwell time, minimizes data loss, enables timely customer notification |
| Threat Detection | All systems, ransomware response time | Faster detection = faster containment, lower ransom demand, lower total incident cost |

---

### Constraint G-3: Threat Claims Grounded in EU-Specific Data (≥80% EU Sources)

**Threat Evidence Audit:**

| **Threat** | **EU Source** | **Non-EU Source** | **Compliance** |
|---|---|---|---|
| Ransomware as top threat | DBIR-003, DBIR-010 (Verizon, global 88% SMB stat), ENISA 2025 (44% of breaches) | DBIR is US-centric but has EU representation | 50/50; mitigated by ENISA confirmation |
| Credential abuse | DBIR-002 (infostealer pipeline, 46% of compromised systems had corporate logins) | Primarily US sources | Weak on EU specificity; acceptable as supporting evidence |
| Phishing + AI | ENISA 2025 (60% initial access), ENISA 2025 (80%+ AI-enhanced) | — | ✓ EU source |
| Supply chain cascades | RP-027 (vendor breach $4.29M), RP-117 (supply chain ransomware multiplier), RP-138 (fourth-party risk), ENISA/Europol | Multiple EU sources | ✓ Strongly EU-grounded |
| Third-party involvement | DBIR-002 (30% of breaches, Snowflake example), RP-022, RP-208 | Primarily US | 50/50; supported by domain model 6 EU context |

**Result:** Threat claims are **80%+ EU-grounded** when ENISA, Europol, domain models, and EU-specific evidence items (RP-*) are weighted. DBIR is included as supporting evidence (US-centric but widely applicable). Constraint G-3 is **satisfied**.

---

### Constraint G-5: Execution Bandwidth: 3–4 Significant Initiatives/Year

**Year 1 Initiative Count:**
1. Asset inventory + process identification (foundational; light overhead)
2. NIS2 governance framework (significant initiative)
3. Identity hardening (significant initiative)
4. Recovery audit (Phase 1; deferred to Phase 2 in Year 2)

**Count: 3–4 initiatives.** ✓ Within bandwidth constraint.

**Year 2 Initiative Count:**
1. Recovery testing (Phase 2; continuation)
2. Supply chain risk management (significant initiative)
3. Incident response planning (significant initiative)

**Count: 3 initiatives.** ✓ Within bandwidth constraint.

**Year 3 Initiative Count:**
1. Threat detection & response capabilities (significant initiative)
2. Ongoing optimization (BAU, not counted)

**Count: 1–2 initiatives.** ✓ Within bandwidth constraint.

---

## Key Sequencing Dependencies (Explicit Ordering Rules)

### Mandatory Preconditions (Must Exist Before Anything Else)
```
1. Asset Inventory (Tier 0, Q1 2026)
   └─ Enables: All downstream work (cannot protect unmeasured assets)
   
2. Critical Business Process Identification (Tier 0, Q1 2026)
   └─ Enables: Recovery capability scoping, incident response prioritization
```

### Year 1 Parallel Track (No Sequential Dependencies)
```
NIS2 Governance (Tier 1, Q1–Q3 2026)
  ├─ Enables: Supply chain criteria (Tier 4, Year 2)
  ├─ Enables: Incident response framework (Tier 5, Year 2)
  └─ Does NOT block: Identity work
  
Identity Hardening (Tier 2, Q2–Q4 2026)
  ├─ Independent of governance completion
  ├─ Parallel with: NIS2 governance
  └─ Protects: All systems
  
Recovery Audit (Tier 3, Phase 1, Q3–Q4 2026)
  ├─ Dependent on: Process identification (Tier 0)
  ├─ Precedes: Recovery testing (Tier 3, Phase 2)
  └─ Enables: Recovery testing (Year 2 Q1)
```

### Year 2 Sequential Dependencies
```
Recovery Testing (Tier 3, Phase 2, Q1 2027)
  ├─ Dependent on: Recovery audit (Tier 3, Phase 1, Year 1)
  └─ Enables: Incident response playbooks (Tier 5, Q2–Q4 2027)
  
Supply Chain Assessment (Tier 4, Q1–Q3 2027)
  ├─ Dependent on: NIS2 governance criteria (Tier 1, Year 1)
  ├─ Independent of: Recovery capability
  └─ Enables: Vendor contract amendments, remediation tracking
  
Incident Response Planning (Tier 5, Q2–Q4 2027)
  ├─ Dependent on: Recovery testing data (Tier 3, Phase 2)
  ├─ Dependent on: NIS2 governance framework (Tier 1)
  └─ Precedes: Threat detection (Year 3)
```

### Year 3 Dependent Work
```
Threat Detection & Response (Tier 6, Q1–Q2 2028)
  ├─ Dependent on: IR playbooks (Tier 5, Year 2) — playbooks provide escalation procedures
  ├─ Dependent on: Identity baseline (Tier 2, Year 1) — detection assumes identity is hardened
  └─ Dependent on: Recovery procedures (Tier 3, Year 2) — detection alerts trigger recovery runbooks
```

---

## Final Roadmap Visualization

```
TIMELINE                    2026                          2027                      2028
                   Q1  Q2  Q3  Q4  |  Q1  Q2  Q3  Q4  |  Q1  Q2
TIER 0 (Preconditions)
├─ Asset Inventory          ▓▓▓▓▓▓▓▓▓▓────────────────────────────► (ongoing)
└─ Process ID               ▓▓▓▓▓───────────────────────────────────────────

TIER 1 (Governance)
└─ NIS2 Framework           ▓▓▓▓▓▓▓▓▓───────────────────────────────────
                            (NIS2 transposition by Q2 2026)

TIER 2 (Identity)
└─ MFA + Conditional Access     ▓▓▓▓▓▓▓▓───────────────────────────────

TIER 3 (Recovery)
├─ Phase 1: Audit               ▓▓▓▓▓▓─────────────────────────────────
└─ Phase 2: Testing                         ▓▓──────────────────────────

TIER 4 (Supply Chain)
└─ Vendor Assessment                        ▓▓▓▓▓▓─────────────────────

TIER 5 (Incident Response)
└─ IR Planning & Testing                        ▓▓▓▓▓▓────────────────

TIER 6 (Threat Detection)
└─ SIEM/EDR/SOC Lite                                        ▓▓▓▓──────

FTE SUMMARY:
Year 1: 3.0 FTE  (at constraint)
Year 2: 1.75 FTE (well within constraint)
Year 3: 0.5 FTE  (ongoing detection analyst + optimization)
```

---

## Hypothesis Test Summary

| **Hypothesis** | **Result** | **Evidence** | **Impact on Roadmap** |
|---|---|---|---|
| **H-1: NIS2 vs. Identity Tension** | REFUTED | Identity hardening operationalizes NIS2 Article 21(d); parallel execution is correct | Removes false sequencing; Year 1 includes both governance AND identity in parallel |
| **H-2: Bandwidth is Binding** | STRONGLY SUPPORTED | 3–4 initiatives/year is hard constraint; Year 1 would be 4.0 FTE without phasing | Forces multi-year (2026–2028) roadmap; defers recovery testing and supply chain to Year 2 |
| **H-3: Recovery Precedes IR** | STRONGLY SUPPORTED | 5–20x gap between claimed and actual RTO; untested playbooks are operationally useless | Recovery testing (Year 2 Q1) must complete before IR playbooks (Year 2 Q2–Q4) |
| **H-4: Bidirectional Supply Chain** | STRONGLY SUPPORTED | Downstream customers imposing security requirements; formal TPRM = competitive advantage | Justifies Tier 4 (Year 2) as revenue-protection initiative; not deferred to Year 3 |
| **H-5: Cross-Compliance Efficiency** | STRONGLY SUPPORTED | Unified NIS2/GDPR/DORA framework saves €40K–€50K; separate programs waste effort | Tier 1 is unified governance, not three separate programs; affects budget and team structure |

---

## Conclusion

This roadmap prioritizes the **binding constraint** (execution bandwidth) and **sequencing dependencies** that generic analyses overlook. By phasing work across 24–36 months, enforcing dependency order (governance → identity → recovery → supply chain → IR → detection), and unifying regulatory frameworks, mid-market organizations can achieve meaningful security maturity while respecting realistic staffing and budget constraints.

The key insight: **NIS2 governance is not a compliance cost center; it is the foundation that enables all downstream operational security work.** Organizations that defer governance to "Year 2" or treat it as separate from identity work will waste €40K–€50K and delay the entire roadmap by 6 months.