#!/usr/bin/env python3
"""Self-contained report figures for the ATT&CK coverage map. No input files.

Outputs (PNG 300 dpi, SVG, PDF) into --outdir:
  fig_coverage         stripe matrix, A|B|C bar per technique   (report body)
  fig_regime_A/B/C     solid-fill matrix per regime             (layer plates / appendix)
  fig_scenario_S1/S2/S3 stripe matrix filtered to one scenario  (scenario cards)
The TECHS table is the source of truth: if you recolour anything in Navigator,
edit the matching row here and re-run.
"""
import argparse, pathlib, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

REGIMES = ["A", "B", "C"]
PAL = {"blocked": "#2E7D32", "detected": "#F2C200", "invisible": "#C62828"}
LBL = {"blocked": "Blocked", "detected": "Detected, not blocked", "invisible": "Invisible"}
FG = lambda b: "#FFFFFF" if b in ("blocked", "invisible") else "#212121"

# Updated tactic list and labels to reflect ATT&CK v20 Defense Impairment split
TLABEL = {"initial-access": "Initial Access", "persistence": "Persistence",
          "stealth": "Stealth", "defense-impairment": "Defense Impairment",
          "collection": "Collection", "exfiltration": "Exfiltration", "impact": "Impact"}
TCOLS = ["initial-access", "persistence", "stealth", "defense-impairment",
         "collection", "exfiltration", "impact"]

PAD, TITLE_H, HEAD_H, REG_H, GAP, LEG_H = .16, .34, .30, .26, .06, .52

# tid, name, tactic, scenarios, (A, B, C)
TECHS = [
    ("T1078",     "Valid Accounts",                         "initial-access", "S1 S2 S3", ("invisible", "detected", "detected")),
    ("T1078.002", "Domain Accounts",                        "initial-access", "S3",       ("invisible", "detected", "detected")),
    ("T1098",     "Account Manipulation",                   "persistence",    "S3",       ("invisible", "detected", "detected")),
    ("T1685",     "Disable or Modify Tools",                "defense-impairment", "S3",   ("invisible", "detected", "detected")),
    ("T1213",     "Data from Information Repositories",     "collection",     "S1 S2",    ("invisible", "detected", "detected")),
    ("T1074",     "Data Staged",                            "collection",     "S1 S2",    ("invisible", "detected", "detected")),
    ("T1560",     "Archive Collected Data",                 "collection",     "S1 S2",    ("invisible", "detected", "detected")),
    ("T1005",     "Data from Local System",                 "collection",     "S1 S2",    ("invisible", "invisible", "detected")),
    ("T1114",     "Email Collection",                       "collection",     "S2",       ("invisible", "detected", "invisible")),
    ("T1052.001", "Exfiltration Over USB",                  "exfiltration",   "S1",       ("invisible", "blocked",  "blocked")),
    ("T1567",     "Exfiltration Over Web Service",          "exfiltration",   "S2",       ("invisible", "detected", "invisible")),
    ("T1567.002", "Exfiltration to Cloud Storage",          "exfiltration",   "S2",       ("invisible", "detected", "detected")),
    ("T1567.003", "Exfiltration to Text Storage Sites",     "exfiltration",   "S2",       ("invisible", "detected", "invisible")),
    ("T1048",     "Exfiltration Over Alternative Protocol", "exfiltration",   "S2",       ("invisible", "detected", "detected")),
    ("T1029",     "Scheduled Transfer",                     "exfiltration",   "S2",       ("invisible", "detected", "invisible")),
    ("T1485",     "Data Destruction",                       "impact",         "S3",       ("invisible", "detected", "detected")),
]

SDESC = {"S1": "data theft via USB",
         "S2": "data theft via personal email, cloud and messaging",
         "S3": "disgruntled-admin sabotage"}
