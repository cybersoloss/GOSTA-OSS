# Domain Model: Regulatory Compliance Analysis

**Source:** Domain expertise — synthesized from publicly available regulatory compliance frameworks (ISO 27001 structure, GDPR enforcement patterns, general regulatory impact assessment methodology)
**Enhancement Sources:** None
**Application Context:** Governing AI-assisted analysis of regulatory requirements, compliance gap assessment, and implementation prioritization for organizations subject to new or evolving regulations
**Created:** 2026-03-25
**Purpose:** Provides evaluation criteria for tactics and strategies aimed at achieving and maintaining regulatory compliance efficiently and defensibly

---

## 1. Core Concepts

### Regulatory Hierarchy and Precedence

Regulations exist in layers: international treaties/frameworks → national legislation → sector-specific regulations → regulatory guidance/opinions → industry standards → organizational policy. Higher layers constrain lower layers, but lower layers often contain the operational specifics that determine day-to-day compliance. When layers conflict, the highest applicable authority prevails, but "applicable" depends on jurisdiction, sector, and organizational characteristics.

This concept applies to strategy evaluation by asking: has the strategy correctly identified which regulatory layer is the binding constraint? Tactics that optimize for industry standards while ignoring the underlying legislation they implement are fragile — the standard can change, or the regulator can interpret the legislation differently than the standard assumes.

**Boundary:** Regulatory hierarchy covers the formal legal and quasi-legal instruments that create compliance obligations. It does NOT cover voluntary best practices, contractual obligations, or customer expectations, which may create business requirements but not regulatory risk.

**Common misapplication:** Treating regulatory guidance as binding law. Guidance documents (FAQs, opinions, recommendations) indicate regulatory intent but are not enforceable in the same way as the regulation itself. Over-reliance on guidance creates false precision; ignoring guidance creates enforcement risk.

### Compliance Maturity Staging

Organizations move through compliance stages: unaware → aware → reactive → systematic → optimized. Each stage has different failure modes. Unaware organizations face existential enforcement risk. Aware-but-reactive organizations spend disproportionately on firefighting. Systematic organizations may over-invest in controls that don't reduce actual risk. Optimized organizations risk complacency.

Tactics should be evaluated against the organization's current maturity stage. A tactic appropriate for the systematic stage (e.g., automated control monitoring) will fail in the reactive stage (where basic control inventory doesn't exist yet). Strategies that skip stages create compliance theater — the appearance of maturity without the foundation.

**Boundary:** Compliance maturity staging covers the organization's operational readiness to meet regulatory obligations. It does NOT cover the substantive quality of the regulations themselves or the organization's lobbying/influence activities regarding future regulation.

**Common misapplication:** Equating documentation with maturity. An organization with comprehensive written policies but no evidence of implementation or monitoring is reactive, not systematic, regardless of how polished the documents are.

### Risk-Based Prioritization

Not all compliance requirements carry equal risk. Risk is a function of: (1) likelihood of enforcement action, (2) severity of penalties, (3) probability of violation given current controls, and (4) detectability of violation by regulators. Requirements with high enforcement likelihood, severe penalties, weak current controls, and high detectability should be addressed first. Requirements that are technically mandatory but rarely enforced and carry minor penalties can be addressed later without materially increasing organizational risk.

This concept applies to tactic evaluation: tactics that address high-risk gaps should score higher than tactics addressing low-risk gaps, even if the low-risk gaps are easier to close. The framework should resist the natural tendency to pick low-hanging fruit when the riskiest gaps remain open.

**Boundary:** Risk-based prioritization covers the ordering of compliance activities based on risk reduction. It does NOT justify non-compliance — all requirements must eventually be addressed. It governs sequencing, not scope.

### Regulatory Change Velocity

Regulations are not static. New regulations emerge, existing ones are amended, enforcement interpretations evolve, and court decisions create precedent. The velocity of regulatory change in a given domain determines how much compliance effort must be allocated to monitoring and adaptation versus initial implementation. High-velocity domains (AI regulation, data privacy, financial services) require continuous monitoring infrastructure. Low-velocity domains (building codes, basic employment law) can rely on periodic review.

Strategies should be evaluated on whether their monitoring cadence matches the actual change velocity of the applicable regulatory landscape. Under-monitoring creates surprise compliance gaps; over-monitoring wastes resources that could be spent on actual compliance activities.

**Boundary:** Regulatory change velocity covers changes to formal regulatory instruments. It does NOT cover changes in business operations that create new regulatory exposure (e.g., entering a new market), which is a business strategy concern that triggers compliance analysis, not a compliance concern itself.

---

## 2. Concept Relationships

