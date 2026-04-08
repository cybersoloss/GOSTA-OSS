# Domain Model: EU Threat Landscape 2025-2026

**Source:** Domain expertise — synthesized from ENISA Threat Landscape 2025 (published October 2025, covering July 2024–June 2025, 4,875 incidents analyzed), ENISA SME threat reports, Europol IOCTA, and publicly available ransomware tracking data
**Application Context:** Evaluating CISO priority decisions for EU-based mid-market organizations (50-500 employees) based on actual threat exposure rather than vendor-driven fear narratives
**Created:** 2026-04-08
**Purpose:** [Operational] Provides threat reality grounding so that priority assessments reflect what actually compromises EU mid-market organizations, not what generates vendor revenue or conference talks

---

## 1. Core Concepts

### Availability Attacks as the Dominant Incident Type

ENISA's 2025 analysis shows DDoS attacks accounting for 77% of reported incidents in the EU. This is driven by hacktivist activity — particularly geopolitically motivated groups targeting EU public administration and organizations perceived as supporting Ukraine. For mid-market organizations, DDoS exposure depends heavily on internet-facing service dependency: a B2B SaaS company is existentially exposed; a manufacturing firm with minimal web presence is barely affected.

This concept applies to priority evaluation by requiring that DDoS resilience assessment be calibrated to business model, not applied uniformly. A CISO who invests heavily in DDoS mitigation for an organization with no revenue-critical internet-facing services is misallocating budget.

**Boundary:** Availability attacks cover network-layer and application-layer denial of service. They do NOT cover availability loss from ransomware (covered separately) or from infrastructure failure, which is a business continuity concern.

**Common misapplication:** Treating the 77% statistic as meaning DDoS is the most important threat. Incident count ≠ impact. Ransomware incidents are far fewer but far more damaging per incident to mid-market organizations.

### Ransomware as the Dominant Destructive Threat

Ransomware accounts for 81.1% of cybercrime incidents targeting EU organizations (ENISA 2025). The threat has evolved: double and triple extortion (encryption + data theft + DDoS/customer notification), Ransomware-as-a-Service (RaaS) lowering operator skill requirements, increasing targeting of backup systems, and exploitation of identity weaknesses as primary entry vector. Average dwell time before encryption continues to provide a detection window, but mid-market organizations typically lack the monitoring capability to exploit it.

For mid-market organizations, ransomware represents the highest-impact realistic threat. The combination of operational disruption, data loss, extortion payment pressure, regulatory notification obligations (NIS2 + GDPR), reputational damage, and potential business failure makes ransomware the threat against which recovery capability must be explicitly tested.

**Boundary:** Ransomware covers the full extortion lifecycle from initial access through encryption/exfiltration to negotiation/payment/recovery. It does NOT cover data theft without extortion (which is a data breach) or hacktivism-motivated data leaks.

**Common misapplication:** Focusing ransomware defense exclusively on prevention (endpoint protection, email filtering) without testing recovery capability. Prevention fails at a non-zero rate; recovery readiness determines whether the incident is survivable.

### Credential Abuse and Identity-Based Attack Chains

Phishing (including vishing, malspam, malvertising) accounts for approximately 60% of observed initial access vectors (ENISA 2025). The attack chain typically follows: phishing/credential stuffing → valid credential acquisition → lateral movement via identity systems → privilege escalation → data access/exfiltration/encryption. AI-enhanced phishing campaigns reportedly represent over 80% of social engineering activity by early 2025, making traditional email-based awareness training less effective.

For mid-market organizations, identity is the critical control surface because: (a) it is the most common entry point, (b) weak identity controls (no MFA, shared admin accounts, dormant accounts) are disproportionately present in mid-market environments, and (c) identity hardening has the highest risk-reduction-per-euro of any control category.

**Boundary:** This covers identity as an attack surface. It does NOT cover identity management as a compliance requirement (covered in regulatory domain model) or identity technology selection (covered in technology domain model).

**Common misapplication:** Treating MFA as a complete identity solution. MFA addresses credential theft but not session hijacking, token theft, MFA fatigue attacks, or privileged access abuse by legitimate accounts. Identity hardening is a spectrum, not a checkbox.

### Threat Actor Convergence

ENISA 2025 identifies convergence between previously distinct threat actor categories: state-sponsored groups, hacktivists, and cybercriminals increasingly share tools, tactics, infrastructure, and sometimes personnel. This means mid-market organizations that previously considered themselves below the threshold of state-sponsored targeting may now face state-level capabilities deployed through criminal or hacktivist channels.

This convergence invalidates the common mid-market assumption that "nation-states don't target companies our size." The tools and techniques developed by state actors are now available to financially motivated criminals who absolutely do target mid-market organizations.

**Boundary:** Threat actor convergence covers the blurring of actor categories and capability sharing. It does NOT predict specific targeting — it expands the capability set that any threat actor may bring to bear.

### Supply Chain as Attack Multiplier

