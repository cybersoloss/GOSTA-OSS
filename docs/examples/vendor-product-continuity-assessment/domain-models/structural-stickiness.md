# Domain Model: Structural Stickiness Assessment

**Domain Code:** STICK-1
**Source:** Domain expertise — synthesized from publicly documented vendor dependency analysis, IT migration research, and third-party risk management frameworks
**Enhancement Sources:** None
**Application Context:** Evaluating the depth of organizational dependency on a vendor-product combination, serving risk determination exclusively — NOT viability assessment
**Created:** 2026-04-20
**Purpose:** Provides evaluation criteria for assessing how deeply embedded a vendor-product is in organizational operations, what migration would cost, and how stickiness combines with viability to produce risk exposure. This model serves risk determination (the "what happens if the vendor fails" question) and must not be conflated with viability assessment (the "will the vendor fail" question)

---

## Scoring Dimensions

This model uses a distinct scoring approach from viability-oriented domain models:

- **Exposure Intensity** (1-10): How deeply embedded the vendor-product is in critical operations. 1 = peripheral tool with ready alternatives. 10 = deeply woven into core revenue-generating processes with no practical alternative.
- **Migration Complexity** (1-10): How difficult and costly a full migration away from this vendor-product would be. 1 = swap-in replacement available, migration achievable in weeks. 10 = multi-year migration program with significant operational risk during transition.
- **Confidence** (low / medium / high): Assessor's confidence in the exposure and complexity scores, based on evidence quality and completeness.

---

## 1. Core Concepts

### Integration Depth

The number and criticality of technical touchpoints between the vendor-product and the organization's infrastructure. Integration depth encompasses API connections, data feeds, authentication dependencies, policy enforcement points, log aggregation, alerting chains, and workflow triggers. A product with 3 API integrations into non-critical systems has fundamentally different stickiness than a product with 40 integrations into authentication, compliance, and incident response workflows.

Measure by cataloging every integration point and classifying each as critical (failure causes operational impact within 4 hours), important (impact within 24 hours), or convenience (impact is workflow degradation, not operational failure).

**Boundary:** Integration depth covers technical connections. It does NOT cover contractual or licensing dependencies, which are assessed under Recovery Cost Estimation.

**Common misapplication:** Counting integrations without weighting by criticality. Ten convenience integrations create less stickiness than one critical integration into an authentication chain.

### Migration Timeline

Realistic estimation of the calendar time required to fully migrate away from the vendor-product. Industry data consistently shows that 61% of technology migrations exceed planned timelines by 40-100%, with the primary causes being underestimated data migration complexity, discovered undocumented integrations, and parallel-running requirements that extend beyond initial estimates.

Estimate by decomposing the migration into phases (evaluation, procurement, data migration, integration rebuild, testing, parallel running, cutover, decommission) and applying historical adjustment factors. A vendor-quoted "90-day migration" should be planned as 150-200 days absent strong contrary evidence.

**Boundary:** Migration timeline covers calendar duration. It does NOT cover migration cost, which is assessed under Recovery Cost Estimation.

**Common misapplication:** Using vendor-provided migration timelines without adjustment. Vendors have structural incentives to understate competitor migration difficulty and overstate their own migration ease.

### Data Dependency

The extent to which organizational data resides within or is processed through the vendor-product, including: data retention limits (vendor-imposed maximums), export mechanisms (API-based vs. manual download vs. no export path), format portability (standard formats vs. proprietary schemas), and historical data accessibility (whether exported data retains full fidelity or loses context, relationships, or metadata).

Score by mapping each data type held by the vendor and assessing: Can it be exported? In what format? With what fidelity loss? Within what time constraints?

**Boundary:** Data dependency covers data portability and retention. It does NOT cover data security or privacy, which are compliance concerns rather than stickiness concerns.

**Common misapplication:** Assuming API availability equals data portability. An API that exposes current records but not historical data, audit trails, or relationship metadata provides incomplete portability.

### Internal Build Feasibility

A buy-vs-build analysis for replacing the vendor-product's capabilities with internally developed solutions. Factors include: engineering team capability, available development capacity, maintenance burden of a custom solution, regulatory certification requirements that custom solutions must independently satisfy, and the opportunity cost of diverting engineering resources from core business functions.

