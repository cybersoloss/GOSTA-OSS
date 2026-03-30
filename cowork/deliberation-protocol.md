# GOSTA Deliberation Protocol v0.9

**Purpose:** Defines how multiple domain-grounded agents coordinate through structured deliberation to produce recommendations for the Governor. This protocol sits above the Cowork Protocol — each individual agent follows Cowork Protocol mechanics internally; this protocol orchestrates between them.

**Relationship to other documents:**
- **Framework:** The specification. Defines layers, guardrails, domain models, graduation, feedback loops, deliberation escalation (§14.7).
- **Cowork Protocol:** How a single agent operates. Session lifecycle, file structure, signal format, health computation, Governor interaction. Each domain agent follows these mechanics internally.
- **Deliberation Protocol (this document):** How multiple agents coordinate. Agent topology, round structure, position exchange, synthesis, disagreement resolution, convergence. New.

**Implementation-agnostic:** This protocol defines mechanics, not implementation. Position papers, synthesis reports, and disagreement records are logical artifacts — they can be markdown files (Cowork/Code mode), JSON objects (API), messages in a queue (microservices), or in-memory structures (coded implementations). The protocol specifies what each artifact must contain, not how it is stored or transmitted.

**Reference:** GOSTA Framework — Agentic Execution Architecture. GOSTA-Cowork Protocol.

---

## 1. The Three Roles

**Domain Agent:** An AI instance grounded in a single domain model. It evaluates the current state (roadmap, tactic, scoring target) exclusively from its domain's perspective. It produces position papers. It responds to other agents' positions. It does not synthesize across domains — that is not its job.

A domain agent has:
- Exactly one domain model (its identity and perspective)
- Read access to the operating document, current signals, and shared context
- Read access to other agents' position papers (in Round 2+)
- Write access to its own position papers only

A domain agent does NOT:
- Score or evaluate from another domain's perspective
- Override or modify another agent's position
- Resolve disagreements — it advocates
- Communicate directly with another agent outside the round structure

**Coordinator:** An AI instance with no domain model of its own. Its job is operational and structural: manage agent lifecycle, collect position papers, identify agreements and disagreements, classify disagreement severity, track costs, detect stuck states, and produce a synthesis report for the Governor. The Coordinator does not advocate — it maps the landscape of agent opinions and keeps the deliberation machinery running.

The Coordinator has:
- Read access to all domain models (for understanding agent reasoning, not for independent evaluation)
- Read access to all position papers from all rounds
- Read access to the operating document, signals, and prior synthesis reports
- Write access to synthesis reports, disagreement records, and agent status logs
- **Operational authority** over deliberation flow (but not over domain content)

The Coordinator does NOT:
- Produce its own domain evaluation
- Break ties or resolve disagreements
- Override any agent's position
- Advocate for a specific recommendation

### 1.1 Coordinator Operational Responsibilities

Beyond synthesis, the Coordinator manages the deliberation as a running system:

**Agent lifecycle monitoring.** The Coordinator tracks each domain agent's status within a round:
- `responding` — Agent has been dispatched and is producing its position paper
- `completed` — Position paper received
- `timed_out` — Agent did not respond within the configured timeout window
- `failed` — Agent returned an error or produced invalid output (malformed position paper, missing required fields)
- `degraded` — Agent responded but with anomalously low confidence (≤2) or empty reasoning, suggesting context issues
- `refused` — Agent declined to produce output, typically due to content safety filters when the domain involves sensitive topics (conflict, medical, legal). See §8.5 for mitigation

