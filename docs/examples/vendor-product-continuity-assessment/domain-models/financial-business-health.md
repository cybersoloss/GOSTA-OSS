# Domain Model: Financial & Business Health

**Source:** Domain expertise — synthesized from SaaS financial analysis frameworks (Rule of 40, SaaS metrics benchmarking), third-party risk management financial viability assessment practices, public company financial reporting patterns, and venture/PE-backed company lifecycle economics
**Application Context:** Assessing the financial viability and business trajectory of a vendor or product as part of a continuity risk evaluation — determining whether the entity will exist, be adequately funded, and remain committed to the assessed product over a 2-5 year planning horizon
**Created:** 2026-04-20
**Domain Code:** ECON-1
**Purpose:** [Analytical] Provides financial and business health grounding so that continuity assessments are anchored in observable economic signals rather than vendor marketing narratives or analyst positioning

---

## Scoring Dimensions

Every concept below contributes to three scoring dimensions:

- **Pressure Intensity** (1-10): How much financial or business stress is the vendor under? 1 = no observable stress; 10 = imminent existential threat.
- **Trajectory** (improving / stable / declining): Is the pressure increasing, holding, or easing over the most recent 2-4 reporting periods?
- **Confidence** (low / medium / high): How much verifiable evidence supports the assessment? Public companies = high ceiling. Private companies with limited disclosure = low ceiling unless supplemented by credible third-party data.

---

## 1. Core Concepts

### Revenue Trajectory

The direction, rate, and composition of revenue change over time. A vendor growing at 30% year-over-year faces fundamentally different continuity risk than one growing at 3% or contracting. Revenue trajectory must be decomposed: organic vs. acquisition-driven growth tells a different story, as does growth from new customers vs. expansion of existing accounts.

For private companies, revenue trajectory is often opaque. Proxy signals include headcount growth (observable via professional networks), office expansion or contraction, job posting volume and seniority mix, and customer-facing communications about new capabilities.

**Boundary:** Revenue trajectory covers the direction and rate of topline change. It does NOT cover profitability, cash position, or capital structure — those are separate concepts below.

**Common misapplication:** Treating revenue growth as inherently positive without examining its cost. A vendor growing revenue at 40% while burning cash at an accelerating rate may be less viable than one growing at 10% profitably. Revenue trajectory must always be read alongside Financial Runway.

### SaaS Financial Metrics

The standard quantitative indicators of SaaS business health: Annual Recurring Revenue (ARR), Monthly Recurring Revenue (MRR), Net Revenue Retention (NRR), gross margin, and market share within the relevant category. These metrics, when available, provide the most objective view of business health.

Key thresholds for continuity assessment:
- **NRR above 120%**: Existing customers are expanding significantly — strong product-market fit signal.
- **NRR 100-120%**: Healthy retention with moderate expansion.
- **NRR below 100%**: Revenue is leaking — existing customers are shrinking or churning faster than they expand. This is a **critical warning signal** for product continuity.
- **Gross margin below 60%**: Unusual for SaaS; may indicate heavy services dependency or infrastructure cost problems that constrain R&D investment.

**Boundary:** SaaS financial metrics cover quantitative financial health indicators. They do NOT cover strategic positioning, competitive dynamics, or product quality — a vendor can have excellent financial metrics while its specific product is being neglected in favor of a newer offering.

**Common misapplication:** Applying public-company SaaS benchmarks to private companies without adjustment. A PE-backed vendor optimizing for EBITDA will show different metric patterns than a VC-backed vendor optimizing for growth. The metric interpretation must match the company's capital structure and stage.

### Financial Runway

The length of time a vendor can continue operating at current burn rates given available cash, credit facilities, and projected revenue. For public companies, this is calculable from filings. For private companies, it must be estimated from funding history, last known valuation, headcount changes, and market conditions.

Critical thresholds:
- **Above 24 months**: Low short-term risk, though long-term viability still depends on trajectory.
- **12-24 months**: Moderate risk. The vendor will need to raise capital, achieve profitability, or find a buyer within this window.
- **Below 12 months**: High risk. Active fundraising, cost-cutting, or acquisition discussions are likely underway. Product investment typically suffers as resources shift to survival.

**Boundary:** Financial runway covers the vendor's ability to continue operating. It does NOT predict what happens when runway expires — acquisition, pivot, wind-down, and emergency fundraising are all possible outcomes with very different continuity implications.

**Common misapplication:** Treating recent large funding rounds as proof of long-term viability. A vendor that raised $200M at a $2B valuation but is burning $20M/month has 10 months of runway regardless of the headline number. Burn rate matters more than total raised.

### Consolidation Positioning

