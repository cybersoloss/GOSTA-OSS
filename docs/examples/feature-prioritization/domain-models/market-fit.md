# Domain Model: Market Fit

**Source:** Domain expertise — synthesized from product-market fit literature (Sean Ellis test methodology, Superhuman PMF engine, Lenny Rachitsky's PMF framework) and B2B SaaS market dynamics
**Application Context:** Evaluating feature priority for a developer tools SaaS targeting mid-market engineering teams
**Created:** 2026-03-25
**Purpose:** Grounds AI agent reasoning in market demand patterns when scoring features for roadmap priority

---

## 1. Core Concepts

### Activation Distance

The number of steps between a new user's first interaction and the moment they experience the product's core value. Shorter activation distance correlates with higher trial-to-paid conversion. Features that reduce activation distance should score higher than features that add capability to already-activated users — unless retention data shows activated users are churning, which inverts the priority.

**Boundary:** Activation distance covers the path from signup to first value moment. It does NOT cover ongoing engagement, feature depth, or power-user workflows. A feature that makes the product stickier for existing users has zero effect on activation distance.

**Common misapplication:** Confusing "first login" with "first value." Users who complete onboarding but never reach the value moment have not been activated. Measuring onboarding completion as activation is the most common error.

### Switching Cost Asymmetry

The difference between the cost of switching TO your product versus switching AWAY from it. Healthy products have low inbound switching cost (easy to adopt) and high outbound switching cost (painful to leave). Features that increase outbound switching cost without increasing inbound friction are strategically superior.

**Boundary:** Switching costs include data migration, workflow retraining, integration rebuilding, and team habit disruption. They do NOT include contractual lock-in, which is a sales mechanism, not a product feature.

### Willingness-to-Pay Signal

Observable behaviors that indicate a user segment will pay for a capability — feature requests from paying customers, workaround patterns (users building manual solutions to problems the feature would solve), competitive losses citing the missing feature, and expansion revenue correlation. WTP signals from non-paying users carry lower weight than signals from paying users unless the feature targets a new market segment.

**Boundary:** WTP signals are demand indicators, not revenue projections. A feature with strong WTP signals may still fail if execution is poor or positioning is wrong.

**Common misapplication:** Treating feature request volume as WTP signal. Volume measures who asks loudest, not who will pay. Weighted signals (request source × revenue × churn risk) are more reliable than raw counts.

### Market Timing Sensitivity

Some features have time-dependent value — they matter now because of a market condition (regulatory deadline, competitor move, platform shift) but will matter less in 6 months. Features with high timing sensitivity should receive priority inflation proportional to the decay rate of the opportunity window.

**Boundary:** Market timing sensitivity covers external conditions that affect feature value. It does NOT cover internal deadlines (sales commitments, board promises), which are organizational constraints, not market signals.

### Segment Concentration Risk

When a feature serves only one customer segment, its strategic value depends entirely on that segment's health. Features that serve multiple segments are more resilient. Features serving a single segment that represents >40% of revenue are high-risk even if demand is strong — the segment could contract.

**Boundary:** Segment concentration measures breadth of demand across customer types. It does NOT measure feature quality or execution difficulty.

### Competitive Parity Gap

Features that competitors have and you don't, where the absence causes measurable deal losses. Parity gaps are defensive — they prevent loss rather than creating growth. They should be scored differently than growth features: parity features have a ceiling (you match the market) while growth features have upside (you differentiate).

**Boundary:** Competitive parity covers feature-level gaps visible in sales processes. It does NOT cover brand positioning, pricing, or go-to-market differences, which affect deal outcomes but are not feature gaps.

---

## 2. Concept Relationships

**Prerequisites:** Activation Distance must be acceptable before Switching Cost Asymmetry matters — users who never activate never experience switching costs. WTP Signals require a minimum user base to be statistically meaningful; in pre-PMF products, they are noisy.

**Tensions:** Activation Distance optimization (simplify, reduce) creates tension with Switching Cost Asymmetry (deepen, embed) — the features that make adoption easy are not the features that make leaving hard. Market Timing Sensitivity creates tension with Segment Concentration Risk — time-sensitive opportunities often target a specific segment, increasing concentration. Competitive Parity Gap creates tension with all growth-oriented concepts — parity investment is defensive and doesn't compound.

**Amplifiers:** Strong WTP Signals amplify Activation Distance improvements — if users already want the product, reducing friction converts that demand. Low Segment Concentration Risk amplifies Switching Cost Asymmetry — switching costs that span multiple segments create broader moats.

---

## 3. Quality Principles

- **QP-1:** Feature scoring must weight WTP signals by revenue source — a request from a $50K ARR customer carries more weight than 100 free-tier requests unless the feature explicitly targets free-to-paid conversion.
- **QP-2:** Activation distance claims must cite specific user journey data, not hypothetical flows. "This will reduce activation distance" without journey mapping is not evidence.
- **QP-3:** Competitive parity features must cite specific deal losses with the gap as a named reason. "Competitors have this" without loss data is not a parity gap — it's a feature list comparison.
- **QP-4:** Market timing claims must specify the window (start date, end date, decay curve) and the consequence of missing it. Open-ended urgency ("we need this soon") is not timing sensitivity.

---

## 4. Anti-Patterns

- **AP-1:** Feature factory — Shipping features based on request volume without strategic evaluation. Produces a broad, shallow product that does many things poorly. Detect by checking whether the roadmap can articulate why each feature exists in terms of a specific concept from this model. If the answer is "customers asked for it" without further analysis, the factory is running.
- **AP-2:** Parity trap — Spending >50% of roadmap capacity on competitive parity features. This is a defensive posture that prevents differentiation. Detect by categorizing roadmap items as parity vs. growth and checking the ratio. Healthy ratio: 20-30% parity, 70-80% growth/differentiation.
- **AP-3:** Segment capture — Building features for your largest customer at the expense of segment diversification. Creates concentration risk. Detect by checking whether >60% of roadmap items serve a single customer or segment.

---

## 5. Hypothesis Library

- **HL-1:** "If we reduce activation distance from 7 steps to 3 by shipping in-app templates, then trial-to-paid conversion will increase by 15%, because Activation Distance predicts that fewer steps to first value correlates with higher conversion."
- **HL-2:** "If we build the Slack integration (competitive parity gap, cited in 4 deal losses), then win rate against Competitor X will improve from 35% to 50%, because Competitive Parity Gap predicts that closing the gap removes the cited objection."
- **HL-3:** "If we ship the EU data residency feature before the July GDPR enforcement deadline (market timing window: 4 months), then we capture the 12 enterprise prospects currently blocked by the requirement, because Market Timing Sensitivity predicts that post-deadline, these prospects will have committed to competitors."

---

## 6. Guardrail Vocabulary

- **GV-1:** Activation distance floor — Severity: hard — No feature may increase activation distance (add steps to first value) without Governor approval and a documented mitigation plan. Activation regressions compound — each additional step loses a percentage of the funnel permanently.
- **GV-2:** Segment concentration ceiling — Severity: soft — No single customer segment may account for >50% of roadmap investment in any quarter. Exceeding this threshold requires Governor acknowledgment of concentration risk and a plan to rebalance in the following quarter.
- **GV-3:** Parity investment cap — Severity: soft — Competitive parity features may not exceed 35% of roadmap capacity. Exceeding triggers a strategic review: is the product in a parity trap, or is this a temporary defensive sprint?
