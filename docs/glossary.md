# GOSTA Glossary

Quick lookup for terminology used across the spec, protocols, examples, and tooling. Entries are alphabetical. Each entry: one-line definition + where the term is primarily defined + when it applies + related terms.

For deeper treatment, follow the "Defined in" links. For when-to-apply context, follow the "See" links.

---

**AFC (Analytical Frame Contract)** — A four-field contract (Stance, Output Verb, Failure Mode, Prohibited Frame) declared at session bootstrap that locks the analytical posture and prevents the deliverable from answering a different question than the one asked. Defined in `cowork/startup.md` Group 2A; transcribed into the OD; audited at deliverable production via §12.12 Frame Integrity Validation. Applies to analytical/assessment scopes only (skipped for operational scopes). Related: Frame Integrity Validation, Prohibited Frame.

**Anti-Pattern** — Component of a domain model. Named failure modes the AI should detect and flag when reasoning in this domain. Defined in `cowork/templates/domain-model.md`. Each anti-pattern is actionable (the AI knows what to flag) and inverse-of-quality-principle (i.e., not redundant with QP). Related: Quality Principle, Domain Model.

**Bootstrap** — Phase 0 of a session; the period from "start a session" through Governor approval of the OD. Driven by `cowork/startup.md`. Outputs: scaffolded directory, populated OD, domain models, V-gate validation manifest, scope-definition. Related: Phase Gate, Operating Document.

**Cite-then-apply** — Reasoning discipline (G-10) requiring every claim to (1) cite the specific concept by name, (2) state its definition from the source, (3) apply the concept to the specific case. Prevents shallow reasoning that uses domain vocabulary without engaging the concepts. Defined in cowork-protocol §6.2. Related: Quality Principle, Position Paper.

**Cluster-then-synthesize** — Deliberation topology for sessions with 7+ domain agents. Domains group into clusters (3-5 clusters typical); each cluster has a sub-coordinator who synthesizes within-cluster; a cross-cluster Coordinator (COORD-1) synthesizes across clusters. Alternative to flat deliberation. Defined in `cowork/deliberation-protocol.md` §3.3, §3.4. Related: Sub-coordinator, Coordinator.

**Convergence Probe** — Adversarial re-examination triggered when Round 1 of deliberation produces unanimous recommendations. Forces agents to identify what evidence would falsify the consensus. Catches sycophantic convergence. Defined in `cowork/deliberation-protocol.md` §3.3. Related: Sycophancy, Position Paper.

**Coordinator** — Deliberation role with no domain model. Manages agent lifecycle, identifies agreements and disagreements across position papers, produces interim assessments and synthesis report. Does not advocate. In cluster-then-synthesize topologies, a cross-cluster Coordinator (COORD-1) sits above sub-coordinators. Defined in `cowork/deliberation-protocol.md` §2.2. Related: Domain Agent, Sub-coordinator.

**Coverage Limitations Disclosure** — Section in deliverables and synthesis reports declaring that coverage came in below the session's threshold (e.g., 60-79% with 80% target), naming which domains and structural causes. Required when coverage was sub-threshold but the session advanced. Surfaces evidence-base limitations to deliverable consumers. §12.15 of cowork-protocol; introduced by Plan #7. Related: Evidence Tier, Phase Gate.

**Cross-domain tension** — Disagreement between domain agents on a candidate's verdict, surfaced during deliberation. The Coordinator's job is to make tensions explicit (with severity classification) rather than smooth them over. Defined in `cowork/deliberation-protocol.md` §5.2. Related: Issue Ledger, VERDICT-SPLIT-CARRIED.

**Deliberation** — Multi-agent coordination protocol where domain agents independently produce position papers, then iterate to converge or surface unresolvable structural disagreement. Activated when Independence Level = 3 or scope declares deliberation = yes. Defined in `cowork/deliberation-protocol.md`. Related: Position Paper, Coordinator, Sub-coordinator.

