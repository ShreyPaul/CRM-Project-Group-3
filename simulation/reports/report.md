# Insider Threat Monitoring Costs and Decisions

A BNY-scale scenario analysis | 21 November 2026

**Under the current assumptions, privacy-preserving monitoring C has the lowest mean cost and P95. Joint improvements in maximum-surveillance regime B can reverse the mean-cost ranking.** This study compares decision conditions; it has not been calibrated with BNY internal data.

## Purpose and alternatives

More monitoring may reduce security losses while increasing alert-handling, employee-impact, and program costs. Simulation lets us compare those costs together.

We model three events: S1 USB data theft, S2 personal-email/cloud exfiltration, and S3 administrator sabotage.

| Regime | Main features |
|---|---|
| A No additional program | Basic IT controls; a comparison baseline, not BNY's actual posture. |
| B Maximum surveillance | Full-content scanning, sentiment analysis, and session recording, alongside USB and data-loss blocking. |
| C Privacy-preserving monitoring | Retains key blocking controls; emphasizes metadata and anomalies, with pseudonyms and two-person approval for disclosure. |

## Where the numbers come from

| Evidence type | Example and use |
|---|---|
| Public facts | BNY reported 48,100 employees and $7.159B Staff expense for 2025, providing scale and a labor-cost proxy. [Annual report](https://prodcs.bny.com/assets/corporate/documents/pdf/investor-relations/annual-report-2025.pdf) |
| External benchmarks | Ponemon reports 6.3 malicious-insider incidents per organization annually and $742,125 mean cost per incident. These provide context, not BNY-specific rates. [Study summary](https://www.ponemon.org/news-updates/blog/security/lessons-learned-from-the-2026-global-cost-of-insider-risks.html) |
| Outline assumptions | Attempt rates, success shares, loss ranges, and employee costs. Individual estimates and reconciliation records are missing, so completed expert elicitation cannot be claimed. |

[Ravid et al.](https://doi.org/10.1111/peps.12514) support considering stress and employee attitudes, but do not establish how much actual turnover monitoring would cause at BNY.

Ranges use min/mode/max: minimum, most likely, and maximum. **Mode is not the mean:** S1's mode is $0.75M, while its modeled mean severity is approximately $1.03M.

## What the script does

1. Samples annual attempt rates, success shares, and costs from the three-point assumptions using corrected Beta-PERT distributions.
2. Samples successful-event counts from a Poisson distribution with mean “attempt rate × success share,” then draws a loss for each event.
3. Adds employee impacts, program costs, and any off-channel communications fine, repeating for **20,000 simulated years**.

> Annual total cost = successful-event losses + employee impacts + program costs + off-channel fine

The validation script corrects the original PDF's use of the mean in place of the mode in its PERT formula. A's zero employee/program lines mean no additional monitoring costs; shared baseline IT spending is outside the comparison.

## Results

Amounts are USD millions ($M). P95 is the cost at or below which approximately 95% of simulated years fall; it is neither a guaranteed ceiling nor a confidence interval.

| Regime | Mean annual cost | P95 |
|---|---:|---:|
| A | $99.57M | $150.00M |
| B | $93.01M | $145.39M |
| C | **$61.08M** | **$99.79M** |

C remains lowest on mean and P95 in three individual tests: removing B's attempt-rate uplift, halving its S2 success shares, or halving its employee costs.

However, **halving B's S2 success shares and employee costs together** produces an analytical mean of **$54.85M**, below C's **$61.18M**, with all other inputs fixed. This joint test compares means only, not P95. Analytical and simulated means differ slightly because of sampling.

## Implications for company decisions

- **Assess employee costs alongside protection.** S2 contributes the largest security losses in this model, making its assumed loss-prevention effectiveness a priority for validation.
- **Pilot the assumptions that can change the ranking.** Collect attempted, blocked, and successful events, alert-handling hours, and employee-impact data before recalibrating.
- **Keep the conclusion conditional.** Independent inputs, bounded per-event losses, and unresolved cost overlap limit the model. It establishes neither a causal turnover rate nor universal superiority for C.

C's proposed 90-day retention needs to apply only to monitoring analytics eligible for deletion. Relevant broker-dealer business communications require at least three years. Separate-retention costs are not individually priced, so the model does not establish C's compliance. [Recordkeeping rule](https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.17a-4)

## Presentation and supporting material

Suggested story: **Why security benefits alone are insufficient → alternatives and assumptions → C leads at baseline → joint improvements can favor B → what the company should measure next.**

- [Five-figure PDF](output/project_charts/project_figures_en.pdf): cost composition, exceedance, individual sensitivities, B/C break-even map, and event frequency versus severity.
- [Original PDF numerical corrections, in Chinese](pdf_numeric_corrections_zh.md): original values, corrections, and effects on the simulation.
- [Detailed evidence and captions](details_en.md) | [Source audit and validation record](Day3-Day4-review.md) | [Traditional Chinese report](report_zh.md).
