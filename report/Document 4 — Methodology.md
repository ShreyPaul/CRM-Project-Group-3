## Monte Carlo Cost Model of Insider-Threat Monitoring Regimes (BNY Context)

**Final simulated results (mean annual total cost, 20,000 simulated years per regime):**

| Regime | Description | Mean annual total cost |
|---|---|---|
| A | No additional monitoring program | **$99.57M** |
| B | Maximum surveillance | **$87.06M** |
| C | Privacy-preserving monitoring | **$69.10M** |

---

## 1. Objective and Scope

The model compares the expected annual cost of insider risk under three monitoring regimes, using BNY as the organizational context. The regimes are analytical scenarios, not descriptions of BNY's actual monitoring arrangements. Each regime is evaluated against three insider-threat scenarios:

- **S1** — USB data theft
- **S2** — Personal email / cloud exfiltration
- **S3** — Administrator sabotage

Company scale (2025 financial baseline): assets under custody/administration $59.3T; assets under management $2.178T; full-time employees 48,100; annual revenue $20.080B; noninterest expense $13.054B; staff expense $7.159B. The reported workforce supplies the scale for the turnover calculation.

## 2. Annual Cost Structure

For each simulated year, total cost is the sum of four components:

**Total cost = Incident losses (S1 + S2 + S3) + Monitoring program cost + First-year employee replacement cost (fixed) + Enforcement penalty (if an enforcement event occurs)**

Alert triage and morale/productivity effects are excluded.

## 3. Distributions and Sampling Method

| Element | Treatment |
|---|---|
| Uncertain inputs (attempts, success shares, losses, program costs, enforcement probabilities, penalties) | Beta-PERT, defined by minimum / most likely (mode) / maximum, shape parameter λ = 4 |
| Successful incident count per scenario | Poisson, with rate = sampled annual attempts × sampled success share |
| Loss per successful incident | Independent Beta-PERT draw per event; identical loss distributions across A, B and C |
| Enforcement | Annual probability sampled from Beta-PERT; enforcement event drawn against that probability; penalty sampled from Beta-PERT if the event occurs |
| Employee replacement cost | Fixed first-year amount per regime (Section 6) |

Beta-PERT with λ = 4 gives mean = (min + 4 × mode + max) / 6, with shape parameters α = 1 + 4(mode − min)/(max − min) and β = 1 + 4(max − mode)/(max − min).

## 4. Simulation Settings

| Setting | Value |
|---|---|
| Simulated years per regime | 20,000 |
| Uncertain-input distribution | Beta-PERT, λ = 4 |
| Successful incident count | Poisson (rate = sampled attempts × sampled success share) |
| Base random seed | 20261120 |
| Regime-specific seed | Base seed + ord(regime) → A: 20261185; B: 20261186; C: 20261187 |

**Procedure per simulated year, per regime:**
1. Sample annual attempts, success share, program cost, enforcement probability and (conditionally) penalty from their Beta-PERT distributions.
2. For each scenario s, compute rate = attempts × success share; draw the successful-event count from Poisson(rate).
3. Draw one loss per successful event and sum to obtain scenario incident losses.
4. Add the program cost and the fixed first-year replacement cost.
5. Draw the enforcement event; if it occurs, add the sampled penalty.
6. Record the annual total; after 20,000 years, report the mean and the 95th percentile.

## 5. Input Parameters (Appendix A Values)

All triples are minimum / most likely / maximum. Monetary values in USD; M denotes millions.

### 5.1 Attempts per year

| Scenario | A | B | C |
|---|---|---|---|
| S1 | 10 / 19 / 29 | 10 / 19 / 29 | 10 / 19 / 29 |
| S2 | 14 / 29 / 48 | 24 / 48 / 96 | 14 / 34 / 58 |
| S3 | 1 / 2.4 / 4.8 | 1.4 / 3.8 / 7.2 | 1 / 2.9 / 5.8 |

### 5.2 Share of attempts that succeed

| Scenario | A | B | C |
|---|---|---|---|
| S1 | 0.50 / 0.70 / 0.90 | 0.05 / 0.10 / 0.20 | 0.05 / 0.10 / 0.20 |
| S2 | 0.60 / 0.80 / 0.95 | 0.20 / 0.35 / 0.50 | 0.30 / 0.45 / 0.60 |
| S3 | 0.50 / 0.70 / 0.90 | 0.10 / 0.20 / 0.30 | 0.10 / 0.20 / 0.30 |

### 5.3 Loss per successful event (identical across regimes)

| Scenario | Minimum / most likely / maximum |
|---|---|
| S1 | $0.2M / $0.75M / $3M |
| S2 | $0.5M / $2M / $10M |
| S3 | $1M / $4M / $20M |

### 5.4 Monitoring program cost per year

| A | B | C |
|---|---|---|
| $0 / $0 / $0 | $2.5M / $5M / $7M | $1.5M / $3M / $5M |

### 5.5 Off-channel enforcement

| Element | A | B | C |
|---|---|---|---|
| Annual probability of enforcement | 0.02 / 0.05 / 0.08 | 0.05 / 0.10 / 0.15 | 0.01 / 0.03 / 0.05 |
| Penalty conditional on enforcement (all regimes) | $10M / $40M / $100M | — | — |