**Domain Agent** — Deliberation role grounded in exactly one domain model. Reasons from that domain's perspective. Produces position papers. Does NOT see other agents' positions during Round 1 to ensure independence. Defined in `cowork/deliberation-protocol.md` §2.1. Related: Domain Model, Position Paper, Scoped Specialist.

**Domain Model** — Structured knowledge file with 6 components (Core Concepts, Concept Relationships, Quality Principles, Anti-Patterns, Hypothesis Library, Guardrail Vocabulary) that grounds the AI's reasoning in codified domain knowledge rather than training data. Authored per `cowork/domain-model-authoring-protocol.md`; templated at `cowork/templates/domain-model.md`. Related: Anti-Pattern, Quality Principle, Hypothesis Library.

**Evidence Channel Disclosure** — Annotation in deliverables stating which evidence channels (analyst-consumed, empirically-validated, AI-domain-agent reasoning) supported claims about Party-X reception (e.g., prospect-attractiveness, regulator-acceptance, candidate-fit). Lets the consumer calibrate trust in the verdict. Introduced by Plan #11'; required in any deliverable carrying Party-X reception claims. Related: Frame Integrity Validation, Verdict Strength Annotation.

**Evidence Tier (T1 / T2 / T3)** — Classification of evidence quality. Tier 1 = primary sources / regulatory texts / first-party data. Tier 2 = established analyst reports / peer-reviewed research. Tier 3 = secondary commentary / vendor blogs / opinion. Defined in `cowork/evidence-collection-protocol.md` §2 + framework spec §14.8. Used in evidence-floor calculations and Verdict Strength Annotation tier-floor field. Related: Reference Pool, Verdict Strength Annotation.

**Frame Integrity Validation** — Audit at deliverable production verifying each AFC field (Stance, Output Verb, Failure Mode, Prohibited Frame) against the actual deliverable content. Surfaces frame-drift before publish. §12.12 of cowork-protocol. Plan #19 extended scope to synthesis-report.md and phase-gate-*.md files. Failure mode is MATERIAL same severity as missing AFC. Related: AFC, Prohibited Frame.

**Governor** — The human with decision authority. Approves OD, dispositions phase gates, makes kill/pivot/persevere decisions, resolves cross-domain tensions. Nine categories of Governor authority are formally non-delegable at any autonomy stage. Defined in framework spec §6.1. Related: Independence Level, Graduation Stage, Phase Gate.

**Graduation Stage** — Within-session autonomy progression (1-4) earned by demonstrating consistent quality. Stage 1 = AI drafts, Governor approves all changes. Stage 4 = AI creates/kills/pivots tactics independently within OD guardrails. Earned, not assumed. Defined in framework spec §6.7. Related: Independence Level, Governor.

**Guardrail** — Typed, inheritable constraint. Each guardrail declares severity (hard violations halt execution; soft violations trigger review) and evaluation type (mechanical = computable check; interpretive = requires judgment). Inherits downward through the hierarchy (goal → objective → strategy → tactic → action) and never relaxes during inheritance. Defined in framework spec §5. Related: Operating Document, Kill Discipline.

**Hook (M1 / M3 / M4 / M5 / log-dispatch / audit-closeout)** — Claude Code shell scripts firing on tool events for mechanizable-discipline enforcement. M1 = signal-first check on PreToolUse Task; M3 = cap-overage check on PostToolUse Write|Edit; M4 = AFC-section-presence check on PostToolUse Write|Edit on deliverable/synthesis-report/phase-gate files; M5 = hook-availability check at bootstrap; log-dispatch = trace all agent dispatches; audit-closeout = SessionEnd validation. Templates at `cowork/templates/hooks-settings.json`; scripts at `cowork/hooks/`. Related: Pre-flight Validation Gate.

**Hypothesis Library** — Component of a domain model. Testable starting points stated in the domain's vocabulary, including Governor-submitted hypotheses. Each hypothesis has a structured result format (confirmed / not confirmed / insufficient data). Defined in `cowork/templates/domain-model.md`. Related: Domain Model, Kill Discipline.

