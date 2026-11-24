# Project consistency audit

The current numerical baseline is internally consistent across the chart generator, methodology, results report and web baseline. The issues below concern the relationship between the coverage artifacts, validation scripts and supporting documents. The results remain conditional on the project's assumptions.

## Findings

1. **Navigator layers do not match the documented coverage.** The coverage table in `make_figs.py` marks cloud-storage exfiltration T1567.002 as detected under B and C, while the corresponding S2 Navigator layers mark it red. The B and C S3 layers similarly differ on T1078.002. Some techniques in the figure table are absent from relevant layers. The file `rc-s1.json` contains three layers (A, B and C), rather than the single C layer its name and the navigation document describe. The layers also use different color codes and include extra colored techniques. Both root and `MITRE-Navigation/` copies have these issues. See [the coverage document](../report/Document%205%20%E2%80%94%20MITRE%20Navigation.md) and [source reconciliation](../simulation/FAIR_MAPPINGS.md). This affects the interactive coverage evidence, not the numerical simulation, which does not read the layers.

2. **The figure script does not regenerate Navigator layers.** The coverage document now notes that static figures and Navigator layers require separate updates. `make_figs.py` writes image and PDF figures only; it does not write JSON layers. A separate generation or reconciliation step is needed.

3. **The standalone NumPy validation script previously failed on fixed inputs.** The original-formula sampler now handles equal minimum and maximum values as a fixed value. Both formula comparisons run successfully; the original formula also uses different A people and program inputs, so its comparison is not solely a formula change.

4. **USB blocking and residual losses need a consistent explanation.** The coverage document defines blocked as stopping the technique and says USB exfiltration is blocked for B and C. The model nevertheless assigns S1 nonzero success probabilities and expects about $2.15M in annual S1 losses under each. The FAIR mapping says a blocked label does not imply zero residual risk. The coverage document now describes residual control failure or bypass as an interpretation of the nonzero assumed success probability; the specific failure paths remain unquantified.

5. **Simulation results depend on the implementation as well as the seed.** The published baseline and P95s come from the NumPy chart generator. Running `python run_validation.py` with the same seed gives A/B/C means of $99.19M/$87.20M/$69.29M and P95s of $149.25M/$139.70M/$107.64M, because it uses a different random-number generator and sampling sequence. Both implement the same model and produce the same ranking; the README and methodology should identify the NumPy implementation when giving exact reproducible values. Analytical expectations are a separate calculation and should not be mistaken for simulation means.

6. **The cost horizon is easy to misread.** The model adds a fixed *first-year* employee replacement cost to each simulated annual total. The published figures should not be interpreted as a fully specified recurring annual or multi-year forecast without assumptions about how turnover effects evolve. Morale, productivity and alert triage are omitted, and enforcement penalties may overlap incident losses. The source and scale of the attempt rates, control effectiveness and employee response remain uncalibrated to BNY; sensitivity tests demonstrate that the ranking can change.

7. **The source audit needed reconciliation with the current model.** `simulation/reports/details.md` was restored to preserve its benchmark discussion, evidence limitations and validation history, then updated to the current results. Its earlier employee-cost worksheet remains labeled as historical.

8. **Minor presentation issues remain.** The project index now identifies analytical expected costs and the simulated P95 separately. The employee-surveillance bibliography contains blank author initials and a different spelling from the methodology's reference. The analysis document and FAIR mapping also describe the relationship between the ATT&CK map and simulation with different degrees of precision: the mapping is qualitative and is not read as simulation input.

## Checks performed

- Ran `simulation/.venv/bin/python make_chart.py`: completed successfully; its current sensitivity CSV reproduces the reported NumPy means and P95s and the 68.5% break-even multiplier.
- Ran `python run_validation.py`: completed successfully and retained the same baseline and sensitivity rankings, with sampling differences described above.
- Reran `simulation/.venv/bin/python run_numpy_validation.py` after adding fixed-value handling: both formula comparisons and the sensitivity runs completed; corrected Beta-PERT results match the reported baseline.
- Confirmed the web baseline records hashes matching the current Python parameter and turnover files. The web model and production build could not be run because Node.js/npm and `web/node_modules` are absent in this environment.
- Checked local Markdown links in the report, simulation and web documentation; no missing local targets were detected. Confirmed that the two sets of individual Navigator files are byte-identical, including the three-layer `rc-s1.json`.
- The source claims and external links were not independently verified during this repository audit.
