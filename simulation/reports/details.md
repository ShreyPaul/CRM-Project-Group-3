# Detailed evidence and validation record

Current summary: [results report](report.md). This record preserves the external evidence and earlier validation history while identifying the current model assumptions and results. See the [methodology](../../report/Document%204%20%E2%80%94%20Methodology.md) for the complete current input tables.

## An ATT&CK and FAIR Simulation at BNY Scale

**Report date:** 20 November 2026; source and interpretation review updated 21 November 2026  
**Evidence base:** Public sources and provisional assumptions supplied by the outline; no BNY internal incident, HR, or alert data were used.

## Executive summary

This study compares the annual total cost of three insider-threat monitoring regimes. It asks how expected security losses change when monitoring, employee responses, program costs, and regulatory exposure are considered together.

The current model uses three attack scenarios and 20,000 simulated years per regime. Privacy-preserving monitoring (C) has the lowest baseline mean annual cost at **$69.10M**, compared with **$87.06M** for maximum surveillance (B) and **$99.57M** for the no-additional-program baseline (A). C also has the lowest baseline 95th-percentile cost.

These are conditional scenario results, not forecasts of BNY's actual losses or assessments of its current controls. The ranking depends on the assumptions: in separate tests, removing B's extra S2/S3 attempt rates or halving B's S2 success probabilities makes B cheaper than C. Employee replacement costs are illustrative fixed first-year amounts, and alert triage and morale/productivity are excluded.

## 1. Why use simulation?

An average incident cost alone cannot describe insider risk. The number of attempts, the share that succeed, the loss per successful event, and the costs of operating a monitoring program are all uncertain. A single point estimate can hide high-cost years.

Monte Carlo simulation propagates ranges for these inputs into a distribution of annual total costs. We compare the mean, median, 95th percentile (P95), and probability-of-exceedance curves. P95 is a high-cost percentile of the modeled annual-cost distribution; it is **not** a guaranteed loss ceiling or a confidence interval for the assumptions.

## 2. Scope

### Attack scenarios

| Scenario | Example behavior | Main potential harm |
|---|---|---|
| S1: USB data theft | An employee copies client data to removable media and takes it out of the organization. | Client-data exposure, investigation, and notification costs. |
| S2: Personal email/cloud exfiltration | An employee sends data to a personal mailbox or uploads it to personal cloud storage. | Client-data exposure, regulatory response, and client costs. |
| S3: Administrator sabotage | A disgruntled administrator abuses legitimate access or disables tools to destroy data. | Business disruption, recovery costs, and client impact. |

