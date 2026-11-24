# ATT&CK and FAIR Risk Mapping Report

## Executive summary

The project models three insider-threat scenarios: USB data theft, personal email or cloud exfiltration, and administrator sabotage. It compares annual losses and monitoring costs under a baseline regime, maximum surveillance, and privacy-preserving monitoring. FAIR concepts structure the model around the frequency of attempts, the likelihood that an attempt results in loss, and the magnitude of that loss.

The current analytical model estimates total annual costs of approximately **$99.61 million for the baseline, $86.97 million for maximum surveillance, and $69.31 million for privacy-preserving monitoring**. These results depend on provisional scenario assumptions and illustrative employee turnover costs; they are not estimates calibrated to BNY incident or employee data.

The project's ATT&CK coverage table describes 16 technique entries, including parent techniques and subtechniques. Those entries provide context for the scenarios, but the simulation does not calculate its inputs from technique-level coverage. A review of the repository also found differences between the figure script and Navigator layers. These differences limit the extent to which the coverage and risk results can be treated as a single reconciled assessment.

## Scope and method

The coverage assessment is drawn from [`make_figs.py`](../make_figs.py), and the numerical model is defined in [`run_validation.py`](run_validation.py). The mapping between them is qualitative. Neither the Navigator layers nor the figure script is an input to the simulation.

## FAIR model

| FAIR concept | Project input | Implementation |
|---|---|---|
| Threat event frequency (TEF) | Annual attempt rate for each scenario and regime | Sampled from a minimum / most likely / maximum Beta-PERT range. |
| Vulnerability, or susceptibility | Share of attempts that result in a loss event | Sampled independently from a Beta-PERT range; represents the combined effect of the scenario and its controls. |
| Loss event frequency (LEF) | Successful events per year | For each simulated year, the Poisson event rate is sampled attempt rate × sampled success share. |
| Loss magnitude (LM) | Loss per successful event | Each event's loss is sampled from the scenario's Beta-PERT range in USD. |
| Annual scenario loss | Frequency × magnitude | Sum of sampled losses across successful events. |

The model also adds program costs, illustrative employee turnover costs, and a separate off-channel enforcement event. These are additional annual cost components; they are not technique-specific FAIR inputs. The enforcement event is modeled separately, so any overlap with scenario loss must be assessed before using the results for a decision.

## ATT&CK coverage and its relationship to risk

The figure script classifies coverage as **I** for invisible, **D** for detected, and **B** for blocked. The columns appear in A / B / C order: A is the no-additional-program baseline, B is maximum surveillance, and C is privacy-preserving monitoring. The final column identifies the scenario-level input that a technique or its controls could inform. The model does not assign probabilities or loss values to individual techniques.

| ATT&CK technique | Scenario | A / B / C | Potential FAIR relevance |
|---|---|---|---|
| T1078 Valid Accounts | S1, S2, S3 | I / D / D | Access and detection can inform susceptibility for each scenario. |
| T1078.002 Domain Accounts | S3 | I / D / D | Privileged account controls can inform S3 susceptibility. |
| T1098 Account Manipulation | S3 | I / D / D | Persistence detection can inform S3 susceptibility. |
| T1685 Disable or Modify Tools | S3 | I / D / D | Detection of impaired defenses can inform S3 susceptibility. |
| T1213 Data from Information Repositories | S1, S2 | I / D / D | Collection controls can inform S1 and S2 susceptibility. |
| T1074 Data Staged | S1, S2 | I / D / D | Staging detection can inform S1 and S2 susceptibility. |
| T1560 Archive Collected Data | S1, S2 | I / D / D | Archive detection can inform S1 and S2 susceptibility. |
| T1005 Data from Local System | S1, S2 | I / I / D | Local collection detection can inform S1 and S2 susceptibility. |
| T1114 Email Collection | S2 | I / D / I | Email collection detection can inform S2 susceptibility. |
| T1052.001 Exfiltration Over USB | S1 | I / B / B | USB blocking can inform S1 susceptibility. |
| T1567 Exfiltration Over Web Service | S2 | I / D / I | Web-service detection can inform S2 susceptibility. |
| T1567.002 Exfiltration to Cloud Storage | S2 | I / D / D | Cloud-transfer detection can inform S2 susceptibility. |
| T1567.003 Exfiltration to Text Storage Sites | S2 | I / D / I | Text-site detection can inform S2 susceptibility. |
| T1048 Exfiltration Over Alternative Protocol | S2 | I / D / D | Alternative-protocol detection can inform S2 susceptibility. |
| T1029 Scheduled Transfer | S2 | I / D / I | Scheduled-transfer detection can inform S2 susceptibility. |
| T1485 Data Destruction | S3 | I / D / D | Detection and response can inform S3 susceptibility and potentially loss magnitude. |