## 6. First-Year Employee Replacement Cost (Fixed)

**Formula:** workforce × incremental turnover-intention gap × conversion to departures × replacement share × cost per replacement.

**Cost per replacement:** $15,000 (hiring, onboarding, ramp-up) + $3,000 (net vacancy) + 50% × $5,000 (first-year compensation difference) = **$20,500**.

| Input | A | B | C |
|---|---|---|---|
| Workforce | 48,100 | 48,100 | 48,100 |
| Additional turnover-intention gap vs. A | 0 pp | 7.3 pp | 5.5 pp |
| Conversion to actual departures | — | 25% | 25% |
| Share of additional departures replaced | — | 80% | 80% |
| **Fixed first-year replacement cost** | **$0** | **$14,396,330** | **$10,846,550** |

## 7. Component Sub-Values (Expected Cost Decomposition)

Closed-form expectations (product of PERT means under independence) are used for the cost decomposition; the headline results in Section 8 are the simulation means. Mean loss per event: S1 ≈ $1.03M; S2 ≈ $3.08M; S3 ≈ $6.17M.

| Component (expected, $M) | A | B | C |
|---|---|---|---|
| S1 incident losses | 13.86 | 2.15 | 2.15 |
| S2 incident losses | 72.42 | 56.12 | 48.10 |
| S3 incident losses | 11.08 | 4.89 | 3.78 |
| Monitoring program | 0.00 | 4.92 | 3.08 |
| Employee replacement (fixed) | 0.00 | 14.40 | 10.85 |
| Expected enforcement penalty | 2.25 | 4.50 | 1.35 |

Notes: S2 is the principal cost driver in every regime. B and C share identical S1 inputs. Components are rounded; the simulation means deviate from the closed-form component sums by less than approximately $0.25M per regime, consistent with Monte Carlo sampling error at 20,000 draws.

## 8. Results

| Statistic | A | B | C |
|---|---|---|---|
| **Mean annual total cost (Monte Carlo)** | **$99.57M** | **$87.06M** | **$69.10M** |
| 95th-percentile annual cost (P95) | $150.00M | $138.74M | $107.46M |

C has both the lowest mean and the lowest tail cost; approximately 5% of simulated years exceed the respective P95 amounts.

## 9. Sensitivity and Break-Even (Supporting Analysis)

- **One-at-a-time changes to B (Monte Carlo, holding A and C at baseline):** removing B's additional S2/S3 attempt rates lowers B's mean to $61.11M; halving B's S2 success probabilities lowers it to $58.96M — both below C's $69.10M. Halving B's replacement cost gives $79.86M, leaving C cheaper.
- **Break-even (closed-form expectations):** with employee costs unchanged, B reaches equal expected cost when its S2 success probabilities fall to approximately 68.5% of baseline (a 31.5% relative reduction).
- **Turnover-only sensitivity:** varying B's intention gap (0 / 7.3 / 19 pp) and conversion (10% / 25% / 50%) moves B between $72.57M and $147.51M; C remains cheaper throughout this comparison.

## 10. Assumptions and Limitations

- Attack rates, control effectiveness and employee responses are team-defined scenario assumptions; published sources provide scale and context only (Ponemon reports incidents rather than attempts; MITRE describes controls without establishing success probabilities; published means do not establish modes).
- The 7.3-point intention gap is informed by a Norwegian monitoring survey and does not measure causal BNY turnover; applying it to the full workforce is a modeling choice.
- Program costs are regime-specific estimates; vendor pricing provides context, not validation of the B/C difference.
- The $40M penalty mode is informed by the 2024 SEC recordkeeping order (BNY Mellon Securities Corporation and Pershing LLC); annual probabilities and the penalty range remain assumptions.

## References

1. The Bank of New York Mellon (BNY). (2025). *2025 Annual Report*. https://www.bny.com/corporate/global/en/investor-relations/annual-report-2025.html
2. Ponemon Institute. (2026). *Lessons Learned from the 2026 Global Cost of Insider Risks*. https://www.ponemon.org/news-updates/blog/security/lessons-learned-from-the-2026-global-cost-of-insider-risks.html
3. MITRE ATT&CK. (n.d.). *Data Loss Prevention (M1057)*. https://attack.mitre.org/mitigations/M1057/
4. IBM. (2026). *Cost of a Data Breach Report 2026*. https://www.ibm.com/reports/data-breach
5. Flatøy, C. A., & Lund-Tønnesen, J. (2025). *Electronic monitoring, trust, and turnover intention in the public and private sector*. https://www.tandfonline.com/doi/full/10.1080/14719037.2025.2608281
6. Microsoft. (n.d.). *Microsoft Purview pricing*. https://www.microsoft.com/en-us/security/microsoft-purview-pricing
7. U.S. Securities and Exchange Commission (SEC). (2024). *Order Instituting Administrative and Cease-and-Desist Proceedings (Release No. 34-100712)*. https://www.sec.gov/files/litigation/admin/2024/34-100712.pdf
8. American Psychological Association (APA). (2023). *2023 Work in America: AI, monitoring technology, and psychological well-being*. https://www.apa.org/topics/healthy-workplaces/employee-electronic-monitoring