Where the vendor sits in the ongoing market consolidation cycle: acquirer, acquisition target, consolidation survivor, or consolidation casualty. Consolidation positioning directly affects product continuity — an acquired product may be maintained, integrated, shelved, or sunset depending on the acquirer's strategy.

Signals to evaluate: Is the vendor actively acquiring (consolidation leader)? Have they received and rejected acquisition offers (independent but targeted)? Are they in a category where consolidation is accelerating (increasing risk of involuntary exit)? Is a PE firm involved (PE typically acquires to consolidate, extract margin, and re-sell within 3-7 years)?

**Boundary:** Consolidation positioning covers the vendor's role in market M&A dynamics. It does NOT cover product-level decisions post-acquisition — a vendor may be acquired and the specific product in question may thrive, stagnate, or be discontinued.

**Common misapplication:** Assuming acquisition is automatically negative for product continuity. Acquisition by a well-resourced platform vendor with strategic interest in the product category can improve continuity. Acquisition by a PE roll-up focused on cost extraction is typically negative. The acquirer's strategy matters more than the event itself.

### Customer Concentration

The degree to which the vendor's revenue depends on a small number of customers or a single customer segment. High customer concentration creates fragility — losing one or two major accounts can trigger a death spiral of reduced revenue, reduced investment, reduced product quality, and further customer loss.

For public companies, customer concentration is often disclosed (e.g., "no customer represents more than 10% of revenue" or "our largest customer represents 22% of revenue"). For private companies, concentration must be inferred from customer references, case studies, and the vendor's sales motion (enterprise-only vs. broad market).

**Boundary:** Customer concentration covers revenue dependency on specific customers or narrow segments. It does NOT cover geographic concentration (relevant but tracked separately) or product-line concentration (tracked under Consolidation Positioning).

**Common misapplication:** Ignoring the inverse risk — a vendor with thousands of small customers and no enterprise anchors may have low concentration risk but also low switching costs for its customers, making revenue volatile for different reasons.

### Market Segmentation Positioning

Where the vendor competes within its category: enterprise, mid-market, SMB, or cross-segment. Market positioning affects continuity risk because different segments face different competitive pressures. A vendor positioned in the mid-market that faces platform bundling from above (enterprise vendors adding the capability for free) and open-source pressure from below faces a shrinking addressable market.

Evaluate whether the vendor's positioning is deliberate and defensible or a default that reflects inability to compete in higher or lower segments.

**Boundary:** Market segmentation positioning covers the vendor's competitive position within its category. It does NOT cover the category's overall growth or decline — a vendor can be well-positioned in a dying category.

**Common misapplication:** Treating analyst quadrant/wave placement as equivalent to market positioning. Analyst positioning reflects evaluation criteria that may not align with actual competitive dynamics or customer purchasing patterns.

### Talent Signals

Observable workforce changes that indicate business health trajectory: hiring patterns, layoff events, leadership departures, and the seniority/function mix of open positions. Talent signals are often the earliest observable indicators of strategic shifts — they precede financial reporting by 3-12 months.

Key patterns: Engineering hiring freeze while sales hiring continues = product investment declining. C-suite departures in clusters = internal distress. Hiring for "integration" or "migration" roles = acquisition preparation. Shift from product engineering to professional services hiring = product maturity plateau.

**Boundary:** Talent signals cover workforce-observable indicators of business trajectory. They are leading indicators, not definitive evidence — they must be corroborated with other signals before driving assessment conclusions.

**Common misapplication:** Over-indexing on individual departures. Executive turnover is normal. Talent signals become meaningful only in aggregate patterns: multiple senior departures in a short window, systematic reduction in a function, or hiring patterns that contradict stated strategy.

---

## Failure Prediction Thresholds

The following thresholds, when 2 or more are breached simultaneously, activate the **[FAILURE-TRAJECTORY]** flag, which escalates the assessment to require explicit Governor review:

| Threshold | Breach Condition | Rationale |
|---|---|---|
| Rule of 40 | Revenue growth rate + profit margin < 40 | Combined growth-profitability indicator below minimum healthy threshold |
| Net Revenue Retention | NRR < 100% | Existing customer base is shrinking — product-market fit eroding |
| Burn Multiple | Net burn / net new ARR > 0.5 | Spending too much to acquire each unit of new revenue |
| CAC Payback | Customer acquisition cost payback > 12 months | Unit economics unsustainable at current growth rate |

When [FAILURE-TRAJECTORY] is activated, all scoring for this domain model must include explicit acknowledgment of the flag, the specific thresholds breached, and a timeline estimate for when financial pressure will force observable action (cost reduction, fundraising, acquisition, or product discontinuation).

---

## 2. Concept Relationships

**Prerequisites:** Revenue Trajectory and SaaS Financial Metrics must be assessed before Financial Runway — runway calculations depend on understanding current revenue dynamics and burn patterns. Customer Concentration and Market Segmentation Positioning should be assessed before Consolidation Positioning — knowing who the vendor's customers are and where they compete reveals whether they are an attractive acquisition target.

