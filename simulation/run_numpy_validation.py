#!/usr/bin/env python3
"""Run the Day 4 model with NumPy/Matplotlib and compare both PERT formulas."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import numpy as np

from run_validation import (
    MILLION,
    N,
    PARAMETERS,
    SEED,
    analytic_expected_mean,
    make_sensitivity_cases,
)


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(OUTPUT_DIR / ".matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PDF_PARAMETERS = {name: dict(values) for name, values in PARAMETERS.items()}
PDF_PARAMETERS["A"]["people"] = (0, 0, 1)
PDF_PARAMETERS["A"]["program"] = (0, 0, 1)


def pert_pdf_original(lo: float, mode: float, hi: float, n):
    """Original PERT formula, extended to handle fixed-value inputs."""
    if lo == hi:
        return np.full(n, lo, dtype=float)
    mu = (lo + 4 * mode + hi) / 6
    alpha = 1 + 4 * (mu - lo) / (hi - lo)
    beta = 1 + 4 * (hi - mu) / (hi - lo)
    return lo + (hi - lo) * np.random.beta(alpha, beta, n)


def pert_standard(lo: float, mode: float, hi: float, n):
    """Standard lambda=4 Beta-PERT sampler, including fixed values."""
    if lo == hi:
        return np.full(n, lo, dtype=float)
    alpha = 1 + 4 * (mode - lo) / (hi - lo)
    beta = 1 + 4 * (hi - mode) / (hi - lo)
    return lo + (hi - lo) * np.random.beta(alpha, beta, n)


def original_formula_mean(triple: tuple[float, float, float]) -> float:
    lo, mode, hi = triple
    if lo == hi:
        return lo
    mu = (lo + 4 * mode + hi) / 6
    alpha = 1 + 4 * (mu - lo) / (hi - lo)
    beta = 1 + 4 * (hi - mu) / (hi - lo)
    return lo + (hi - lo) * alpha / (alpha + beta)


def expected_mean_original(parameters: dict) -> float:
    expected = original_formula_mean(parameters["people"])
    expected += original_formula_mean(parameters["program"])
    expected += original_formula_mean(parameters["oc"]) * original_formula_mean(
        (1e7, 4e7, 1e8)
    )
    for scenario in ("S1", "S2", "S3"):
        attempts, success, loss = parameters[scenario]
        expected += (
            original_formula_mean(attempts)
            * original_formula_mean(success)
            * original_formula_mean(loss)
        )
    return expected


def run_regime(regime: str, parameters: dict, sampler) -> np.ndarray:
    total = sampler(*parameters["people"], n=N) + sampler(
        *parameters["program"], n=N
    )
    total += (np.random.rand(N) < sampler(*parameters["oc"], n=N)) * sampler(
        1e7, 4e7, 1e8, n=N
    )
    for scenario in ("S1", "S2", "S3"):
        attempts, success, loss = parameters[scenario]
        counts = np.random.poisson(
            sampler(*attempts, n=N) * sampler(*success, n=N)
        )
        max_count = max(1, int(counts.max()))
        total += (
            sampler(*loss, n=(N, max_count))
            * (np.arange(max_count) < counts[:, None])
        ).sum(axis=1)
    return total


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_base_comparison() -> tuple[list[dict], dict[str, dict[str, np.ndarray]]]:
    methods = {
        "Initial PERT formula": (pert_pdf_original, PDF_PARAMETERS, expected_mean_original),
        "Corrected Beta-PERT": (
            pert_standard,
            PARAMETERS,
            analytic_expected_mean,
        ),
    }
    output: dict[str, dict[str, np.ndarray]] = {}
    rows: list[dict] = []
    for method, (sampler, parameters, expected_fn) in methods.items():
        output[method] = {}
        for regime in ("A", "B", "C"):
            np.random.seed(SEED + ord(regime))
            values = run_regime(regime, parameters[regime], sampler)
            expected = expected_fn(parameters[regime])
            row = {
                "method": method,
                "regime": regime,
                "n": N,
                "seed": SEED + ord(regime),
                "mc_mean_usd": float(values.mean()),
                "analytic_mean_usd": float(expected),
                "relative_mean_error": float(abs(values.mean() - expected) / expected),
                "median_usd": float(np.median(values)),
                "p95_usd": float(np.percentile(values, 95)),
            }
            rows.append(row)
            output[method][regime] = values
            print(
                f'{method} {regime}: mean ${row["mc_mean_usd"]/MILLION:.2f}M; '
                f'analytic ${expected/MILLION:.2f}M; '
                f'median ${row["median_usd"]/MILLION:.2f}M; '
                f'P95 ${row["p95_usd"]/MILLION:.2f}M'
            )
            if row["relative_mean_error"] > 0.03:
                raise AssertionError(
                    f"{method} {regime} Monte Carlo mean differs from its "
                    f"analytical expectation by more than 3%"
                )
    write_csv(OUTPUT_DIR / "numpy_formula_comparison.csv", rows)
    return rows, output


def make_comparison_chart(output: dict[str, dict[str, np.ndarray]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
    colors = {"A": "#b33a3a", "B": "#3567a5", "C": "#25815a"}
    for axis, method in zip(axes, output):
        for regime, values in output[method].items():
            ordered = np.sort(values)
            axis.plot(
                ordered / MILLION,
                1 - np.arange(N) / N,
                label=f"Regime {regime}",
                color=colors[regime],
            )
        axis.set_title(method)
        axis.set_xlabel("Annual total cost (USD millions)")
        axis.grid(True, alpha=0.25)
        axis.legend()
    axes[0].set_ylabel("Probability of exceeding")
    fig.suptitle("Initial PERT implementation vs corrected Beta-PERT")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "numpy_pert_comparison.png", dpi=160)
    fig.savefig(OUTPUT_DIR / "numpy_pert_comparison.svg")
    plt.close(fig)


def run_sensitivities() -> list[dict]:
    rows: list[dict] = []
    for case_name, case_parameters in make_sensitivity_cases().items():
        values_by_regime = {}
        for regime in ("A", "B", "C"):
            np.random.seed(SEED + ord(regime))
            values_by_regime[regime] = run_regime(
                regime, case_parameters[regime], pert_standard
            )
        means = {name: float(values.mean()) for name, values in values_by_regime.items()}
        p95s = {
            name: float(np.percentile(values, 95))
            for name, values in values_by_regime.items()
        }
        mean_order = sorted(means, key=means.get)
        p95_order = sorted(p95s, key=p95s.get)
        row = {"case": case_name, "mean_order": " < ".join(mean_order), "p95_order": " < ".join(p95_order)}
        for regime in ("A", "B", "C"):
            row[f"{regime}_mean_usd"] = means[regime]
            row[f"{regime}_p95_usd"] = p95s[regime]
            row[f"{regime}_mean_rank"] = mean_order.index(regime) + 1
            row[f"{regime}_p95_rank"] = p95_order.index(regime) + 1
        rows.append(row)
        print(f'{case_name}: mean {row["mean_order"]}; P95 {row["p95_order"]}')
    write_csv(OUTPUT_DIR / "numpy_sensitivity.csv", rows)
    return rows


def main() -> None:
    print(
        f"NumPy {np.__version__} | Matplotlib {matplotlib.__version__} | "
        f"n={N:,} | seed base={SEED}"
    )
    print("Base case: Monte Carlo mean, analytical mean, median, P95 (USD millions)")
    _, output = run_base_comparison()
    make_comparison_chart(output)
    print("\nSensitivity runs using corrected Beta-PERT:")
    run_sensitivities()
    print(f"\nWrote NumPy results and charts under {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