**Independence Level** — Bootstrap-time choice (1, 2, or 3) determining the session's baseline autonomy posture. Level 1 = AI proposes every action and waits for approval. Level 2 = AI executes within approved bounds, surfaces decisions at phase gates (default). Level 3 = maximum autonomy with post-hoc reporting; activates multi-agent deliberation. Set in `cowork/startup.md` Group 1. Related: Graduation Stage, Deliberation.

**Issue Ledger** — Deliberation artifact tracking unresolved disagreements across rounds. Each entry has structured fields including class (verdict-band split, taxonomy-reason disagreement, etc.) and disposition path. Plan #21 added a mandatory row class for rejection-taxonomy disagreements with canonical/secondary structure. Defined in `cowork/deliberation-protocol.md` §4.2. Related: VERDICT-SPLIT-CARRIED, Cross-domain tension.

**Kill Discipline** — Mandatory 6-point confounder analysis required before every kill decision. Prevents premature termination of tactics that failed for reasons unrelated to their hypothesis. Defined in framework spec §4.3. Three options at every phase gate: kill / pivot / persevere. Related: Hypothesis Library, Phase Gate.

**Operating Document (OD)** — The central runtime artifact containing goal, guardrails, AFC (when applicable), objectives, strategies, tactics, actions, domain model references, deliberation config (when applicable), evidence collection config (when applicable), and pre-flight validation manifest. Single source of truth for the session. Templated at `cowork/templates/operating-document.md`. Related: Bootstrap, Guardrail.

**Phase Gate** — Decision boundary between session phases. Each gate produces a structured Phase Gate Request that Governor (or governor-policy) dispositions: APPROVE / ESCALATE / REJECT. Defined in `cowork/gosta-cowork-protocol.md` §5.1. Pre-flight V-gates fire at phase entry/exit. Related: Pre-flight Validation Gate, Governor.

**Pool-agent** — Python CLI (`cowork/tools/pool-agent.py`) providing offline semantic search over reference pools using a quantized ONNX embedding model (all-MiniLM-L6-v2). Subcommands: setup-model, build, index-doc, query, update, delete, tags, verify-store. Score thresholds: ≥0.58 read full article, 0.50-0.57 excerpt only, <0.50 ignore. Related: Reference Pool, Evidence Tier.

**Position Paper** — Round-1 deliberation artifact produced by each domain agent. Per-candidate verdict from that domain's perspective with cite-then-apply discipline. Sized per per-deliverable cap (formula-based recommended for content-density-variable artifacts). Defined in `cowork/deliberation-protocol.md` §4.1. Related: Domain Agent, Cite-then-apply.

**Pre-flight Validation Gate (V1–V9)** — Mechanical validation gates running at lifecycle boundaries. V1 = retrieval contract validation; V2 = post-build shape verification; V3 = cross-doc consistency; V4 = continuous-capture coverage; V5 = first-call-per-session import test; V6 = declared-artifact existence + population (Layer A existence + Layer B sentinel-removal); V7 = inheritance vertical fit (coverage); V8 = subagent-dispatch capability smoke-test (conditional); V9 = inheritance framework-residue audit (conditional). Defined in framework spec §8.7. Related: Phase Gate, Hook.

**Prohibited Frame** — AFC field declaring what analytical frame would answer a different question than the stated goal. Example: a vendor-risk session prohibits procurement-advisory framing. Frame Integrity Validation audits deliverables against this declaration. Defined in `cowork/startup.md` Group 2A. Related: AFC, Frame Integrity Validation.

**Quality Principle** — Component of a domain model. Testable standard for "good" in the domain. Each principle references specific concepts and provides an observable criterion. Defined in `cowork/templates/domain-model.md`. Quality-gated at bootstrap: principles must be testable. Related: Anti-Pattern, Domain Model.

**Reference Pool** — Curated collection of source material (research documents, regulatory texts, analyst reports) that grounds AI reasoning in verified content rather than training data. Built and queried via pool-agent. Each pool has a YAML index. Defined in framework spec §18. Related: Pool-agent, Evidence Tier.