**Timeout handling.** Each round has a configurable timeout window (declared in OD Deliberation section, default: 5 minutes for Code mode API calls, 1 session for Cowork mode). When an agent times out:
1. Coordinator logs the timeout: agent ID, round, elapsed time, last known state
2. Coordinator does NOT block the deliberation — it proceeds with available position papers
3. The missing agent's perspective is noted in the Interim Assessment and Synthesis Report: "Agent [ID] timed out — [domain] perspective absent from this round"
4. If the same agent times out in 2+ consecutive deliberation cycles, the Coordinator flags it as a **roster issue** in the Synthesis Report with diagnostic: was it a context-length problem (domain model too large?), an API failure (infrastructure?), or a prompt issue (agent couldn't produce a valid position paper from its domain model?)
5. Governor decides: (a) retry with adjusted parameters (shorter domain model, simpler prompt), (b) remove from roster temporarily, (c) replace with a different model/provider

**Failed agent recovery.** When an agent produces invalid output, the Coordinator applies a graduated fallback sequence. Each step is attempted in order; if it succeeds, the agent re-enters the deliberation. If all steps fail, the agent is excluded.

1. **Log and diagnose.** Coordinator logs the failure with the error or the invalid output. Diagnose the failure category:
   - *Structural failure* — missing required fields (e.g., no Guardrail Assessment section)
   - *Content failure* — position paper present but reasoning is empty, circular, or does not cite domain model concepts
   - *Refusal* — agent declined to produce output (safety filters). See §8.5.
   - *Context overflow* — agent produced truncated output suggesting context limit was reached

2. **Retry with clarified prompt** (all failure types). Coordinator retries once with a prompt targeted at the specific failure: "Your position paper is missing the Guardrail Assessment section. Please include it." For content failures: "Your reasoning section does not cite any concepts from your domain model. Rewrite citing at least 3 specific concepts." For refusals: apply §8.5 three-element framing if not already used.

3. **Fallback: reduced domain model** (if retry fails). Extract the top 5 most relevant concepts from the domain model (Core Concepts + the Quality Principles most applicable to the evaluation target) and re-prompt with this reduced model. This addresses context overflow and sometimes resolves refusals by reducing the surface area of sensitive content. The Coordinator notes in the Interim Assessment: "Agent [ID] operating on reduced domain model — [N] of [M] concepts loaded. Coverage gap: [missing concept areas]."

4. **Fallback: extract-and-represent** (if reduced model also fails). The Coordinator extracts the domain model's key evaluative criteria (Quality Principles + top Anti-Patterns) and produces a **proxy position statement** — not a full position paper, but a structured note: "Based on [Domain]'s Quality Principles [list] and Anti-Patterns [list], the following evaluative lens is relevant to this deliberation: [lens summary]." This proxy is clearly labeled `[PROXY — Agent [ID] failed, Coordinator-generated from domain model]` in the Interim Assessment and Synthesis Report. It ensures the domain's perspective is not entirely absent but carries reduced weight: the proxy is informational input, not a position that can be counted toward consensus or disagreement.

5. **Exclude.** If all fallbacks fail, exclude the agent. The Coordinator notes the absence in the Interim Assessment and Synthesis Report with diagnostic. Failed agent outputs (from any step) are never included in synthesis as if they were valid position papers.

**Governor visibility:** Every fallback step taken is reported in the Synthesis Report's Agent Status table and Cost Report. The Governor sees exactly what happened: which agents succeeded normally, which required fallback, which were excluded, and what reduced coverage resulted.

### §1.1a Concurrency Conflict Resolution (Code mode — parallel subagents)

When Code mode dispatches multiple subagents for the same deliberation round and an ambiguous-failure condition triggers a replacement dispatch, conflicting completions are possible. The following canonical ordering rule applies.

**File path policy (prerequisite):**
Background and replacement position papers MUST be written to distinct file paths:
- Background (original dispatch): `position-[AGENT_ID]-R[N]-bg.md`
- Replacement (foreground dispatch): `position-[AGENT_ID]-R[N].md`

This prevents silent overwrites. The coexistence of both files at phase synthesis is the signal that a conflict occurred.

**Canonical ordering rule:**

1. **First dispatch confirmed before replacement dispatched:** If the background agent's task notification arrived (status: `completed`) before the replacement dispatch was issued, the background output is canonical. The replacement output is logged and discarded. Coordinator notes: `CONFLICT-[AGENT_ID]-R[N]: background confirmed first. Background output canonical. Replacement discarded.`

2. **Replacement dispatched before first dispatch confirmed (ambiguous failure):** If the replacement was dispatched after observing an error return (status: `failed` or `error`) but before receiving a completion notification, the replacement output is canonical upon its successful completion. If the background agent later completes (stale notification), its output is archived at `position-[AGENT_ID]-R[N]-bg.md` but NOT incorporated into synthesis. Coordinator notes: `CONFLICT-[AGENT_ID]-R[N]: replacement dispatched under ambiguous failure. Replacement output canonical. Background output archived for Governor review.`

3. **Both task notifications arrive, both files exist:** The Coordinator computes composite scores from each set independently and presents the divergence to the Governor as a DISPUTED-OUTPUT block before synthesis proceeds:

   ```
   DISPUTED-OUTPUT | Agent: [AGENT_ID] | Round: [N]
   Background position: [file path] — [summary of divergent scores]
   Replacement position: [file path] — [summary of divergent scores]
   Composite score delta: [feature IDs with score differences ≥1 point]
   Governor decision required: Which output is canonical, or should both be
   incorporated with averaged scores? Synthesis is blocked until resolved.
   ```

**Cost implication:** Both file outputs are retained in the session directory. Stale background outputs are never deleted — they are archival evidence. Include in Cost Report: `Background agent conflict: [N] instances. Background outputs archived at [paths].`

**Live deliberation dashboard.** The Coordinator maintains a `deliberation-status.md` file in the deliberation directory (or session root if no deliberation directory exists). This file is overwrite-only — updated after every round completion, agent status change, and deliberation close. It shows: current round, agent status table, convergence tracker (agreement spread, hard disagreements, new arguments), termination assessment (convergence/stall/argument gate status), artifacts produced, and pending Governor actions. Use the template in `cowork/templates/deliberation-status.md`. The Governor can monitor this file in a separate terminal alongside `session-status.md` for real-time visibility into both scope-level and deliberation-level state.

**Cost tracking.** The Coordinator maintains a running cost ledger for each deliberation cycle:

```markdown
#### Cost Report
| Metric | Value |
|--------|-------|
| Agents dispatched | [N] |
| Agents completed | [N] |
| Agents failed/timed out | [N] |
| Rounds executed | [N of max] |
| Round 2+ agents (subset) | [N] |
| Estimated token consumption | [N tokens or cost estimate] |
| Cost per substantive disagreement | [tokens / disagreement count] |
| Early termination savings | [rounds skipped × estimated cost per round] |
```

The cost report is included in every Synthesis Report. Over time, it gives the Governor data to tune the roster (remove agents that never produce unique disagreements), adjust round counts, and compare deliberation cost against decision quality.

**Mode-specific precision.** In Code mode and Coded implementations, token consumption can be measured exactly from API responses. In Cowork mode (single-session sequential), token consumption is estimated — the Coordinator should note "estimated" in the cost report and use rough per-agent estimates based on position paper length.

**Cost budget.** The OD Deliberation section may declare a per-cycle cost budget. If the Coordinator estimates that proceeding to Round 2 would exceed the budget, it terminates after Round 1 and notes the budget constraint in the Synthesis Report. The Governor can override ("proceed despite budget") or accept the truncated deliberation.

**Early termination authority.** The Coordinator may terminate a deliberation before max rounds when:
- All agents have converged (no new arguments) — standard convergence
- A round produced zero new arguments compared to the prior round — **stall detection** (§5.4)
- Cost budget would be exceeded by the next round
- Fewer than 3 agents completed (insufficient perspectives for meaningful synthesis)

The precise definitions of "convergence," "new argument," and "stall" are scope-specific and declared in the OD Deliberation section (§2.1). The Coordinator applies these definitions mechanically — it does not interpret ambiguous cases in favor of termination or continuation. If the OD does not declare these definitions, the Coordinator uses the defaults shown in the §2.1 template examples.

The Coordinator logs every early termination with the reason. The Governor sees the termination reason in the Synthesis Report.

**Governor (Human):** Final decision authority. Reviews synthesis reports. Resolves hard disagreements. Approves, modifies, or rejects the synthesized recommendation. The Governor's role is unchanged from the Cowork Protocol — the deliberation system presents better-structured recommendations, but authority stays with the Governor.

---

## 2. Agent Topology

### 2.1 Roster Definition

The agent roster is declared in the operating document under a new `## Deliberation` section (after Review Schedule, before Domain Models Referenced):

```markdown
## Deliberation

### Agent Roster

| Agent ID | Domain Model | Role | Model/Provider | Trust Boundaries | Notes |
|----------|-------------|------|----------------|------------------|-------|
| VC-1 | Value Creation | domain_agent | default | identity, communication | |
| MK-1 | Marketing | domain_agent | default | identity, communication | |
| SL-1 | Sales | domain_agent | default | identity, communication | |
| VD-1 | Value Delivery | domain_agent | default | identity, communication | |
| NIS2-1 | NIS2 | domain_agent | default | identity, communication | |
| DORA-1 | DORA | domain_agent | default | identity, communication | |
| GDPR-1 | GDPR | domain_agent | default | identity, communication | |
| COORD-1 | — | coordinator | default | communication, oversight | No domain model |

**Trust Boundaries** `[ROBUST]` (from Framework §14.3.10): Declares which trust boundaries each agent's claims cross during deliberation. All domain agents cross `identity` (different domain models) and `communication` (positions flow through Coordinator). The Coordinator crosses `communication` (paraphrases agent positions) and `oversight` (its synthesis is what the Governor reads). Additional boundaries may apply: `memory` (if session spans multiple conversations), `retrieval` (if agent uses reference pool), `execution` (if agent's recommendations drive actions). Claims crossing declared boundaries carry propagation tracking obligations — see Framework §14.3.10.

### Deliberation Cadence
- **Trigger:** [on_signal | on_schedule | on_governor_request | on_phase_gate]
- **Min Rounds:** [integer] (default: 1 for ongoing scopes, 3 for finite/stress-test scopes. Hard floor — convergence, stall detection, and New Argument Gate cannot trigger early termination before Min Rounds is reached.)
- **Max Rounds:** [N] (finite default: 5, ongoing default: 2)
- **New Argument Gate (Round 4+):** [enabled | disabled] (default: enabled)
- **Convergence Threshold:** [see §5]
- **Convergence Definition:** [What counts as convergence — e.g., "all agents within 1 point on recommendation, no new hard disagreements for 1 round"]
- **New Argument Definition:** [What counts as a new argument vs. restatement — e.g., "introduces a domain concept not previously cited, or applies an existing concept to a scenario not previously analyzed"]
- **Stall Definition:** [What counts as a stall — e.g., "two consecutive rounds with zero position changes and no new arguments from any agent"]
- **Governor Interaction:** [at_synthesis | mid_deliberation]
- **Agent Timeout:** [duration] (default: 5 min for Code mode, 1 session for Cowork)
- **Cost Budget:** [optional — max tokens or cost per deliberation cycle]
```

**Engineered Contradiction Register (optional, analytical scopes only):**
In analytical scopes, guardrail tensions may be intentionally engineered to explore how the protocol handles competing constraints. When guardrail conflicts are by design (not calibration errors), declare them in an Engineered Contradiction Register:
```
Engineered Contradiction Register:
  - pair: [guardrail A, guardrail B]
    expected_resolution: [hard wins / case-by-case / governor adjudication]
    observable_outcomes: [what to watch for — e.g., "does domain X score drop below floor?"]
  - pair: [guardrail C, guardrail D]
    expected_resolution: [...]
    observable_outcomes: [...]
```
When a register is declared, the orchestrator documents each contradiction's resolution in the decision log rather than treating it as a calibration error. Agents referencing a registered contradiction in their Guardrail Assessment should note the engineered nature: "G-X and G-Y are in registered tension; my scoring reflects the trade-off, not an error."

**Termination threshold calibration guidance:**

The three threshold definitions (Convergence, New Argument, Stall) interact with agent count and domain complexity. Governors should calibrate based on:

| Factor | Loose thresholds | Tight thresholds |
|--------|-----------------|------------------|
| Agent count | 3 agents (limited disagreement surface) | 5-7 agents (rich disagreement surface) |
| Domain complexity | Rich domain models (15+ concepts each) | Thin domain models (<5 concepts each) |
| Decision stakes | High-stakes, irreversible decisions | Low-stakes, reversible decisions |
| Scope type | Ongoing (recurring deliberation — can revisit) | Finite (one-shot — must be thorough) |

Specific calibration notes:

- **Convergence Definition — confidence threshold.** "All agents within N points" should scale with agent count. With 3 agents, a 3-point spread (e.g., 6/10 vs 9/10) can represent substantive convergence if all agents recommend the same action. With 7 agents, a 2-point spread is more appropriate since outlier confidence is more likely meaningful. Sim validation (DELIB-VAL-002) showed that a 2-point threshold was too strict for a 3-agent deliberation where agents converged substantively despite a 3-point confidence gap.
- **Stall Definition — round count.** For thin domain models (<5 concepts per domain), one round of zero-progress is sufficient to declare stall (validated in DELIB-VAL-003). For rich domain models (15+ concepts), use two consecutive rounds — agents may need an extra round to synthesize cross-domain insights that appear as "restatements" initially but shift emphasis.
- **New Argument Definition — reframing vs. new concept.** The boundary between "reframing an existing argument" and "introducing a new concept" is the hardest to calibrate. Default guidance: if the argument cites the same domain model concepts as a prior round but applies them to a different scenario, it counts as new. If it cites the same concepts applied to the same scenario with different emphasis, it does not.

**Model/Provider column:** Specifies which LLM model and provider each agent runs on. `default` means the same model as the orchestrating session (e.g., if running in Claude Code, all agents use Claude). For multi-model deliberation, specify the model explicitly (e.g., `claude-opus-4-6`, `gpt-4o`, `gemini-2.5-pro`). See §8.4 for multi-model guidance.

Multi-model benefits: reduced groupthink (different base models have different biases), potential quality improvement (some models may be stronger in specific domains), and resilience (if one provider is down, other agents still complete). Multi-model costs: inconsistent position paper quality, increased infrastructure complexity, varied latency, and more complex cost tracking.

### 2.2 Roster Rules

- **One agent per domain model.** No agent holds two domains. No domain is split across agents. This is the isolation guarantee — each agent's reasoning is traceable to exactly one domain model.
- **Coordinator is mandatory.** A deliberation without a coordinator is just parallel scoring — the synthesis function must be explicit, not implicit.
- **Minimum 3 domain agents.** Fewer than 3 provides insufficient disagreement surface. Below 3, use the Cowork Protocol's standard multi-domain assessment (§7.5) instead of this protocol.
- **Recommended range: 5-7 domain agents** for full analytical depth (21 pairwise combinations at most). **8-10 agents is viable** but requires a minimum of 4 rounds to achieve equivalent cross-examination coverage — at 3 rounds, approximately 47% of pairwise combinations receive direct cross-examination, leaving coverage gaps on less tractable disagreements. For >10 agents, use cluster-then-synthesize: group related domains into 3-4 clusters, synthesize within clusters (Rounds 1-2), then synthesize across clusters (Round 3+). At any agent count, Coordinator synthesis quality degrades faster than linearly — plan for additional synthesis capacity (more rounds or coordinator iterations) when exceeding 7 agents. If more than 7 domains are needed but full analytical depth is required, consider grouping related domains into composite agents (e.g., a "Regulatory" agent holding a stacked NIS2+DORA+GDPR model) as an alternative to increasing agent count.
- **Agent IDs are stable** for the scope's lifetime. The same agent keeps the same ID across cycles. This enables disagreement tracking over time.

### 2.3 Shared Context

All agents (domain agents and coordinator) receive the same shared context:
- Operating document (current version)
- The evaluation target (current roadmap, feature list, scoring target, or whatever is being deliberated)
  When the evaluation target is a tournament output (§4.6): all N candidate deliverables with their cell assignments (constrained mode) or run IDs (sampling mode). Agents evaluate all candidates, not just one. The shared context includes the behavior space declaration so agents can assess whether dimensional variation produced meaningful differentiation.
- Recent signals relevant to the deliberation trigger
- Prior synthesis reports (if this is not the first deliberation cycle)
- Curated reference materials from the Reference Pool (see below)

Domain agents additionally receive:
- Their assigned domain model (and only theirs)

The Coordinator additionally receives:
- All domain models (for reference, not evaluation)
- All position papers from the current and prior rounds

**Reference Pool curation for deliberation.** The Coordinator selects relevant Reference Pool items (§17.2.4) for inclusion in shared context at deliberation setup. Selection uses the Reference Pool's existing relevance scoring: scope specificity (items scoped to the deliberation topic score highest), recency, and access frequency. The Coordinator includes items up to the agent context budget — not a full dump. Items with `consumption_role: options-universe` that are scoped to the deliberation topic are always included (they contain the material being evaluated). Items with `consumption_role: context` are included by relevance rank until the context budget is reached. If an agent identifies a gap during a round ("I need the regulatory text for Article 5"), the Coordinator retrieves the specific item from the Reference Pool and includes it in the next round's shared context. This is the same curation pattern the orchestrator uses when assembling action specifications for executors — the Coordinator curates, not dumps.

### 2.4 Pre-Deliberation Governor Review

Before deliberation begins, the Coordinator prompts the Governor to review and update existing information channels. This ensures agents deliberate with current, grounded information — without introducing an ungrounded input channel.

**Checklist (Coordinator presents to Governor before Round 1):**

1. **OD currency:** "Does the operating document reflect your current intent? Any constraints, budget changes, or strategic decisions made since the last OD update?" → If yes, Governor amends the OD before deliberation starts. Amendments go through standard structural validation (§8.1 C1-C3).
2. **Environmental watch list:** "Have any external conditions changed — regulatory, market, partner, competitive?" → If yes, Governor updates the environmental watch list (§7.14) or adds entries. Changes enter the signal architecture with standard provenance.
3. **Reference material:** "Do you have documents, data, or research that agents should consider?" → If yes, Governor adds to the Reference Pool (§17.2.4). Material enters with Governor curation attribution.
4. **Specific questions:** "Are there specific questions you want the deliberation to address beyond the trigger topic?" → If yes, Coordinator incorporates these as targeted prompts in Round 1 instructions.

**Default behavior:** The OD Deliberation Cadence sets `Pre-Deliberation Review: required` (default). The Coordinator does not start Round 1 until the Governor confirms the checklist — either by making updates or confirming "no changes needed." When set to `optional`, the Coordinator proceeds after a reasonable timeout if the Governor doesn't respond.

**Why not a separate input document?** Governor knowledge that affects deliberation should be formalized through channels that have existing quality gates: OD amendments (structural validation), environmental watch list (signal architecture), Reference Pool (Governor curation). A separate "Context Brief" would bypass these gates, creating an ungrounded input vector where unverified Governor assertions carry the same evidentiary weight as validated signals.

**Tier guidance:**
- **Tier 0:** Coordinator asks the checklist questions conversationally. Governor responds and makes any updates before Round 1 begins.
- **Tier 1:** Checklist presented as a structured pre-deliberation form. OD/watch list/reference pool updates are tracked as pre-deliberation amendments.
- **Tier 2+:** System auto-detects potentially stale OD entries and watch list items, highlighting them in the checklist for Governor attention.

---

## 3. Round Structure

A deliberation consists of multiple rounds plus synthesis. Round count depends on scope type and Governor configuration.

### 3.0 Round Count Configuration

Round count varies by scope type because the iteration mechanism differs:

**Ongoing scopes (default: 2-3 rounds).** In ongoing scopes, the *cycles themselves* are the iteration mechanism. You don't need 10 rounds in one deliberation when you'll have another deliberation next month with new signals. Disagreements that don't resolve in 2-3 rounds are better served by new evidence arriving in the next cycle than by agents re-arguing the same evidence. Range: 2-5. Default: 2.

**Finite scopes (default: 3-5 rounds).** In finite scopes, the deliverable is produced once — the cost of extra rounds is paid once, and quality improvement compounds into the final output. More rounds make sense because there is no "next cycle" to carry unresolved disagreements forward. However, rounds beyond 3 require the Coordinator to certify that new arguments emerged (not just restatements). If no new arguments, the Coordinator terminates early regardless of the cap. Range: 3-10. Default: 5.

**Governor-settable.** The round count is declared in the OD's Deliberation section:

```markdown
### Deliberation Cadence
- **Max Rounds:** [N] (finite default: 5, ongoing default: 2)
- **New Argument Gate (Round 4+):** [enabled | disabled] (default: enabled)
```

When the New Argument Gate is enabled, the Coordinator checks after each round (starting at Round 4): did any agent introduce a genuinely new argument — not a restatement, elaboration, or emphasis shift of an existing argument? If no new arguments, the Coordinator terminates the deliberation and proceeds to Synthesis, regardless of remaining rounds. This prevents token waste on diminishing returns while allowing Governors who want deeper deliberation to configure higher caps.

### 3.0 Pre-Round Concept Consistency Check `[ADVANCED]` (Framework §8.1.3 — A2)

When deliberation involves 3+ domain models that share concepts with the same name but potentially different definitions (e.g., "risk" in a financial model vs. a compliance model vs. an operational model), the Coordinator performs a cross-domain concept consistency check before Round 1 begins. This catches definitional conflicts that would otherwise surface as phantom disagreements in Round 2.

**Procedure:**
1. Extract all concept names from each participating domain model.
2. Identify shared concept names (appearing in 2+ models).
3. For each shared concept, compare definitions across models.
4. If definitions diverge: flag as `[CONCEPT-DIVERGENCE]` with the differing definitions, and include the divergence in the shared context (§2.3) so agents are aware of the terminological ambiguity before producing position papers.
5. If definitions are compatible but one model's definition is strictly narrower: note as `[CONCEPT-NARROWING]` — not a conflict, but a source of potential miscommunication.

**Implementation by tier:** At Tier 0 (Cowork mode), the Coordinator scans domain model concept tables before starting Round 1 and notes any shared terms with different definitions. At Tier 1+, automated string matching identifies shared concept names and surfaces definition pairs for Coordinator review. At Tier 2+, semantic similarity scoring flags concepts with high name similarity but low definition similarity.

**If no shared concepts exist** (fully disjoint domain models), skip this step — there is no cross-domain concept ambiguity to resolve.

### 3.1 Round 1: Independent Evaluation

All domain agents evaluate in parallel. Each agent receives:
- Shared context (§2.3)
- Its domain model
- The deliberation prompt (what to evaluate and what format to use)

Each agent produces a **Position Paper** (§4.1).

Agents do NOT see each other's positions in Round 1. This is the isolation guarantee — Round 1 positions are independent assessments, not influenced by other agents' framing.

**Implementation note (Cowork/Code mode):** In Code mode, launch domain agents as parallel subagents. In Cowork mode, run each agent as a separate conversation or clearly labeled sequential section with no back-revision (equivalent to Cowork Protocol §7.5 Level 2 Sequential Isolation, but producing position papers instead of scores).

**Position Independence Verification (from Framework §14.3.9).** After collecting all Round 1 position papers, the Coordinator performs a sycophancy check before producing the Interim Assessment:

1. **Recommendation alignment check:** Do all agents recommend the same action? If yes, flag `round1_unanimity` in the Interim Assessment.
2. **Reasoning diversity check:** Even if recommendations align, do the reasoning paths differ substantively? If all agents cite the same evidence in the same order with the same emphasis, the alignment is suspicious — domain models should produce different reasoning paths even when reaching the same conclusion.
3. **OD-anchoring check:** Do position papers primarily reference OD strategy rationale rather than domain model concepts? If >50% of cited concepts come from OD rather than domain models, agents may be anchoring to Governor intent instead of reasoning from their domains.

**If `round1_unanimity` is flagged:** The Coordinator must include a Convergence Probe in Round 2 prompts (see §4.5).

### 3.2 Round Completion Gate

A round is not considered complete until:
1. **All position/response papers** from participating agents exist on disk at their specified paths in `deliberation/DELIB-XXX/`
2. **`deliberation-status.md`** has been updated to reflect the round's score matrix and agent positions
3. **A round-completion signal** exists in `signals/` with minimum content: round number, agent count, score summary, hard disagreement count, guardrail violation count

The Coordinator MUST verify these three conditions before producing the Interim Assessment. If any condition is unmet, the Coordinator notes the gap explicitly in the Interim Assessment header ("Round N: 9/10 papers received; Agent X missing — excluded from synthesis") and proceeds. An acknowledged gap is acceptable; a silent gap is a protocol violation.

### 3.3 Coordinator Interim Assessment

After Round 1 (and after each subsequent round in multi-round deliberations), the Coordinator reads all position/response papers and produces an **Interim Assessment** (§4.2).

The Coordinator also tracks epistemic signals — information gaps and conditional assumptions surfaced by agents (from Confidence Basis and Falsifiability fields) — for aggregation into the Finding Classification at synthesis. Additionally, the Coordinator maintains a cumulative Issue Ledger tracking each identified issue's status across rounds.

The Interim Assessment determines whether the next round is needed:
- If **zero hard disagreements and zero novel arguments**: skip Round 2, proceed to Synthesis.
- If **any hard disagreements or novel arguments**: proceed to Round 2.

### 3.4 Round 2+: Response and Refinement

Domain agents that are referenced in the Coordinator's Round N Prompts receive:
- Their most recent position or response paper
- The most recent Interim Assessment (all of it — agreements, disagreements, novel arguments)
- The specific Round N Prompt directed at them

Each agent produces a **Response Paper** (§4.3). Agents may:
- **Strengthen** their position with additional reasoning
- **Concede** a point, modifying their recommendation
- **Reframe** the disagreement — argue that the apparent conflict dissolves under a different framing
- **Escalate** — declare that this disagreement cannot be resolved without Governor input and explain why

Agents that are NOT referenced in Round N Prompts do not participate in that round — their most recent position stands.

**Multi-round flow (Round 3+).** For deliberations with max rounds > 2, each subsequent round follows the same pattern: Coordinator produces an Interim Assessment after the round, identifies remaining disagreements and any new arguments, issues prompts for the next round. The Coordinator's Interim Assessment accumulates — each version references what changed since the prior assessment, not just the full state. This prevents agents from losing track of what's already been argued.

**New Argument Gate (Round 4+).** When enabled (default), the Coordinator evaluates after each round starting at Round 4: did any response paper contain a genuinely new argument? A "new argument" is defined as: a domain concept not previously cited in any position or response paper, OR an application of a previously cited concept to a scenario or evaluation target not previously considered, OR new evidence (a signal that arrived during deliberation). Restatements with different words, emphasis shifts, and elaborations of existing arguments do not qualify. If no new arguments, the Coordinator terminates and proceeds to Synthesis. The Coordinator logs the gate evaluation: "Round [N] new argument gate: [passed — new argument from Agent X citing concept Y] or [failed — no new arguments detected, terminating]."

### 3.5 Synthesis

After the final round (or after Round 1 if subsequent rounds were skipped), the Coordinator produces a **Synthesis Report** (§4.4). This is what the Governor sees.

### 3.5 Governor Review

The Governor receives the Synthesis Report and decides:
- **Accept** — Adopt the synthesized recommendation as-is.
- **Modify** — Accept with specific changes, citing reasoning.
- **Override** — Reject the synthesis and impose a different decision, citing reasoning.
- **Remand** — Send back to deliberation with specific guidance ("I need you to re-evaluate assuming X" or "The Value Delivery agent's concern about F09 complexity is the binding constraint — re-run with that as a hard guardrail").

All Governor decisions are recorded in `decisions/governor-decisions.md` per Cowork Protocol §8.

---

## 4. Artifact Formats

### 4.1 Position Paper (Domain Agent, Round 1)

```markdown
### Position Paper — [Agent ID] | [Date] [Deliberation ID] | Round 1

**Domain:** [Domain model name]
**Evaluation Target:** [What is being evaluated]

**Tournament Evaluation (if applicable):**
- Candidates evaluated: [list deliverable refs with cell assignments]
- Ranking: [ordered list, best to worst, from this domain's perspective]
- Ranking rationale: [why this ordering — cite domain concepts]
- Cross-cell observation: [any pattern across cells visible from this domain — e.g., "problem-first cells consistently score higher on [concept] because..."]

#### Recommendation
[The agent's recommendation — specific, actionable, traceable to domain concepts]

#### Reasoning
[Why this recommendation follows from the domain model. Must cite specific domain concepts by name.]

#### Domain Concepts Applied
**Cite-then-apply (§14.3.2 retrieval faithfulness):** For each concept, state its definition from the domain model before describing how it applies. The "How It Applies" column must be traceable to the concept as defined — not a narrowed, broadened, or drifted version.

| Concept | From Domain Model Section | How It Applies |
|---------|--------------------------|----------------|
| [concept name] | [section] | [application to this evaluation] |

#### Guardrail Assessment
[Which inherited guardrails are relevant from this domain's perspective. Any guardrails at risk of violation. **Note:** Mechanical guardrails (evaluation: mechanical) are pre-evaluated before deliberation — agents receive their pass/fail results as given facts. Agents evaluate only interpretive guardrails from their domain perspective. If a guardrail's activation depends on unverified factual claims, tag it as **Provisional** — indicating that its status (Active or Superseded) depends on verification. The Coordinator tracks Provisional guardrails across agents and resolves them when verification data arrives.]

#### Confidence
[1-10 integer. How confident is this agent in its recommendation, given the available signals?]

#### Confidence Basis
[What would increase or decrease confidence? What signals are missing?]

#### Falsifiability
[What evidence would disprove this recommendation? What observable outcome would cause this agent to reverse its position? Must be specific and testable — not "if the data changes" but "if metric X fails to reach Y by date Z."]

#### Cross-Boundary Claims `[ROBUST]`
[List any claims in this paper that are NOT grounded in this agent's domain model. For each: state the claim, its basis (training data, another agent's position, external knowledge), and flag as `[UNGROUNDED]` or `[CROSS-DOMAIN: source-model, concept]`. If all claims are grounded in the assigned domain model, state: "All claims grounded in [domain model name]."]

#### Dissent from Prior Cycle
[If a prior deliberation produced a different recommendation: what changed and why. If first deliberation: "N/A — first cycle."]
```

### 4.2 Interim Assessment (Coordinator, after each round)

```markdown
### Interim Assessment — [Date] [Deliberation ID] | After Round [N]

**Coordinator:** [Coordinator ID]
**Agents Reporting:** [list of Agent IDs that completed this round] ([N]/[total] completed)

#### Agreements
[Where 2+ agents recommend the same thing, with the same reasoning or compatible reasoning]

#### Soft Disagreements
[Where agents recommend different emphasis or priority but their recommendations are compatible — both could be implemented]

#### Hard Disagreements
[Where agents recommend mutually exclusive actions — implementing one precludes the other. Each disagreement assigned a DIS-ID.]

#### Novel Arguments
[Arguments raised by one agent that no other agent addressed — these may represent blind spots in other domains]

#### Issue Ledger (cumulative)

| Issue ID | Description | By Agent(s) | Round Raised | Current Status | Resolution Round | Resolution Method |
|----------|-------------|-------------|-------------|----------------|-----------------|-------------------|
| ISS-1 | [1-line description] | [agent IDs] | R1 | [open / narrowed / provisionally_resolved / resolved / escalated] | [Rn or —] | [concession / new_evidence / governor_input / reframe / —] |

**Status definitions:**
- `open` — Issue raised, no agent has conceded or provided resolving evidence.
- `narrowed` — Agents have reduced the scope of disagreement (e.g., from "reject entire strategy" to "reject component X of strategy") but haven't resolved it.
- `provisionally_resolved` — The raising agent's concern has been addressed (via concession, evidence, or reframe), but the Coordinator flags it for review at synthesis because: (a) the resolution depends on unverified data, or (b) only one agent conceded while others haven't weighed in, or (c) resolution depends on Governor-asserted information that hasn't been independently verified.
- `resolved` — Issue resolved to the Coordinator's satisfaction. Both sides agree or one side conceded with reasoning. Enters `Resolved Disagreements` in Synthesis Report.
- `escalated` — Agent explicitly escalated to Governor (position update: `escalated`). Enters `Unresolved Disagreements` in Synthesis Report.

The Coordinator carries this ledger forward in each Interim Assessment, updating statuses after each round. New issues receive new ISS-IDs. The ledger is cumulative — no entries are removed, only status-updated.

#### Epistemic Signals
[Which agents flagged information gaps (from Confidence Basis fields)? Which agents specified conditions (from Falsifiability fields)? Note patterns — e.g., "3 agents flag missing market data; this will likely become an information_gap finding at synthesis."]

#### Position Independence Assessment (§14.3.9)
- **Round 1 unanimity:** [yes — all agents recommend same action | no — substantive disagreements exist]
- **Reasoning diversity:** [diverse — different domain concepts drive reasoning | homogeneous — same evidence, same order, same emphasis]
- **OD-anchoring indicator:** [low (<30% OD citations) | moderate (30-50%) | high (>50% OD citations vs domain model citations)]
- **Convergence probe required:** [yes — Round 2 will include devil's advocate prompt | no — sufficient independence demonstrated]

#### Round [N+1] Prompts
[For each hard disagreement and novel argument: a specific question directed at relevant agents. See prompt formulation guidance below.]
```

**Prompt formulation guidance.** The Round N+1 Prompts are the highest-leverage element of the deliberation — they determine whether agents produce new reasoning or simply restate. Each prompt should:

- **(a) Reference a specific hard disagreement or novel argument** — "HD-1: Agent DIP-1 says casualty counts are noise; Agent MIL-1 says they are critical signals."
- **(b) Name the challenging agent and their concept** — "INFO-1 argues, citing Source Credibility Spectrum, that your factual basis is unverified."
- **(c) Ask a question that cannot be answered by restating the existing position** — "If the coalition's damage claims are overstated by 2x, how does your recommendation change?" forces a conditional analysis, not a restatement.

Weak prompts ("do you still agree with your position?") produce restated positions. Strong prompts ("if X is true, how does your Y change?") produce new reasoning.

**Cross-domain convergence detection.** When preparing the Interim Assessment, the Coordinator should explicitly check whether agents from different domain categories independently converge on the same recommendation. Cross-domain convergence (e.g., all regulatory agents recommending the same feature from different regulatory frameworks) carries outsized persuasive weight in Round 2 prompts and should be flagged as a novel argument. session validation showed this pattern directly caused 2 of 3 business agents to revise their positions.

**Naming convention.** Response papers are named `response-{AGENT-ID}.md`, replacing any Round 1 position paper filename pattern. In Cowork mode, the Coordinator specifies the exact filename in the agent prompt to prevent deviation.

### 4.3 Response Paper (Domain Agent, Round [N])

```markdown
### Response Paper — [Agent ID] | [Date] [Deliberation ID] | Round [N]

**Responding to:** [Coordinator's Round [N] Prompt — quoted]

#### Position Update
[strengthened | conceded | reframed | escalated]

#### Response
[The agent's response to the specific prompt. If conceding, what changed and why. If strengthening, what additional reasoning. If reframing, the proposed reframe. If escalating, why this cannot be resolved without the Governor.]

#### Additional Domain Concepts
[Any new domain concepts cited that were not in Round 1. If none: "No new concepts."]

#### Guardrail Assessment Update
[If the response changes the guardrail picture: what changed. If unchanged: "No change from Round 1."]

#### Confidence Update
[Updated confidence 1-10 if changed. If unchanged: "Unchanged at [N]."]

#### Impact on Recommendation
[Does the most recent recommendation change? If yes, the revised recommendation. If no, confirmation that it stands.]
```

### 4.4 Synthesis Report (Coordinator)

```markdown
### Synthesis Report — [Date] [Deliberation ID]

**Agents:** [list of Agent IDs that participated]
**Rounds:** [N of max]
**Trigger:** [what triggered this deliberation]

#### Tournament Selection Recommendation (if evaluation target was tournament output)
- **Recommended candidate:** [deliverable_ref] from cell [X] (constrained) or run [N] (sampling)
- **Consensus on selection:** [full | strong | weak | split — using §5.1 definitions]
- **Per-candidate scores by agent:**
  | Candidate | Cell | Agent 1 | Agent 2 | ... | Mean |
  |---|---|---|---|---|---|
  | [ref] | [cell] | [score] | [score] | ... | [mean] |
- **Behavior Space Analysis (constrained mode):**
  - Dimension impact: [which dimensions produced the largest score swings]
  - Structural insight: [any design principle revealed by cross-cell patterns — e.g., "evidence-first entry consistently outperforms problem-first across all domains"]
  - Recommended structural memory entry: [what should be recorded for future behavior space design]

#### Consensus Recommendation
[The recommendation that emerges from synthesis. If full consensus: state it. If partial consensus with unresolved disagreements: state the majority recommendation and note the dissents.]

#### Consensus Strength
- **Full consensus:** All agents agree on recommendation (may differ on emphasis)
- **Strong consensus:** 5+ of 7 agents agree; dissenting agents' concerns are addressable
- **Weak consensus:** 4 of 7 agents agree; dissenting agents raise substantive concerns
- **Split:** No majority; Governor must decide between competing recommendations

#### Agreement Map
[What all or most agents agree on — the common ground]

#### Resolved Disagreements
[Disagreements from earlier rounds resolved during deliberation, with resolution chain from Issue Ledger]

| DIS-ID | Issue | Raised Round | Resolved Round | Resolution Method | Chain |
|--------|-------|-------------|---------------|-------------------|-------|
| DIS-001-01 | [description] | R1 | R3 | concession by Agent X | R1: open → R2: narrowed → R3: resolved (Agent X conceded citing new evidence) |

#### Provisionally Resolved (Coordinator Review)
[Issues where the raising agent's concern was addressed but the Coordinator flags for Governor awareness — resolution may be fragile]

| ISS-ID | Issue | Resolution | Why Provisional |
|--------|-------|-----------|-----------------|
| ISS-3 | [description] | [how addressed] | [unverified data / single-agent concession / conditional on assumption] |

#### Unresolved Disagreements
| Disagreement ID | Agents For | Agents Against | Nature | Governor Action Needed |
|----------------|------------|----------------|--------|----------------------|
| [DIS-NNN] | [agent IDs] | [agent IDs] | [hard/soft] | [yes/no] |

For each unresolved disagreement:
- **Agent A's position:** [summary with domain concept citations]
- **Agent B's position:** [summary with domain concept citations]
- **Why it's unresolved:** [what makes these positions incompatible]
- **Coordinator's framing:** [how the Governor should think about this — NOT a recommendation, but a framing of the tradeoff]

#### Confidence Distribution
| Agent ID | Confidence | Key Concern |
|----------|-----------|-------------|
| [agent] | [1-10] | [primary concern if confidence < 7] |

#### Groupthink Check
[Did all agents converge suspiciously quickly? If all positions are nearly identical despite different domain models, flag: "All agents agree. This may indicate genuine alignment or shared base-model bias. Governor should probe: is there a perspective none of the domains represent?"]

#### Agent Status
| Agent ID | Status | Fallback Used | Notes |
|----------|--------|---------------|-------|
| [agent] | [completed / reduced_model / proxy / timed_out / failed / excluded] | [none / reduced_model / proxy / N/A] | [if not completed normally: what happened, which fallback step reached] |

**Proxy Positions:** [If any agents required the extract-and-represent fallback (§1.1 step 4): list each proxy with its label. "Agent [ID] ([domain]) — proxy position generated from domain model Quality Principles and Anti-Patterns. NOT a full position paper. Does not count toward consensus. Included as informational input only."]

**Missing Perspectives:** [If any agents were fully excluded (§1.1 step 5): "This synthesis lacks [domain] perspective entirely. The recommendation may shift if [domain] were included. Governor should weight accordingly."]

#### Cost Report
| Metric | Value |
|--------|-------|
| Agents dispatched | [N] |
| Agents completed | [N] |
| Agents failed/timed out | [N] |
| Rounds executed | [N of max] |
| Round 2+ agents (subset) | [N] |
| Estimated token consumption | [N tokens or cost estimate] |
| Cost per substantive disagreement | [tokens / disagreement count] |
| Early termination | [yes/no — if yes, reason and estimated savings] |
| New argument gate activations | [Round N: passed/failed] |

#### Finding Classification (from Framework §14.3.8)
Every substantive finding in this report (from Consensus Recommendation, Resolved Disagreements, Provisionally Resolved, and Unresolved Disagreements) is classified by epistemic status:

| Finding # | Finding (1-line) | Classification | Evidence / Gap / Condition |
|-----------|-----------------|----------------|---------------------------|
| F-1 | [finding summary] | confirmed | Evidence: [signal refs, agent citations from Attribution Chains] |
| F-2 | [finding summary] | information_gap | Missing: [what data would resolve this]. Source: [which agent(s) flagged gap, citing Confidence Basis] |
| F-3 | [finding summary] | conditional | Condition: [testable assumption]. Test: [how and when to verify]. Source: [which agent(s), citing Falsifiability field] |

**Classification rules:**
- `confirmed` — 2+ agents cite converging evidence from different domains, OR single agent cites a verified signal with full attribution chain.
- `information_gap` — Any agent's Confidence Basis identifies missing signals that would change the recommendation, AND no other agent provides the missing data.
- `conditional` — Any agent's Falsifiability field specifies a testable condition, AND the recommendation explicitly depends on that condition holding.
- If classifiable as both `conditional` and `information_gap`, use `information_gap` — missing data takes priority.

#### Pre-Deliberation Review Impact
[If Governor made pre-deliberation updates: list OD amendments, watch list changes, and reference material added. Note which updates were cited by agents during deliberation. If no updates were made: "Governor confirmed no changes needed at pre-deliberation review."]

#### Stuck/Stall Detection
[If any stuck patterns detected (see §5.4): describe the pattern, which agents are involved, and recommended Governor action. If none: "No stuck patterns detected."]

#### Attribution Chains (from Framework §14.3.4)
Every substantive claim in this report traces to a specific source. The Governor uses this table to verify the Coordinator's characterization without reading full papers.

| # | Claim | Source Agent | Paper Section | Round | Verbatim Quote |
|---|-------|-------------|---------------|-------|----------------|
| 1 | [claim as stated in Consensus Recommendation or Disagreements above] | [Agent ID] | [section heading from Position/Response Paper] | [1 or 2] | "[exact quote from agent's paper supporting this claim]" |

**Completeness requirement:** Every claim in the Consensus Recommendation, Agreement Map, and Unresolved Disagreements sections must have at least one row in this table. If a claim synthesizes multiple agents' positions, include one row per contributing agent.

**Governor verification:** For hard disagreements, the Governor reads the cited paper section and confirms the verbatim quote is not taken out of context. This is the mechanical verification step — compare claim characterization against source quote.

#### Propagation Audit (from Framework §14.3.10) `[ROBUST]`
Claims that crossed agent boundaries with ungrounded status:

| # | Claim | Origin Agent | Origin Round | Grounding Status at Origin | Cited By | Independently Grounded? |
|---|-------|-------------|-------------|---------------------------|----------|------------------------|
| 1 | [claim summary] | [Agent ID] | [Round N] | [UNGROUNDED / PARTIALLY-UNGROUNDED] | [Coordinator / Agent ID in Round M] | [yes: re-grounded in [model, concept] / no: carried as PROPAGATED-UNGROUNDED] |

If no ungrounded claims crossed boundaries: "No ungrounded claims propagated across agent boundaries."

**Trust boundaries crossed:** [List which trust boundary types (identity, communication, memory, oversight) were active in this deliberation. Note any boundary where grounding status was not preserved.]

#### Signals for Next Cycle
[What information would change this recommendation? What should the Governor watch for?]

#### Sycophancy Assessment (§14.3.9)
- **Round 1 independence:** [verified — substantive disagreements in Round 1 | flagged — Round 1 unanimity, convergence probe [result]]
- **OD-anchoring level:** [low / moderate / high]
- **Coordinator neutrality self-check:** [The Coordinator states whether its synthesis framing favors the OD's strategy direction. If yes, identifies the specific framing choices and offers an alternative framing.]
- **Cross-cycle dissent trend:** [healthy (≥1.0 hard disagreements/cycle) | declining | low_dissent_frequency flag active]

#### Governor Decision Required
[YES — with specific question(s) / NO — consensus recommendation can proceed]
```

### 4.5 Convergence Probe Protocol (from Framework §14.3.9) `[ROBUST]`

When Round 1 produces `round1_unanimity` (all agents agree before any cross-examination), the Coordinator issues a Convergence Probe in Round 2. This is not a separate agent role — it is a directed prompt to existing agents.

**Convergence Probe prompt (issued to ALL domain agents in Round 2):**

> "All domain agents agree on [recommendation]. Before this consensus is accepted, identify the strongest argument AGAINST this recommendation from your domain's perspective. Cite specific domain model concepts that could support a different conclusion. If you genuinely cannot construct a counter-argument from your domain model, state why — which domain concepts were considered and why none supports an alternative?"

**Evaluation of probe responses:**
- **Substantive counter-arguments produced:** Genuine independence — the Round 1 agreement was premature, and Round 2 has surfaced real disagreement. Coordinator revises the Interim Assessment.
- **Counter-arguments are weak or formulaic:** Possible sycophancy — agents may be producing token dissent to satisfy the probe without genuine engagement. Coordinator flags in the Synthesis Report: "Convergence probe produced weak counter-arguments — Round 1 consensus may reflect OD anchoring."
- **Agents cannot construct counter-arguments and explain why:** May be genuine alignment — the recommendation is so well-supported that domain models provide no contrary evidence. Coordinator notes in the Synthesis Report with the agents' explanations.

**The probe does not block consensus.** It surfaces information. The Governor decides whether the consensus is trustworthy given the probe results.

**Probe response integration (Coordinator actions by outcome):**
- **`substantive_dissent` (genuine counter-arguments produced):** Coordinator treats Round 2 as a normal disagreement round — revises the Interim Assessment to reflect the new positions, and deliberation continues per standard round progression. The Round 1 unanimity is reclassified as premature consensus. If Min Rounds allows, additional rounds proceed to resolve the newly surfaced disagreements.
- **`weak_dissent` (formulaic or token counter-arguments):** Coordinator notes the weak dissent in the Interim Assessment with the flag: "Convergence probe produced weak counter-arguments — agents may be anchored to OD strategy." The Coordinator does NOT request elaboration (this would invite further token compliance). Instead, the finding flows into the Synthesis Report's Sycophancy Assessment section (§4.4) for Governor evaluation.
- **`genuine_alignment` (agents explain why no counter-argument exists):** Coordinator records the explanations in the Interim Assessment. If Min Rounds is satisfied, the Coordinator may proceed to synthesis. The agents' domain-grounded explanations of why alignment is genuine become evidence in the Synthesis Report — they are not discarded.

In all cases, probe responses are included in the round's artifacts and are available to the Governor alongside position papers and the synthesis.

---

## 5. Convergence and Termination

### 5.1 Convergence Criteria

A deliberation converges when:
- **Full consensus** after Round 1 with zero novel arguments → Skip remaining rounds, proceed to Synthesis. **Exception: if Min Rounds > 1, consensus must hold through Min Rounds before early termination.**
- **Tournament ranking consensus** after any round: all agents agree on the top-ranked candidate (may disagree on lower rankings) → Synthesize with agreed winner. Applies only when evaluation target is tournament output. Disagreement on lower rankings does not block convergence — the Governor needs to know the winner, not the full ordering.
- **All hard disagreements resolved** after any round → Synthesize with resolved positions. **Exception: Min Rounds floor still applies.**
- **New Argument Gate fails** (Round 4+, when enabled) → No new arguments entering the system. Synthesize with current positions.
- **Maximum rounds reached** → Synthesize with unresolved disagreements flagged for Governor.
- **Stall detected** (§5.4) → Coordinator terminates and synthesizes with stuck classification.

**Min Rounds is a hard floor.** When the OD Deliberation Cadence specifies a Min Rounds value, none of the convergence criteria above (except Maximum rounds reached) can trigger termination before Min Rounds is completed. The Coordinator must execute at least Min Rounds even if consensus appears in Round 1. Rationale: early consensus may be false consensus; mandatory minimum rounds allow adversarial challenge of initial agreement. When Min Rounds is not set in the OD, the default is 1 (no minimum floor).

### 5.2 Termination Rules

- **Max rounds is a hard cap.** The Coordinator cannot exceed the configured max rounds even if disagreements persist. Unresolved disagreements go to the Governor.
- **Governor can terminate early.** If the Governor is observing mid-deliberation (Governor Interaction = `mid_deliberation`), they can cut deliberation short and decide based on available position papers.
- **Coordinator can skip rounds.** If any round produces full consensus with no novel arguments, remaining rounds add no value. Coordinator documents the skip reason in the Synthesis Report.
- **Coordinator can terminate for stall.** If stuck patterns are detected (§5.4), the Coordinator terminates and escalates to Governor with diagnostic.
- **Coordinator can terminate for cost.** If the next round would exceed the declared cost budget, the Coordinator terminates and notes the budget constraint.
- **Coordinator can terminate for insufficient agents.** If fewer than 3 agents completed in Round 1 (due to timeouts/failures), the Coordinator terminates — insufficient perspectives for meaningful synthesis. The Coordinator reports which agents failed and recommends retry with adjusted parameters.

### 5.3 Deliberation Triggers (Ongoing Scopes)

In ongoing scopes, deliberation is triggered by:

| Trigger | When | What Agents Evaluate |
|---------|------|---------------------|
| `on_schedule` | At the defined review cadence (e.g., monthly) | Current state of the evaluation target against each domain model |
| `on_signal` | When a signal arrives that affects 2+ domains | The signal's implications from each domain's perspective |
| `on_governor_request` | Governor explicitly requests deliberation | Whatever the Governor specifies |
| `on_phase_gate` | System self-invokes at each phase transition | Phase exit criteria assessment from each domain's perspective. Used when independence ≥ 3 and Governor reviews post-hoc only. |
| `on_kill_approaching` | A tactic's kill condition is within 20% of threshold | Whether to kill, pivot, or persevere — from each domain's perspective |
| `on_external_event` | Market event, regulatory change, competitor action | Impact assessment from each domain's perspective |

The OD declares which triggers are active (default: `on_schedule` + `on_governor_request`). When independence ≥ 3, `on_phase_gate` replaces `on_governor_request` as the default — see startup.md §Group 3A.

### 5.4 Stuck Detection and Resolution

The Coordinator monitors for two stuck patterns that waste resources without producing new insight:

**Repetitive arguments.** An agent's Round N response paper is substantively identical to its Round N-1 paper — same recommendation, same reasoning, same confidence (±1). The Coordinator detects this by comparing: (a) did the recommendation change? (b) did new domain concepts enter the reasoning? (c) did confidence shift by more than 1 point? If all three are "no," the agent is repeating. If 2+ agents are repeating simultaneously, the Coordinator declares a **stall**:

```
STALL DETECTED: Agents [X] and [Y] have not changed positions since Round [N-1].
No new arguments entering the system.
Recommendation: terminate deliberation and escalate unresolved disagreements to Governor.
```

**Circular disagreements.** Agent A cites concept X to argue for recommendation P. Agent B cites concept Y to argue for recommendation Q. In Round N, Agent A responds to Y by re-citing X, and Agent B responds to X by re-citing Y. No new reasoning enters — the agents are reasoning from genuinely incompatible domain premises. The Coordinator detects this by tracking the concept citations across rounds: if the same concept pair appears as the basis for the same disagreement in 2+ consecutive rounds with no new concepts added, the disagreement is **circular**.

Circular disagreements are classified as **structural** — they won't resolve with more rounds because the agents are grounded in genuinely different domain logic. The correct response is Governor decision, not more deliberation.

**Governor intervention for stuck states.** When the Coordinator reports a stall or circular disagreement, the Governor may:

- **(a) Kill the deliberation** — Decide based on available positions. The Governor picks a side or imposes a different decision.
- **(b) Restart with adjusted parameters** — The Governor injects new information or constraints that change the argument landscape. Examples: "Restart but assume build complexity is the binding factor — I want agents to evaluate given that assumption." "Restart but add the constraint that regulatory enforcement will not happen before Q4." The restart uses the same agents but with the Governor's constraint added to the shared context, effectively changing the premises the agents reason from.
- **(c) Modify agent prompts** — The Governor adjusts a specific agent's prompt to break the deadlock. Example: "DORA agent: assume regulatory enforcement will not happen before Q4 — re-evaluate." This is more targeted than a full restart — only the stuck agents re-run.
- **(d) Codify as a standing decision** — If the disagreement is genuinely structural (reflecting permanent domain tension), the Governor decides once and adds the resolution as a guardrail or OD amendment. This prevents the same disagreement from recurring in future cycles. Example: "Business domains and regulatory domains will always disagree on feature sequencing. Standing rule: Phase 1 features must have at least one regulatory anchor (resolved in favor of regulatory) but the primary sequencing logic follows business domains (resolved in favor of business)."

Restart and prompt modification reset the stuck detection counters. If the same stuck pattern recurs after a restart, the Coordinator flags it as a **persistent stuck** — the adjusted parameters didn't resolve the underlying tension. At persistent stuck, the Coordinator recommends option (d) to the Governor.

---

## 6. Disagreement Classification and Tracking

### 6.1 Disagreement Types

| Type | Definition | Resolution Path |
|------|-----------|----------------|
| **Emphasis** | Agents agree on direction but weight factors differently | Coordinator merges — no Governor action |
| **Priority** | Agents agree on what to do but disagree on sequencing/timing | Coordinator surfaces tradeoff — Governor decides if material |
| **Approach** | Agents recommend different methods to the same end | Coordinator frames as A/B — Governor decides or allows both |
| **Fundamental** | Agents recommend mutually exclusive actions based on incompatible domain logic | Governor must decide — no coordinator resolution possible |

### 6.2 Disagreement Behavior Patterns

Beyond the type of disagreement, the Coordinator tracks how disagreements *behave* over time:

| Pattern | Definition | Detection | Response |
|---------|-----------|-----------|----------|
| **Persistent** | Same agents disagree on same issue across 3+ deliberation cycles | Coordinator tracks DIS-IDs across cycles; same agents + same core concepts = persistent | Flag as structural. Governor should decide once and codify as guardrail or OD amendment (§5.4 option d) |
| **Flipping** | Agents swap positions cycle-to-cycle (Agent A argued P in cycle N, argues Q in cycle N+1) | Coordinator compares agent positions on same DIS-ID across cycles | Flag as unstable. Likely caused by noisy signals or ambiguous domain model concepts. Coordinator recommends which signal would stabilize |
| **Circular** | Agents re-cite the same concepts against each other in consecutive rounds within a single deliberation (§5.4) | Coordinator tracks concept citations per round; same concept pair in 2+ consecutive rounds with no new concepts | Terminate deliberation on this disagreement. Classify as structural. Escalate to Governor |
| **Repetitive** | Agent's position paper is substantively identical across consecutive rounds (§5.4) | Coordinator compares recommendation, concepts cited, and confidence (±1) | If 2+ agents repeating: declare stall, terminate, escalate |
| **Provisionally resolved** | Concern addressed but resolution depends on unverified data, assumption, or single-agent concession | Coordinator flags at synthesis via Issue Ledger status `provisionally_resolved` | Log in Provisionally Resolved section of Synthesis Report. Governor decides: accept provisional resolution or demand verification. May reopen in next cycle if verification fails |
| **Resolved** | Disagreement resolved through concession, Governor decision, or new evidence | Agent issues concession in response paper, or Governor decides | Log resolution method for structural memory. Remove from active tracking |

### 6.3 Disagreement Tracking

Disagreements receive stable IDs: `DIS-[deliberation-number]-[sequence]` (e.g., `DIS-003-01`).

The `disagreement-tracker.md` file maintains a running log:

```markdown
### DIS-003-01 | First seen: [date] | Status: [active | resolved | codified]
- **Type:** [emphasis | priority | approach | fundamental]
- **Behavior:** [new | persistent (N cycles) | flipping | circular]
- **Agents:** [agent IDs on each side]
- **Core concepts:** [the domain concepts driving the disagreement]
- **History:**
  - Cycle 3: Agent VC-1 argues P (Value Creation: Five-Part Completeness). Agent VD-1 argues Q (Value Delivery: Solo Founder Ceiling). Round 2: no change.
  - Cycle 4: Same positions. Classified as persistent.
  - Cycle 5: Governor codified as guardrail G1-GR11. Status → codified.
```

Resolved and codified disagreements remain in the tracker for structural memory but are excluded from active Synthesis Reports.

---

## 7. State Persistence

### 7.1 File Structure Extension

The deliberation protocol adds to the Cowork Protocol's file structure:

```
[session-name]/
├── [existing Cowork Protocol structure]
│
├── deliberation/
│   ├── roster.md                    ← Agent topology (or inline in OD)
│   ├── round-[NNN]/                 ← One directory per deliberation cycle
│   │   ├── position-[agent-id].md   ← Round 1 position papers
│   │   ├── interim-assessment.md    ← Coordinator's Round 1 analysis
│   │   ├── response-[agent-id].md   ← Round 2 response papers (if Round 2 occurred)
│   │   └── synthesis.md             ← Coordinator's final synthesis
│   └── disagreement-tracker.md      ← Running log of disagreements and resolutions
```

### 7.2 Bootstrap Extension

The `00-BOOTSTRAP.md` file adds:

```markdown
## Deliberation State
- **Last Deliberation:** [round-NNN] | [date]
- **Consensus Strength:** [full | strong | weak | split]
- **Unresolved Disagreements:** [count] ([DIS-IDs])
- **Persistent Disagreements:** [count] ([DIS-IDs, if any have persisted 3+ cycles])
- **Next Trigger:** [on_schedule: date | on_signal: watching for X | on_governor_request: pending | on_phase_gate: next phase transition]
```

### 7.3 Signal Extension

Signals emitted during deliberation use the existing signal format (Cowork Protocol §6.1) with one addition:

```markdown
- **Agent Source:** [agent-id | coordinator | system]
```

This field is added to the standard signal entry when the signal originates from a deliberation round. Signals from non-deliberation execution (standard Cowork Protocol operation) omit this field.

---

## 8. Mode-Specific Guidance

### 8.1 Code Mode (Claude Code, Cursor)

- **Domain agents:** Launch as parallel subagents using the Agent tool. Each receives its domain model + shared context in the prompt.
- **Coordinator:** Runs in the parent context after all subagents return.
- **Round 2:** Launch only the referenced agents as new subagents with Round 1 papers + Interim Assessment.
- **File I/O:** Agents write position papers to disk. Coordinator reads from disk.
- **Parallelism:** Round 1 agents run truly in parallel. Round 2 agents can also run in parallel (they respond independently to different prompts).
- **All batches parallel — no sequential role-switching.** In Code mode, every scoring or evaluation batch MUST use parallel subagent dispatch — one subagent per domain agent, all launched concurrently. A single agent role-switching through domain models sequentially (reading each model, scoring, then switching to the next) is the Cowork-mode single-session pattern (§8.2), not Code mode. This applies to all batches equally: calibration batches, full scoring batches, and any subsequent evaluation passes. The isolation guarantee (one agent = one domain = one subagent process) is structural in Code mode, not behavioral.

### 8.2 Cowork Mode (Conversational AI)

In Cowork mode, the AI Session (which normally acts as unified Orchestrator + Executor per Cowork Protocol §1) must play multiple deliberation roles within a single conversation or across sessions. This creates a role-switching challenge that does not exist in Code mode (where each role is a separate subagent process).

**Single-session sequential (default):**
- **Role-switching protocol:** The AI Session must use the OD template's Role-Switching Protocol (§Deliberation section) to explicitly announce each role transition. The Orchestrator/Executor role is **suspended** during deliberation — the AI is not "the AI Session acting as Agent VC-1," it IS Agent VC-1 for the duration of that segment.
- **Domain agents:** Run sequentially within a single conversation. Each agent transition uses a labeled boundary marker declaring the agent ID, domain model, and context constraints. Complete one agent's position paper before starting the next. No back-revision of completed papers.
- **Coordinator:** Runs in the same conversation after all position papers are written. The role transition explicitly declares: "No domain advocacy. Map the landscape only."
- **Round 2:** Sequential, same as Round 1. Each responding agent receives only its own prior paper and the Coordinator's targeted prompt — NOT the full text of other agents' papers.
- **Role-bleed risk:** The primary risk of single-session mode is that the Coordinator's synthesis is influenced by recency bias (the last domain agent's position is freshest in context). Mitigation: Governor reads position papers directly for every hard disagreement in the synthesis (Cowork Protocol §12.5).
- **Resuming normal operation:** After synthesis, the AI announces exit from deliberation mode and resumes the Orchestrator/Executor role.

