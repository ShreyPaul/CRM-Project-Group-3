# Monitoring Trade-off Explorer — SPA Specification

Status: MVP specification, 24 November 2026.

## 1. Purpose

Help an audience discover, within three minutes, when the security benefits of monitoring outweigh its program and employee costs.

Core question: **“When is more monitoring worth the cost?”**

Users must be able to obtain outcomes favoring either B or C. Protection effectiveness, behavioral responses, and employee impacts are independent controls. Do not automatically make stronger monitoring increase dissatisfaction, departures, or attack attempts. Describe the result as **“Lowest modeled cost”**, rather than the best or safest strategy.

BNY supplies the workforce and cost context. The experience does not require role-playing or a company introduction page.

## 2. MVP Scope

- A single page, without login, suitable for static hosting; calculations run locally in the browser.
- Compare A, B, and C across S1 USB theft, S2 email/cloud exfiltration, and S3 administrator sabotage.
- Main controls: protection effectiveness, additional attack attempts, and additional employee departures.
- Immediate analytical expectations, cost composition, incident counts, rankings, and explanations of changes.
- Advanced editing of minimum/mode/maximum inputs, program costs, and enforcement inputs.
- Presets, reset, and export of settings and results.
- Monte Carlo simulation, P95, exceedance curves, multi-user voting, and production deployment are outside the MVP.

Primary results label: **“Expected first-year cost · USD millions”**.

## 3. Baseline and Regime Names

Initialize from `PARAMETERS` in `../simulation/run_validation.py`, recording its source version or hash. Use `../simulation/turnover_sensitivity.py` for the employee replacement calculation.

The current code retains A's original USB success triple of 0.50/0.70/0.90 and zero program cost. Use these labels:

| Regime | Label | Short explanation |
|---|---|---|
| A | Reference baseline | Current project baseline |
| B | Extensive monitoring | Broader monitoring coverage |
| C | Privacy-preserving monitoring | Monitoring with privacy safeguards |

Do not label the existing A baseline as having the same USB protection as B/C. Equal USB protection is a separate experiment described in Section 8.

Persistent context: **“Classroom scenario model. Results reflect your assumptions.”**

## 4. Layout

On desktop, allocate approximately 40% of the width to controls and 60% to persistently visible results. On mobile, show the question and a compact total-cost summary first, followed by controls and detailed charts. Avoid large fixed panels covering content.

```text
When is more monitoring worth the cost?       [Reset] [Export]
Change one assumption and see the trade-off.

[All scenarios] [USB] [Email / cloud] [Admin sabotage]

Controls                              Live comparison
Edit regime: [B] [C]                  A $…  B $…  C $…
                                      Lowest modeled cost: …
1. Protection effectiveness           Stacked cost bars
2. Additional attack attempts         [All costs] [Incident losses only]
3. Additional employee departures
                                      What changed?
[Try a scenario…]                     One sentence + cost difference
[Advanced inputs ▾]                   [See the calculation ▾]
```

Scenario tabs change the visible controls and incident details. Total cards always include all scenarios and display **“All-scenario total”**. Switching tabs must not remove hidden scenarios from calculations.

## 5. Main Controls

### 5.1 Protection Effectiveness

Label: **“Successful attacks remaining”**

Helper: **“Lower values mean fewer attempts cause a loss.”**

- Select B or C; default to B and S2 in simple mode.
- Scale the success triple from 0–200%, initially 100%. Restrict the available upper bound so the maximum probability cannot exceed 1.
- Display **“100% = project baseline”** beside the multiplier. After advanced edits, use **“100% = your applied inputs”** where applicable.
- Display the actual mean probability more prominently: for baseline B S2, **“35 out of 100 attempts succeed.”**
- Show `Expected attempts → Expected successful incidents → Expected incident loss`.
- Provide `Baseline`, `25% fewer successes`, and `50% fewer successes` shortcuts.
- This control does not automatically change employee costs or attempt rates.

Even on the All scenarios tab, identify the control's scope, such as **“Editing B · Email / cloud”**. Avoid an ambiguous global success slider.

### 5.2 Behavioral Response

Label: **“Additional attack attempts”**

Helper: **“Explore whether monitoring leads to more attempts through other channels.”**