Assess by estimating: build timeline, ongoing maintenance FTE requirement, certification/compliance effort, and total 3-year cost of ownership. Compare against alternative vendor options, not just against the current vendor's pricing.

**Boundary:** Covers the technical and economic feasibility of self-building. Does NOT cover whether self-building is strategically desirable, which is a governance decision.

**Common misapplication:** Underestimating ongoing maintenance cost. The build cost is typically 30-40% of the 3-year total cost of ownership; the remaining 60-70% is maintenance, updates, and compliance re-certification.

### Standards-Based Integration vs. Proprietary Lock-in

The degree to which the vendor-product uses open standards (REST APIs, SCIM, SAML, syslog, CEF, STIX/TAXII, OpenTelemetry) versus proprietary protocols, data formats, or integration mechanisms. Standards-based integration reduces migration complexity because replacements can connect through the same interfaces. Proprietary integration increases stickiness because every integration must be rebuilt from scratch during migration.

Assess by classifying each integration point as standards-based or proprietary and weighting by integration criticality.

**Boundary:** Covers integration protocol and format choices. Does NOT cover product functionality or quality.

**Common misapplication:** Treating API availability as evidence of standards compliance. A proprietary API is still proprietary — the standard is the protocol and data format, not the existence of an API endpoint.

### Recovery Cost Estimation

A structured framework for estimating total migration cost across six categories: (1) **Data migration** — extraction, transformation, loading, and validation of all organizational data from the current vendor to the replacement; (2) **Integration rebuild** — re-implementing every integration point with the replacement product's interfaces; (3) **Parallel running** — operating both current and replacement products simultaneously during transition, including duplicate licensing costs; (4) **Compliance remediation** — re-certification, re-audit, and updated documentation required by regulatory frameworks when changing a compliance-relevant vendor; (5) **Revenue disruption** — estimated revenue impact from reduced operational capability during transition; (6) **Opportunity cost** — value of other initiatives delayed or cancelled to fund and staff the migration.

Estimate each category independently with low/medium/high ranges. The sum provides total recovery cost exposure.

**Boundary:** Covers financial and operational costs of migration. Does NOT cover the probability of needing to migrate, which is a viability concern.

**Common misapplication:** Omitting opportunity cost. Organizations routinely estimate direct migration costs while ignoring the strategic cost of diverting resources from growth initiatives for 12-24 months.

### Supply Chain Cascade Multiplier

When the vendor-product serves not only the assessing organization but also that organization's intermediaries, partners, or downstream customers, vendor disruption creates cascading impacts. A vendor failure affecting the organization's own operations is a direct risk. A vendor failure that simultaneously affects the organization's service delivery to its own customers is an amplified risk. The cascade multiplier estimates the ratio of total impact (direct + downstream) to direct impact alone.

Assess by mapping: Does this vendor-product participate in services delivered to our customers? Do our partners or intermediaries depend on the same vendor? Would vendor disruption trigger our own SLA violations or contractual penalties?

**Boundary:** Covers downstream impact amplification. Does NOT cover the vendor's own supply chain risks (vendor's vendors), which is a separate assessment.

**Common misapplication:** Ignoring intermediary dependencies. If the organization uses a managed service provider who depends on the same underlying vendor, the cascade multiplier applies even though the organization has no direct relationship with the underlying vendor.

### Escrow and Continuity Guarantees

The contractual and technical mechanisms that provide protection if the vendor ceases operations: source code escrow, data escrow, continuity-of-service agreements, transition assistance clauses, and insurance bonds. The assessment evaluates both the existence of these mechanisms and their practical enforceability — an escrow clause that triggers only on formal bankruptcy (not on product discontinuation or acquisition) provides limited protection.

Assess by reviewing contract terms and testing trigger conditions: Under what specific scenarios do continuity guarantees activate? Do they cover acquisition-driven product discontinuation? Is the escrow current (updated within 12 months)?

**Boundary:** Covers contractual protection mechanisms. Does NOT cover the operational feasibility of exercising those mechanisms (whether the organization could actually use escrowed source code is an Internal Build Feasibility question).

**Common misapplication:** Treating escrow existence as sufficient protection. Source code escrow is only valuable if the organization has the capability and resources to build, deploy, and maintain the product from source — which most organizations do not.

### Stickiness-Viability Combination Matrix