ENISA reports increasing targeting of dependency points in digital supply chains. For mid-market organizations, supply chain compromise manifests in two directions: (a) upstream — a software vendor, cloud provider, or MSP the organization depends on is compromised, giving attackers indirect access; (b) downstream — the organization itself is compromised and becomes a vector into its customers' environments. Mid-market firms are attractive targets precisely because they have weaker security than large enterprises but maintain trusted access to larger organizations' networks and data.

**Boundary:** Supply chain attacks cover compromise via trusted third-party relationships. They do NOT cover general vendor risk (service quality, financial stability) — only security-relevant compromise paths.

---

## 2. Concept Relationships

**Prerequisites:** Credential Abuse and Identity-Based Attack Chains must be understood before Ransomware defense can be properly scoped — ransomware entry almost always passes through identity compromise. Supply Chain as Attack Multiplier requires understanding both Credential Abuse (how supplier access is compromised) and Ransomware (the payload commonly delivered through supply chain access).

**Tensions:** Availability Attacks (high volume) create tension with Ransomware (high impact) for monitoring and response prioritization — alert fatigue from DDoS noise can mask ransomware indicators. Threat Actor Convergence creates tension with budget-constrained defense — the expanding capability set of adversaries outpaces mid-market defensive investment, forcing harder triage decisions about which capabilities to defend against.

**Amplifiers:** Credential Abuse amplifies Supply Chain risk — compromised supplier credentials provide authenticated access that bypasses perimeter controls. Threat Actor Convergence amplifies Ransomware severity — state-level reconnaissance and exploitation techniques make ransomware attacks more targeted and harder to prevent.

---

## 3. Quality Principles

- **QP-1:** Threat-to-control mapping specificity — Every defensive priority must trace to a specific threat mechanism (not just a threat category), with reasoning for why the control addresses that mechanism. Evaluate by checking whether defensive investments reference specific attack chain steps.
- **QP-2:** Impact-weighted prioritization — Threat priorities must weight business impact per incident alongside incident frequency. Evaluate by checking whether the priority rationale distinguishes between volume threats (DDoS) and destructive threats (ransomware).
- **QP-3:** Recovery-inclusive defense — Threat assessments must evaluate both prevention probability and recovery capability for each major threat. Evaluate by checking whether each top-5 threat has both a prevention control and a tested recovery path.
- **QP-4:** Evidence-based threat calibration — Threat priorities must cite actual EU threat data (ENISA, Europol, national CERT reports) rather than vendor marketing or US-centric threat reports. Evaluate by checking source citations.

---

## 4. Anti-Patterns

- **AP-1:** Vendor-driven threat perception — Allowing security vendor marketing to define the threat landscape. Vendors emphasize threats their products address, creating distorted prioritization. Detect by checking whether the organization's top-5 threats correspond to their vendor's product categories rather than ENISA/CERT data. Address by anchoring threat assessment to independent, EU-specific threat intelligence.
- **AP-2:** Prevention-only thinking — Investing exclusively in preventing attacks without building and testing recovery capability. Creates brittle defense that catastrophically fails when prevention (inevitably) fails. Detect by checking whether backup restoration, AD recovery, and business process failover have been tested under realistic conditions. Address by allocating explicit budget and calendar time to recovery testing.
- **AP-3:** Frequency-impact conflation — Equating the most common threat (DDoS by volume) with the most dangerous threat (ransomware by impact). Leads to misallocation of limited defensive resources. Detect by checking whether defensive spending correlates with incident count rather than impact assessment. Address by emphasizing impact-weighted threat assessment.

---

## 5. Hypothesis Library

- **HL-1:** "If we implement MFA on all privileged and remote access accounts plus dormant account cleanup, then we will block 60-70% of realistic initial access vectors, because credential abuse accounts for ~60% of initial access and identity hardening directly addresses the most common attack chain entry point."
- **HL-2:** "If we test full recovery from ransomware (AD rebuild, critical system restore, data recovery) at least annually, then we will reduce mean time to recovery by 50%+ compared to untested recovery, because recovery failures during real incidents are almost always caused by untested assumptions about backup integrity, recovery sequencing, and dependency chains."
- **HL-3:** "If we focus monitoring resources on identity anomalies (impossible travel, privilege escalation, service account usage) rather than broad network monitoring, then we will detect more real incidents with fewer staff, because the dominant attack chains pass through identity systems before reaching other layers."

---

## 6. Guardrail Vocabulary

- **GV-1:** Threat priorities must be grounded in EU-specific threat data, not global averages or US-centric reports — Severity: hard — EU threat landscape has distinct characteristics (hacktivist DDoS prevalence, NIS2-driven reporting) that differ materially from US/global patterns.
- **GV-2:** No defensive strategy shall assume prevention is sufficient — every top-5 threat must have a tested recovery path — Severity: hard — Prevention failure is guaranteed at organizational timescales; recovery readiness determines survival.
- **GV-3:** Threat intelligence sources must be assessed for commercial bias — vendor-sponsored reports require corroboration from independent sources (ENISA, Europol, national CERTs) — Severity: soft — Commercial threat reports systematically overweight threats their products address.
