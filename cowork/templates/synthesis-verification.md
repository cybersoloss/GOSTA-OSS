# Synthesis Verification Checklist — DELIB-[NNN]

**Governor:** [name] | **Date:** [date] | **Deliberation Cycle:** DELIB-[NNN]
**Verification Mode:** [full | spot_check]

Use this checklist after receiving a Synthesis Report. Full verification for ≤5 agents or high-stakes decisions. Spot-check for 4+ agents or 3+ rounds when full verification is impractical. See Deliberation Protocol §9.3.

---

## 1. Consensus Strength Check

**Coordinator reports consensus as:** [full / strong / weak / split]

Count actual position papers:

| Agent ID | Recommendation (from position paper) | Matches Coordinator's characterization? |
|----------|--------------------------------------|----------------------------------------|
| [agent] | [1-line recommendation — read from actual paper, not synthesis] | [yes / no / partial — explain] |

**Your count:** [N] of [total] agents support the consensus recommendation
**Coordinator's count matches?** [yes / no — if no, this is a consensus inflation flag]

---

## 2. Hard Disagreement Verification (MANDATORY — all verification modes)

For EVERY hard disagreement in the Synthesis Report, read both agents' actual papers.

### DIS-[NNN]: [disagreement summary from synthesis]

**Agent A ([ID]):**
- Coordinator says Agent A's position is: [quote from synthesis]
- Agent A's actual recommendation (from paper): [quote from position/response paper]
- **Match?** [accurate / distorted / missing context]
- If distorted: [what was changed and how it matters]

**Agent B ([ID]):**
- Coordinator says Agent B's position is: [quote from synthesis]
- Agent B's actual recommendation (from paper): [quote from position/response paper]
- **Match?** [accurate / distorted / missing context]
- If distorted: [what was changed and how it matters]

**Coordinator's framing of the tradeoff:** [fair / biased toward A / biased toward B / missing key context]

[Repeat for each hard disagreement]

---

## 3. Random Spot-Check (spot_check mode only)

Select 2 agents NOT involved in hard disagreements. Read their papers. Compare to synthesis.

### Spot-check Agent: [ID]
- Coordinator characterization: [from synthesis Agreement Map or Consensus Recommendation]
- Actual paper recommendation: [from position paper]
- **Match?** [accurate / distorted]

### Spot-check Agent: [ID]
- Coordinator characterization: [from synthesis]
- Actual paper recommendation: [from position paper]
- **Match?** [accurate / distorted]

**If ANY spot-check reveals distortion:** Escalate to full verification. Read all remaining papers.

---

## 4. Proxy Position Review (if applicable)

For any agent that required the extract-and-represent fallback:

| Agent ID | Domain | Proxy labeled correctly? | Coverage gaps noted? | Proxy excluded from consensus count? |
|----------|--------|--------------------------|---------------------|--------------------------------------|
| [agent] | [domain] | [yes/no] | [yes/no — what's missing] | [yes/no] |

---

## 5. Concept Fidelity Check (§14.3.2 retrieval faithfulness)

For each `[CONCEPT-DISTORTED]` flag in the Coordinator's Interim Assessment (if any), and for 1-2 key domain concepts in the Consensus Recommendation:

| Agent ID | Concept Cited | Domain Model Definition (verbatim or summary) | Agent's Application (from "How It Applies") | Faithful? |
|----------|--------------|-----------------------------------------------|----------------------------------------------|-----------|
| [agent] | [concept] | [definition from domain model] | [how agent applied it] | [yes / narrowed / broadened / drifted — explain] |

**If distortion found:** Does the distortion affect the agent's recommendation? If yes, the recommendation is partially ungrounded — note this in your verdict. If no (agent applied a valid subset), note as advisory.

**Systemic pattern check:** If the same concept was distorted by multiple agents, the concept definition in the domain model may be ambiguous. Flag for domain model revision in learnings.md under Retrieval Faithfulness Observations.

---

## 6. Verdict

- [ ] Consensus strength matches actual paper count
- [ ] All hard disagreements accurately characterized
- [ ] No distortion found in spot-checks (or full verification passed)
- [ ] Proxy positions correctly labeled and excluded from consensus
- [ ] Attribution chains in synthesis traceable to source papers
- [ ] No material concept distortion found (or distortion noted and impact assessed)

**Verification result:** [passed / failed — specify which check failed]

**If failed:** Governor should [remand for re-synthesis / override with own reading / request specific corrections].

**Governor decision on synthesis:** [accept / modify / override / remand] → Record as DEC-[NNN] in governor-decisions.md