Detection does not necessarily prevent a loss, and a blocked label does not imply zero residual risk. Effects on attempt frequency, susceptibility, and severity require separate evidence; the coverage labels alone cannot determine them. Parent techniques and subtechniques are listed as they appear in the coverage source, not as independent events to add together.

## Current scenario-level FAIR inputs

Each cell is **minimum / most likely / maximum**. Attempts are per year; success shares are probabilities; losses are USD millions per successful event. These are provisional model assumptions, not measured BNY values or values derived mechanically from the technique table.

| Scenario | Regime | Attempts / year | Success share | Loss / event ($M) |
|---|---|---|---|---|
| S1 USB theft | A | 10 / 19 / 29 | 0.50 / 0.70 / 0.90 | 0.2 / 0.75 / 3 |
| S1 USB theft | B | 10 / 19 / 29 | 0.05 / 0.10 / 0.20 | 0.2 / 0.75 / 3 |
| S1 USB theft | C | 10 / 19 / 29 | 0.05 / 0.10 / 0.20 | 0.2 / 0.75 / 3 |
| S2 Email/cloud exfiltration | A | 14 / 29 / 48 | 0.60 / 0.80 / 0.95 | 0.5 / 2 / 10 |
| S2 Email/cloud exfiltration | B | 24 / 48 / 96 | 0.20 / 0.35 / 0.50 | 0.5 / 2 / 10 |
| S2 Email/cloud exfiltration | C | 14 / 34 / 58 | 0.30 / 0.45 / 0.60 | 0.5 / 2 / 10 |
| S3 Administrator sabotage | A | 1 / 2.4 / 4.8 | 0.50 / 0.70 / 0.90 | 1 / 4 / 20 |
| S3 Administrator sabotage | B | 1.4 / 3.8 / 7.2 | 0.10 / 0.20 / 0.30 | 1 / 4 / 20 |
| S3 Administrator sabotage | C | 1 / 2.9 / 5.8 | 0.10 / 0.20 / 0.30 | 1 / 4 / 20 |

The model uses the same loss range across regimes within a scenario, even where detection or response could plausibly reduce severity. B and C use the same S1 and S3 success ranges; S2 differs. B and C also assume higher S2 and S3 attempt rates than A. These are model choices, not conclusions established by the coverage table.

## Derived frequency and loss

Under the model's independent inputs, the analytical expected annual event count is mean attempt rate × mean success share; the expected annual event loss multiplies that count by mean loss per event. The Beta-PERT mean is `(minimum + 4 × mode + maximum) / 6`. These are expectations, not products of the modes and not simulation percentiles.

| Regime | Scenario | Expected loss events / year | Mean loss / event ($M) | Expected annual event loss ($M) |
|---|---|---:|---:|---:|
| A | S1 | 13.417 | 1.033 | 13.864 |
| A | S2 | 23.486 | 3.083 | 72.416 |
| A | S3 | 1.797 | 6.167 | 11.079 |
| B | S1 | 2.076 | 1.033 | 2.146 |
| B | S2 | 18.200 | 3.083 | 56.117 |
| B | S3 | 0.793 | 6.167 | 4.892 |
| C | S1 | 2.076 | 1.033 | 2.146 |
| C | S2 | 15.600 | 3.083 | 48.100 |
| C | S3 | 0.613 | 6.167 | 3.782 |

## Other modeled costs

