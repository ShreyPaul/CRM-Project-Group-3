#!/usr/bin/env python3
"""Reproduce and audit Day 4 model assumptions with only the Python stdlib.

The PDF's PERT sampler applies the weighted mean twice. This version uses the
standard Beta-PERT alpha/beta shape parameters and preserves fixed values such
as Regime A's zero people/program costs. Sampling semantics otherwise follow
the PDF: uncertain annual attempt rate times success share is the Poisson
intensity, event losses are sampled independently, and off-channel enforcement
is a Bernoulli event with an uncertain annual probability.
"""

from __future__ import annotations

import csv
import math
import platform
import random
from copy import deepcopy
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
N = 20_000
SEED = 20261120
MILLION = 1_000_000.0

# Each triple is (minimum, mode, maximum). Monetary values are USD.
PARAMETERS = {
    "A": {
        "S1": ((10, 19, 29), (0.5, 0.7, 0.9), (2e5, 7.5e5, 3e6)),
        "S2": ((14, 29, 48), (0.6, 0.8, 0.95), (5e5, 2e6, 1e7)),
        "S3": ((1, 2.4, 4.8), (0.5, 0.7, 0.9), (1e6, 4e6, 2e7)),
        "people": (0, 0, 0),
        "program": (0, 0, 0),
        "oc": (0.02, 0.05, 0.08),
    },
    "B": {
        "S1": ((10, 19, 29), (0.05, 0.1, 0.2), (2e5, 7.5e5, 3e6)),
        "S2": ((24, 48, 96), (0.2, 0.35, 0.5), (5e5, 2e6, 1e7)),
        "S3": ((1.4, 3.8, 7.2), (0.1, 0.2, 0.3), (1e6, 4e6, 2e7)),
        "people": (1e7, 1.9e7, 3.8e7),
        "program": (2.5e6, 5e6, 7e6),
        "oc": (0.05, 0.10, 0.15),
    },
    "C": {
        "S1": ((10, 19, 29), (0.05, 0.1, 0.2), (2e5, 7.5e5, 3e6)),
        "S2": ((14, 34, 58), (0.3, 0.45, 0.6), (5e5, 2e6, 1e7)),
        "S3": ((1, 2.9, 5.8), (0.1, 0.2, 0.3), (1e6, 4e6, 2e7)),
        "people": (5e5, 2.4e6, 6.2e6),
        "program": (1.5e6, 3e6, 5e6),
        "oc": (0.01, 0.03, 0.05),
    },
}


def pert_mean(triple: tuple[float, float, float]) -> float:
    """Mean of the standard lambda=4 Beta-PERT distribution."""
    low, mode, high = triple
    return (low + 4 * mode + high) / 6


def sample_pert(
    rng: random.Random, triple: tuple[float, float, float]
) -> float:
    """Sample standard Beta-PERT; fixed triples return their fixed value."""
    low, mode, high = triple
    if low == high:
        return low
    if not low <= mode <= high:
        raise ValueError(f"PERT mode {mode} is outside [{low}, {high}]")
    alpha = 1 + 4 * (mode - low) / (high - low)
    beta = 1 + 4 * (high - mode) / (high - low)
    return low + (high - low) * rng.betavariate(alpha, beta)


def poisson(rng: random.Random, rate: float) -> int:
    """Knuth Poisson sampler; rates in this model are below 50."""
    if rate <= 0:
        return 0
    limit = math.exp(-rate)
    product = 1.0
    count = 0
    while product > limit:
        count += 1
        product *= rng.random()
    return count - 1