**Prerequisites:** Regulatory Hierarchy and Precedence must be mapped before Risk-Based Prioritization can operate — you cannot prioritize compliance gaps without first knowing which requirements actually apply and at what authority level. Compliance Maturity Staging assessment must precede tactic design — tactics designed for the wrong maturity stage will fail.

**Tensions:** Risk-Based Prioritization creates tension with Compliance Maturity Staging when a high-risk gap requires systematic-stage capabilities but the organization is still reactive. The risk says "fix this now" but the maturity says "you can't yet." Resolution requires interim risk mitigation (manual controls, insurance, scope limitation) while building maturity. Regulatory Change Velocity creates tension with Risk-Based Prioritization — in high-velocity domains, the risk landscape shifts faster than implementation cycles, which means priorities computed at planning time may be stale by execution time.

**Amplifiers:** Mature Compliance Maturity Staging amplifies Risk-Based Prioritization by providing the control inventory and monitoring data needed to accurately assess residual risk. Understanding Regulatory Hierarchy and Precedence amplifies Regulatory Change Velocity monitoring by enabling efficient filtering — you know which changes matter for your specific regulatory exposure.

---

## 3. Quality Principles

- **QP-1:** Regulatory mapping completeness — Every compliance obligation should trace to a specific regulatory source (article, section, clause) with identified authority level. Evaluate by sampling 10 compliance requirements and checking whether each has a traceable source citation.
- **QP-2:** Control-to-requirement traceability — Every implemented control should map to one or more specific regulatory requirements it addresses, and every requirement should map to at least one control. Evaluate by generating a traceability matrix and checking for orphaned controls and uncovered requirements.
- **QP-3:** Evidence defensibility — Compliance evidence should be contemporaneous (generated at the time of the compliant activity), immutable (not editable after the fact), and attributable (tied to a specific person or system). Evaluate by examining evidence collection processes for each critical control.
- **QP-4:** Gap closure velocity — Identified compliance gaps should be closed at a rate that keeps the organization ahead of enforcement probability. Evaluate by tracking mean time from gap identification to control implementation over trailing 90 days.

---

## 4. Anti-Patterns

- **AP-1:** Checkbox compliance — Implementing the literal minimum to satisfy each requirement without considering whether the control actually reduces the underlying risk. Detect by examining whether controls are tested for effectiveness or merely for existence. Address by requiring periodic control effectiveness testing, not just control presence audits.
- **AP-2:** Regulation-by-analogy — Assuming that compliance approaches from one regulation transfer directly to another without analyzing the specific requirements. Example: applying GDPR consent mechanisms to a regulation that uses a different legal basis framework. Detect by checking whether compliance approaches cite the specific regulation they address. Address by requiring regulation-specific analysis before reusing existing controls.
- **AP-3:** Compliance island — Treating compliance as a standalone function disconnected from business operations. This creates parallel processes (one for "how we actually work" and one for "what we tell the regulator"), which diverge over time until an audit exposes the gap. Detect by comparing documented compliance processes to actual operational workflows. Address by embedding compliance controls into operational processes rather than layering them on top.

---

## 5. Hypothesis Library

- **HL-1:** "If we implement automated regulatory change monitoring for our top 3 applicable regulations, then surprise compliance gaps will decrease by 50% within 6 months, because Regulatory Change Velocity predicts that manual monitoring in high-velocity domains misses changes that affect compliance posture."
- **HL-2:** "If we conduct a maturity-stage assessment before designing the compliance program, then implementation timeline accuracy will improve by 40%, because Compliance Maturity Staging predicts that tactics mismatched to maturity stage fail regardless of their theoretical merit."
- **HL-3:** "If we prioritize compliance activities by quantified enforcement risk rather than by ease of implementation, then residual regulatory risk will decrease faster per unit of effort invested, because Risk-Based Prioritization predicts that effort sequencing has a larger impact on risk posture than effort volume."

---

## 6. Guardrail Vocabulary

- **GV-1:** Hard-law floor — Severity: hard — No strategy may deprioritize a compliance requirement from binding legislation (national law or directly applicable regulation) below a 90-day remediation window, regardless of assessed enforcement probability. Enforcement probability estimates can be wrong; the consequence of being wrong about hard law is existential.
- **GV-2:** Evidence retention — Severity: hard — Compliance evidence must be retained for the longer of: the regulatory retention period, or 3 years from generation. Destroying evidence before this threshold, even inadvertently, creates inference of non-compliance during enforcement proceedings.
- **GV-3:** Maturity stage skip — Severity: soft — Tactics that require capabilities two or more maturity stages above the organization's assessed current stage should be flagged for review. They may be approved with explicit interim mitigation plans, but proceeding without such plans risks implementation failure and wasted resources. Recovery: decompose the tactic into maturity-appropriate sub-steps.
