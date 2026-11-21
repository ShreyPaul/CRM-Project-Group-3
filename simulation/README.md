# Reproduce the simulation figures

This folder generates five English figures comparing three insider-threat monitoring regimes at BNY scale. All model inputs are defined in `run_validation.py`; no external dataset or PDF is needed to run the code.

## Files to commit

| File | Purpose |
|---|---|
| `make_chart.py` | Generates the figures, review data, and ZIP bundle. |
| `run_validation.py` | Defines model parameters, analytical expectations, and sensitivity cases. |
| `run_numpy_validation.py` | Provides the NumPy sampler and simulation used by the chart script. |
| `pyproject.toml` | Declares Python and package requirements. |
| `uv.lock` | Locks dependency versions for reproduction. |
| `.gitignore` | Excludes generated outputs, environments, and caches. |
| `README.md` | Run instructions and expected results. |

## Run

Install Python 3.10 or later and [uv](https://docs.astral.sh/uv/getting-started/installation/). From the repository root:

```bash
cd simulation
uv sync --frozen
uv run --frozen python make_chart.py
```

The first run needs network access to install dependencies. Matplotlib uses a noninteractive backend and its bundled DejaVu Sans font, so no desktop session or extra fonts are required. Run the chart script directly; there is no need to execute either validation script first.

## Outputs

Results are written to `output/project_charts/en/`. Running again overwrites files with the same names.

- Five PNG and five SVG figures: cost composition, cost exceedance, individual sensitivities, B/C break-even, and event frequency versus severity.
- `project_figures_en.pdf`: all five figures in one PDF.
- CSV files: cost components, annual samples, sensitivity results, event severity, and the break-even grid.
- `methods_and_inputs.json`: parameters, seeds, software versions, and source hashes.
- `project_charts_bundle.zip`: figures, review data, and reproduction files under `scripts/`.

To run an extracted bundle, enter its `scripts/` folder and use the same `uv sync --frozen` and `uv run --frozen python make_chart.py` commands.

## Check the results

The model uses 20,000 simulated years per regime and seed `20261120 + ord(regime)`. Baseline results should round to the following values, in USD millions:

| Regime | Mean annual cost | P95 |
|---|---:|---:|
| A | 99.57 | 150.00 |
| B | 93.01 | 145.39 |
| C | 61.08 | 99.79 |

Figures 1, 4, and 5 use analytical expectations; figures 2 and 3 use simulated samples. The script checks simulated means against analytical means within 3% and checks the break-even grid against the model evaluator. Python and library versions are recorded in the manifest; image bytes can differ across platforms even when numerical results agree.

These are conditional scenario results, not observed BNY losses. Figure 4 compares mean costs only, not P95. Changing model parameters requires regenerating the figures.

Generated files belong in `output/`, which Git ignores. Commit the seven files listed above; existing charts, reports, PDFs, virtual environments, and cached data are not inputs to this simulation.