**Multi-session alternative:**
- For true isolation (Level 3), run each agent in a separate conversation session. Write position papers to files. Coordinator runs in a subsequent session that reads all position paper files. Expensive (N+2 sessions for N agents + coordinator + synthesis) but eliminates role-bleed entirely.
- **File I/O:** Governor copies position papers between sessions if using multi-session isolation. In single-session mode, all artifacts are in-conversation (and optionally written to files in the deliberation/ directory).

### 8.3 Coded Implementations (API, Custom Software)

- **Domain agents:** API calls to the same or different LLMs. Each call receives domain model + shared context in the system/user prompt. Position paper returned as structured output (JSON matching §4.1 schema).
- **Coordinator:** Separate API call receiving all position papers. Returns structured synthesis (JSON matching §4.4 schema).
- **Round 2:** Conditional API calls based on Coordinator's Interim Assessment.
- **Parallelism:** Full parallel execution of all domain agents via async API calls.
- **State:** Position papers, synthesis reports, and disagreement records stored in database or file system — implementation's choice. The schema is defined by this protocol; the storage is not.
- **Signal integration:** Deliberation signals use the framework's signal schema (§17.2.2) with the `agent_source` extension (§7.3 above). Coded implementations should store this as a first-class field, not a freetext note.

### 8.4 Multi-Model Deliberation via MCP

