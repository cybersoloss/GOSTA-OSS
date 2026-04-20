# Domain Model: Adaptation Capacity

**Source:** Domain expertise — synthesized from technology adoption lifecycle theory (Moore's crossing-the-chasm model adapted for vendor-side adaptation), platform evolution patterns, AI investment signal analysis, and product portfolio management (specifically the divergence between vendor-level and product-level investment trajectories)
**Application Context:** Assessing a vendor's capacity to adapt its product to evolving market conditions, technology shifts, and competitive pressures — with particular attention to whether vendor-level adaptation efforts actually benefit the specific product being assessed
**Created:** 2026-04-20
**Domain Code:** ADAPT-1
**Purpose:** [Analytical] Provides adaptation capacity grounding so that continuity assessments distinguish between vendors that are genuinely investing in product evolution and those whose adaptation signals are superficial, misdirected, or benefit other products in the portfolio rather than the assessed product

---

## Key Insight: Vendor-Product Divergence

Vendor-level adaptation capacity and product-level adaptation capacity are not the same thing. A vendor may be investing heavily in AI, expanding its platform, and forging strategic partnerships — but all of that investment may flow to a newer product line while the assessed product receives maintenance-level attention. This divergence between vendor trajectory and specific product trajectory is among the most critical and most commonly missed risk signals in continuity assessment.

Every concept below must be evaluated at both the vendor level and the specific product level, with explicit notation when they diverge.

---

## 1. Core Concepts

### AI Investment Signals

Observable indicators that the vendor is investing in artificial intelligence and machine learning capabilities: AI-related engineering hires, research publications, patent filings, product features with genuine AI underpinning, partnerships with AI infrastructure providers, and participation in AI-related standards or consortia.

Evaluate the depth of AI investment, not just its existence. A vendor that hires a "Head of AI" and publishes a blog post has made a marketing investment. A vendor that builds a dedicated ML engineering team, ships models trained on proprietary data, and iterates on model performance over multiple releases has made a product investment.

Critical distinction: AI investment at the vendor level may not reach the assessed product. A vendor with three product lines may concentrate AI investment in its newest offering while the legacy product receives only cosmetic AI features. Always trace AI investment to the specific product.

**Boundary:** AI investment signals cover observable indicators of genuine AI capability development. They do NOT assess whether the AI capabilities are valuable, effective, or well-implemented — that is a product quality question, not an adaptation capacity question.

**Common misapplication:** Equating AI marketing with AI investment. Press releases, conference keynotes, and product rename to include "AI" are not investment signals. Investment signals are observable in hiring patterns, engineering output (release notes, API changes, model documentation), and customer-facing capability changes.

### Platform Expansion Moves

Actions indicating the vendor is broadening its product's scope, integration surface, or ecosystem role: new APIs, marketplace/app-store development, cross-product integrations, acquisition of complementary capabilities, and platform-as-a-service offerings. Platform expansion signals intent to become a category anchor rather than a point solution.

Platform expansion is a positive adaptation signal when it deepens the product's value proposition and increases switching costs for existing customers. It is a neutral or negative signal when it disperses engineering effort across too many directions, resulting in shallow capabilities across a broad surface rather than deep capability in the core use case.

**Boundary:** Platform expansion covers deliberate broadening of product scope and ecosystem role. It does NOT cover feature additions within the product's existing category — those are normal product development, not platform expansion.

**Common misapplication:** Treating every new integration or API as platform expansion. A product that adds a single-vendor integration is connecting to an ecosystem; a product that publishes an integration framework enabling arbitrary third-party connections is building a platform. Scale and openness distinguish platform moves from feature additions.

### Strategic Partnerships

Formal and observable partnerships that enhance the vendor's competitive position, technology access, or market reach: technology partnerships (OEM agreements, joint development), go-to-market partnerships (channel, reseller, co-sell), and ecosystem partnerships (standards bodies, industry consortia). Partnerships signal where the vendor sees its future and which relationships it considers strategic.

Evaluate partnership depth, not breadth. A vendor with 200 "technology partners" listed on its website may have 195 superficial logo-swap arrangements. A vendor with 3 deep partnerships involving joint engineering, shared roadmaps, and co-developed integrations has made meaningful strategic commitments.

**Boundary:** Strategic partnerships cover formal inter-vendor relationships that affect product trajectory. They do NOT cover customer relationships, analyst relationships, or investor relationships — those are assessed in other domain models.

**Common misapplication:** Treating partnership announcements as equivalent to partnership execution. Many announced partnerships produce no tangible product integration or customer value. Evaluate partnerships by their observable outputs (joint features, co-developed integrations, shared customer deployments), not by their press releases.

### Product Investment vs. Neglect

The critical vendor-product divergence detector. This concept specifically assesses whether the vendor is investing in the assessed product or neglecting it in favor of other priorities. Product investment is measured by: release cadence and content (new capabilities vs. maintenance patches), engineering team size and trajectory, roadmap commitments and delivery, support quality and responsiveness, and documentation currency.

Product neglect is signaled by: declining release cadence, releases containing only bug fixes and minor updates, engineering talent migrating to other products, roadmap commitments repeatedly deferred, support quality degradation, and stale documentation. These signals are often visible 12-18 months before a formal product end-of-life announcement.

This is the most operationally important concept in ADAPT-1 because it directly answers the question: will this specific product continue to receive investment that keeps it competitive?

**Boundary:** Product investment vs. neglect covers the vendor's resource allocation to the specific assessed product. It does NOT cover the product's current quality or capability — a product can be excellent today but neglected, meaning its quality will erode over time as competitors iterate.

**Common misapplication:** Confusing vendor-level investment with product-level investment. A vendor that announces a $500M AI initiative while the assessed product's engineering team has been halved is not investing in the assessed product. Always trace investment claims to the specific product.

### Agentic-Native vs. Retrofit Adaptation

How the vendor is adapting the assessed product to AI-native and agentic computing paradigms. This overlaps with DISP-1's concept of the same name but evaluates it from the vendor's perspective (are they adapting?) rather than the competitor's perspective (are they displacing?).

Genuine agentic adaptation involves rearchitecting data access patterns for machine consumption, building API-first interaction surfaces, enabling autonomous decision loops, and designing for multi-agent orchestration. Retrofit adaptation involves adding a chatbot to the existing UI, wrapping existing APIs with natural language parsing, or rebranding existing automation as "agentic."

**Boundary:** This concept covers the assessed product's architectural adaptation toward agentic computing. It does NOT assess whether agentic computing is relevant to the product's category — that assessment belongs in DISP-1.

**Common misapplication:** Treating any AI feature addition as evidence of agentic adaptation. A product that adds an AI-generated summary of its dashboard has added an AI feature; a product that exposes its full analytical pipeline as composable agent actions has adapted for agentic computing. The distinction is architectural, not cosmetic.

### Ecosystem and Standards Alignment

The degree to which the vendor and product align with emerging industry standards, open frameworks, and ecosystem conventions. Standards alignment signals willingness to participate in an interoperable ecosystem rather than attempting to maintain a proprietary lock-in position. In rapidly evolving categories (especially those affected by AI), standards alignment is an adaptation signal — vendors that resist emerging standards risk isolation.

Evaluate: Does the product support emerging open standards in its category? Does the vendor participate in standards bodies? Does the product integrate with commonly used tools and platforms through standard interfaces? Is the vendor contributing to or resisting the open-source ecosystem in its category?

**Boundary:** Ecosystem alignment covers standards and interoperability positioning. It does NOT cover product quality, competitive positioning, or market share — a vendor can be perfectly standards-aligned while losing market share for unrelated reasons.

**Common misapplication:** Equating "supports open standards" with "has open-source components." Standards alignment is about interoperability and ecosystem participation. Open-source involvement is one signal but not the defining characteristic. A proprietary product that implements industry-standard APIs and data formats is well-aligned; an open-source product that uses proprietary data formats is not.

### Open-Source Dependency Health

The health and sustainability of open-source components that the assessed product depends on. Many commercial products are built on open-source foundations. If those foundations are poorly maintained, losing contributors, or facing license changes, the product built on them faces adaptation risk.

Evaluate: Are the product's critical open-source dependencies actively maintained? Is the contributor base growing or shrinking? Have there been license changes or forks that affect commercial use? Does the vendor contribute back to its critical dependencies (indicating awareness and investment in their health)?

**Boundary:** Open-source dependency health covers the sustainability of the product's open-source foundations. It does NOT cover the vendor's own open-source strategy or the competitive dynamics of open-source alternatives to the product.

**Common misapplication:** Ignoring open-source dependency risk for commercial products. Many commercial security, analytics, and infrastructure products depend on open-source components whose health directly affects the commercial product's quality and evolution rate.

### Customer Segment Abandonment Detection

Signals that the vendor is de-prioritizing or abandoning the customer segment that the assessed product serves. Segment abandonment is often a precursor to product discontinuation — the vendor shifts sales and marketing focus to a different segment, the assessed product's customer base receives less attention, and eventually the product is sunset.

Signals include: sales team restructuring away from the product's segment, marketing content shifting to a different buyer persona, pricing changes that push small or mid-market customers toward self-service while concentrating human support on enterprise accounts, and roadmap content that addresses a different segment's requirements.

**Boundary:** Customer segment abandonment covers the vendor's commitment to the product's current customer segment. It does NOT cover the segment's overall health or growth — a vendor may abandon a healthy segment because it has identified a more attractive one.

**Common misapplication:** Treating any pricing change or packaging restructuring as segment abandonment. Vendors regularly adjust pricing. Abandonment signals are sustained, multi-dimensional shifts in attention (sales, marketing, support, roadmap) away from a segment, not isolated pricing events.

### Exit Preparation vs. Commitment Discrimination

Distinguishing between vendor actions that indicate preparation for product exit (sale, sunset, or end-of-life) versus genuine investment in the product's future. This is the most difficult assessment in ADAPT-1 because some exit preparation activities resemble investment activities.

Exit preparation signals disguised as investment: "platform rewrite" that moves customers to a different product, "migration to cloud" that actually migrates customers to an acquiring vendor's infrastructure, "strategic partnership" that is actually an OEM transition before discontinuation, and "product unification" that consolidates the assessed product into a larger platform where it loses its identity and eventually its dedicated development.

Genuine commitment signals: dedicated engineering team with growth trajectory, product-specific roadmap with multi-year vision, customer advisory board with product-specific input, and independent P&L accountability for the product line.

**Boundary:** Exit preparation vs. commitment covers the vendor's long-term intent for the specific product. It does NOT predict the outcome — a vendor genuinely committed to a product may still fail financially (tracked in ECON-1). This concept assesses intent, not capability.

**Common misapplication:** Taking vendor statements of commitment at face value. Vendors invariably claim commitment to all products until the day they announce discontinuation. Evaluate actions (engineering investment, roadmap delivery, support quality) not words (blog posts, executive quotes, customer reassurances).

---

## 2. Concept Relationships

**Prerequisites:** Product Investment vs. Neglect must be assessed before Exit Preparation vs. Commitment Discrimination — investment patterns provide the evidence base for discriminating between exit and commitment. AI Investment Signals and Agentic-Native vs. Retrofit Adaptation should be assessed together — they address the same underlying question (is the product evolving for AI?) from quantitative (investment) and qualitative (architecture) angles.

**Tensions:** AI Investment Signals at the vendor level create tension with Product Investment vs. Neglect at the product level — vendor AI investment may not reach the assessed product. Platform Expansion Moves create tension with product focus — broad expansion can dilute engineering attention on the core product. Strategic Partnerships create tension with independence — deep partnerships may indicate future acquisition or OEM transition, not just collaboration.

**Amplifiers:** Product Investment vs. Neglect amplifies every other concept — a neglected product will not benefit from the vendor's AI investment, platform expansion, or partnerships regardless of how strong those vendor-level signals are. Ecosystem and Standards Alignment amplifies Agentic-Native adaptation — products built on standard interfaces can integrate more easily into agentic workflows. Open-Source Dependency Health amplifies Product Investment — a product built on healthy open-source foundations can adapt faster than one built on stagnating proprietary components.

---

## 3. Quality Principles

- **QP-1:** Vendor-product separation — Every adaptation signal must be assessed at both the vendor level and the specific product level, with explicit notation when they diverge. A positive vendor-level signal that does not reach the assessed product is not a positive signal for the product. Evaluate by checking whether each concept includes both vendor-level and product-level assessment.
- **QP-2:** Action over announcement — Adaptation capacity must be evaluated based on observable actions (shipping features, hiring engineers, delivering roadmap commitments), not vendor announcements, press releases, or executive statements. Evaluate by checking whether evidence citations reference observable outputs vs. vendor communications.
- **QP-3:** Temporal pattern recognition — Single-point-in-time adaptation signals are weak. Adaptation capacity is revealed by patterns over time: increasing or decreasing release cadence, growing or shrinking engineering teams, accelerating or decelerating roadmap delivery. Evaluate by checking whether each concept includes trend data across at least 2-3 data points.
- **QP-4:** Architectural depth assessment — AI and agentic adaptation claims must be evaluated for architectural depth, not surface features. A chatbot bolted onto an existing UI is not architectural adaptation. Evaluate by checking whether AI/agentic assessments distinguish between cosmetic additions and structural changes.
- **QP-5:** Exit signal sensitivity — Assessments must actively look for exit preparation signals rather than assuming continued commitment. The default assumption for any vendor product should be "prove commitment" not "assume commitment." Evaluate by checking whether the assessment includes explicit exit signal analysis for the assessed product.

---

## 4. Anti-Patterns

- **AP-1:** AI marketing as investment — Treating AI-related marketing (product renaming, "AI-powered" labels, conference demos, blog posts about AI strategy) as evidence of genuine AI investment. Marketing spend and engineering investment are independent variables. Detect by checking whether AI investment conclusions cite engineering outputs (features, models, APIs, hire counts) vs. marketing outputs (announcements, brand changes, demos). Address by requiring at least two engineering-level evidence points for any positive AI investment assessment.
- **AP-2:** Vendor adaptation equals product adaptation — Assuming that a vendor's adaptation efforts (AI investment, platform expansion, partnerships) automatically benefit the specific assessed product. This is the most dangerous assumption in continuity assessment because it is usually implicit — the analyst evaluates vendor-level signals and attributes them to the product without checking. Detect by checking whether vendor-level adaptation signals include product-specific tracing. Address by requiring explicit "product-level impact" assessment for every vendor-level adaptation signal.
- **AP-3:** Rewrite-as-commitment — Interpreting a vendor's announcement of a product rewrite, major version, or platform migration as evidence of long-term commitment. Rewrites can be genuine reinvestment, but they can also be exit preparation: migrating customers to a platform where the product's identity will eventually dissolve, or rewriting as a prelude to selling the updated asset. Detect by checking whether rewrite/migration assessments evaluate the outcome for the assessed product's independent identity and dedicated development. Address by requiring explicit analysis of whether the product retains independent identity, dedicated engineering, and customer-specific roadmap after the rewrite.
