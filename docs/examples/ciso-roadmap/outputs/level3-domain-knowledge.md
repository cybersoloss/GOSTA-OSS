# Level 3 Output: Single Prompt + Domain Model Context

## Prompt
"As a CISO of an EU-based mid-market company (50-500 employees), what should my cybersecurity priorities be for 2026, and in what order should I tackle them?"

## Context Provided
6 domain model files (Regulatory Compliance, Threat Landscape, Operational Capacity, Business Value & Continuity, Technology & Architecture, Supply Chain & Third-Party Risk)

## Output

### Priorities (5 items):
1. Identity & Access Control Foundation (MFA, access review, conditional access, vendor identity mapping) — €5K–€15K
2. Incident Response & Business Continuity Readiness (RTO/RPO definition, quarterly backup testing, IR playbook, breach notification template) — €10K–€25K
3. Vulnerability Management & Patching Discipline (asset enumeration, threat-driven prioritization via CISA KEV, monthly patch cycle) — €2K–€5K
4. Asset Inventory & Supply Chain Risk Mapping (SaaS discovery, critical supplier documentation, contractual baseline, third-party risk register) — €5K–€15K
5. Detection & Response Capability (activate Microsoft Defender, basic SIEM/log aggregation, crown jewel alert thresholds) — €2K–€8K

Plus cross-cutting governance: evidence collection for regulatory reporting

### Notable characteristics:
- 5 priorities (vs Level 1's 11 and Level 2's 10) — domain knowledge about execution bandwidth constraint clearly influenced this
- Budget-realistic: €24K–€68K total, well within mid-market range
- Explicitly leverages Microsoft existing licensing (domain model concept)
- Mentions crown jewels, recovery time gap, vendor assessment paradox — domain concepts are visible
- Sequencing logic present: "Priority 3 requires asset inventory from Priority 4 to be effective"
- References specific regulatory articles (NIS2 Article 21, GDPR)

### What Level 3 does NOT produce (vs Level 4):
- No cross-domain tensions identified
- No forced disagreement — single perspective smooths over trade-offs
- No reference pool evidence (54 scored citations in Level 4 vs 0 here)
- No explicit tension resolution map
- No non-obvious insights section
- Sequencing is logical but not constraint-tested (doesn't verify FTE totals)
- No bidirectional supply chain insight (downstream = revenue play)
- No "recovery must precede IR planning" dependency identified
- No cross-compliance efficiency insight (40-60% reduction)
- Lists Detection as Priority 5 but doesn't explain the EDR scope tension
