#!/usr/bin/env python3
"""Illustrative first-year turnover cost sensitivity, relative to regime C."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from run_validation import PARAMETERS, analytic_expected_mean, pert_mean

WORKFORCE = 48_100
INTENTION_GAPS = (0, 0.073, 0.19)
CONVERSIONS = (0.10, 0.25, 0.50)
REPLACEMENT_RATE = 0.80
HIRING_COST = 15_000
NET_VACANCY_COST = 3_000
ANNUAL_PAY_DIFFERENCE = 5_000
FIRST_YEAR_FRACTION = 0.50


def incremental_cost(gap, conversion):
    departures = WORKFORCE * gap * conversion
    hires = departures * REPLACEMENT_RATE
    return departures, hires, hires * (HIRING_COST + NET_VACANCY_COST + ANNUAL_PAY_DIFFERENCE * FIRST_YEAR_FRACTION)


def generate(out=None, pdf=None):
    out = out or Path(__file__).resolve().parent / "output" / "turnover_sensitivity"
    out.mkdir(parents=True, exist_ok=True)
    base_b = analytic_expected_mean(PARAMETERS['B'])
    base_c = analytic_expected_mean(PARAMETERS['C'])
    # Replace B's baseline turnover cost; C stays at its own baseline.
    baseline_b_people = pert_mean(PARAMETERS['B']['people'])
    rows = []
    for gap in INTENTION_GAPS:
        for conversion in CONVERSIONS:
            departures, hires, cost = incremental_cost(gap, conversion)
            rows.append(dict(intention_gap=gap, conversion=conversion, incremental_departures=departures, replacement_hires=hires, incremental_turnover_cost_usd=cost, b_mean_usd=base_b-baseline_b_people+cost, c_mean_usd=base_c))
    with (out / 'turnover_scenarios.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(INTENTION_GAPS)); width = .24
    for i, conversion in enumerate(CONVERSIONS):
        values = [r['b_mean_usd']/1e6 for r in rows if r['conversion'] == conversion]
        bars = ax.bar(x+(i-1)*width, values, width, label=f'{conversion:.0%} conversion')
        ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=9)
    ax.axhline(base_c/1e6, color='#218574', linestyle='--', label=f'C baseline: ${base_c/1e6:.1f}M')
    ax.set(xticks=x, xticklabels=['0', '7.3', '19'], xlabel='Illustrative intention gap (percentage points)', ylabel='Expected first-year cost (USD millions)', title='Turnover assumptions and regime B cost')
    ax.legend(ncol=2, frameon=False); ax.set_ylim(0, max(r['b_mean_usd'] for r in rows)/1e6*1.20)
    fig.text(.1, .01, 'Illustrative B vs A assumptions; C remains at its 5.5-point baseline.', fontsize=9)
    fig.tight_layout(rect=(0,.04,1,1)); fig.savefig(out/'turnover_sensitivity.png', dpi=180); fig.savefig(out/'turnover_sensitivity.svg')
    if pdf is not None:
        pdf.savefig(fig)
    plt.close(fig)
    print(f'Wrote {out}')


if __name__ == '__main__':
    generate()