Values below come from the current `PARAMETERS` in `run_validation.py`. Triples are minimum / mode / maximum; amounts are USD millions. These lines are separate from the three event-loss scenarios.

| Input | A | B | C | Model treatment |
|---|---|---|---|---|
| Additional employee turnover cost | 0 | 14.39633 | 10.84655 | Fixed illustrative first-year amounts; triage and morale are excluded. |
| Program cost | 0 / 0 / 0 | 2.5 / 5 / 7 | 1.5 / 3 / 5 | Annual Beta-PERT cost. |
| Off-channel enforcement probability | 0.02 / 0.05 / 0.08 | 0.05 / 0.10 / 0.15 | 0.01 / 0.03 / 0.05 | Sampled annual probability of a separate enforcement event. |
| Fine per enforcement event | 10 / 40 / 100 | 10 / 40 / 100 | 10 / 40 / 100 | USD millions, sampled if the enforcement event occurs. |

With these inputs, the analytical expected total annual costs are approximately **$99.609M for A, $86.967M for B, and $69.308M for C**. The current README reports simulated means and P95s; the analytical values above are not P95s. [`turnover_sensitivity.py`](turnover_sensitivity.py) replaces B's fixed turnover input in its illustrative scenarios while C remains at baseline.

## Source reconciliation and limitations

| Source | What it supplies | Reconciliation needed |
|---|---|---|
| [`make_figs.py`](../make_figs.py) | The 16 technique rows and A/B/C coverage labels used in this sheet and the generated coverage figures. | Its table is independent of the Navigator files and simulation. |
| [Navigator layers](../MITRE-Navigation/) | Scenario/regime technique colors; identical copies also exist at the repository root. | They do not consistently match `TECHS`: for example, B/S2 and C/S2 color T1567.002 red while the figure table marks it detected; B/S3 and C/S3 color T1078.002 red while the table marks it detected. Several table entries, including T1005, are absent from the relevant layers. `rc-s1.json` contains a list of three layers, not a single RC layer. Reconcile with the team before claiming one definitive coverage map. |
| [`run_validation.py`](run_validation.py) and [`run_numpy_validation.py`](run_numpy_validation.py) | Current input triples and standard Beta-PERT/Poisson model; the latter also compares the original PERT formula. | Coverage labels are not inputs, and no individual control's contribution to success shares is calculated. |
| [`make_chart.py`](make_chart.py) | Analytical components, simulation and sensitivities, and chart outputs. | The B/C break-even grid changes B's S2 success shares and employee costs together; it compares means only. |
| [`reports/details.md`](reports/details.md) and [`reports/report.md`](reports/report.md) | Evidence and validation record; current results summary. | The detailed record preserves a clearly labeled historical employee-cost worksheet alongside current inputs and results. Use the scripts and README for model parameters and reproduction. |
| [`monitoring_turnover_findings.md`](monitoring_turnover_findings.md) | Basis and limitations of the illustrative turnover calculation. | Intention gaps and conversion to departures are assumptions, not measured causal effects at BNY. |

The simulation samples inputs independently and uses a Poisson count conditional on the sampled attempt rate and success share. Per-event loss is bounded by the specified maximum. It does not model dependence between controls, employee behavior, incidents, or loss severity, nor the effect of a specific ATT&CK technique on a specific parameter. The separate enforcement line and incident severity may overlap; reconcile their cost scope before interpreting totals.

## Assessment and evidence gaps

The principal evidence gap is the absence of organization-specific data connecting attempts, control performance, successful events, and resulting losses for each scenario and regime. The current ranges also lack a complete record of their source, rationale, ownership, and uncertainty. The assumed changes in attempt rates under monitoring and the turnover costs are particularly consequential to the comparison.

A calibrated assessment would need consistent definitions and observation periods for attempted, blocked, and successful events, together with response-effectiveness and loss data. It would also need a reconciled cost ledger to establish whether enforcement and incident losses overlap. The existing analysis is therefore best understood as a comparison of alternatives under stated assumptions. Further evidence and limitations are documented in [`reports/details.md`](reports/details.md).
