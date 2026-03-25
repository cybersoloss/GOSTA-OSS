# Domain Model: Open-Source Community Growth

**Source:** Domain expertise — synthesized from publicly documented patterns in open-source project management (Apache Foundation governance docs, GitHub Open Source Guides, Nadia Eghbal's "Working in Public" themes)
**Enhancement Sources:** None
**Application Context:** Governing AI-assisted strategy for growing an open-source project's contributor base, adoption, and sustainability
**Created:** 2026-03-25
**Purpose:** Provides evaluation criteria for tactics and strategies aimed at increasing open-source project adoption, contributor engagement, and long-term sustainability

---

## 1. Core Concepts

### Contributor Funnel Dynamics

Open-source projects follow a funnel: awareness → first use → issue filed → first contribution → repeat contributor → maintainer. Each stage has distinct drop-off causes. Awareness-to-use drops when documentation is poor or onboarding friction is high. Use-to-contribution drops when contribution paths are unclear or the project feels "complete" (no obvious gaps). Contribution-to-retention drops when review cycles are slow, feedback is discouraging, or governance is opaque.

This concept applies to tactic evaluation by asking: which stage of the funnel does this tactic target, and what is the evidence that this stage is the current bottleneck? Tactics that target late-funnel stages (retention) while early-funnel stages (awareness) are the actual constraint will score poorly.

**Boundary:** The contributor funnel covers voluntary individual contributions. It does NOT cover corporate adoption decisions (see Institutional Adoption below) or paid development contracts, which follow different decision logic.

**Common misapplication:** Treating "GitHub stars" as evidence of funnel health. Stars correlate weakly with actual use and almost not at all with contribution intent.

### Documentation as Product

In open-source, documentation is not a support artifact — it is the primary product surface for most users. The quality, structure, and discoverability of docs determines adoption more than feature completeness in most cases. This includes READMEs, getting-started guides, API references, architecture decision records, and contribution guides.

Tactics involving documentation should be evaluated on whether they reduce time-to-first-success (how quickly a new user achieves something useful) and time-to-first-contribution (how quickly someone goes from user to contributor).

**Boundary:** Documentation-as-product covers written artifacts that help users and contributors. It does NOT cover marketing content, blog posts, or conference talks, which serve awareness rather than enablement.

**Common misapplication:** Generating exhaustive reference documentation while neglecting task-oriented guides. Users need "how do I do X" before they need "what does every parameter do."

### Institutional Adoption

Organizations adopt open-source projects through a different path than individuals: technical evaluation → security/license review → internal champion advocacy → procurement/legal approval → deployment → contribution (maybe). The decision is made by committees, not individuals, and factors like license compatibility, maintenance track record, and corporate contributor agreements matter more than developer enthusiasm.

Strategies targeting institutional adoption should be evaluated on whether they address institutional concerns (governance transparency, release cadence predictability, security response process) rather than individual developer preferences.

**Boundary:** Institutional adoption covers organizations evaluating the project for use in their own products or infrastructure. It does NOT cover individual developers using it for personal projects, even if those developers work at large companies.

### Sustainable Maintenance Economics

Open-source projects fail not from lack of interest but from maintainer burnout. Sustainability requires that the ratio of maintenance burden to maintenance capacity stays below 1.0 over time. Maintenance burden includes issue triage, PR review, dependency updates, security patches, release management, and community moderation. Maintenance capacity is the available volunteer/paid hours from people with commit access.

This concept applies to strategy evaluation: any strategy that increases adoption without proportionally increasing maintenance capacity is borrowing against future sustainability. Tactics should be assessed for their maintenance cost, not just their adoption benefit.

**Boundary:** Sustainable maintenance covers the operational health of the project's development process. It does NOT cover financial sustainability models (sponsorship, dual licensing, SaaS), which are a separate strategic concern.

---

## 2. Concept Relationships

**Prerequisites:** Documentation as Product must reach a minimum quality threshold before Contributor Funnel Dynamics can operate — contributors cannot emerge from a project they cannot understand. Institutional Adoption requires a baseline of governance transparency and release predictability that only emerges after the project has some Contributor Funnel maturity.

**Tensions:** Contributor Funnel growth creates tension with Sustainable Maintenance Economics — more contributors means more PRs to review, more issues to triage, and more architectural opinions to reconcile. Aggressive funnel optimization without maintenance capacity planning leads directly to burnout. Institutional Adoption's demand for stability and predictability creates tension with the rapid iteration that Contributor Funnel growth often requires (frequent breaking changes attract contributors but repel institutions).

**Amplifiers:** Strong Documentation as Product amplifies the entire Contributor Funnel by reducing friction at every stage. Institutional Adoption, when achieved, amplifies Sustainable Maintenance Economics by providing organizations that may contribute engineering time back to the project.

---

## 3. Quality Principles

- **QP-1:** First-use success within 15 minutes — A new user, following the README and getting-started guide, should achieve a meaningful first result within 15 minutes on a standard development environment. Evaluate by timing a fresh walkthrough.
- **QP-2:** Contribution path visibility — At any point in the project, there should be at least 5 clearly labeled "good first issues" or equivalent entry points for new contributors. Evaluate by checking issue tracker labels and staleness.
- **QP-3:** Review cycle under 72 hours — First substantive response to any PR should occur within 72 hours (weekdays). Evaluate by measuring median first-response time over trailing 30 days.
- **QP-4:** Bus factor above 1 — No single maintainer should be the sole person capable of performing any critical project operation (releases, security patches, infrastructure access). Evaluate by listing critical operations and mapping who can perform each.

---

## 4. Anti-Patterns

- **AP-1:** Vanity metric optimization — Pursuing GitHub stars, Twitter followers, or conference talk invitations as proxy metrics for project health. These metrics are weakly correlated with actual adoption and uncorrelated with sustainability. Detect by checking whether reported metrics map to funnel stages or maintenance capacity. Redirect effort toward measuring actual usage (downloads, active installations) and contribution health (PR merge rate, contributor retention).
- **AP-2:** Cathedral-in-the-bazaar — Accepting external contributions for peripheral features while keeping all architectural decisions opaque and centralized. This creates the appearance of openness while preventing the community investment needed for sustainability. Detect by examining whether any non-founder has influenced a design decision in the last 6 months. Address by publishing architecture decision records and inviting RFC-style discussion for significant changes.
- **AP-3:** Documentation debt compounding — Shipping features without corresponding documentation updates, creating a growing gap between what the project can do and what users can discover. Detect by comparing changelog entries to documentation updates over the last 3 releases. Address by making documentation a blocking requirement for feature completion.

---

## 5. Hypothesis Library

- **HL-1:** "If we add a 'quick start' tutorial that gets users to a working result in under 10 minutes, then first-week retention (return visits) will increase by 20%, because Documentation as Product predicts that time-to-first-success is the primary driver of early-stage funnel conversion."
- **HL-2:** "If we implement a 'contributor office hours' weekly session, then first-time PR submissions will increase by 30% within 8 weeks, because Contributor Funnel Dynamics predicts that human interaction at the contribution threshold reduces the perceived barrier to first PR."
- **HL-3:** "If we publish a governance document describing decision-making processes and maintainer roles, then corporate inquiries about adoption will increase, because Institutional Adoption predicts that governance transparency is a prerequisite for organizational evaluation."

---

## 6. Guardrail Vocabulary

- **GV-1:** Maintenance capacity ratio — Severity: hard — No strategy or tactic may be approved that is projected to increase maintenance burden by more than 20% without a corresponding plan to increase maintenance capacity. Violating this guardrail risks maintainer burnout, which is an existential threat to the project.
- **GV-2:** License compatibility — Severity: hard — All contributed code, documentation, and dependencies must be compatible with the project's license. No exceptions. License violations create legal risk that can force project shutdown.
- **GV-3:** Breaking change cadence — Severity: soft — Breaking changes should not occur more than once per quarter in stable releases. Exceeding this cadence signals instability that undermines Institutional Adoption. Recovery: batch breaking changes into planned major releases with migration guides.