- Scale B's or C's S2/S3 attempt uplift relative to A.
- Range: 0–200%. At 100%, retain the original uplift; at 0%, match A's attempt triple.
- Display actual expected counts alongside the multiplier, such as **“29.7 → 50.0 attempts/year.”**
- In All scenarios, provide **“Apply to email/cloud and admin sabotage”**, checked by default. A single-scenario tab changes only that scenario.
- S1 has no baseline uplift. Show **“USB attempts are equal across regimes in this baseline.”** instead of an ineffective slider.
- Treat additional attempts as an exploratory assumption. Do not describe them as a demonstrated effect of monitoring.

### 5.3 Employee Impact

Label: **“Additional employees who leave”**

Helper: **“Extra departures relative to A during the first year.”**

- Direct departure control: 0–5,000, step 1, paired with a numeric input.
- Initially show approximately 878 for B and 661 for C. Preserve the exact underlying values of 877.825 and 661.375 until edited.
- Display `Extra departures × 80% replaced × $20,500 per replacement = cost`.
- Use four small readouts: departures, replacement rate, replacement hires, and cost.
- Offer **“Same replacement cost as C”** when editing B, plus **“No additional departures.”** Equality uses C's current cost.
- Expand **“Where does this estimate come from?”** to show workforce × intention gap × conversion: baseline gaps of 7.3 percentage points for B and 5.5 for C, with 25% conversion.
- A direct edit becomes a **“Custom departure assumption”**; it does not imply an observed change in intention or conversion.
- Employee cost is charged once per regime, across all scenarios.

## 6. Intuitive Results

### Cost Cards

Show each regime's total and change from the immutable project baseline. Mark the lowest cost with a label and border. Regime identity colors remain fixed as rankings change. If totals differ by less than $0.01M, show **“Approximately tied.”**

### Stacked Cost Bars

Use three horizontal bars with segments for S1, S2, S3, employee replacement, program, and expected enforcement penalty. Mouse, touch, and keyboard users can reveal labels and exact amounts. Include an expandable data table.

**“Incident losses only”** changes the chart view, while total-cost cards remain visible and explicitly labeled. Rankings continue to use total costs.

### Dynamic Explanation

Generate a concise, numerical explanation after each change, for example:

- “B's expected email/cloud loss fell by $14.03M. Its total is now $3.63M above C.”
- “Equal replacement costs reduce the B–C gap, but C still has the lower modeled total.”

Compute the text from actual results. After multiple edits, identify the largest component of the current difference instead of attributing the entire difference to the last slider. Regime comparisons use current values; baseline deltas explicitly refer to the project baseline.

### Calculation Disclosure

An expandable view connects ATT&CK scenarios → FAIR factors → expected incident losses → total strategy costs. Pair technical terms with plain-language labels. Say **“Attack success probability”**, avoiding a bare “success” label that could mean defensive success.

## 7. Three-Minute Experience

1. Show full baseline costs and ask **“Which assumption would you challenge?”**
2. Try **“No additional attack attempts in B”** and observe a potential ranking change.
3. Reset and try **“Same replacement cost for B and C.”**
4. Adjust S2 effectiveness to find where B and C approach equal cost.
5. Explain the choice using **“What changed?”**, then export the settings if desired.

All steps are optional. There is no forced tour or correct/incorrect answer.

## 8. Presets and Equal USB Protection

Each standard preset reloads the project baseline before applying its change. Show **“Loads baseline + this change”** so repeated clicks do not silently accumulate adjustments.

| Preset | Exact change |
|---|---|
| Project baseline | Restore all versioned baseline values |
| No additional attack attempts in B | B S2/S3 attempt triples = A |
| Stronger email/cloud protection in B | B S2 success triple × 0.5 |
| Same replacement cost for B and C | B employee cost = C employee cost |

The advanced USB experiment is labeled **“Give A the same USB blocking as B/C.”**

