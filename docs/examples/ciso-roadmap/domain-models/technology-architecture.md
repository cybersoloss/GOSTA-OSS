# Domain Model: Technology & Architecture

**Source:** Domain expertise — synthesized from EU mid-market technology adoption patterns, Microsoft 365/Azure AD prevalence data, SaaS dependency research, identity architecture best practices (NIST 800-63, ENISA guidance), and cloud security posture management patterns
**Application Context:** Evaluating CISO priority decisions through the lens of technology reality — what is actually deployed, what architectural patterns create risk, and what technology investments yield the highest security return
**Created:** 2026-04-08
**Purpose:** [Operational] Provides technology-reality grounding so that priority assessments account for the actual technology stack and architectural patterns of EU mid-market organizations rather than idealized reference architectures

---

## 1. Core Concepts

### Microsoft Monoculture and Concentration Benefit

The vast majority of EU mid-market organizations run Microsoft 365 as their core productivity platform, with Azure AD (Entra ID) as their identity provider, Exchange Online for email, and often Microsoft Defender for endpoint protection. This monoculture creates both concentration risk (Microsoft outage = total organizational stop) and concentration benefit (a single platform investment in Microsoft security features — Conditional Access, Defender for Endpoint, Purview — covers a disproportionate share of the attack surface).

For priority evaluation, this means: before recommending any new security tool, check whether the required capability already exists in the organization's Microsoft licensing. Many mid-market organizations pay for security features (Conditional Access, DLP, advanced audit logging) they haven't activated. Activating existing licensed capabilities has zero acquisition cost and minimal integration overhead.