**Tensions:** Revenue Trajectory may conflict with Talent Signals — a vendor can show revenue growth through backlog recognition while simultaneously cutting engineering staff, indicating future product decline. Consolidation Positioning creates tension with Financial Runway — a vendor actively pursuing acquisitions may shorten its own runway while appearing strategically healthy. SaaS Financial Metrics may conflict with Market Segmentation Positioning — strong financial metrics in a shrinking segment do not indicate long-term viability.

**Amplifiers:** Talent Signals amplify Financial Runway assessment — engineering layoffs combined with short runway strongly predict product investment decline. Customer Concentration amplifies Revenue Trajectory risk — declining revenue from a concentrated customer base accelerates faster than from a diversified base. Market Segmentation Positioning amplifies Consolidation Positioning analysis — vendors in segments under platform bundling pressure are more likely to become acquisition targets.

---

## 3. Quality Principles

- **QP-1:** Source-grounded financial claims — Every financial metric cited must trace to a specific source: public filing, credible third-party estimate, or documented proxy signal. Unattributed financial claims are prohibited. Evaluate by checking whether each metric includes its source and recency.
- **QP-2:** Stage-appropriate benchmarking — Financial metric interpretation must account for the vendor's capital structure and lifecycle stage (public, late-stage private, PE-backed, bootstrapped). Applying uniform thresholds across stages produces misleading assessments. Evaluate by checking whether benchmark comparisons acknowledge the vendor's stage.
- **QP-3:** Temporal currency — Financial data older than 12 months must be flagged as potentially stale with explicit confidence reduction. Markets shift; last year's metrics may not reflect current reality. Evaluate by checking whether data recency is documented for each metric.
- **QP-4:** Trajectory over snapshot — Point-in-time financial metrics must be accompanied by trend data (minimum 2 data points, ideally 4+). A vendor with $50M ARR and declining NRR is in a fundamentally different position than one with $50M ARR and expanding NRR. Evaluate by checking whether each metric includes directional context.
- **QP-5:** Proxy signal transparency — When direct financial data is unavailable (private companies), proxy signals must be explicitly labeled as proxies with stated confidence levels. Evaluate by checking whether indirect evidence is distinguished from direct financial data.
- **QP-6:** Cross-concept coherence — Financial signals must be checked for internal consistency. Revenue growth combined with engineering layoffs, or strong NRR combined with high customer concentration, are incoherent patterns that require explicit investigation. Evaluate by checking whether the assessment addresses apparent contradictions between concepts.

---

## 4. Anti-Patterns

- **AP-1:** Analyst-report-as-financial-analysis — Substituting an industry analyst's vendor positioning for actual financial health assessment. Analyst reports evaluate product capability and market vision, not financial viability. A vendor can be a "leader" in an analyst framework while facing financial distress. Detect by checking whether financial conclusions cite financial sources vs. analyst positioning. Address by requiring at least one primary financial source per financial claim.
- **AP-2:** Last-round-itis — Treating the most recent funding round as proof of financial health without examining burn rate, valuation trajectory (up-round vs. down-round vs. flat), and investor composition. A large funding round at a declining valuation with primarily existing investors participating is a distress signal, not a health signal. Detect by checking whether funding analysis includes round terms and context. Address by requiring burn rate and runway calculation alongside funding history.
- **AP-3:** Revenue-growth-blindness — Focusing exclusively on topline revenue growth while ignoring profitability, retention, and unit economics. Unsustainable growth accelerates failure rather than preventing it. Detect by checking whether the assessment includes profitability and retention metrics alongside growth. Address by requiring the Failure Prediction Thresholds to be evaluated for every vendor.
- **AP-4:** Public-company-only-rigor — Applying thorough financial analysis to public vendors while hand-waving private vendor financial health as "unknown" without pursuing available proxy signals. Detect by checking whether private vendor assessments include proxy signal analysis (talent, hiring, funding, customer references). Address by requiring proxy signal assessment for all private vendors, with explicit confidence level documentation.

---

## 5. Hypothesis Library

- **HL-1:** "If a vendor breaches 2+ Failure Prediction Thresholds simultaneously while showing declining Talent Signals, then observable product degradation (reduced release cadence, support quality decline, feature stagnation) will follow within 6-12 months, because financial pressure forces resource reallocation away from product investment before it forces market exit."
- **HL-2:** "If a PE-backed vendor's financial metrics optimize toward EBITDA improvement (cost cutting, price increases, reduced R&D as percentage of revenue) while market growth continues, then the vendor is being prepared for resale rather than long-term product investment, because PE exit economics reward margin expansion over product excellence."