- Set A S1 success to the original shared B/C triple: 0.05/0.10/0.20.
- Require an explicit entry for **“Annual basic-control cost already included in B and C.”** Zero is allowed when deliberately entered.
- Set A's program triple to this fixed cost. B/C retain their totals, which already include the common control cost.
- The common cost must not exceed either B/C program minimum. Otherwise, ask the user to establish consistent program costs in advanced inputs first.
- Identify the entered cost as an assumption; do not invent a sourced default.
- Change only the designated A fields; switching off restores their pre-experiment values.
- If advanced edits have made B/C USB controls unequal, disable the experiment until a shared USB assumption is restored; the label must match the actual comparison.

## 9. Calculation Contract

For a triple `(a, m, b)`, the Beta-PERT mean is `(a + 4m + b) / 6`.

For each regime and scenario:

- Expected successful events = mean(attempts) × mean(success share).
- Expected incident loss = expected events × mean(loss).
- Expected fine = mean(enforcement probability) × mean(penalty).
- Expected total = sum of scenario losses + employee replacement + mean(program) + expected fine.

For behavioral multiplier `k`, calculate each triple position as `A + k × (selected regime anchor − A)`. Apply multipliers to a stable anchor, never cumulatively to the previous slider result. Initially the anchor is the project baseline; after Apply in advanced inputs, it is the newly committed input set. At `k = 0`, the triple must equal the corresponding A anchor. Disable the shortcut with a specific explanation if edited inputs no longer represent a valid nonnegative uplift or produce an invalid triple.

Employee replacement cost = departures × replacement rate × (hiring cost + net vacancy cost + annual pay difference × first-year fraction).

Initial cost assumptions: 80%, $15,000, $3,000, $5,000, and 50%, respectively. A's employee cost is zero because the calculation represents incremental costs relative to A.

Keep the project baseline immutable. Recompute from valid committed inputs and current control state. Validate `0 ≤ minimum ≤ mode ≤ maximum`, probability bounds of 0–1, and finite numbers. Provide inline corrections without silently sorting or clipping inputs. During invalid edits, retain the last valid results and show **“Fix inputs to update results.”**

## 10. Advanced Inputs and Usability

- Select any regime/scenario to edit attempt, success, and loss triples. Label monetary inputs in $M.
- Simple and advanced modes share the same effective model. Committing advanced inputs resets shortcut anchors and multipliers to those values; project-baseline comparisons stay unchanged.
- Use Apply to commit a complete advanced input set.
- Pair sliders with number inputs and keyboard support. Give every field a label and unit.
- Target result updates within 100ms. Dragging must not trigger scrolling or modal dialogs.
- Use labels and symbols alongside color. Avoid page-wide horizontal scrolling on mobile.
- Respect reduced-motion preferences. Announce a short result update to screen readers when an adjustment is completed.
- Reset restores baseline and offers Undo. Reloading starts from baseline for the next audience member.
- Export JSON includes schema version, baseline hash, all effective inputs, results, and control state. Include the date in the filename.

## 11. Implementation Approach

Use React, TypeScript, and Vite with SVG charts, without a backend or external computation API. Centralize calculations in `model.ts`; the UI consumes its results. Generate `baseline.json` from Python PARAMETERS to avoid independently maintained parameter copies.

Represent scenarios, regimes, triples, turnover assumptions, and source metadata explicitly. Provide a README covering local development, production builds, and baseline updates. Keep implementation files in `web/` and preserve the Python simulation.

## 12. Acceptance Criteria

- Baseline analytical totals match Python within $1: A $99.60884259M, B $86.96748741M, C $69.30770741M.
- Halving B S2 success gives approximately $58.90915407M.
- Setting B S2/S3 attempts to A gives approximately $61.13943185M.
- Setting B employee cost to C gives approximately $83.41770741M.
- Setting B extra departures to zero gives approximately $72.57115741M.
- The initial turnover calculation reproduces B $14,396,330 and C $10,846,550 exactly; display rounding does not change calculations.
- Editing B leaves A/C unchanged. Scenario selection does not remove other scenarios or duplicate regime-level costs.
- Presets do not accumulate. Reset, Undo, and export reflect the actual state.
- Invalid triples, negative values, empty inputs, and probabilities above 100% show actionable errors.
- The equal-USB experiment updates A's success and confirmed program cost together; it cannot activate with an empty cost.
- All interactions work on desktop and mobile, including keyboard operation and readable chart details.
- A person unfamiliar with the project can identify a ranking-changing assumption within three minutes and explain that the result depends on their inputs.
- Apply the visual and accessibility requirements in Section 13 to cards, controls, charts, and responsive states.

