# Claude Generic Output (No GOSTA)

**Prompt used:** "You are a cybersecurity expert. What should an EU-based mid-market CISO (company size 50-500 employees) prioritize in 2026, considering NIS2 compliance, the current threat landscape, limited budget and staff, supply chain security requirements, and business continuity? Give me a structured priority list with reasoning for each item."

**Model:** Claude (Opus 4.6)
**Date:** 2026-04-08
**Context:** Zero framework, zero domain models, zero structure. Raw prompt.

---

## Tier 1: Foundational Compliance & Risk Management (Must Do)

**1. NIS2 Compliance Framework Implementation**
- Reason: NIS2 becomes enforceable in October 2024 (already in effect). Non-compliance carries significant fines (up to 10M EUR or 2% revenue) and reputational damage. Mid-market firms are now in-scope as "operators of essential services" or "digital service providers."
- Action: Conduct gap assessment against NIS2 Annex I (incident notification, supply chain security, cryptography, access control). Designate NIS2 accountability officer. Document compliance posture.

**2. Supply Chain Risk Management Program**
- Reason: NIS2 explicitly requires supply chain security measures. Ransomware and third-party breaches remain top vectors. Mid-market firms are attractive targets precisely because they're easier than large enterprises but have valuable data/access.
- Action: Inventory all critical vendors (especially cloud, software, infrastructure). Require security attestations (SOC 2, ISO 27001, or tailored questionnaires). Establish SLA breach clauses. Prioritize vendors with access to customer data or critical systems.

**3. Incident Response & Business Continuity Planning**
- Reason: NIS2 mandates incident notification within 24 hours (72 for GDPR). Ransomware dwell time averages 228 days — early detection prevents catastrophic loss. Limited staff means you need automation and clear escalation.
- Action: Document IR plan with clear roles, contact trees, and communication templates. Conduct at least one tabletop exercise. Establish SLA for critical system recovery (RTO/RPO). Test backup restoration annually.

## Tier 2: Technical Controls (High Impact, Moderate Effort)

**4. Identity & Access Management (IAM) Hardening**
- Reason: ~80% of breaches involve compromised credentials. MFA adoption is now non-negotiable; privileged access is the crown jewel.
- Action: Enforce MFA for all remote access and admin accounts (priority: cloud, email, infrastructure). Implement privileged access management (PAM) for admin credentials. Review user entitlements quarterly.

**5. Vulnerability Management & Patching Discipline**
- Reason: Unpatched vulnerabilities are exploited within days of disclosure. Your limited staff cannot manually track every system. Automation is essential.
- Action: Adopt a free or low-cost vulnerability scanner. Establish SLA: critical patches within 48 hours, high within 2 weeks. Prioritize internet-facing systems and remote access tools.

**6. Endpoint Detection & Response (EDR) or Next-Gen Antivirus**
- Reason: Ransomware, info-stealers, and APTs often start at endpoints. Traditional AV is insufficient.
- Action: Deploy EDR on critical systems (servers, key workstations). Focus on servers first. Enable behavioral detection and telemetry.

## Tier 3: Governance & Detection (Medium-Term, Scalable)

**7. Security Awareness & Phishing Resilience**
- Reason: Social engineering remains the #1 entry vector. Limited cost; significant ROI.
- Action: Run mandatory training. Deploy email filtering with advanced threat detection. Conduct quarterly phishing simulations.

**8. Logging, Monitoring & SIEM (Cost-Optimized)**
- Reason: NIS2 requires detection capability. You cannot defend what you don't see.
- Action: Centralize logs from critical systems. Use free tools: Wazuh, ELK stack, or cloud-native solutions. Define alert rules for suspicious activity.

**9. Cryptography & Data Protection**
- Reason: NIS2 mandates "appropriate cryptographic security." GDPR requires encryption of sensitive data in transit and at rest.
- Action: Inventory all data flows. Enforce HTTPS/TLS 1.2+ for all web services. Encrypt databases and backups.

## Tier 4: Strategic & Emerging (Ongoing, Lower Immediate Pressure)

**10. Cyber Resilience & Zero Trust Architecture (Multi-Year)**
- Reason: Zero Trust is industry best practice but requires architectural changes. Start small; build over 2-3 years.
- Action: Begin with identity. Gradually enforce network segmentation. Move to least-privilege access.

**11. Threat Intelligence Integration**
- Reason: Understanding adversaries targeting your vertical informs risk prioritization.
- Action: Subscribe to free/low-cost threat feeds. Share IoCs with your SIEM.

---

## Resource Allocation for Limited Budget & Staff

| Priority | Year 1 Budget Est. | FTE Cost | Quick Win? | Compliance Req? |
|----------|------------------|----------|-----------|-----------------|
| NIS2 Assessment | €10-20K | 0.5 | Yes | Yes (mandatory) |
| Vendor Risk Mgmt | €5-15K | 0.3 | Yes | Yes (mandatory) |
| IR/BC Planning | €5-10K | 0.5 | Yes | Yes (mandatory) |
| MFA Rollout | €3-8K | 0.2 | Yes | Yes (implicit) |
| Patching Automation | €2-5K | 0.1 | Yes | Yes (critical controls) |
| EDR (lite) | €10-25K | 0.2 | Partial | Recommended |
| SIEM (free tier + training) | €0-5K | 0.3 | Partial | Recommended |
| **Total Year 1** | **€35-88K** | **~2.2 FTE** | — | — |

---

## Key Success Factors for Mid-Market CISOs

1. Automate ruthlessly. You cannot hire your way out.
2. Start with data flows. Know where sensitive data lives.
3. Buy cheap, build culture. Tools matter less than discipline.
4. Align with business continuity. Frame security as business enablement, not cost center.
5. Document everything for auditors. NIS2 and GDPR auditors want evidence of intent, not perfection.