def simulate_regime(
    regime: str,
    parameters: dict,
    n: int = N,
    seed: int = SEED,
) -> list[float]:
    rng = random.Random(seed)
    results: list[float] = []
    for _ in range(n):
        total = sample_pert(rng, parameters["people"])
        total += sample_pert(rng, parameters["program"])

        enforcement_probability = sample_pert(rng, parameters["oc"])
        enforcement_fine = sample_pert(rng, (1e7, 4e7, 1e8))
        if rng.random() < enforcement_probability:
            total += enforcement_fine

        for scenario in ("S1", "S2", "S3"):
            attempt_rate, success_share, loss = parameters[scenario]
            event_rate = sample_pert(rng, attempt_rate) * sample_pert(
                rng, success_share
            )
            event_count = poisson(rng, event_rate)
            for _ in range(event_count):
                total += sample_pert(rng, loss)
        results.append(total)
    return results


def percentile(values: list[float], p: float) -> float:
    """Linear interpolation, matching NumPy's default percentile method."""
    ordered = sorted(values)
    position = (len(ordered) - 1) * p / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def analytic_expected_mean(parameters: dict) -> float:
    """Expected total under independent standard PERT input distributions."""
    total = pert_mean(parameters["people"]) + pert_mean(parameters["program"])
    total += pert_mean(parameters["oc"]) * pert_mean((1e7, 4e7, 1e8))
    for scenario in ("S1", "S2", "S3"):
        attempt_rate, success_share, loss = parameters[scenario]
        total += pert_mean(attempt_rate) * pert_mean(success_share) * pert_mean(loss)
    return total


def make_sensitivity_cases() -> dict[str, dict]:
    cases = {"Base": deepcopy(PARAMETERS)}

    no_uplift = deepcopy(PARAMETERS)
    for scenario in ("S2", "S3"):
        _, success, loss = no_uplift["B"][scenario]
        no_uplift["B"][scenario] = (
            PARAMETERS["A"][scenario][0], success, loss
        )
    cases["B S2/S3 attempts = A"] = no_uplift

    stronger_detection = deepcopy(PARAMETERS)
    s2 = stronger_detection["B"]["S2"]
    stronger_detection["B"]["S2"] = (
        s2[0],
        tuple(value / 2 for value in s2[1]),
        s2[2],
    )
    cases["B S2 success share halved"] = stronger_detection

    lower_people_cost = deepcopy(PARAMETERS)
    lower_people_cost["B"]["people"] = tuple(
        value / 2 for value in lower_people_cost["B"]["people"]
    )
    cases["B people cost halved"] = lower_people_cost
    return cases