## 13. Visual Design and Color System

### Palette

Build the interface around the supplied indigo palette, using pink accents sparingly for interaction and emphasis.

| Token | Color | Role |
|---|---|---|
| `--primary` | `#2A3990` | Primary actions, selected tabs, slider thumbs, main indigo identity |
| `--indigo-deep` | `#212D74` | Main text on light surfaces, headings, primary-button hover |
| `--indigo-soft` | `#7890CD` | Supporting graphics, slider tracks, neutral regime markers |
| `--indigo-medium` | `#3949AB` | Secondary emphasis and chart segments |
| `--canvas` | `#F2EDEC` | Warm page background and quiet section surfaces |
| `--accent` | `#D23369` | Small emphasis marks, active comparison highlights, chart segments |
| `--accent-soft` | `#F06292` | Light accent fills and secondary chart segments |
| `--accent-deep` | `#9C254D` | Error text and borders on light surfaces; accent hover |
| `--surface` | `#FFFFFF` | Cards, fields, chart backgrounds, and text on dark buttons |

White is a supporting neutral. Use opacity or tints derived from the palette for subtle borders and backgrounds. Do not introduce a separate green/red ranking palette.

### Component Rules

- Page: warm `--canvas`, white cards, generous whitespace, and deep-indigo text. Avoid large saturated accent backgrounds.
- Primary buttons: `--primary` with white text; hover uses `--indigo-deep`. Secondary actions use white with indigo text and borders.
- Selected tabs: indigo fill with white text. Unselected tabs use dark-indigo text on a light surface, with a visible boundary or underline where needed.
- Focus: a visible primary-indigo outline with a contrasting light offset. Focus must remain distinguishable on both light and indigo backgrounds.
- Sliders: indigo thumb and filled track, subdued soft-indigo remaining track. Labels show the affected regime, units, and current value.
- Errors: `--accent-deep` text and border, plus an icon and explicit message. Accent color used elsewhere must never be the only indication of an error.
- Lowest-cost card: a primary-indigo outline and **“Lowest modeled cost”** badge applied dynamically to whichever regime qualifies. Preserve its regime identity marker.
- Changed-value badges: pale accent background, deep-accent text, and an explicit signed amount. Label direction in words where helpful; color alone must not imply beneficial or harmful change.

### Chart Colors

Use distinct encodings for regime identity and cost components. A regime color appears in its letter badge or card marker; stacked-bar fills represent cost categories consistently across all three bars.

| Regime identity | Color |
|---|---|
| A | `#7890CD` |
| B | `#2A3990` |
| C | `#9C254D` |

| Cost component | Color | Additional distinction |
|---|---|---|
| S1 USB theft | `#7890CD` | Direct S1 label |
| S2 Email/cloud theft | `#2A3990` | Direct S2 label |
| S3 Admin sabotage | `#3949AB` | Diagonal pattern plus S3 label |
| Employee replacement | `#D23369` | Text label in legend and details |
| Program | `#F06292` | Text label in legend and details |
| Expected enforcement penalty | `#9C254D` | Dotted pattern plus text label |

Separate adjacent segments with thin white dividers. Keep A/B/C row labels visible. Small segments can use external labels or accessible details instead of cramped internal text. Use tooltips, keyboard-accessible details, and a data table to distinguish values independent of hue.

### Accessibility and Restraint

- Verify actual rendered foreground/background combinations: at least 4.5:1 contrast for normal text, 3:1 for large text, and 3:1 for essential control boundaries and graphical indicators.
- Use deep indigo for text on white, warm neutral, soft-indigo, and soft-pink surfaces where the tested contrast permits. Do not assume white text is readable on the lighter palette colors.
- Prefer dark fills with white text or light fills with dark text; adjust derived surface tints if a contrast check fails while retaining the supplied base colors.
- Pair selected, lowest-cost, changed, and error states with text, icons, borders, or patterns.
- Keep card geometry and ordering stable as values change. Use brief optional transitions; honor reduced motion.
- Validate the final chart in grayscale and with color-vision simulation. Users must still identify regimes, cost categories, and the current lowest-cost result.