**Sub-coordinator** — Deliberation role in cluster-then-synthesize topologies. Synthesizes within a single cluster (e.g., 4 agents → 1 sub-coordinator) before COORD-1 cross-cluster synthesis. Plan #24 added an explicit re-engagement decision rule for Round 2+. Defined in `cowork/deliberation-protocol.md` §3.4. Related: Cluster-then-synthesize, Coordinator.

**Sycophancy** — AI compliance bias producing correctly-computed but misleadingly-framed content (e.g., accurate health score with optimistic narrative). Six detection flags formalized. Hardest bias to catch because it looks like good news. Defined in framework spec §14.3 + cross-cutting through deliberation. Related: Convergence Probe.

**Tier 0 / 1 / 2 / 3** — Implementation tiers independent of feature complexity. Tier 0 = file-based, no code, conversational AI as orchestrator. Tier 1 = MVP coded product (database, signal store, basic automation). Tier 2 = robust operations (full grounding infrastructure, automated verification). Tier 3 = production-hardened (multi-scope hierarchies, high autonomy, conversion funnels). Tier 0 is currently the only validated tier. Defined in framework spec §0. Related: Independence Level.

**U1 Independent Reviewer** — Subagent dispatched at phase-gate decision support and at closeout to audit orchestrator's claims against actual files. No domain model. Per Plan #30, dispatched in **two distinct roles** as separate subagent dispatches: **U1-adversarial** (`cowork/templates/independent-reviewer-prompt-adversarial.md`) enumerates weaknesses (ungrounded citations, tier-inflation, verdict-doesnt-survive, classification issues, sycophancy patterns, vague rejection reasons, omitted coverage gaps); **U1-constructive** (`cowork/templates/independent-reviewer-prompt-constructive.md`) verifies pass conditions on revised output (each adversarial finding's disposition verified, AFC frame-integrity holds, signal integrity holds, V6 closeout-mandated artifacts populated). Sequencing: adversarial first → orchestrator dispositions findings (revise / rebut / acknowledge-as-limitation) → constructive verifies on revisions. Constructive produces aggregate verdict PASS / FAIL / PASS-WITH-NOTES. Dual-role separation prevents the rubber-stamping bias of single-role dispatch where enumeration + verification compete in the same generation. Related: Sycophancy, Phase Gate.

**Verdict Strength Annotation** — Per-verdict annotation in synthesis report and deliverables: `[cluster-confirmation: N, tier-floor: T<X>]`. N = count of clusters confirming the verdict; T<X> = minimum evidence tier across supporting items. Lets readers distinguish high-confidence consensus from single-lens or floor-tier-anchored verdicts within the same band. Introduced by Plan #8. Related: Cross-cluster confirmation, Evidence Tier.

**VERDICT-SPLIT-CARRIED** — Inline annotation on verdicts where a verdict-band split was carried into the deliverable rather than force-resolved at deliberation termination. Surface format includes split-width descriptor and disagreeing agents/clusters. Introduced by Plan #13 verdict-split-aware termination. Related: Issue Ledger, Cross-domain tension.

**WMBT (What Must Be True)** — Strategy-level field declaring conditions that must hold for the strategy's reasoning to be valid. If WMBT is invalidated by signal data, the strategy may need to be killed regardless of individual tactic health. Defined in framework spec §3.3. Related: Kill Discipline, Operating Document.

---

**Cross-references:** Glossary entries linked from [README.md](../README.md), [walkthrough.md](walkthrough.md), [architecture-guide.md](architecture-guide.md), [examples/README.md](examples/README.md), [is-gosta-right-for-this.md](is-gosta-right-for-this.md), [troubleshooting.md](troubleshooting.md), [faq.md](faq.md), [authoring-domain-models.md](authoring-domain-models.md). New term not listed here? Open an issue or PR per [CONTRIBUTING.md](../CONTRIBUTING.md).
