# GOSTA FAQ

Common questions about GOSTA. Each answer anchors in an existing claim from the README, protocols, or framework spec — not speculation. If your question isn't here, see [glossary.md](glossary.md), [troubleshooting.md](troubleshooting.md), or [is-gosta-right-for-this.md](is-gosta-right-for-this.md).

---

## Setup and Installation

### Do I need to install anything?

No, for Tier 0 (file-based, conversational AI). You clone the repo, paste a prompt into your AI assistant, and the AI orchestrates the session. The only optional install is the pool-agent setup if you want offline semantic search:

```bash
pip install numpy pyyaml onnxruntime tokenizers huggingface-hub onnx
python3 cowork/tools/pool-agent.py setup-model
```

This downloads a ~22MB embedding model. No API keys needed.

### Can I use GOSTA with ChatGPT, Gemini, or Claude?

Yes. The protocol is provider-agnostic by design. Tier 0 operates through any conversational AI that can read files (or have file content pasted into context). Cowork mode and Code mode in `cowork/startup.md` accommodate both file-access and paste-only AI tools.

Most testing has been done with Claude (the maintainer's primary tool). Other providers should work but may have quirks (different default behaviors around file reads, different tool-use conventions). Report issues per [CONTRIBUTING.md](../CONTRIBUTING.md).

### What's the difference between Cowork mode and Code mode?

- **Cowork mode**: AI works through a chat conversation. You paste prompts; the AI returns content; you copy that content into files. Slower, but works with any AI tool.
- **Code mode**: AI has direct file access (e.g., Claude Code). The AI reads, writes, and edits files autonomously. Faster, but requires a tool with file-system permissions.

Default is `code` per `cowork/startup.md` Group 1. Choose based on your AI tool's capabilities.

### Do I need to write code to use GOSTA?

No, for Tier 0. The framework runs entirely on markdown files and conversation. You don't write code; the AI doesn't write code. The output is markdown documents (Operating Document, signals, decisions, deliverables).

Yes, for Tier 1+ if you want a coded implementation (database, signal store, orchestration engine). Tier 1+ doesn't exist yet — it's on the roadmap.

---

## Session Mechanics

### How long does a GOSTA session take?

Depends on complexity:
- **Simple finite scope** (no deliberation, 1-2 domain models): 30-60 minutes.
- **Moderate finite scope** (deliberation, 3-4 domain agents, 12-30 candidates): 4-8 hours.
- **Complex finite scope** (8+ agents, evidence collection, multi-round deliberation): 6-12 hours.
- **Ongoing scope**: per-cycle cadence — typically 30-90 min per review cycle.

Most of the time is the AI working autonomously between phase gates. Active Governor time is much less — typically 30-45 min for bootstrap + 15-30 min per phase gate disposition.

### Can I run multiple GOSTA sessions in parallel?

Yes. Each session has its own directory. Concurrency limits depend on your AI tool. Code mode supports concurrent dispatches (per `cowork/deliberation-protocol.md` §1.1a). Cowork mode is sequential by nature of the chat interface.

### How do I resume a session that I started yesterday?

Re-enter the session directory and have the AI read `00-BOOTSTRAP.md` first — that's the orientation file. It carries cross-session state (action retry counters, kill deadline proximity, deferred decisions). Then load files in the Context Loading Order specified in the bootstrap.

The CLAUDE.md in the session directory tells the AI exactly what to do on re-entry. Just point your AI tool at the directory.

### What happens when the AI's context window resets?

Tier 0 handles this through the bootstrap file (`00-BOOTSTRAP.md`) which carries cross-session state, plus the canonical artifacts (OD, signals/, decisions/, etc.) in the session directory. When the AI re-enters, it reads the bootstrap and reconstitutes session state from the files.

This is why GOSTA mandates file-based persistence even at Tier 0 — without it, multi-session scopes would lose continuity.

### Can I customize the bootstrapper questions?

Yes. `cowork/startup.md` is markdown; fork and modify. For session-specific tweaks, use `cowork/session-launcher-template.md` to pre-fill specific values.

If your modifications would benefit other users, contribute a PR per [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Maturity and Limitations

### Is GOSTA production-ready?

Beta. The specification is complete (v6.1, 8,500+ lines, 22 sections), and Tier 0 (file-based) is usable for real work. Tier 1+ (coded implementations) doesn't exist yet — it's on the roadmap.

What this means: you can run governed sessions today and produce real decisions. You shouldn't expect plug-and-play infrastructure (databases, dashboards, automation) — those would be Tier 1+.

### What has been tested?

Per the README Status section: 8 simulation designs run by the authors covering operational scopes, analytical scopes (product roadmap, policy analysis), multi-agent deliberation (up to 10 agents, 3 rounds), and failure injection — 15 scenario runs producing 1,107 decisions total. Internal validation; no external deployments yet.

### What doesn't exist yet?

- Tier 1+ coded implementations (database, signal store, orchestration engine, dashboard)
- Per-cycle observability tooling beyond markdown
- Integration patterns for connecting to external data sources (CRM, analytics, financial feeds)
- Full OD Drafting Protocol (current release is minimal)
- Domain model authoring tools beyond templates
- Public sector / sustainability worked examples

See README §"What's Next" for the roadmap.

### Why does the spec keep getting larger?

Framework evolution per session-execution observations. Each plan executed adds derivation entries to `cowork/sync-manifest.md`. Backward-compatible: old sessions retain validity; framework changes apply prospectively.

If you want to know what's changed between two states, grep `sync-manifest.md` for the version range. The change log is the authoritative record.

---

## Specific Use Cases

### Can I use GOSTA for personal decisions?

Yes — career moves, major purchases, project planning, relocation decisions. The README's Use Cases section explicitly mentions this. See [is-gosta-right-for-this.md](is-gosta-right-for-this.md) borderline-cases section for fit guidance.

The lowest-cost test: spend 30 minutes following the [walkthrough](walkthrough.md). If structure helps your decision-making, you'll feel it; if it adds bureaucracy, you'll feel that too.

### Can I use GOSTA for research / academic work?

Yes — systematic literature reviews, multi-criteria evaluations, hypothesis testing across competing theories. The audit trail and reproducibility align with research norms (same protocol, same inputs → reproducible reasoning chain).

Adapt `docs/examples/feature-prioritization/` to your research question. Replace the domain models with your evaluation criteria, replace the candidates with your research targets.

### Does GOSTA help with compliance? EU AI Act / NIS2?

GOSTA's architecture aligns structurally with EU AI Act requirements (risk management, record-keeping, transparency, human oversight) and NIS2 resilience requirements. This alignment is structural, not certified — using GOSTA does not constitute legal compliance.

GOSTA provides the architectural patterns; your organization's compliance work maps the framework outputs to specific regulatory provisions. EU AI Act compliance mapping is on the roadmap.

### Can I integrate GOSTA with my CRM / analytics / Slack / etc.?

Not at Tier 0 (file-based). At Tier 0, integration is manual — you copy data from external sources into reference materials. Domain models score against that captured data.

At Tier 1+ (coded), integration patterns will support automated signal collection. Tier 1+ doesn't exist yet; integration patterns are roadmapped.

### How do I handle sensitive data?

Tier 0 inherits the AI tool's data handling. Whatever your AI tool does with prompts and files, that's what GOSTA does — it's a markdown-and-conversation framework, no separate data store.

For sensitive data, run against a private model deployment (Claude on AWS Bedrock, Azure OpenAI with VPC, etc.) where the data stays within your network boundary.

---

## Comparison with Other Tools

### How does GOSTA compare to LangChain / LangGraph / AutoGen?

Orthogonal layers. Orchestration frameworks (LangChain, LangGraph, AutoGen) define **how** agents execute tasks. GOSTA defines **who decides what within what bounds, what happens when things go wrong, and how the system proves its reasoning is sound.**

You can use GOSTA to govern an agent system built with any orchestration framework. The README explicitly frames this as "orchestration with governance, not orchestration vs governance."

### How does GOSTA compare to Constitutional AI / RLHF / safety-tuned models?

Different layer. Constitutional AI / RLHF / safety-tuned models constrain what an individual model output looks like. GOSTA constrains what the system around the model does — multi-step reasoning, multi-agent deliberation, decision-making, audit trail.

Models with safety tuning still produce outputs that need governance to become decisions. GOSTA is the governance layer; safety-tuned models are inputs to that governance.

### How does GOSTA compare to Anthropic's Safe Agents framework / OpenAI's Bounded Autonomy?

GOSTA emerged from analysis of these and similar approaches (Knight First Amendment Institute autonomy levels, Singapore IMDA Model AI Governance Framework, etc.). It integrates concerns those approaches address individually:
- Autonomy classification (graduated independence levels + within-session graduation stages)
- Formal constraints (typed guardrails + pre-flight validation gates)
- Compliance checkpoints (phase gates + Governor disposition)
- Hybrid team protocols (multi-agent deliberation with structured roles)

The integration produces mechanisms none of the individual approaches have — see README §"What's Novel" for the specifics (hallucination taxonomy, reasoning integrity, kill discipline with confounder analysis, structural sycophancy detection, autonomy that degrades gracefully).

---

## Contribution

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md). Common contribution paths:
- Domain models for `domain-models/examples/` with primary source citation
- Examples for `docs/examples/` demonstrating new patterns
- Bug reports / clarification requests via issues
- Protocol improvements via PR with sync-manifest derivation entry

### Can I disclose AI was used in my contribution?

Yes, and it's required for AI-assisted contributions. See [CONTRIBUTING.md §GenAI Disclosure](../CONTRIBUTING.md#genai-disclosure) for the disclosure format (tool used, what it generated, what was edited).

### How do I propose framework changes?

Three paths:
1. **Issue**: describe the gap or proposed change; maintainer dispositions.
2. **PR with sync-manifest entry**: implement the change and add a derivation entry per the existing C-numbered format.
3. **Verification-patterns-driven proposal**: apply `cowork/verification-patterns.md` to your proposal before submitting; the verification result strengthens the proposal.

Recent significant framework changes (Plans #6–#25) all originated from session-execution observations and were verified before applying. The verification-patterns file documents this discipline.

---

## Related

- [Is GOSTA right for this?](is-gosta-right-for-this.md) — fit assessment
- [Walkthrough](walkthrough.md) — first session in 10 minutes
- [Glossary](glossary.md) — terminology lookup
- [Troubleshooting](troubleshooting.md) — symptom-driven issue resolution
- [Examples](examples/) — completed sessions across complexity levels
- [README](../README.md) — what GOSTA is
- [CONTRIBUTING.md](../CONTRIBUTING.md) — how to contribute