**Boundary:** Microsoft monoculture covers the dominant technology platform in EU mid-market. It does NOT imply that Microsoft-only security is sufficient — gaps exist in areas like backup (Microsoft's native retention is not backup), advanced threat detection for non-Microsoft systems, and operational technology.

**Common misapplication:** Assuming Microsoft Defender alone constitutes adequate endpoint protection. For organizations that are pure Microsoft shops with relatively simple environments, it may be sufficient. For organizations with significant non-Microsoft infrastructure, Linux servers, or OT environments, dedicated solutions are needed for those segments.

### Identity as the Architectural Control Plane

In cloud-first, SaaS-dependent mid-market environments, identity is the de facto perimeter. Every SaaS application, cloud service, VPN, and remote access tool authenticates through the identity provider. Compromising the identity layer (Azure AD/Entra ID) provides authenticated access to everything — no lateral movement needed in the traditional sense.

This makes identity hardening the highest-leverage architectural investment: MFA enforcement, Conditional Access policies, privileged access management, dormant account cleanup, and service account governance. Each of these controls protects the entire technology stack, not just one system.

**Boundary:** Identity as control plane covers authentication and authorization architecture. It does NOT cover data-level access controls within applications, which are application-specific and managed differently.

**Common misapplication:** Treating MFA deployment as the endpoint of identity hardening. MFA is the floor, not the ceiling. Post-MFA identity risks include: session token theft, MFA fatigue attacks, over-privileged service accounts, dormant accounts with active credentials, and lack of conditional access policies (allowing authentication from any location/device).

### SaaS Dependency and Shadow IT

Mid-market organizations typically use 50-200 SaaS applications, with IT formally managing 15-30 of them. The remainder — shadow IT — is adopted by business units without security review, creating unmonitored data flows, unmanaged authentication, and invisible third-party dependencies. Each SaaS application is a potential data exfiltration path and a supply chain dependency.

Priority evaluation must account for the gap between managed and actual SaaS usage. A CISO who secures the 20 known applications while ignoring the 80 unknown ones has secured 25% of the SaaS attack surface.

**Boundary:** SaaS dependency covers cloud application usage and its security implications. It does NOT cover on-premises application security or custom-developed software.

### Asset Inventory as the Foundational Capability

You cannot protect what you don't know you have. Mid-market organizations frequently lack complete asset inventories — especially for internet-facing systems, cloud resources created outside IT processes, IoT/OT devices, and SaaS applications. Without asset inventory, vulnerability management is incomplete (unscanned systems), access control is porous (unknown access paths), and incident response is blind (unknown blast radius).

Asset inventory is the unsexy foundational capability that most priority lists undervalue because it doesn't directly reduce risk — it enables risk reduction by other controls. It is a force multiplier, not a direct defense.

**Boundary:** Asset inventory covers knowing what technology assets exist, where they are, who owns them, and what they connect to. It does NOT cover asset valuation or risk assessment — those are separate processes that depend on inventory as input.

### Patching and Configuration Hygiene as Persistent Attack Surface

ENISA and multiple incident datasets consistently show that exploitation of known vulnerabilities — with patches available — remains a top attack vector. Mid-market organizations struggle with patching not because patches don't exist but because: (a) they don't know all their assets (inventory gap), (b) they lack automated patch deployment for heterogeneous environments, (c) they fear breaking production systems, and (d) they have no patch SLA discipline.

Secure configuration is the sibling problem: default configurations, unnecessary services, overly permissive network rules, and legacy remote access tools create attack surface that doesn't require vulnerability exploitation at all.

**Boundary:** Patching and configuration covers vulnerability remediation and hardening for known assets. It does NOT cover zero-day vulnerabilities (by definition unpatched) or application-level security (code quality, API security).

---

## 2. Concept Relationships

**Prerequisites:** Asset Inventory must exist before Patching and Configuration Hygiene can operate comprehensively — you cannot patch what you don't know about. Identity as Control Plane understanding must precede SaaS Dependency management — identity federation governs SaaS access.

**Tensions:** Microsoft Monoculture Concentration Benefit (use what you have) creates tension with the need for defense-in-depth (avoid single-vendor dependency). SaaS Dependency management requires visibility investment that competes with Identity hardening for the same limited security budget and staff time. Asset Inventory is foundational but produces no direct risk reduction, creating tension with the urgency to implement controls that directly block attacks.

**Amplifiers:** Asset Inventory amplifies everything — Patching becomes comprehensive, Identity governance becomes complete, SaaS Dependency becomes visible. Identity as Control Plane amplifies Microsoft Monoculture Benefit — hardening Azure AD/Entra ID secures the entire Microsoft ecosystem and all federated SaaS applications simultaneously.

---

## 3. Quality Principles

- **QP-1:** Existing-capability-first evaluation — Before recommending any new tool, verify whether the required capability exists in the organization's current licensing (especially Microsoft E3/E5 features). Evaluate by checking tool recommendations against the organization's license inventory.
- **QP-2:** Identity-first architecture — Security architecture recommendations must prioritize the identity layer over network and endpoint layers when the organization is cloud-first/SaaS-dependent. Evaluate by checking whether the recommended architecture secures identity before adding network or endpoint controls.
- **QP-3:** Asset completeness metric — Any vulnerability management or patching recommendation must include an asset coverage estimate. Evaluate by checking whether the recommendation acknowledges and addresses the gap between known and actual assets.
- **QP-4:** Configuration drift prevention — Secure configuration recommendations must include mechanisms for maintaining configuration over time, not just initial hardening. Evaluate by checking whether configuration monitoring or drift detection is included.

---

## 4. Anti-Patterns

- **AP-1:** Shelfware accumulation — Acquiring security tools without the staff or processes to operate them. Creates false confidence and wastes budget. Detect by inventorying security tools and checking utilization rates (features enabled, alerts investigated, reports reviewed). Address by consolidating to fewer tools operated at full capability.
- **AP-2:** Network-perimeter thinking in a cloud-first environment — Investing in firewalls and network segmentation as primary defenses when 80%+ of business applications are SaaS and users work remotely. The perimeter dissolved years ago for most mid-market organizations. Detect by checking whether security architecture assumes a defended network boundary. Address by shifting investment to identity, endpoint, and cloud security.
- **AP-3:** Inventory procrastination — Continuously deferring asset inventory because it's unglamorous and doesn't directly stop attacks. Creates a compounding problem where every subsequent security initiative operates on incomplete information. Detect by asking for a current, complete asset inventory. Address by making asset inventory a prerequisite for all other initiatives.

---

## 5. Hypothesis Library

- **HL-1:** "If we activate all security features included in our existing Microsoft licensing before purchasing any new tools, then we will close 30-50% of our security gaps at zero incremental tool cost, because Microsoft Monoculture means most mid-market organizations are paying for capabilities they haven't enabled."
- **HL-2:** "If we implement Conditional Access + MFA + privileged access governance in Azure AD before any other security initiative, then we will block the largest single category of attacks, because Identity as Control Plane means identity compromise provides access to the entire technology estate."
- **HL-3:** "If we conduct a comprehensive asset and SaaS discovery before building our vulnerability management program, then our patching coverage will increase from an estimated 60-70% to 90%+, because Asset Inventory completeness directly determines the ceiling of patch coverage."

---

## 6. Guardrail Vocabulary

- **GV-1:** No new security tool shall be recommended without first verifying that the required capability does not exist in the organization's current technology licensing — Severity: hard — Tool sprawl is the default failure mode of mid-market security programs.
- **GV-2:** Security architecture recommendations for cloud-first organizations must not assume a network perimeter as primary defense — Severity: hard — Network perimeter thinking in SaaS-dependent environments misallocates resources.
- **GV-3:** Vulnerability management and patching recommendations must acknowledge and address the asset inventory gap — Severity: soft — Patching programs operating on incomplete asset inventories provide false coverage confidence.