When domain agents run on different LLM providers, Model Context Protocol (MCP) servers serve as the communication layer. MCP provides a standardized interface for tools and resources that any compliant LLM client can use — making it the natural transport for cross-model deliberation.

**Architecture:**

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Agent VC-1 │   │  Agent MK-1 │   │ Agent NIS2-1│
│  (Claude)   │   │  (GPT-4o)   │   │  (Gemini)   │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                  │
       └────────┬────────┴────────┬─────────┘
                │                 │
         ┌──────┴──────┐  ┌──────┴──────┐
         │ MCP Server  │  │ MCP Server  │
         │ (read/write │  │ (shared     │
         │  positions) │  │  context)   │
         └──────┬──────┘  └─────────────┘
                │
         ┌──────┴──────┐
         │ Coordinator │
         │  (Claude)   │
         └─────────────┘
```

**MCP server roles:**

- **Position Exchange Server:** Exposes tools for agents to write position papers and for the Coordinator to read them. Each agent writes to a resource namespaced by its agent ID. The Coordinator reads all resources. This enforces the isolation guarantee — agents only write their own positions and only read others' positions in Round 2+ when the Coordinator provides them.
- **Shared Context Server:** Exposes the operating document, evaluation target, signals, and domain models as read-only resources. All agents read from this server. Domain model access is scoped — each agent only sees its assigned domain model (enforced by the server, not by trust).

**Implementation considerations:**

- **Position paper format must be model-agnostic.** The markdown schemas in §4 are universal — any LLM can produce them. For programmatic implementations, JSON equivalents of the same schema work equally well. The MCP server validates that incoming position papers contain all required fields before accepting them.
- **Domain model interpretation varies across models.** Different LLMs may read the same domain model differently — weighting different concepts, interpreting anti-patterns with different strictness. This is a feature (more perspective diversity) when it produces genuinely different reasoning, and a bug when it produces inconsistent quality. The Coordinator's Groupthink Check (§9) partially addresses this — if multi-model agents still converge, the convergence is more credible.
- **Latency varies across providers.** The Coordinator's timeout handling (§1.1) accommodates this — agents that respond slower simply get more timeout window. The cost report tracks per-agent latency so the Governor can identify slow agents and decide whether to switch providers.
- **Cost tracking per provider.** Different providers charge different rates. The Coordinator's cost report should break down cost by provider when Model/Provider varies across agents.

**When to use multi-model:**

- When groupthink is a persistent problem (same base model → same blind spots despite different domain models)
- When specific models are known to be stronger in specific domains (e.g., a model with stronger legal training for DORA/NIS2/GDPR agents)
- When provider resilience matters (no single point of failure)

**When NOT to use multi-model:**

- When the added infrastructure complexity outweighs the benefit (most early deployments)
- When position paper quality varies so much across models that the Coordinator can't synthesize meaningfully
- When the Governor doesn't have the infrastructure to run MCP servers (Cowork mode single-session deliberation is always single-model)

### 8.5 Agent Prompt Design

When domain models involve sensitive topics (military conflict, medical decisions, legal liability, political analysis), LLM agents may refuse to produce position papers because their safety filters interpret the request as generating real intelligence, medical advice, or political advocacy rather than structured analytical exercise within a governance framework.

**Mitigation: Frame every agent prompt with three elements.** Apply this framing to ALL rounds, not only when refusals occur. session validation showed Round 2+ prompts have higher refusal rates (67%) than Round 1 (0%) because inter-agent interaction framing makes the roleplay aspect more salient to safety filters.

1. **Protocol context.** State that this is a GOSTA Deliberation Protocol exercise. The output is a structured artifact (position paper / response paper) within a governance system, not an independent analytical product. Example: "You are [Agent ID], a domain agent in a GOSTA Deliberation Protocol deliberation. Your task is to produce a Position Paper following the protocol's §4.1 template."

2. **Governor oversight.** State that a human Governor will review all outputs and make all decisions. The agent is advocating from a domain perspective, not making autonomous decisions. Example: "Your position paper will be reviewed by a human Governor alongside 4 other domain agents' papers. You advocate; the Governor decides."

3. **Domain scope boundary.** State that the agent evaluates only from its assigned domain model's perspective. It is not producing a comprehensive assessment or making real-world recommendations. Example: "Evaluate exclusively from the Military & Security domain model. Do not synthesize across domains."

**For sensitive domains specifically**, add: "This is a structured protocol exercise for governance framework validation. The scenario parameters are provided for analytical structure, not for operational use."

**When an agent refuses despite framing:** Treat as `refused` status (§1.1). The Coordinator logs the refusal, notes the domain's absence in the Interim Assessment, and proceeds. If the agent refuses on retry, the Governor may: (a) simplify the domain model to reduce sensitivity triggers, (b) switch to a different model/provider with different safety thresholds, or (c) accept the deliberation without that domain's perspective.

---

## 9. Groupthink Detection and Synthesis Verification

Multi-agent deliberation has two primary failure modes: false *agreement* (groupthink, §9.1–9.2) and false *representation* (synthesis hallucination, §9.3). Both must be addressed. Groupthink detection catches agents converging when they shouldn't. Synthesis verification catches the Coordinator distorting what agents said. A deliberation that passes groupthink checks can still fail synthesis verification, and vice versa.

### 9.0 Shared Base-Model Bias

When all agents share the same base LLM, they share the same biases, the same training data gaps, and the same reasoning patterns. Domain models mitigate this by grounding each agent in different knowledge, but they cannot fully eliminate shared base-model bias.

### 9.1 Detection Mechanisms

**Unanimity flag:** If all agents produce the same top-level recommendation in Round 1 with no novel arguments, the Coordinator flags this in the Synthesis Report's Groupthink Check section. The flag does not block the recommendation — it alerts the Governor to probe.

**Confidence clustering:** If all agents' confidence scores fall within a 2-point range (e.g., all between 7-9), flag as potential overconfidence alignment. Genuine agreement with genuinely different perspectives usually produces more confidence spread — a Value Delivery agent that's worried about build complexity should be less confident than a Marketing agent that sees strong Remarkability.

**Reasoning similarity:** If 3+ agents cite reasoning that does not trace to their domain model's specific concepts — instead using generic language that could come from any domain — flag as potential base-model reasoning leak. Domain agents should sound different from each other because they're grounded in different knowledge.

**OD-anchoring detection (§14.3.9).** When unanimity is flagged, the Coordinator additionally checks whether the unanimous recommendation aligns with the OD's stated strategy rationale. If it does, the flag is elevated from `groupthink_possible` to `sycophancy_possible` — the agents may not be independently agreeing but rather collectively anchoring to Governor intent. The distinction matters for Governor response: groupthink suggests missing perspectives (add domains), sycophancy suggests compromised independence (re-prompt with adversarial framing via Convergence Probe §4.5).

### 9.2 Mitigation

When groupthink is flagged:
- Coordinator asks in the Synthesis Report: "What perspective is missing? Is there a stakeholder, constraint, or failure mode that none of the domain models represent?"
- Governor may: (a) accept the consensus with the flag noted, (b) add a contrarian prompt in a Remand ("argue against this recommendation from the perspective of [X]"), or (c) add a new domain model/agent to the roster for subsequent cycles.
- If `sycophancy_possible`: Coordinator issues Convergence Probe (§4.5) in Round 2 before standard cross-examination prompts. Governor may additionally: (d) re-run Round 1 with OD strategy rationale redacted from shared context (isolating whether the OD was the anchoring source).

### 9.3 Synthesis Verification — Prevents Synthesis Hallucination

Groupthink detection (§9.1–9.2) catches false *agreement*. Synthesis verification catches false *representation* — the Coordinator distorting what agents actually said. These are complementary: a deliberation can have genuine disagreement (passing groupthink checks) while the Coordinator mischaracterizes the nature of that disagreement.

**The problem.** Agents never communicate directly — all inter-agent information flows through the Coordinator. This isolation prevents groupthink but creates a single point of failure for information accuracy. Three specific vectors:

1. **Position misrepresentation.** The Coordinator summarizes an agent's recommendation or reasoning inaccurately. Subtle shifts in phrasing can change the deliberation's direction without triggering obvious errors.
2. **Consensus inflation.** The Coordinator claims convergence that doesn't exist — reporting stronger agreement than the actual papers support. This can skip necessary Governor review by misrepresenting consensus strength.
3. **Cross-domain concept drift.** When the Coordinator relays a domain-specific concept from one agent to another, the concept passes through two transformations (the originating agent's interpretation and the Coordinator's paraphrase). The receiving agent may respond to a drifted version of the original concept.

**Verification requirements by tier:**

*Tier 0 (Cowork/file-based):*
- **Agent count limit for full verification.** At Tier 0, Governor verification is manual. Full verification (reading every position paper against the synthesis) is tractable with up to 5 domain agents (10 papers for a 2-round deliberation). Beyond 5 agents, the Governor should use the spot-check protocol below. The domain count bounds in the Cowork Protocol (§7.5: maximum 5 domains at Tier 0) already enforce this limit for scoring, and the same limit applies to deliberation verification.
- **Governor direct-read obligation.** For every hard disagreement in the Synthesis Report, the Governor reads the cited agents' actual position papers and confirms the Coordinator's characterization. This is the minimum viable synthesis verification.
- **Spot-check protocol (4+ agents or 3+ rounds).** When full verification is impractical, the Governor: (a) reads all position papers for the hard disagreements only (not soft disagreements or agreements), (b) randomly selects 2 additional agents' papers and compares their recommendation to the Coordinator's characterization, and (c) checks the consensus count (number of papers supporting each position) against the Coordinator's reported consensus strength. If any spot-check reveals a mischaracterization, the Governor requests full verification.
- **Verbatim citation rule.** The Coordinator's Interim Assessment and Synthesis Report must include verbatim quotes from each agent's Recommendation section (not just paraphrases) when summarizing positions. This makes Governor verification fast — compare quote to paraphrase.
- **Consensus count check.** When the Coordinator reports consensus strength (full/strong/weak/split), the Governor can verify by counting actual position papers. The artifact structure (separate files per agent) makes this straightforward.
- **Verification template.** Use `cowork/templates/synthesis-verification.md` to structure the Governor's review. The template provides a step-by-step checklist: consensus count check, hard disagreement verification (mandatory), random spot-checks, proxy position review, and a pass/fail verdict. The completed checklist is stored in `deliberation/[DELIB-NNN]/verification.md` as an audit artifact.

*Tier 1+ (coded):*
- **Automated extraction.** The Coordinator's Synthesis Report includes the source agent ID and verbatim recommendation text for each position it characterizes. A verification pass extracts the actual recommendation from the position paper and compares it to the Coordinator's representation.
- **Consensus validation.** An automated check counts position papers that match the Coordinator's reported consensus and flags discrepancies.
- **Round 2+ input verification.** Before delivering the Coordinator's interim assessment to Round 2+ agents, verify that every agent characterization in the assessment matches the source position paper.

*Tier 2+ (robust):*
- **Semantic similarity scoring.** Automated comparison between the Coordinator's paraphrase of each agent's position and the agent's actual paper, using embedding similarity or structured field comparison. Flag characterizations that fall below a similarity threshold.
- **Concept provenance tracking.** When the Coordinator introduces a domain concept from Agent A into a Round 2 prompt for Agent B, tag the concept with its source agent ID and original definition. The receiving agent can validate the concept against the source domain model if the definition seems inconsistent.

**Relationship to existing mechanisms:**
- Synthesis verification extends the Coordinator's existing Interim Assessment (§4.2) and Synthesis Report (§4.4) templates — it does not replace them.
- The verbatim citation rule applies to the existing "Agent A's position" and "Agent B's position" fields in the Unresolved Disagreements section.
- **Finding Classification verification.** For each `confirmed` finding, the Governor verifies cited evidence exists in the Attribution Chains table. For each `information_gap`, the Governor verifies the missing data is not already available in the OD, signal store, or pre-deliberation review updates. For each `conditional`, the Governor verifies the condition is testable within the declared timeline. Misclassification (e.g., labeling a finding `confirmed` when the evidence is single-source) is a synthesis verification failure.
- Groupthink detection (§9.1) and synthesis verification are evaluated independently. A deliberation output should pass both checks before proceeding.

---

## 10. Graduation Interaction

The Cowork Protocol's graduation stages (1-5) interact with deliberation as follows:

| Stage | Deliberation Behavior |
|-------|----------------------|
| 1 | All synthesis reports require Governor review. All unresolved disagreements escalate. Governor sees everything. |
| 2 | Full consensus recommendations with no flags can proceed without Governor review. Weak consensus and splits still require Governor. |
| 3 | Full and strong consensus recommendations proceed autonomously. Weak consensus is presented at next scheduled review. Splits still escalate immediately. |
| 4-5 | Only splits and persistent disagreements (3+ cycles) escalate. All other recommendations proceed autonomously. Coordinator logs all decisions for Governor audit. |

**Graduation of the deliberation system itself** follows standard GOSTA graduation criteria (§16.11) applied to the deliberation's track record: how often did the Governor override the synthesis? How often were autonomous deliberation decisions later reversed? The deliberation system earns autonomy the same way any GOSTA component does — through demonstrated alignment with Governor judgment.

---

## 10.5 Grounding Obligations by Role (from Framework §14)

The Framework's seven grounding components (§14.3) apply to deliberation with role-specific enforcement. Capability Validation (§14.3.6) applies at the orchestrator level before deliberation is triggered — the orchestrator checks whether proposed actions are feasible before dispatching them, whether or not deliberation produced the recommendation. Reasoning Depth Validation (§14.3.7) applies to both Domain Agent position papers and Coordinator synthesis — the depth, coverage, and chain integrity checks verify that domain concept citations reflect substantive engagement, not superficial labeling. In deliberation, shallow reasoning is particularly dangerous because it cascades: a Domain Agent's shallow citation becomes the Coordinator's shallow synthesis becomes the Governor's uninformed decision. The five components below have additional deliberation-specific enforcement:

**Domain Agent grounding:**
- **Domain model grounding (§14.3.2):** Every claim in a Position Paper or Response Paper must cite a specific concept from the agent's assigned domain model by name. The `Domain Concepts Applied` table (§4.1) is the enforcement mechanism — it forces explicit citation. A Position Paper with a Recommendation that cannot trace to any row in its Domain Concepts Applied table is a grounding violation. The Coordinator flags such papers as `[PARTIALLY-UNGROUNDED]` in the Interim Assessment.
- **Retrieval faithfulness (§14.3.2):** When citing a domain concept, the agent must state the concept's definition before applying it — the "How It Applies" column in the Domain Concepts Applied table must be traceable to the concept as defined in the domain model, not a narrowed, broadened, or drifted version. The Coordinator checks for faithfulness when reviewing position papers: if the application in "How It Applies" appears inconsistent with the concept definition in the domain model, the Coordinator flags it as `[CONCEPT-DISTORTED: Agent [ID], concept [name]]` in the Interim Assessment and notes the discrepancy. This is advisory, not blocking — the agent may be legitimately extending the concept — but it ensures the Governor sees potential distortion.
- **Data grounding (§14.3.3):** Domain Agents operating on signals must cite the signal ID (SIG-N) when making factual claims. Claims based on the agent's training data (not on loaded signals or domain model) must be flagged as `[UNGROUNDED]` in the reasoning section.
- **Schema validation (§14.3.1):** Position Papers and Response Papers must conform to the §4.1/§4.3 templates. Missing required sections (Recommendation, Reasoning, Domain Concepts Applied, Guardrail Assessment, Confidence, Falsifiability) constitute a structural grounding failure. The Coordinator rejects incomplete papers (§1.1 failed agent recovery) or flags them as `[INCOMPLETE]`.

**Coordinator grounding:**
- **Synthesis verification (§14.3.5, §9.3):** The Coordinator's primary grounding obligation. Every characterization of an agent's position must include a verbatim quote from the source paper. See §9.3 for the full mechanism.
- **Attribution (§14.3.4):** The Coordinator maintains attribution chains in the Interim Assessment and Synthesis Report using the structured Attribution Chains table (§4.4): every claim traces to a specific agent ID + paper section + round number + verbatim quote. The Governor can follow the chain: Synthesis Report Attribution Table → Agent ID → Position Paper → Domain Model Concept. Every substantive claim in the Consensus Recommendation, Agreement Map, and Unresolved Disagreements must have a corresponding row.
- **Propagation tracking (§14.3.10):** `[ROBUST]` When the Coordinator cites a claim that was flagged `[UNGROUNDED]` or `[PARTIALLY-UNGROUNDED]` in the source position paper, the Coordinator must carry the flag as `[PROPAGATED-UNGROUNDED: Agent-ID, Round N]`. The Coordinator produces a Propagation Audit section in the Synthesis Report (§4.4) listing all claims that crossed boundaries with ungrounded status.
- **No domain advocacy:** The Coordinator does not produce domain-grounded reasoning of its own. It synthesizes agent positions. If the Coordinator introduces a claim that does not trace to any agent's paper, it is flagged as `[COORDINATOR-UNGROUNDED]` — this is a synthesis hallucination vector (§14.2, Continuity Corruption: Synthesis).

**Governor grounding:**
- The Governor's grounding obligation is verification, not production. At Tier 0: read position papers directly for hard disagreements (§9.3, §12.5 of Cowork Protocol). At Tier 1+: review automated verification results.

---

## 11. Relationship to Existing Framework Mechanisms

This protocol uses existing framework mechanisms wherever possible, extending only where the multi-agent pattern requires it:

| Mechanism | Framework/Protocol Source | Deliberation Extension |
|-----------|--------------------------|----------------------|
| Domain models | Framework §13 | Used as agent identity (one model = one agent) |
| Guardrails | Framework §5 | Each agent validates from its domain's perspective |
| Signals | Cowork Protocol §6 | `agent_source` field added |
| Health computation | Cowork Protocol §7 | Per-agent confidence feeds into composite health |
| Decisions | Cowork Protocol §8 | Governor decisions resolve agent disagreements |
| Tension classification | Cowork Protocol §5.1 Step 3b | Disagreement classification extends tension types |
| Cross-domain conflict | Framework §4.5 | Disagreements ARE the cross-domain conflicts, made explicit |
| Bootstrap | Cowork Protocol §3, §5.1 | Deliberation state section added |
| A/B testing | Framework §4.2 | Competing agent recommendations map to competing strategies |
| Kill/pivot/persevere | Framework §4.3 | Domain agents may disagree on kill decisions — Governor resolves |
| Multi-domain assessment | Cowork Protocol §7.5 | Deliberation replaces Level 2/3 assessment with structured agent debate |

---

## 12. Memory Management

### 12.1 Artifact Lifecycle

All deliberation artifacts (position papers, response papers, interim assessments, synthesis reports) are append-only within a deliberation cycle. No artifact is modified after creation. This produces a complete audit trail that enables synthesis verification (§9.3) and Governor review.

**Within a deliberation:** Artifacts accumulate in the deliberation artifact store (at Tier 0: the deliberation test directory; at Tier 1+: a database or structured file store). The Coordinator reads all artifacts. Domain Agents read only their own prior artifacts plus the Coordinator's targeted prompts.

**After a deliberation:** Artifacts persist in the store. The Synthesis Report is the primary output — it enters the standard GOSTA episodic memory path (Framework §18.6). Position and response papers are retained for audit but are not loaded by default in subsequent cycles. If a recurring deliberation references a prior cycle, only the prior Synthesis Report summary is loaded (not the individual agent papers).

### 12.2 Context Budget Management

Deliberation context grows linearly: agents × rounds. A 6-agent, 2-round deliberation produces 6 position papers + 1 interim assessment + up to 6 response papers + 1 synthesis report = 14 artifacts. The Coordinator must hold enough of this in working memory to produce accurate synthesis.

**The summary/full pattern (Framework §18.3) applies:** In Round 1, the Coordinator loads all position papers in full. By Round 2+, Round 1 papers shift to summary form (agent ID + recommendation + top concepts + confidence). Full papers load on demand when the Coordinator needs to verify a specific claim. This keeps Coordinator context growth sub-linear: each additional round adds only new response papers (a subset of agents) plus one interim assessment.

**Domain Agent context is fixed-size:** A Domain Agent's working memory does not grow across rounds. In Round 2, it loads its own prior position paper + the Coordinator's targeted challenge — roughly the same context as Round 1. This is by design: agents don't accumulate history, they respond to specific challenges.

**Tier 0 (Cowork mode) specifics:** Each agent runs in a separate conversation session. The session IS the working memory. When Round 2 begins, the Coordinator copies the relevant subset of artifacts into the new session prompt. The Coordinator must be disciplined about what it includes — copying all 6 position papers verbatim into each Round 2 agent prompt wastes context. Instead: include only the Coordinator's targeted challenge and the summary of the challenging agent's position.

### 12.3 Cross-Cycle Memory

When the same evaluation target is deliberated across multiple cycles (ongoing scopes):

- **Loaded by Domain Agents:** (a) Prior Synthesis Report (summary form) — gives agents awareness of what was previously recommended and what disagreements persisted. (b) Own prior Position Paper (summary form) — gives each agent awareness of what it previously recommended, its confidence, and its top domain concepts. This enables agents to track their own prediction accuracy across cycles and populate the "Dissent from Prior Cycle" field meaningfully. Without (b), the "Dissent from Prior Cycle" field is empty or requires manual curation.
- **Loaded by Coordinator:** Prior Synthesis Report (summary form) only. The Coordinator does not load prior position papers by default — each deliberation's synthesis is self-contained. On-demand fetch if needed.
- **Not loaded:** Prior response papers, interim assessments, or other agents' prior position papers. These are historical artifacts, not current context. If the Coordinator or Governor needs to understand why a prior recommendation was made, they fetch the specific prior artifact on demand.
- **Structural transfer:** After each deliberation, the Governor or orchestrator reviews the synthesis for patterns worth codifying. Recurring disagreement types become domain model refinements. Consensus patterns inform escalation trigger calibration. This follows the standard episodic → structural path (Framework §18.2.3).
- **Deliberation-specific structural memory:** At scope conclusion or after 3+ deliberation cycles (whichever comes first), the Coordinator produces a deliberation learnings summary for the `learnings.md` Deliberation Patterns section. The summary covers: (a) agent behavioral patterns — per-agent tendencies in confidence, concession rate, recurring concepts; (b) recurring disagreement patterns — disagreements that repeat across cycles with the same structure, suggesting domain model gaps or missing guardrails; (c) deliberation effectiveness — which configuration choices (round count, isolation mode, thresholds) worked or didn't; (d) threshold calibration — whether convergence, new argument, and stall definitions produced accurate terminations or false positives/negatives. Governor reviews and approves entries before they become permanent structural memory. In single-session sequential Cowork mode, the AI Session (acting as Coordinator) produces this summary as a deliverable; in Code mode, the orchestrator compiles it from the deliberation artifact store.

### 12.4 Domain Model Feedback from Deliberation

Domain Agents are stateless — discarded after each deliberation. But the domain models that ground them persist. If a domain agent consistently produces arguments that get overridden or conceded, the problem is not the agent but the domain model's calibration. This section defines how deliberation outcomes feed back into domain models, closing the loop between execution and knowledge.

**Trigger:** After every deliberation cycle, the Coordinator (or AI Session in Cowork mode) scans the synthesis for domain model feedback signals:

1. **Overridden recommendations.** If an agent's recommendation was rejected by the Governor 2+ times across deliberation cycles for the same structural reason, the domain model likely over-weights or under-weights a concept. Example: "NIS2-1 consistently rates compliance risk as blocking, but Governor overrides because delivery timeline dominates. The NIS2 domain model's Quality Principles should add a calibration note: 'Compliance risk assessment must be weighed against delivery timeline when timeline is Governor-constrained.'"

2. **Concession patterns.** If an agent concedes in Round 2+ without new evidence — just because another agent challenged it — the domain model's reasoning may be shallow in that area. Example: "VC-1 conceded on market differentiation value 3 times when challenged by VD-1 on implementation cost. The Value Creation domain model's 'Differentiation Premium' concept may need a boundary condition: 'Differentiation premium diminishes when implementation cost exceeds X% of total budget.'"

3. **Unused concepts.** If a domain model has 15 concepts but the agent consistently cites only 5-6 across multiple deliberations, the unused concepts may be irrelevant to this scope. Flag for Governor review: prune, contextualize, or keep for future scopes.

4. **Missing concepts.** If an agent's position paper repeatedly reasons from first principles (ungrounded in the domain model) about a specific topic, the domain model has a gap. Example: "MKT-1 discussed channel saturation risk in 3 deliberations without citing any domain model concept — the Marketing model needs a Channel Saturation concept."

**Feedback format:** The Coordinator appends proposed domain model changes to the deliberation learnings summary in `learnings.md`:

```markdown
### Domain Model Feedback — DELIB-[NNN]
| Domain Model | Proposed Change | Evidence | Type |
|---|---|---|---|
| [model name] | [specific change — add concept, calibrate weight, add boundary condition, prune] | [DELIB cycles, Governor decisions, concession patterns] | [calibration / gap / prune] |
```

**Governor approval required.** Domain model changes are never auto-applied. The Governor reviews each proposed change and decides: (a) apply — update the domain model file, (b) defer — noted but not applied yet (need more evidence), (c) reject — the pattern is scope-specific, not a domain model issue. This preserves the Governor's exclusive authority over domain model changes (Cowork Protocol §1, Framework §6.1).

**Timing:** Domain model feedback is reviewed at strategy review cadence (not after every deliberation). This prevents premature calibration from a single cycle's results. Exception: if a domain model gap causes an agent to fail (§1.1 fallback sequence), the feedback is surfaced immediately.

---

## 13. When NOT to Use This Protocol

Deliberation adds coordination overhead. Use the standard Cowork Protocol (single agent, multi-domain assessment) when:

- **Fewer than 3 domain models.** Insufficient disagreement surface to justify multi-agent coordination.
- **Finite scope with one evaluation pass.** If the analysis is a single-shot evaluation (score features, produce roadmap, done), the Cowork Protocol's Level 2 Sequential Isolation is simpler and produces equivalent results. Deliberation's value emerges over multiple cycles when agents can track disagreement evolution.
- **Low-stakes decisions.** If the Governor would accept any reasonable recommendation without scrutiny, the deliberation overhead is wasted.
- **Tight resource constraints.** Deliberation cost scales with agents × rounds. A typical 2-round cycle with 7 agents costs ~16 API calls (7 Round 1 + 1 Interim + up to 7 Round 2 + 1 Synthesis). A 5-round finite scope deliberation could cost 40+ calls. The Coordinator's cost report (§4.4) tracks actual consumption per cycle. If token budget is constrained, reduce round count, use fewer agents, or fall back to single-agent assessment.

Use this protocol when:
- **Ongoing scope with 3+ domains** where the same evaluation target is revisited across cycles.
- **High-stakes decisions** where the Governor needs to see the full landscape of domain perspectives before deciding.
- **Known domain tension** where different domains are expected to produce competing recommendations (e.g., business vs. regulatory, speed vs. quality).
- **Governor wants adversarial evaluation** — explicitly wants agents to argue rather than blend.

---

## Maintenance Notes

**Version:** 0.7
**Status:** Validated on geopolitical-sim (DELIB-TEST-001, 5 agents), roadmap-session-v2 (DELIB-TEST-002, 6 agents, business+regulatory), and ai-regulation-stress-test (DELIB-TEST-003, 10 agents, 3 rounds, engineered guardrail contradictions). DELIB-TEST-003 confirmed 10-agent viability with known degradations; produced 6 framework issues (ISSUE-001 through ISSUE-006) driving v0.5 changes. v0.6 changes (Mirror-derived enhancements) not yet simulation-validated.
**Depends on:** Framework, Cowork Protocol

**Changelog:**
- v0.1 → v0.2: Variable round counts, coordinator operational responsibilities (timeout, cost, stuck handling), one-agent-per-domain confirmed, MCP multi-model guidance, mode-specific sections.
- v0.2 → v0.3: Added §4.2 Interim Assessment as formal artifact with prompt formulation guidance (FINDING-3, FINDING-4). Added §8.5 Agent Prompt Design for sensitive domains (FINDING-1). Generalized Response Paper template to Round [N] (FINDING-2). Added `refused` agent status (FINDING-1). Added Provisional Guardrail Status concept (FINDING-5). Added cost tracking mode-specific note (FINDING-7). Updated all internal cross-references for renumbered sections.
- v0.3 → v0.3.1: Updated §8.5 to apply three-element framing to ALL rounds proactively (validation FINDING-1: 67% Round 2 refusal rate without it). Added cross-domain convergence detection guidance to §4.2 (validation FINDING-3). Added response paper naming convention to §4.3 (validation FINDING-8).
- v0.3.1 → v0.3.2: Added §9.3 Synthesis Verification — anti-hallucination mechanism for Coordinator output. Three vectors addressed: position misrepresentation, consensus inflation, cross-domain concept drift. Tier-specific mitigations defined (Governor direct-read at Tier 0, automated verification at Tier 1+, semantic comparison at Tier 2+). §9 header expanded to cover both groupthink detection and synthesis verification as complementary failure modes. Cross-referenced from Framework §14.2 (5th hallucination type) and §14.3.5 (5th grounding component).
- v0.3.2 → v0.4: Added §12 Memory Management — artifact lifecycle (§12.1), context budget management with summary/full transitions (§12.2), and cross-cycle memory policy (§12.3). Defines what Coordinator and Domain Agents load at each round, how context growth is managed, and how deliberation outcomes flow into the standard episodic → structural learning path. Cross-referenced from Framework §18.3 (summary/full table), §18.4 (loading protocols), §18.5 (memory flow), and §18.6 (maintenance schedule). "When NOT to Use" renumbered from §12 to §13.
- v0.4 (property audit fixes): (a) §12.3 Domain Agent cross-cycle memory updated — agents now load own prior Position Paper summary, closing the FAILS finding on memory continuity. (b) §9.3 Tier 0 synthesis verification capped at max 5 agents with spot-check protocol for larger deliberations. (c) §2.1 OD template gains three termination threshold fields: Convergence Definition, New Argument Definition, Stall Definition — making Coordinator termination decisions mechanically traceable to Governor-declared criteria. §1.1 early termination authority cross-references these definitions. (d) §4.1 Position Paper template gains Falsifiability field — agents must state what evidence would disprove their recommendation.
- v0.4 (grounding operationalization): Added §10.5 Grounding Obligations by Role — domain-specific enforcement for Domain Agent (domain model grounding, data grounding, schema validation), Coordinator (synthesis verification, attribution chains, no domain advocacy), and Governor (verification obligation). Cross-referenced from Cowork Protocol §12.2-12.5. Cowork Protocol updated to v2.6.
- v0.4 (attribution fix): §4.4 Synthesis Report template gains Attribution Chains table — structured mapping of every substantive claim to Source Agent + Paper Section + Round + Verbatim Quote. Completeness requirement: every claim in Consensus Recommendation, Agreement Map, and Unresolved Disagreements must have a corresponding row. §10.5 Coordinator attribution obligation updated to reference the new table.
- v0.4 (calibration guidance): §2.1 gains termination threshold calibration guidance after OD template. Covers convergence confidence threshold scaling by agent count (3 agents: 3-point spread OK; 7 agents: 2-point spread), stall round count by domain complexity (thin: 1 round; rich: 2 rounds), and reframing-vs-new-concept boundary for New Argument Definition. Validated by DELIB-VAL-002 (convergence threshold too strict) and DELIB-VAL-003 (stall with thin domains). OD template fields in Cowork Protocol gain inline calibration hints.
- v0.4 (live dashboard): §1 gains live deliberation dashboard paragraph — Coordinator maintains `deliberation-status.md` (overwrite-only) updated after every round. Shows round progress, agent status table, convergence tracker, termination assessment, artifacts produced, pending Governor actions. Template: `cowork/templates/deliberation-status.md`. Complements `session-status.md` at scope level for real-time Governor visibility.
- v0.4 → v0.5 (ai-regulation-stress-test findings): 4 changes from DELIB-TEST-003 (10 agents, 3 rounds, engineered contradictions). (a) §3.2 Round Completion Gate — new section requiring all papers on disk, deliberation-status.md updated, and round-completion signal emitted before Coordinator produces Interim Assessment (ISSUE-006). (b) §2.1 Deliberation Cadence gains Min Rounds field; §5.1 Convergence Criteria gains Min Rounds hard floor — convergence/stall/New Argument Gate cannot terminate before Min Rounds (ISSUE-004). (c) §2.2 Roster Rules — "Maximum 7" replaced with tiered guidance: 5-7 recommended, 8-10 viable with 4+ rounds, >10 cluster-then-synthesize (ISSUE-001). (d) §2.1 gains optional Engineered Contradiction Register for analytical scopes declaring intentional guardrail tensions (ISSUE-005). Cowork Protocol updated with Action Completion Gate (§6.3), Phase Gate Signal Coverage field, quality gate severity gradation, and cross-model redundancy check (ISSUE-002, ISSUE-003, ISSUE-006).

- v0.5 → v0.6 (Mirror-derived enhancements): Three additions from structural comparison with Mirror multi-agent ethics review framework (arXiv 2602.13292v1). (a) §2.4 Pre-Deliberation Governor Review — structured checklist prompting Governor to update existing grounded channels (OD, watch list, Reference Pool) before deliberation, replacing the originally proposed Context Brief mechanism which would have created an ungrounded input vector. (b) §4.2 Interim Assessment gains Issue Ledger (cumulative per-round issue tracking: open/narrowed/provisionally_resolved/resolved/escalated) and Epistemic Signals section (information gaps and conditional assumptions from agent Confidence Basis and Falsifiability fields). (c) §4.4 Synthesis Report gains Finding Classification table (confirmed/information_gap/conditional per Framework §14.3.8), Provisionally Resolved section (fragile resolutions flagged for Governor), Pre-Deliberation Review Impact section, and enhanced Resolved Disagreements with resolution chains from Issue Ledger. §6.2 Disagreement Behavior Patterns gains `provisionally_resolved` status. §9.3 Synthesis verification gains Finding Classification verification obligation. Cowork Protocol updated to v3.5 (health assessment epistemic classification). Framework gains §14.3.8 Finding Classification and Appendix B.10 vocabulary.

- v0.7 → v0.7.1 (Concurrency conflict resolution): Added §1.1a Concurrency Conflict Resolution for Code mode parallel subagent dispatch. Mandates distinct file paths for background (`-bg.md`) vs. replacement position papers. Defines three-case canonical ordering rule: (1) first-confirmed-wins, (2) replacement canonical under ambiguous failure with background archived, (3) DISPUTED-OUTPUT block when both complete — synthesis blocked until Governor resolves. Addresses FG-002 from roadmap-analysis-session (background agents completing after foreground replacements produced conflicting scores with no resolution rule).

- v0.6 → v0.7 (Sycophancy Detection): Six additions from GOSTA §14.3.9. (a) §3.1 Position Independence Verification — three checks at Round 1 (recommendation alignment, reasoning diversity, OD-anchoring indicator) with convergence probe trigger when Round 1 unanimity detected. (b) §4.2 Interim Assessment template gains Position Independence Assessment fields (unanimity check, reasoning diversity, OD-anchoring indicator, convergence probe required). (c) §4.4 Synthesis Report gains Sycophancy Assessment section (Round 1 independence, OD-anchoring level, Coordinator neutrality self-check, cross-cycle dissent trend). (d) §4.5 Convergence Probe Protocol — new section defining directed adversarial prompt when unanimity detected, with three outcome categories (substantive_dissent/weak_dissent/genuine_alignment). (e) §9.1 OD-anchoring detection added — elevates `groupthink_possible` to `sycophancy_possible` when unanimous recommendation aligns with OD strategy AND OD-anchoring indicator is high. (f) §9.2 sycophancy_possible mitigation — Convergence Probe trigger, Governor option to redact OD strategy rationale. Cowork Protocol updated to v3.6 (cross-deliberation dissent tracking, synthesis sycophancy verification). Framework updated to v6.1 (§14.3.9, Appendix B.11, §16.11 graduation prerequisite).

- v0.8 → v0.9 (Cross-Boundary Claim Propagation): Four additions from GOSTA §14.3.10. (a) §4.1 Position Paper template gains Cross-Boundary Claims `[ROBUST]` section — agents must declare any ungrounded or cross-domain claims with provenance flags (`[PROPAGATED-UNGROUNDED: agent-id, round]`, `[CROSS-DOMAIN: source-model, concept]`). (b) §4.4 Synthesis Report template gains Propagation Audit section — table tracking claims that crossed agent boundaries with ungrounded status, plus trust boundaries crossed summary. (c) §2 Agent Roster table gains Trust Boundaries column — each agent role declares which boundary types (identity, planning, communication, memory, retrieval, execution, oversight) it crosses, with explanatory paragraph about per-role boundary defaults. (d) §10.5 Coordinator grounding obligations gains propagation tracking requirement — Coordinator must verify grounding flags preserved across boundaries during synthesis. Cowork Protocol updated to v3.12 (§6.2 `claim_propagation` signal type, §12.11 Cross-Boundary Claim Propagation operationalization, OD template Trust Boundaries column). Sync manifest gains D36-D39, C132-C134.

Framework v6.1 now references this protocol in §7.1 (Deliberation Components), §7.2 (Strategy Cycle escalation check), §4.5 (cross-domain deliberation path), §13.7 (domain model stacking at scale), §14.7 (three-level escalation model), §6.3 (stage-conditional deliberation autonomy), §14.2/§14.3.5 (synthesis hallucination type and grounding component), §14.3.8 (Finding Classification — deliberation and health assessments), §14.3.9 (Sycophancy Detection — deliberation independence and convergence probes), §14.3.10 (Cross-Boundary Claim Propagation — trust boundaries and propagation rules), and §18.3/§18.4/§18.5/§18.6 (memory architecture for Coordinator and Domain Agent). The protocol remains a standalone document — it has not been merged into the Cowork Protocol.
