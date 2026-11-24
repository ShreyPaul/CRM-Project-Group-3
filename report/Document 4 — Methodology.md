Document 4 — Methodology

## Design
We use **Monte Carlo simulation** to compare annual costs under three regimes (A: no additional monitoring; B: maximum surveillance; C: privacy-preserving monitoring), each evaluated across three scenarios:

- **S1** — USB data theft
- **S2** — personal email/cloud exfiltration
- **S3** — administrator sabotage

Mechanics:
- 20,000 simulated years per regime.
- Uncertain inputs follow **Beta-PERT distributions** (minimum / most likely / maximum; shape λ = 4).
- Successful incident counts follow a **Poisson distribution** with rate = sampled annual attempts × sampled success share.
- Each successful incident receives a sampled loss.
- **Total cost = incident losses + monitoring program cost + fixed first-year employee replacement cost + enforcement penalty (if a sampled enforcement event occurs).**
- Seeds: base 20261120; regime seed = base + ord(regime).

Figures 1, 4, 5, 6 in the source use analytical expectations; Figures 2 and 3 use Monte Carlo results.

## Parameters (min / mode / max; USD)

**Attempts per year**
| Scenario | A | B | C |
|---|---|---|---|
| S1 | 10 / 19 / 29 | 10 / 19 / 29 | 10 / 19 / 29 |
| S2 | 14 / 29 / 48 | 24 / 48 / 96 | 14 / 34 / 58 |
| S3 | 1 / 2.4 / 4.8 | 1.4 / 3.8 / 7.2 | 1 / 2.9 / 5.8 |

**Share of attempts that succeed**
| Scenario | A | B | C |
|---|---|---|---|
| S1 | 0.50 / 0.70 / 0.90 | 0.05 / 0.10 / 0.20 | 0.05 / 0.10 / 0.20 |
| S2 | 0.60 / 0.80 / 0.95 | 0.20 / 0.35 / 0.50 | 0.30 / 0.45 / 0.60 |
| S3 | 0.50 / 0.70 / 0.90 | 0.10 / 0.20 / 0.30 | 0.10 / 0.20 / 0.30 |

**Loss per successful event** (same for A, B, C): S1 $0.2M / $0.75M / $3M; S2 $0.5M / $2M / $10M; S3 $1M / $4M / $20M.

**Program cost per year:** A $0; B $2.5M / $5M / $7M; C $1.5M / $3M / $5M.

**Annual probability of off-channel enforcement:** A 0.02 / 0.05 / 0.08; B 0.05 / 0.10 / 0.15; C 0.01 / 0.03 / 0.05. Rationale for the regime ordering: **[blank — not in source]**.
**Penalty conditional on enforcement** (all regimes): $10M / $40M / $100M.

**Employee replacement cost (fixed, first year):** A $0; B $14,396,330; C $10,846,550. Formula (same for B and C): workforce × incremental intention gap × conversion to departures × replacement share × cost per replacement.
| Input | A | B | C |
|---|---|---|---|
| Workforce | 48,100 | 48,100 | 48,100 |
| Additional turnover-intention gap vs A | 0 pp | 7.3 pp | 5.5 pp |
| Conversion to departures | — | 25% | 25% |
| Share replaced | — | 80% | 80% |
| Hiring/onboarding/ramp-up per replacement | — | $15,000 | $15,000 |
| Net vacancy cost per replacement | — | $3,000 | $3,000 |
| Annual compensation difference per replacement | — | $5,000 | $5,000 |
| First-year fraction of compensation difference | — | 50% | 50% |

Cost per replacement = $20,500. These costs exclude alert triage and morale/productivity effects.

## Where the assumptions come from
| Input | Basis and limitations |
|---|---|
| Company scale | BNY reports 48,100 year-end employees; applying turnover to the full workforce and scaling attempts with headcount are modelling choices (BNY, 2025) |
| Attempts and success shares | Scenario estimates informed by insider-risk benchmarks and documented control capabilities. Ponemon reports incidents, not attempted actions; MITRE describes controls without establishing success probabilities (Ponemon Institute, 2026; MITRE ATT&CK, n.d.) |
| Loss per incident | Published insider-incident and financial-services breach costs give severity context; the min/mode/max values remain estimates — a published mean does not establish a mode or distribution (Ponemon Institute, 2026; IBM, 2026) |
| Replacement costs | B's 7.3-pp gap informed by a Norwegian monitoring survey; C's 5.5-pp gap assumed; illustrative, not causal BNY turnover (Flatø & Lund-Tønnesen, 2025; BNY, 2025) |
| Program costs | Regime-specific estimates; public vendor prices give context but do not validate BNY spending or the B/C difference (Microsoft, n.d.) |
| Enforcement | The historical $40M BNY-related penalty informs severity; annual probabilities and penalty range are scenario assumptions (SEC, 2024) |

Regime differences represent **hypotheses** about control effectiveness and employee behaviour, not measured effects.

## Results (USD millions)
- **Expected totals:** A $99.61M; B $86.97M; C $69.31M. S2 is the largest component in every regime: $72.42M / $56.12M / $48.10M.
- **Exceedance (Monte Carlo):** P95 costs A $150.00M; B $138.74M; C $107.46M. C has the lowest tail risk.
- **Frequency vs severity:** S3 has the highest mean loss per event (~$6.17M; S2 $3.08M; S1 $1.03M), but S2 occurs more often and drives total expected loss. B and C overlap on S1 (identical inputs).
- **Sensitivity (Monte Carlo):** B's mean falls from $87.06M to $61.11M if its extra S2/S3 attempts are removed, and to $58.96M if its S2 success probabilities are halved — both below C's $69.10M. Halving B's replacement cost gives $79.86M (C still cheaper). P95 rankings match.
- **Turnover sensitivity:** varying B's intention gap (0 / 7.3 / 19 pp) and conversion (10% / 25% / 50%), B ranges $72.57M–$147.51M; C stays $69.31M. Turnover changes alone do not reverse the baseline decision.
- **Break-even:** with employee costs unchanged, B matches C when its S2 success probabilities fall to ~68.5% of baseline (a 31.5% relative reduction). Halving both S2 success and replacement cost gives B $51.71M vs C $69.31M.

## References
BNY. (2025). *2025 annual report*. https://www.bny.com/assets/corporate/documents/pdf/investor-relations/annual-report-2025.pdf

Flatø, ____, & Lund-Tønnesen, ____. (2025). *Electronic monitoring and turnover intention*. https://doi.org/10.1080/14719037.2025.2608281

IBM. (2026). *2026 cost of a data breach findings* [Press release]. https://newsroom.ibm.com/2026-07-29-ibm-study-one-in-four-malicious-breaches-are-ai-enabled,-costing-companies-6-million-on-average

Microsoft. (n.d.). *Microsoft Purview pricing*. https://www.microsoft.com/en-us/security/microsoft-purview-pricing

MITRE ATT&CK. (n.d.). *Data loss prevention (M1057)*. https://attack.mitre.org/mitigations/M1057/

Ponemon Institute. (2026). *Lessons learned from the 2026 global cost of insider risks*. https://www.ponemon.org/news-updates/blog/security/lessons-learned-from-the-2026-global-cost-of-insider-risks.html

SEC. (2024). *Order 34-100712* (Section IV.D). https://www.sec.gov/files/litigation/admin/2024/34-100712.pdf

---

