## Focus
We model **traitor-based insider threat**: current employees who hold a grievance against the organisation and misuse their legitimate access. The candidate defence is **AI-based monitoring** of employee behaviour — mainly text data such as emails and messages — to detect signs of disgruntlement early and intervene before an incident.

## Core concern
If employees know they are constantly monitored, even honest employees may change their behaviour to avoid false flags. This can push concerns away from official reporting channels and create new risk, including cyber risk. Evidence and commentary: **Document 2**.

## What we compare
| Regime | Description |
|---|---|
| A | No additional monitoring program (baseline) |
| B | Maximum surveillance |
| C | Insider-threat monitoring with checks on permitted data use, plus privacy and anonymisation features |

These are analytical scenarios, not descriptions of BNY's actual monitoring arrangements.

## Approach
1. Use **MITRE ATT&CK** as an initial framework to structure what each regime gains and loses — which attacks become more or less likely (**Document 5**).
2. Quantify with **FAIR**-style risk modelling, implemented as a **Monte Carlo simulation** of annual costs (**Document 4**).
3. Model effects on employees, not just the organisation — currently via retention/turnover costs; satisfaction effects are planned (**Documents 2 and 4**).

## Organisational context
BNY is a global financial services firm (custody, payments, clearing, investment management) with 48,100 employees at year-end 2025 and $59.3 trillion in assets under custody/administration (BNY, 2025). Details: **Document 3**.

## Headline results (baseline assumptions)
- Expected annual total cost: **A $99.61M, B $86.97M, C $69.31M**. C also has the lowest 95th-percentile cost ($107.46M).
- **Personal email/cloud exfiltration (S2)** is the largest cost driver in every regime.
- The ranking is assumption-dependent: removing B's extra attack attempts, or cutting B's S2 success probabilities by ~31.5%, makes B cheaper than C. Full results and sensitivities: **Document 4**.

## Document map
| Document | Contents |
|---|---|
| 1 — Current implementations | Vendor tools (Proofpoint, Securonix, Living Security), reviews, research datasets |
| 2 — Surveillance effects on employees | Literature review and our comments |
| 3 — BNY background | Company profile, scale, insider-risk relevance, SEC recordkeeping case |
| 4 — Methodology | Simulation design, assumptions and their basis, parameters, results, limitations |
| 5 — MITRE Navigation | Scenario-to-technique mapping, rationale, documented mitigation (M1057) |

## References
BNY. (2025). *2025 annual report*. https://www.bny.com/assets/corporate/documents/pdf/investor-relations/annual-report-2025.pdf

---