The risk determination framework that combines stickiness assessment (this model) with viability assessment (other domain models) to produce actionable risk classification:

| | **High Viability** | **Medium Viability** | **Low Viability** |
|---|---|---|---|
| **High Stickiness** | Acceptable — monitor | Elevated — contingency plan required | **MAXIMUM RISK** — immediate action |
| **Medium Stickiness** | Acceptable | Moderate — review cycle acceleration | High — migration planning triggered |
| **Low Stickiness** | Minimal | Low — standard monitoring | Moderate — replacement evaluation |

The maximum-risk quadrant (high stickiness + low viability) demands immediate executive attention because it combines the highest migration cost with the highest probability of needing to migrate. Organizations in this quadrant face the worst-case scenario: expensive migration under time pressure.

**Boundary:** Covers the combination logic between stickiness and viability. The matrix is the integration point — stickiness and viability must be assessed independently before combination.

**Common misapplication:** Allowing stickiness to inflate viability scores. The reasoning "we're deeply integrated, so the vendor must be viable because we chose well" is a cognitive bias, not an analytical conclusion. Stickiness and viability must be scored by separate analytical processes.

---

## 2. Concept Relationships

**Prerequisites:** Integration Depth and Data Dependency must be mapped before Recovery Cost Estimation can be performed — cost estimation requires knowing what must be migrated and rebuilt. Standards-Based Integration assessment must precede Migration Timeline estimation — proprietary vs. standards-based integration directly determines rebuild complexity.

**Tensions:** Internal Build Feasibility creates tension with Recovery Cost Estimation — building internally eliminates vendor dependency but may increase total cost of ownership. Escrow and Continuity Guarantees create tension with Migration Timeline — escrow provides theoretical protection but exercising it extends the actual recovery timeline because building from source is slower than migrating to an established alternative.

**Amplifiers:** Supply Chain Cascade Multiplier amplifies every other stickiness dimension — high cascade multiplier means that underestimating Integration Depth, Data Dependency, or Migration Timeline has proportionally larger consequences. The Stickiness-Viability Combination Matrix amplifies the urgency of all stickiness findings when viability scores are low.

---

## 3. Quality Principles

- **QP-1:** Integration catalog completeness — Every assessment must include a complete integration catalog with criticality classification (critical/important/convenience). Evaluate by comparing the catalog against architecture diagrams, API gateway logs, and network flow data. An assessment with fewer than 80% of actual integrations cataloged will materially understate stickiness.
- **QP-2:** Migration timeline reality adjustment — All migration timelines must include a historical adjustment factor. Unadjusted vendor-provided or internally estimated timelines are not acceptable as final estimates. Apply a minimum 1.5x multiplier to internal estimates and 2.0x to vendor-provided estimates absent specific historical evidence supporting lower multipliers.
- **QP-3:** Independent stickiness and viability scoring — Stickiness scores must be produced without reference to viability scores, and vice versa. The combination matrix is applied only after both assessments are independently complete. Evaluate by checking whether the stickiness assessment references vendor financial health, strategic direction, or other viability indicators.

---

## 4. Anti-Patterns

- **AP-1:** Stickiness-as-viability confusion — Reasoning that high stickiness implies high viability ("we depend on them heavily, so they must be reliable") or that high viability eliminates stickiness concerns ("they're a strong vendor, so dependency doesn't matter"). These are independent dimensions that must be assessed separately and combined only through the matrix. Detect by checking whether stickiness arguments reference vendor health or viability arguments reference integration depth.
- **AP-2:** Shelfware false positivity — Counting vendor products that are licensed but minimally deployed as evidence of integration depth. A product that was purchased as part of a bundle but is used by fewer than 10% of eligible users has near-zero stickiness regardless of its licensing status. Detect by requiring usage metrics (active users, daily events processed, integrations exercised) alongside licensing data for every product counted toward stickiness.
- **AP-3:** Escrow comfort syndrome — Treating the existence of escrow or continuity clauses as a material reduction in stickiness without evaluating enforceability, trigger conditions, and organizational capability to exercise the protections. Detect by checking whether escrow is cited as a mitigating factor without corresponding analysis of trigger scenarios and exercise feasibility. Address by requiring a tabletop exercise: "If the escrow triggered today, what would we actually do with it?"
