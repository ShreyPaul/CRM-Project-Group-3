# Monitoring, turnover and replacement costs

## Purpose and current model

This note records evidence and proposed sensitivity inputs for comparing extensive monitoring (B) with privacy-preserving monitoring (C). Each regime combines several controls; neither represents AI alone. The model uses illustrative first-year turnover costs of **$14.40 million for B** and **$10.85 million for C**. These replace the outline’s aggregate people-cost assumptions and exclude alert triage and morale/productivity costs, which have not been separately estimated. The resulting total costs are therefore incomplete. The costs are fixed values in the simulation and do not represent uncertainty in these assumptions.

## Evidence

| Evidence | Finding | Relevance and limits |
|---|---|---|
| [APA, 2023 Work in America](https://www.apa.org/pubs/reports/work-in-america/2023-work-america-ai-monitoring) | 42% of workers reporting monitoring intended to look for another job within a year, versus 23% reporting no monitoring: a 19 percentage-point gap. | U.S. survey association across broad monitoring practices; neither a causal effect nor actual turnover. It does not compare B with C. |
| [Flatø and Lund-Tønnesen, electronic monitoring and turnover intention](https://doi.org/10.1080/14719037.2025.2608281) | For private-sector workers, estimated intention was 24.43% with time-use monitoring versus 17.13% without, a 7.3 percentage-point difference. Productivity monitoring did not significantly predict intention in that group. | Adjusted Norwegian survey association. The monitoring types and intention measure differ from our regimes and the APA survey. |
| [BNY 2024 sustainability report](https://www.bny.com/assets/corporate/documents/pdf/2024-sustainability-report.pdf) | Company-wide retention was 92%; 21% of open positions were filled internally. | Context only. The retention complement is not necessarily a standardized voluntary turnover rate. Internal fills are a share of openings, not a replacement rate; an internal move can create another vacancy. |
| [BNY European Bank 2024 annual report](https://www.bny.com/assets/corporate/documents/pdf/investor-relations/the-bank-of-new-york-mellon-sa-nv-2024-annual-report.pdf) | The European entity reported 263 exits and 15% turnover, using average headcount over 13 months. | Entity-specific, not global or attributable to monitoring. |
| [BNY 2025 annual report](https://www.bny.com/assets/corporate/documents/pdf/investor-relations/annual-report-2025.pdf) | Year-end full-time headcount was 48,100, versus 51,800 in 2024; annual staff expense was $7.159 billion. | About $149,000 per year-end employee is a rough staff-expense scale check, not average salary or replacement cost. Headcount change does not identify departures, hiring, or AI substitution. |
| [BLS JOLTS](https://www.bls.gov/news.release/jolts.a.htm) | The U.S. financial activities monthly hires rate was 1.7% in September 2026. | Hiring includes growth and replacement; this is not the share of leavers replaced or a BNY rate. |
| [Longitudinal turnover study](https://doi.org/10.1002/job.281) | Intentions predicted actual departures among Netherlands Navy professionals followed for two years. | Supports considering both outcomes, but supplies no transferable BNY conversion factor. |
| [Stanford Digital Economy Lab](https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf) | Payroll analysis found no evidence of widespread economy-wide displacement and differing trends by AI exposure. | Supports exploring substitution by role, but does not estimate BNY's AI replacement rate. |

## Parameter assumptions

The following values define illustrative sensitivity scenarios. They are not validated BNY estimates, and the observed monitoring comparisons do not directly measure the difference between B and C.

| Input | Scenario values | Justification and status |
|---|---|---|
| Exposed workforce | 48,100; smaller exposed populations | 48,100 is BNY's 2025 year-end full-time headcount; applying the effect to everyone is a scale assumption. The actual covered workforce is unknown. |
| Intention gap versus A | B: 7.3 points; C: 5.5 points | B uses the Norwegian time-use association as an illustrative reference. C is an assumed smaller effect reflecting its safeguards; neither is a measured causal effect. B sensitivities use 0, 7.3 and 19 points; the 19-point APA association covers different monitoring and a different outcome. |
| Incremental intention-to-departure conversion | 10%, 25%, 50% | Illustrative low, middle and high assumptions, not observed conversion rates. A BNY-specific estimate would require employee surveys and subsequent voluntary departures over a matching period. |
| Departures replaced | 80% in the illustrative case | Illustrative placeholder, not a reported BNY rate. Roles may be eliminated, redesigned, or filled later. |
| Internal share of filled openings | 21% reference | BNY's reported share of all openings filled internally, not necessarily the share of replacements. An internal move may require a further backfill. |
| Hiring, onboarding and ramp-up per replacement | $15,000 in the worked example | Illustrative placeholder; recruiting, training and lost-output data by role and location are unavailable. |
| Net vacancy cost per replaced role | $3,000 in the worked example | Illustrative placeholder after compensation savings; temporary cover and lost output remain unmeasured; overlap with ramp-up costs must be avoided. |
| Annual compensation difference per replacement | $5,000, with half a year worked, in the example | Illustrative placeholder. Comparable departing and starting compensation by role and location is unavailable. |
| AI substitution | No measured BNY rate; varies by role | Headcount decline does not establish substitution; an AI alternative also entails implementation, operating and residual-work costs. |

Alert triage and morale are not included in the modeled turnover costs; they require separate estimates that avoid overlap.

## Calculation and illustrative breakdown

Incremental departures are calculated as exposed workforce × intention gap × assumed conversion. The calculation treats the gap as a causal incremental effect for the scenario; the studies do not establish that relationship. The measures require compatible time horizons and must account for departures that would have occurred anyway.

With 48,100 employees, a 7.3-point gap and 25% conversion, the calculation gives approximately **878 additional departures**. At an assumed 80% replacement rate, approximately **702 roles are filled**. The following values are illustrative:

| First-year component | Calculation | Approximate cost |
|---|---|---:|
| Recruiting, onboarding and ramp-up | 702 × $15,000 | $10.5M |
| Net vacancy cost | 702 × $3,000 | $2.1M |
| Compensation difference | 702 × $5,000 × 50% of year | $1.8M |
| **Total** | | **$14.4M** |

For C, 48,100 × 5.5% × 25% × 80% × $20,500 gives **$10,846,550**. The same formula at 7.3% gives **$14,396,330** for B. These amounts are fixed model inputs, not empirical estimates.

This example excludes costs and savings associated with unfilled roles and any internal-backfill chain. It is not a predicted BNY loss. Regular replacement salaries are not automatically new costs: the incremental amount is the net difference from departing employees' compensation. Vacancy savings, lost output, and employee impacts already included in the model must not be counted twice. First-year costs differ from recurring effects.

The principal evidence gaps are monitoring coverage, actual voluntary departures following surveys, replacement and internal-backfill rates, vacancy duration, role-specific costs, and AI substitution costs. A cost ledger reconciled with the existing employee-impact assumptions is needed before recalibrating the baseline.