MITRE ATT&CK, a public knowledge base of adversary behavior and techniques based on real-world observations, describes the steps in each scenario. Controls are then translated into changes in attempt rates, success shares, and loss magnitudes using FAIR (Factor Analysis of Information Risk). The current figure table contains 16 in-scope technique entries, including parent techniques and subtechniques. Its relationship to the simulation is qualitative: the model does not read the mapping or calculate control effectiveness from it. The existing Navigator layers differ from the figure table and require reconciliation; see [FAIR mapping](../FAIR_MAPPINGS.md). [MITRE ATT&CK](https://attack.mitre.org/); [FAIR Institute method overview](https://www.fairinstitute.org/blog/3-steps-to-combine-mitre-attck-and-fair-to-focus-cyber-risk-management)

### Monitoring regimes

| Regime | Model definition |
|---|---|
| A: No additional insider-threat program | Standard IT controls, with no dedicated DLP, USB restriction, or behavioral analytics. This is a counterfactual comparison baseline, not a statement about BNY's actual controls. |
| B: Maximum surveillance | Full-content email/chat scanning with sentiment analysis, session recording, USB blocking, DLP across channels, all alerts sent to the SOC, no anonymization, and indefinite retention. |
| C: Privacy-preserving monitoring | The same USB, identity-and-access, and DLP blocking controls as B, but monitoring focuses on metadata and behavioral anomalies. Identities remain pseudonymous until a threshold is met; content or identity disclosure requires two-person approval; the outline proposes 90-day retention, subject to the scope clarification below; no sentiment inference is used. |

The proposed 90-day period concerns monitoring analytics eligible for deletion, not records subject to longer retention requirements. Applicable broker-dealer communications rules and separate retention costs require review for the actual system; the model does not establish compliance. See [SEC recordkeeping rule 17a-4](https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.17a-4).

## 3. Where the numbers come from

### Public evidence

| Public figure | Value | Use and boundary |
|---|---:|---|
| BNY full-time employees, 2025 | 48,100; 51,800 in 2024 | Scale context and employee-cost calculations. The 48,100-to-10,000 ratio is 4.81×; applying that factor linearly to attempt estimates is a modeling assumption, not a rate established by the annual report. |
| BNY 2025 revenue and noninterest expense | $20.080B; $13.054B | Cost plausibility checks and comparison of modeled losses with revenue. |
| BNY 2025 Staff expense | $7.159B | About $149k per year-end employee when divided by headcount. This is a rough all-staff expense proxy, not average salary. |
| BNY 2025 AUC/A and AUM | $59.3T; $2.2T | Business-scale context; these balances do not determine per-incident loss. |
| Ponemon 2026 insider-risk study | $742,125 average cost per malicious-insider incident and 6.3 such incidents per organization; $19.5M average annual cost across insider-risk categories; 67-day average containment | Cross-organization context and a reference point for S1 severity, not BNY incident rates. The study was sponsored by DTEX and covers several types of insider risk. |
| IBM 2026 Cost of a Data Breach study | $6.3M average per financial-services data breach | A broad industry reference for S1/S2 data-exposure severity, not an insider-only figure or a scenario-specific distribution. |
| SEC action involving BNY Mellon Securities Corporation and Pershing | $40M joint and several penalty | Magnitude reference for the off-channel communications line. The matter concerned broker-dealer recordkeeping, not insider data theft, and it does not establish an annual enforcement probability. |
| BNY Q3 2026 earnings call | About $4B annual technology spend on a roughly $13B expense base | Program-cost plausibility check. A third-party transcript attributes the $4B figure to CEO Robin Vince during the 15 October 2026 call; this is not a vendor quote or a verified cost for this program. |

BNY employee and financial figures are from its [2025 Annual Report](https://prodcs.bny.com/assets/corporate/documents/pdf/investor-relations/annual-report-2025.pdf). Ponemon figures are in the [study summary](https://www.ponemon.org/news-updates/blog/security/lessons-learned-from-the-2026-global-cost-of-insider-risks.html) and [2026 report page](https://ponemon.dtex.ai/); the penalty and case facts are in the [SEC order](https://www.sec.gov/files/litigation/admin/2024/34-100712.pdf); the technology-spend quote is in the [BNY Q3 2026 call transcript](https://www.fool.com/earnings/call-transcripts/2026/10/16/bny-bny-q3-2026-earnings-call-transcript/).

For review: the annual report's printed p. 2 (PDF p. 25) contains the financial summary; printed p. 10 (PDF p. 33) gives Staff expense and headcount. The SEC order's Section IV.D (PDF p. 10) specifies one $40M penalty jointly and severally, not $40M per company. Monetary benchmarks retain their source years; no common-year inflation adjustment was applied.

### What public evidence can and cannot establish

**It cannot establish BNY-specific “correct values” for these inputs.** FAIR separates Threat Event Frequency from Susceptibility (the probability that a threat event results in loss) and derives loss-event frequency from them. This is a useful model structure, but public sources generally count discovered incidents or confirmed breaches. They do not provide the full denominator of stopped attempts or a success rate for this project's USB, personal-email/cloud, and administrator-sabotage scenarios under regimes A, B, and C. [FAIR Standard v3.0](https://www.fairinstitute.org/hubfs/Standards%20Artifacts/Factor%20Analysis%20of%20Information%20Risk%20%28FAIR%29%20Standard%20v3.0%20%28January%202025%29.pdf)

| Input | External evidence located | Implication for this model |
|---|---|---|
| Attempts/incidents per year | Ponemon's 2026 study reports an average of **6.3 malicious-insider incidents per organization per year** across 354 organizations. This is a mean of discovered malicious incidents, not all attempted actions and not a BNY-specific rate. | It is an external comparison point for total malicious-insider incidents. It cannot be split into S1/S2/S3 or scaled linearly by 4.81× headcount. |
| Share of attempts that succeed | One available descriptive statistic is Verizon's Financial and Insurance sample: 927 confirmed disclosures among 3,336 incidents, about **27.8%**; the report summarizes this as roughly one-third. This is a sample-wide incident-to-confirmed-disclosure ratio across actor types, not the success rate for all insider attempts. The separate **22% internal-actor** figure is the share of confirmed breaches involving internal actors, not a success rate. [Verizon 2025 DBIR](https://www.verizon.com/business/resources/T859/reports/2025-dbir-data-breach-investigations-report.pdf) | This describes the reported sample only. Because the denominator is not all attempts, 27.8% should not calibrate a success-share parameter, including in a sensitivity test. |
| Loss per successful event | Ponemon reports **$742,125 per malicious-insider incident** on average. IBM reports a **$6.3M average cost per financial-services data breach** in its 2026 study. The event definitions, samples, and loss scope differ. | These are severity reference points, not min/mode/max distributions. No directly comparable financial-services average was found for S3 administrator sabotage. |

Multiplying the expected values of the current Beta-PERT attempt and success inputs produces about **38.7 successful events/year under A, 21.1 under B, and 18.3 under C**. Those modeled counts are higher than Ponemon's 6.3 incidents per organization. Because event definitions, survey populations, and company sizes differ, this is not a like-for-like error test, but it is a material calibration warning. The original S1/S2/S3 attempt counts, success shares, and 4.81× linear headcount scaling must remain labeled as team estimates, not externally validated figures.

**The defensible provisional benchmarks are:** 6.3 malicious-insider incidents per organization per year for frequency context; about 28% solely as a description of the financial-sector incident sample, not a success-rate calibration; and $742,125 per malicious-insider incident plus $6.3M per financial-services data breach for severity context. These figures come from different studies, definitions, and samples and must not be combined into one BNY parameter set. Public evidence does not support BNY-specific attempt counts, regime-specific success shares, or scenario-specific S1/S2/S3 min/mode/max values. To present this as a BNY scenario estimate, recalibrate it with internal blocked-attempt, confirmed-incident, control-effectiveness, and loss data, and document who elicited each remaining range and why.

### Provisional model inputs from the outline

The following min/mode/max values are provisional scenario assumptions supplied by the outline, not observations of BNY or documented completed expert elicitation. The simulation samples from a standard Beta-PERT distribution using these three points.

Day 3, Step 3.2 of the original outline calls for each member to submit min/mode/max values with a one-line rationale, reconcile differences, and log the result. That describes a proposed structured elicitation procedure, not evidence that it was completed. Until individual estimates, rationales, and reconciliation records are attached, the numbers should be labeled outline assumptions. Attempt counts use an assumed 10,000-person starting point multiplied by about 4.8; the S2/S3 uplift under B is attributed to grievance and channel-shifting behavior, while C's smaller uplift is attributed to perceived fairness. The specific counts are not verified by observed data. Success shares are estimates of control effects; no measured efficacy rates are provided. For losses, S1's $0.75M mode references Ponemon's average, S2 is framed around custody-bank client data and Reg S-P/SEC consequences, and S3 around G-SIB disruption and notification requirements. The latter scenario anchors and all endpoints remain team judgments. The outline requires logging the individual estimates and rationales, but it does not include those records, so the derivation of each value cannot currently be audited.

**Attempts per year:**

| Scenario | A | B | C |
|---|---:|---:|---:|
| S1 | 10 / 19 / 29 | 10 / 19 / 29 | 10 / 19 / 29 |
| S2 | 14 / 29 / 48 | 24 / 48 / 96 | 14 / 34 / 58 |
| S3 | 1 / 2.4 / 4.8 | 1.4 / 3.8 / 7.2 | 1 / 2.9 / 5.8 |

**Share of attempts that succeed:**

| Scenario | A | B | C |
|---|---:|---:|---:|
| S1 | 0.50 / 0.70 / 0.90 | 0.05 / 0.10 / 0.20 | 0.05 / 0.10 / 0.20 |
| S2 | 0.60 / 0.80 / 0.95 | 0.20 / 0.35 / 0.50 | 0.30 / 0.45 / 0.60 |
| S3 | 0.50 / 0.70 / 0.90 | 0.10 / 0.20 / 0.30 | 0.10 / 0.20 / 0.30 |

**Loss per successful event:**

| Scenario | Minimum / most likely / maximum |
|---|---:|
| S1 | $0.2M / $0.75M / $3M |
| S2 | $0.5M / $2M / $10M |
| S3 | $1M / $4M / $20M |

**Mode is the most likely value, not the mean.** S1 places its $0.75M mode near Ponemon's $742,125 mean. With standard Beta-PERT, however, its mean is (0.2 + 4 × 0.75 + 3) / 6 = **$1.033M**, about 39% above that external mean. This is a modeling choice, not a match validated by the study; a mean alone cannot identify a mode or endpoints. S2, S3, and all range endpoints remain scenario estimates. AUC/A, AUM, and notification obligations provide context; they do not directly calculate these loss ranges.

**Current employee, program, and off-channel costs:**

| Input | A | B | C | Basis |
|---|---:|---:|---:|---|
| Additional employee replacement cost | $0 | $14.39633M fixed | $10.84655M fixed | Illustrative first-year turnover calculation; excludes alert triage and morale/productivity. |
| Annual program cost | $0 | $2.5M / $5M / $7M | $1.5M / $3M / $5M | Scenario assumptions; the broad technology budget is context, not a program quote. |
| Annual off-channel enforcement probability | 0.02 / 0.05 / 0.08 | 0.05 / 0.10 / 0.15 | 0.01 / 0.03 / 0.05 | Scenario assumptions, not estimates derived from the SEC case. |
| Fine per enforcement event | $10M / $40M / $100M | Same | Same | The $40M mode references the SEC case; the endpoints are estimates. |

The current employee cost uses 48,100 employees, assumed intention gaps of 7.3 percentage points for B and 5.5 for C, 25% conversion to departures, 80% replacement, and $20,500 per replacement. These assumptions are not measured causal BNY effects. See [turnover findings](../monitoring_turnover_findings.md) for the calculation and evidence. The fixed first-year amounts are included in each simulated annual total; this does not establish the cost of a recurring multi-year program.

**Historical worksheet, retained for evidence:** The earlier model used aggregate employee-impact triples of $10M / $19M / $38M for B and $0.5M / $2.4M / $6.2M for C. Those amounts and the following component ranges are no longer current simulation inputs. They illustrate earlier ideas about triage, attrition and productivity, but their aggregation and overlaps were not reconciled.

The original employee-cost worksheet uses the following assumed components; none is a measured BNY monitoring effect, and components may overlap:

| Cost component | Calculation | Annual range |
|---|---|---:|
| Alert triage | 0.5%–2% of staff flagged monthly × 12 gives about 2,886–11,544 flags/year; 1–3 hours per flag at $60–$100/hour | $0.2M–$3.5M |
| Additional attrition | 0.1–0.4 percentage points of additional annual departures, about 48–192 employees, at $70k–$140k replacement cost each | $3.4M–$27M |
| Productivity impact | 20%–40% of employees × $136k employee-cost proxy × 0.25%–0.75% productivity decline | $3.3M–$20M |

**Updated worksheet check:** the old proxy is 50% × $13.054B / 48,100 = $135,696; the reported Staff line instead gives $7.159B / 48,100 = **$148,836 per employee-year**. This uses year-end headcount and all-staff expense, not average salary. Keeping the outline's unverified impact rates and 0.5–1× replacement-cost multiplier gives:

| Component | Recalculation with reported Staff expense | Annual range |
|---|---|---:|
| Alert triage | Same flags, hours, and hourly rates | $0.173M–$3.463M |
| Additional attrition | 48.1–192.4 expected departures × $74,418–$148,836 | $3.580M–$28.636M |
| Productivity impact | $7.159B × 20%–40% × 0.25%–0.75% | $3.580M–$21.477M |

This verifies arithmetic, not those assumed rates or multipliers. It does **not** derive a mode, remove overlap, or validate B/C aggregate costs. The current simulation no longer uses the outline's aggregate triples; the missing aggregation rationale remains relevant if these historical components are reconsidered. A's zero people/program lines mean zero **additional modeled monitoring costs**, not zero company payroll or IT spend. Shared baseline costs are outside this comparison.

### Evidence for employee impacts and limits on transferring effect sizes

Pages 5–6 of the outline name Thiel, Bernstein, and Ravid. Day 3 Step 3.4 explicitly states “directions from Ravid/Thiel, magnitudes elicited.” Behavioral mechanisms therefore have empirical support, while their magnitude at BNY remains an unverified outline assumption. The outline lacks full bibliographic entries; the following papers match the named authors and mechanisms, but their exact correspondence to the intended citations cannot be guaranteed.

| Matching study | Empirical support | Boundary for this model |
|---|---|---|
| [Ravid et al., 2023, EPM meta-analysis](https://doi.org/10.1111/peps.12514) | 94 independent samples, 23,461 participants; monitoring is associated with higher stress, and transparent, less invasive designs with more positive attitudes. | Turnover intentions are grouped with commitment in Table 1; intentions are not observed departures. Overall satisfaction and commitment associations in Table 2 are not statistically significant. |
| [Thiel et al., 2023, Stripped of Agency](https://doi.org/10.1177/01492063211053224) | A field study and experiment support reduced agency and displaced responsibility as mechanisms for deviance; perceived justice buffers the effect. | This is more specific than grievance. Workplace deviance is not a calibrated frequency of bank data theft or administrator sabotage. |
| [Bernstein, 2012, The Transparency Paradox](https://doi.org/10.1177/0001839212453028) | Factory field research and an experiment link observability to concealment and show benefits of group privacy under particular conditions. | Concealment includes productive process improvements. The paper does not directly test USB blocking causing personal-cloud data theft; that channel shift is a project extrapolation. |

Ravid's Table 1 (printed p. 17) and Table 2 (p. 19) were checked in the [full-text copy](https://gwern.net/doc/sociology/technology/2022-ravid.pdf). The corrected monitoring–stress correlation is approximately 0.16, 95% CI [0.13, 0.20]. It is not a 16% stress increase or a turnover-rate estimate, and the study does not establish universal productivity harm.

The assumed 0.1–0.4 percentage-point increase in annual departures (48–192 people), 20–40% affected staff, 0.25–0.75% productivity dip, and aggregate B/C costs lack a direct calibration chain from these studies. A defensible presentation states: **Research motivates including employee impacts; simulation explores decisions across assumed magnitudes of those impacts.**

### Corrected DBIR interpretation

Verizon's 2025 DBIR reports internal actors in **18%** of breaches overall and **22%** in its Financial and Insurance industry section. The widely reported **30%** figure refers to third-party involvement, not internal actors in financial services. DBIR's internal-actor category also includes errors and mistakes, not only malicious insiders. [Verizon 2025 DBIR](https://www.verizon.com/business/resources/T859/reports/2025-dbir-data-breach-investigations-report.pdf)

## 4. What the simulation does

For each simulated year, the model samples attempt rates, success shares, program costs, off-channel enforcement probability, and incident losses and fine severity when applicable. Employee replacement costs are fixed for each regime. Successful-event counts are sampled from a Poisson distribution with an expected rate equal to the sampled annual attempt rate multiplied by the sampled success share. Total annual cost is:

> employee cost + program cost + off-channel fine (if triggered) + losses from successful S1, S2, and S3 events

Attempt inputs are **annual rates**, so fractional values such as 2.4 are valid. The script samples the successful-event count directly; it does not simulate a fixed number of individual attempts. Each successful event gets a fresh severity draw. Enforcement contributes at most one off-channel fine per simulated year, independently of the three security scenarios; that annual timing is a simplification, not inferred from the SEC case.

The NumPy implementation runs **20,000 simulations**, then calculates mean, median, P95, and exceedance curves. A fixed random seed makes the run reproducible. We corrected the initial Beta-PERT parameterization: it uses the weighted mean as if it were the mode, changing the input distributions' means. The standard parameterization derives alpha and beta directly from the minimum, mode, and maximum. [Beta-PERT parameter reference](https://search.r-project.org/CRAN/refmans/prevalence/html/betaPERT.html)

The earlier comparison of PERT formulas used the former employee-cost assumptions and should be treated as historical validation, not as the current baseline. The standalone comparison script currently fails on fixed employee-cost inputs; the chart generator uses the corrected sampler and reproduces the current results. The standard-library simulation uses a different random stream, so its exact sampled means and percentiles differ even with the same seed.

### Sensitivity runs

In addition to the base case, we ran the three planned sensitivities:

1. Set B's S2 and S3 attempt ranges equal to A's, removing the grievance/channel-shift uplift.
2. Halve B's S2 success-share range to model more effective loss prevention. Detection only supports this change if intervention actually prevents loss.
3. Halve B's fixed employee replacement cost.

## 5. Results

The table reports the current NumPy simulation, in USD millions; P95 is the 95th percentile of modeled annual costs. Unchanged A and C values are the same across the tests.

| Case | A mean / P95 | B mean / P95 | C mean / P95 | Mean ranking, lowest first |
|---|---:|---:|---:|---|
| Baseline | 99.57 / 150.00 | 87.06 / 138.74 | 69.10 / 107.46 | C < B < A |
| B S2/S3 attempts set equal to A | 99.57 / 150.00 | 61.11 / 103.41 | 69.10 / 107.46 | B < C < A |
| B S2 success shares halved | 99.57 / 150.00 | 58.96 / 101.27 | 69.10 / 107.46 | B < C < A |
| B replacement cost halved | 99.57 / 150.00 | 79.86 / 131.55 | 69.10 / 107.46 | C < B < A |

Analytical baseline expectations are $99.61M, $86.97M and $69.31M for A, B and C. They differ slightly from simulation means because the latter use finite random samples.

## 6. Conclusion and limits

C has the lowest mean and P95 in the baseline, but B is cheaper in the first two individual sensitivity tests. These results reflect specified assumptions, not measured causal relationships or a prediction of BNY's losses.

Use the result to structure a policy discussion, not as a measured BNY risk ranking. Key limitations are:

- No BNY internal incident, alert, or HR data were available; attempt rates, success shares, losses, and employee impacts are outside-in estimates.
- Inputs are sampled independently. The model does not represent linked attacks or common shocks; the same real incident might cross S1/S2 and must not be counted twice. It also mixes uncertainty about rates with year-to-year randomness, rather than separately estimating confidence in the parameters.
- Individual event severities are bounded by the assumed maxima ($3M/$10M/$20M); larger single-event losses are excluded. Annual totals are not capped because Poisson event counts are unbounded. P95 therefore depends on both tail assumptions and independence.
- Cost definitions still need a ledger: triage may overlap program staffing, replacement costs may overlap productivity loss, and scenario regulatory losses may overlap the separate off-channel penalty. The current data do not verify these exclusions. The reported total covers the modeled items, not every enterprise cost.
- P95 is a percentile of modeled annual cost, not a confidence interval. The original decision rule's phrase “overlapping uncertainty” needs a precise definition.
- The EU AI Act's Article 5(1)(f) workplace emotion-inference prohibition applies from 2 February 2025, with medical/safety exceptions; Article 3(39) defines emotion recognition using biometric data. Text-only sentiment analysis should not automatically be labeled prohibited under that provision; other obligations still need assessment against the actual system and entity. The maximum Article 5 fine is EUR 35M or 7% of worldwide annual turnover, whichever is higher; this fine is not separately included in the simulation, which is not a legal opinion. [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689)

### What the notification rules actually establish

Regulation S-P requires covered institutions, subject to limited exceptions, to notify affected individuals as soon as practicable and within 30 days of awareness of a qualifying customer-information incident. Separately, the bank incident rule requires notice to the primary federal regulator as soon as possible and within 36 hours of determining a qualifying significant computer-security incident. These are different recipients and triggers; neither is a recovery deadline or a formula for the S2/S3 loss ranges. [SEC Regulation S-P summary](https://www.sec.gov/newsroom/press-releases/2024-58); [Federal Reserve joint rule summary](https://www.federalreserve.gov/newsevents/pressreleases/bcreg20211118a.htm)

### Hypotheses and consistency with the conclusions

The outline does not formally enumerate H1/H2 or specify statistical tests. The labels below reconstruct its hypotheses from the decision question, Day 3 inputs, and Day 4 Step 4.4 expectations.

| Hypothesis | Representation in the model | What the results establish |
|---|---|---|
| H1: C has lower annual total cost and P95 than A and B. | Comparison of simulated outputs. | Consistent with the base case; B becomes lower in two individual sensitivity tests. |
| H2: Employee impacts and behavioral responses partly offset B's stronger monitoring, leaving B close to A. | Lower success shares under B, but higher people costs, S2/S3 attempts, and enforcement probability. | Base means are B $87.06M and A $99.57M, a 12.6% difference. No equivalence margin defines “close”; the results do not show B is more expensive than A. |
| H3: Intrusive surveillance increases grievance and channel shifting, while privacy safeguards reduce that response. | S2/S3 attempt rates are B > C > A. | An input assumption, not an empirically tested behavioral effect. The simulation cannot establish causality or effect size. |
| H4: C retains key blocking capabilities while imposing lower employee costs than B. | B/C have identical S1/S3 success shares; C has a higher S2 success share and lower people costs. | Assumed control and cost relationships. The outputs do not independently establish equivalent security or improved employee outcomes. |

The outline's expected A cost of $60–70M conflicts with the standard-PERT analytical total of $99.61M; security-event losses alone contribute $97.36M. “B approximately equals A” needs a predefined equivalence margin. Three one-factor runs with different perturbation sizes cannot establish a global ranking of parameter sensitivity. The Day 1 preference for C on legal-feasibility grounds is a decision criterion, not a simulation finding. Several inputs favor C. Section 8 describes individual and joint sensitivity cases; further adverse cases would test other assumptions; the assumed behavioral mechanisms must not be presented as independently proven by the output.

**Historical validation correction:** An earlier attempt-rate sensitivity accidentally changed success shares as well; the current sensitivity changes only attempt rates. The values associated with the historical correction used the old employee-cost assumptions and are not current results.

## 7. Suggested presentation structure

1. Set out the decision, scenarios and monitoring regimes.
2. Distinguish public benchmarks from provisional model inputs.
3. Explain the baseline results and the first-year employee-cost assumption.
4. Show the sensitivity cases that can reverse the ranking and identify the data needed to test them.

## 8. Current figures and sensitivity findings

The [current results report](report.md) includes cost composition, coverage and sensitivity figures. The chart generator writes its figures and review data under `simulation/output/project_charts/en/`; see the [simulation README](../README.md) for reproduction instructions. The cost composition and break-even figures use analytical expectations, while the exceedance and individual sensitivity figures use simulated samples.

With B's other inputs fixed, its S2 success probabilities must fall to about **68.5%** of baseline for its analytical mean to equal C's—a relative reduction of about **31.5%**. Halving both B's S2 success probabilities and employee replacement cost yields an analytical B mean of **$51.71M**, compared with C's **$69.31M**. These break-even comparisons concern means, not P95 or evidence that the changes are achievable.

The baseline ATT&CK figure and Navigator layers do not currently agree on all coverage entries. The mapping is qualitative and does not calculate simulation parameters; see [source reconciliation](../FAIR_MAPPINGS.md).

## 9. Checks still needed before treating this as a company estimate

| Unresolved item | Evidence the team needs |
|---|---|
| Attempt rates and control success shares | Consistent incident definitions, attempted/blocked/successful counts, exposure period, and control tests. |
| Employee and program costs | Actual monitoring-related HR/alert data, implementation quotes, individual three-point estimates, and an overlap-adjusted cost ledger. |
| Traceability and decision criteria | Full bibliography from the outline authors; who chose each range and why; an agreed equivalence margin; retention and legal-scope review for the actual design. |

**Audit status:** the retained public-source discussion and historical worksheet document the earlier evidence review. The current numerical results have been reconciled with the chart generator; BNY-specific calibration remains unresolved. External sources and legal requirements have not been independently reverified in this update.

## Key references

- [BNY 2025 Annual Report](https://prodcs.bny.com/assets/corporate/documents/pdf/investor-relations/annual-report-2025.pdf)
- [SEC order involving BNY Mellon Securities Corporation and Pershing](https://www.sec.gov/files/litigation/admin/2024/34-100712.pdf)
- [Verizon 2025 Data Breach Investigations Report](https://www.verizon.com/business/resources/T859/reports/2025-dbir-data-breach-investigations-report.pdf)
- [Ponemon Institute: 2026 Cost of Insider Risks](https://www.ponemon.org/news-updates/blog/security/lessons-learned-from-the-2026-global-cost-of-insider-risks.html)
- [IBM: 2026 Cost of a Data Breach Report](https://newsroom.ibm.com/2026-07-29-ibm-study-one-in-four-malicious-breaches-are-ai-enabled,-costing-companies-6-million-on-average)
- [FAIR Institute: FAIR Standard v3.0](https://www.fairinstitute.org/hubfs/Standards%20Artifacts/Factor%20Analysis%20of%20Information%20Risk%20%28FAIR%29%20Standard%20v3.0%20%28January%202025%29.pdf)
- [BNY Q3 2026 earnings call transcript](https://www.fool.com/earnings/call-transcripts/2026/10/16/bny-bny-q3-2026-earnings-call-transcript/)
- [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689)
- [Beta-PERT parameter reference](https://search.r-project.org/CRAN/refmans/prevalence/html/betaPERT.html)
- [FAIR Institute: combining MITRE ATT&CK and FAIR](https://www.fairinstitute.org/blog/3-steps-to-combine-mitre-attck-and-fair-to-focus-cyber-risk-management)
- [MITRE ATT&CK knowledge base](https://attack.mitre.org/)