def write_summary_csv(rows: list[dict]) -> None:
    path = OUTPUT_DIR / "summary.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_sensitivity_csv(rows: list[dict]) -> None:
    path = OUTPUT_DIR / "sensitivity.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_exceedance_svg(results: dict[str, list[float]]) -> None:
    width, height = 960, 600
    left, right, top, bottom = 90, 35, 45, 75
    plot_width = width - left - right
    plot_height = height - top - bottom
    max_data_millions = max(max(values) for values in results.values()) / MILLION
    max_millions = max(25, math.ceil(max_data_millions / 25) * 25)
    colors = {"A": "#b33a3a", "B": "#3567a5", "C": "#25815a"}
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="480" y="28" text-anchor="middle" font-size="20" font-family="sans-serif">Annual cost exceedance (20,000 simulations)</text>',
    ]
    for tick in range(0, 101, 20):
        y = top + plot_height * (1 - tick / 100)
        pieces.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#ddd"/>')
        pieces.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" font-size="12" font-family="sans-serif">{tick}%</text>')
    for tick in range(0, int(max_millions) + 1, 25):
        x = left + plot_width * tick / max_millions if max_millions else left
        pieces.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" stroke="#eee"/>')
        pieces.append(f'<text x="{x:.1f}" y="{height-bottom+22}" text-anchor="middle" font-size="12" font-family="sans-serif">${tick}M</text>')
    pieces.extend([
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#333"/>',
        f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#333"/>',
        f'<text x="{left + plot_width/2:.1f}" y="{height-20}" text-anchor="middle" font-size="14" font-family="sans-serif">Annual total cost (USD)</text>',
        f'<text x="22" y="{top + plot_height/2:.1f}" transform="rotate(-90 22 {top + plot_height/2:.1f})" text-anchor="middle" font-size="14" font-family="sans-serif">Probability of exceeding</text>',
    ])
    for name, values in results.items():
        ordered = sorted(values)
        points = []
        step = max(1, len(ordered) // 500)
        for index in range(0, len(ordered), step):
            x = left + plot_width * (ordered[index] / MILLION) / max_millions
            probability = 1 - index / len(ordered)
            y = top + plot_height * (1 - probability)
            points.append(f'{x:.1f},{y:.1f}')
        pieces.append(f'<polyline fill="none" stroke="{colors[name]}" stroke-width="2" points="{" ".join(points)}"/>')
    for index, name in enumerate(results):
        y = top + 20 + index * 24
        pieces.append(f'<line x1="{width-180}" y1="{y}" x2="{width-150}" y2="{y}" stroke="{colors[name]}" stroke-width="3"/>')
        pieces.append(f'<text x="{width-142}" y="{y+5}" font-size="13" font-family="sans-serif">Regime {name}</text>')
    pieces.append('</svg>')
    (OUTPUT_DIR / "exceedance.svg").write_text("\n".join(pieces), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Python {platform.python_version()} | n={N:,} | seed={SEED}")
    print("Base case: Monte Carlo mean / analytic mean / median / P95 (USD millions)")

    base_results: dict[str, list[float]] = {}
    base_summary: list[dict] = []
    for regime in ("A", "B", "C"):
        # Separate streams keep A/C samples identical across sensitivity cases.
        values = simulate_regime(regime, PARAMETERS[regime], seed=SEED + ord(regime))
        base_results[regime] = values
        row = {
            "regime": regime,
            "n": N,
            "seed": SEED + ord(regime),
            "mc_mean_usd": mean(values),
            "analytic_mean_usd": analytic_expected_mean(PARAMETERS[regime]),
            "median_usd": median(values),
            "p95_usd": percentile(values, 95),
        }
        base_summary.append(row)
        print(
            f'{regime}: ${row["mc_mean_usd"]/MILLION:.2f}M / '
            f'${row["analytic_mean_usd"]/MILLION:.2f}M / '
            f'${row["median_usd"]/MILLION:.2f}M / '
            f'${row["p95_usd"]/MILLION:.2f}M'
        )

    write_summary_csv(base_summary)
    write_exceedance_svg(base_results)

    sensitivity_rows: list[dict] = []
    print("\nSensitivity: mean rank and P95 rank (1 = lowest cost)")
    for case_name, case_parameters in make_sensitivity_cases().items():
        case_means = {}
        case_p95s = {}
        for regime in ("A", "B", "C"):
            values = simulate_regime(
                regime,
                case_parameters[regime],
                seed=SEED + ord(regime),
            )
            case_means[regime] = mean(values)
            case_p95s[regime] = percentile(values, 95)
        mean_ranks = {
            name: rank + 1
            for rank, (name, _) in enumerate(sorted(case_means.items(), key=lambda item: item[1]))
        }
        p95_ranks = {
            name: rank + 1
            for rank, (name, _) in enumerate(sorted(case_p95s.items(), key=lambda item: item[1]))
        }
        row = {"case": case_name}
        for regime in ("A", "B", "C"):
            row[f"{regime}_mean_usd"] = case_means[regime]
            row[f"{regime}_p95_usd"] = case_p95s[regime]
            row[f"{regime}_mean_rank"] = mean_ranks[regime]
            row[f"{regime}_p95_rank"] = p95_ranks[regime]
        sensitivity_rows.append(row)
        print(
            f'{case_name}: mean {" < ".join(sorted(case_means, key=case_means.get))}; '
            f'P95 {" < ".join(sorted(case_p95s, key=case_p95s.get))}'
        )
    write_sensitivity_csv(sensitivity_rows)
    print(f"\nWrote results to {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
