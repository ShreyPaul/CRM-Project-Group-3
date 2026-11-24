# Monitoring Trade-off Explorer

An English SPA for exploring how insider-threat protection, employee responses, and program spending change the expected first-year cost of three monitoring strategies. Uses the indigo and pink palette in [SPEC.md](SPEC.md).

## Run locally

Requires Node.js 22 or later and npm. From the repository root:

```sh
cd web
npm ci
npm run dev
```

Open the local URL printed by Vite, normally http://localhost:5173. Calculations run in the browser; no backend, API keys, or database are needed.

```sh
npm run build
npm run preview
```

The production build is written to `dist/`. Its relative asset paths support serving it from a subdirectory on a static host.

## Try the model

1. Start with the project baseline. The expected costs are A **$99.61M**, B **$86.97M**, and C **$69.31M**.
2. Try **No additional attack attempts in B**. B falls to **$61.14M**.
3. Try **Stronger email/cloud protection in B**. Each preset starts from baseline; B falls to **$58.91M**.
4. Reset, select B or C, and change protection, attempts, or additional departures independently.
5. Expand **Advanced inputs** to edit attack, program, and enforcement triples, plus departure counts and replacement-cost assumptions. Invalid values retain the last valid results until corrected and applied.

Scenario tabs change the editing scope, not the all-scenario total. The employee cost is counted once per strategy.

## Model and source of inputs

`src/model.ts` calculates analytical expectations with the same independent Beta-PERT structure as Python:

```text
PERT mean = (minimum + 4 × mode + maximum) / 6
Expected successful events = mean(attempts) × mean(success probability)
Expected incident loss = expected events × mean(loss per event)
Expected total = incident losses + employee replacement + program + expected penalty
```

The SPA implements the analytical MVP in the current specification. It displays expected costs, not Monte Carlo distributions or P95. Published sources supply scenario context; the input ranges remain project assumptions. Input provenance and limitations are recorded in the simulation's evidence documents.

`src/baseline.json` is generated from `simulation/run_validation.py`, with turnover constants from `simulation/turnover_sensitivity.py`. To pick up changes to Python parameters:

```sh
npm run baseline
npm test
npm run build
```

Commit the regenerated JSON alongside the Python changes. The generation script requires Python 3 with the standard library; it does not import NumPy or plotting libraries. The generator initializes departure counts from Python’s baseline employee costs and the original unit costs once. The browser then stores departures explicitly: changing replacement rates or unit costs automatically recalculates all regimes’ employee costs without changing departure counts. There is no manual total-cost override.

## Verification

```sh
npm test
npm run build
```

Model tests cover parity with Python, sensitivity totals, turnover calculations, stable slider scaling, isolated updates, and validation.

For browser checks, install Chromium once, start the dev server, and run:

```sh
npx playwright install chromium
npm run test:browser
```

Set `APP_URL` to test a different running server. Browser checks exercise desktop/mobile interactions, presets, reset, keyboard control, advanced validation and Apply, and horizontal overflow. Screenshots are saved under ignored `test-results/`.

Before presenting, have a person unfamiliar with the model try it for three minutes and explain which assumption changed the ranking. This audience comprehension check requires human review.

## Files

| File | Purpose |
|---|---|
| `src/model.ts` | Input types, calculations, validation, and scenarios |
| `src/main.tsx` | Controls, result cards, accessible SVG chart, and advanced editor |
| `src/styles.css` | Palette, layout, responsive and focus states |
| `src/baseline.json` | Generated, versioned Python baseline |
| `scripts/generate_baseline.py` | Refreshes baseline and source hashes |
| `tests/model.test.ts` | Numerical and input-invariant tests |
| `tests/browser.mjs` | Real-browser interaction checks |

Generated builds, installed packages, and browser artifacts are ignored by Git. Python source files and the original specifications are preserved.