CHAINS = {
    "S1": ("T1078 → T1213 → T1074 → T1560 → T1052.001",
           ["T1078", "T1213", "T1074", "T1560", "T1052.001"]),
    "S2": ("T1078 → T1213 / T1005 → T1074 → T1560 → T1114 → T1567.002 "
           "(alternate channels: T1567, T1567.003, T1048, T1029)",
           ["T1078", "T1213", "T1005", "T1074", "T1560", "T1114",
            "T1567", "T1567.002", "T1567.003", "T1048", "T1029"]),
    "S3": ("T1078.002 → T1685 → T1485, with T1098 for persistence",
           ["T1078", "T1078.002", "T1098", "T1685", "T1485"]),
}

NAME = {t[0]: t[1] for t in TECHS}
COLS = {t[0]: t[4] for t in TECHS}
SCEN = {t[0]: t[3] for t in TECHS}

def canvas(width, H):
    fig = plt.figure(figsize=(width, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width); ax.set_ylim(0, H); ax.axis("off")
    return fig, ax

def tile_solid(ax, x, y, w, h, tid, b, fs, wrap):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=PAL[b], edgecolor="#9AA5B1", lw=.6, zorder=2))
    ax.text(x + .05, y + h - .05, tid, fontsize=fs - 1, va="top", color=FG(b), alpha=.85, zorder=3)
    ax.text(x + w - .05, y + h - .05, SCEN[tid].replace(" ", "·"), fontsize=fs - 1.4,
            va="top", ha="right", color=FG(b), alpha=.7, zorder=3)
    ax.text(x + w / 2, y + (h - .16) / 2, "\n".join(textwrap.wrap(NAME[tid], wrap)),
            fontsize=fs, ha="center", va="center", color=FG(b), linespacing=1.15, zorder=3)

def tile_stripe(ax, x, y, w, h, tid, fs, wrap, text_h, bar_h):
    ax.add_patch(Rectangle((x, y), w, h, facecolor="#FFFFFF", edgecolor="#9AA5B1", lw=.6, zorder=2))
    ax.text(x + .05, y + h - .05, tid, fontsize=fs - 1, va="top", color="#52606D", zorder=3)
    ax.text(x + w - .05, y + h - .05, SCEN[tid].replace(" ", "·"), fontsize=fs - 1.4,
            va="top", ha="right", color="#9AA5B1", zorder=3)
    ax.text(x + w / 2, y + bar_h + (text_h - .14) / 2, "\n".join(textwrap.wrap(NAME[tid], wrap)),
            fontsize=fs, ha="center", va="center", color="#1F2933", linespacing=1.15, zorder=3)
    sw = w / len(REGIMES)
    for i, (lab, b) in enumerate(zip(REGIMES, COLS[tid])):
        ax.add_patch(Rectangle((x + i * sw, y), sw, bar_h, facecolor=PAL[b],
                               edgecolor="#FFFFFF", lw=.6, zorder=3))
        ax.text(x + i * sw + sw / 2, y + bar_h / 2, lab, fontsize=fs - 1.2, weight="bold",
                ha="center", va="center", color=FG(b), zorder=4)

def build(mode, width, tile_h, outdir, regime=None, scen=None):
    techs = TECHS
    if scen:
        techs = [T for tid in CHAINS[scen][1] for T in TECHS if T[0] == tid]
    st = {c: [t[0] for t in techs if t[2] == c] for c in TCOLS}
    cols = [c for c in TCOLS if st[c]]
    cw = (width - 2 * PAD) / len(cols)
    fs = max(5.0, min(7.6, cw * 6.2))
    wrap = max(10, int((cw - .16) / (fs * .5 / 72)))
    bar_h = .20 if mode == "stripe" else 0.0
    th = tile_h + bar_h
    body = max(len(st[c]) for c in cols) * (th + GAP)
    H = PAD + TITLE_H + REG_H + HEAD_H + body + LEG_H + PAD
    fig, ax = canvas(width, H)
    if scen:
        title = f"Scenario {scen} — {SDESC[scen]}: regime comparison"
    elif mode == "stripe":
        title = f"ATT&CK coverage of the {len(TECHS)} in-scope techniques by monitoring regime"
    else:
        title = f"Regime {regime} — ATT&CK coverage, {len(TECHS)} in-scope techniques"
    ax.text(PAD, H - PAD, title, fontsize=9.5, weight="bold", va="top", color="#1F2933")
    top = H - PAD - TITLE_H
    ax.text(PAD, top - .02,
            "Colour bar under each technique: regimes A | B | C" if mode == "stripe"
            else "Green blocked, amber detected not blocked, red invisible",
            fontsize=8, va="top", color="#52606D")
    if scen:
        ax.text(PAD, top - .14, "Chain: " + CHAINS[scen][0],
                fontsize=7, va="top", color="#7B8794")
    hy = top - REG_H
    for ci, c in enumerate(cols):
        x = PAD + ci * cw
        ax.add_patch(Rectangle((x + .02, hy - HEAD_H + .06), cw - .04, HEAD_H - .06,
                               facecolor="#F5F7F8", edgecolor="none"))
        ax.text(x + cw / 2, hy - HEAD_H / 2 + .02, TLABEL[c], ha="center", va="center",
                fontsize=fs + .4, weight="bold", color="#3E4C59")
        ax.plot([x + .02, x + cw - .02], [hy - HEAD_H + .04] * 2, color="#9AA5B1", lw=.7)
    base = hy - HEAD_H - GAP
    for ci, c in enumerate(cols):
        ypos = {}
        for ri, tid in enumerate(st[c]):
            x, w = PAD + ci * cw + .03, cw - .06
            y = base - (ri + 1) * th - ri * GAP
            ind = 0.0
            par = tid.split(".")[0]
            if "." in tid and par in ypos:
                ind = .12
                ax.plot([x + .05] * 2, [ypos[par], y + th / 2], color="#B0BEC5", lw=.6, zorder=1)
                ax.plot([x + .05, x + ind], [y + th / 2] * 2, color="#B0BEC5", lw=.6, zorder=1)
            ypos[tid] = y
            if mode == "stripe":
                tile_stripe(ax, x, y, w, th, tid, fs, wrap, tile_h, bar_h)
            else:
                tile_solid(ax, x, y, w, th, tid, COLS[tid][REGIMES.index(regime)], fs, wrap)
    lx, ly = PAD, PAD + .30
    for k in ("blocked", "detected", "invisible"):
        ax.add_patch(Rectangle((lx, ly), .16, .12, facecolor=PAL[k], edgecolor="#9AA5B1", lw=.5))
        ax.text(lx + .22, ly + .06, LBL[k], fontsize=7, va="center", color="#3E4C59")
        lx += .30 + len(LBL[k]) * .05
    ax.text(PAD, PAD + .24, textwrap.fill(
        "Source: authors' mapping, ATT&CK v20; each technique shown under its principal tactic. "
        "Only the in-scope techniques are shown.", 150),
        fontsize=6, color="#7B8794", va="top")
    name = (f"fig_scenario_{scen}" if scen else
            "fig_coverage" if mode == "stripe" else f"fig_regime_{regime}")
    for ext in ("png", "svg", "pdf"):
        fig.savefig(f"{outdir}/{name}.{ext}", dpi=300, facecolor="white")
    plt.close(fig)
    print(f"wrote {outdir}/{name}.png/.svg/.pdf  ({width:.1f} x {H:.1f} in)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="report/figs")
    ap.add_argument("--width", type=float, default=6.8)
    ap.add_argument("--tile-h", type=float, default=0.52)
    a = ap.parse_args()
    pathlib.Path(a.outdir).mkdir(parents=True, exist_ok=True)
    ab = {"invisible": "inv", "detected": "det", "blocked": "blk"}
    print(f"{'ID':10} {'scenarios':9} A   B   C")
    for tid, _, _, scen, cols in TECHS:
        print(f"{tid:10} {scen:9} " + "  ".join(ab[c] for c in cols))
    build("stripe", a.width, a.tile_h, a.outdir)
    for r in REGIMES:
        build("solid", a.width, a.tile_h, a.outdir, regime=r)
    for s in ("S1", "S2", "S3"):
        build("stripe", a.width, a.tile_h, a.outdir, scen=s)
