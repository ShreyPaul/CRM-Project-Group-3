import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import {
  baseline,
  clone,
  regimes,
  scenarios,
  names,
  titles,
  techniques,
  keys,
  labels,
  mean,
  money,
  number,
  evaluate,
  costPerReplacement,
  departureCost,
  departuresFor,
  withDepartures,
  successScale,
  withUplift,
  upliftReason,
  preset,
  validate,
  type Inputs,
  type Regime,
  type Scenario,
  type Triple,
  type Component,
} from "./model";
import "./styles.css";
const colors: Record<Component, string> = {
  S1: "#7890CD",
  S2: "#2A3990",
  S3: "#3949AB",
  people: "#D23369",
  program: "#F06292",
  fine: "#9C254D",
};
const original = evaluate(baseline);
const desc = {
  S1: "An employee copies client information to removable storage.",
  S2: "An employee transfers sensitive information to personal email or cloud storage.",
  S3: "A privileged user destroys data or disrupts business systems.",
};
type Snapshot = {
  input: Inputs;
  anchor: Inputs;
  applied: boolean;
  multipliers: Record<string, number>;
};
const initial = (): Snapshot => ({
  input: clone(baseline),
  anchor: clone(baseline),
  applied: false,
  multipliers: {},
});
function Range({
  label,
  value,
  max,
  step = 1,
  onChange,
  unit = "",
  disabled = false,
}: {
  label: string;
  value: number;
  max: number;
  step?: number;
  onChange: (n: number) => void;
  unit?: string;
  disabled?: boolean;
}) {
  const [draft, setDraft] = useState<string | null>(null);
  const invalid =
    draft !== null &&
    (draft.trim() === "" ||
      !Number.isFinite(Number(draft)) ||
      Number(draft) < 0 ||
      Number(draft) > max);
  return (
    <div className="range-pair">
      <input
        type="range"
        aria-label={label}
        min="0"
        max={max}
        step={step}
        value={Math.min(max, value)}
        disabled={disabled}
        onChange={(e) => {
          setDraft(null);
          onChange(+e.target.value);
        }}
      />
      <div>
        <label className="number-wrap">
          <span className="sr-only">{label} numeric value</span>
          <input
            type="number"
            aria-label={`${label} numeric value`}
            min="0"
            max={max}
            step="any"
            disabled={disabled}
            value={draft ?? String(Math.round(value * 1000) / 1000)}
            aria-invalid={invalid}
            onChange={(e) => {
              const v = e.target.value;
              setDraft(v);
              if (
                v.trim() !== "" &&
                Number.isFinite(+v) &&
                +v >= 0 &&
                +v <= max
              )
                onChange(+v);
            }}
            onBlur={() => {
              if (!invalid) setDraft(null);
            }}
          />
          {unit}
        </label>
      </div>
      {invalid && (
        <span className="error">
          Enter a number between 0 and {number(max)}. Fix this input to update
          its value.
        </span>
      )}
    </div>
  );
}
function Advanced({
  input,
  onApply,
}: {
  input: Inputs;
  onApply: (i: Inputs) => void;
}) {
  const [draft, setDraft] = useState(clone(input));
  const [errors, setErrors] = useState<string[]>([]);
  const [r, setR] = useState<Regime>("A");
  const edit = (update: (x: Inputs) => void) => {
    const next = clone(draft);
    update(next);
    setDraft(next);
    setErrors(validate(next));
  };
  const triple = (
    label: string,
    t: Triple,
    scale: number,
    set: (x: Inputs, t: Triple) => void,
    prob = false,
  ) => (
    <fieldset className="triple">
      <legend>
        {label}
        {scale === 1e6 ? " ($M)" : prob ? " (0–1)" : ""}
      </legend>
      {["Minimum", "Mode", "Maximum"].map((l, i) => (
        <label key={l}>
          {l}
          <input
            type="number"
            step="any"
            value={Number.isFinite(t[i]) ? t[i] / scale : ""}
            onChange={(e) =>
              edit((x) => {
                const v = [...t] as Triple;
                v[i] =
                  e.target.value.trim() === ""
                    ? NaN
                    : Number(e.target.value) * scale;
                set(x, v);
              })
            }
          />
        </label>
      ))}
    </fieldset>
  );
  return (
    <details className="advanced">
      <summary
        onClick={(e) => {
          if (!e.currentTarget.parentElement?.hasAttribute("open")) {
            setDraft(clone(input));
            setErrors([]);
          }
        }}
      >
        Advanced inputs <span>All triples & costs</span>
      </summary>
      <p className="muted">
        Minimum / most likely (mode) / maximum. Apply commits all regimes
        together and anchors the sliders to your inputs.
      </p>
      <div className="segmented">
        {regimes.map((v) => (
          <button key={v} aria-pressed={r === v} onClick={() => setR(v)}>
            {v} · {names[v]}
          </button>
        ))}
      </div>
      {scenarios.map((s) => (
        <section className="advanced-scenario" key={s}>
          <h4>
            {s} · {titles[s]}
          </h4>
          {(["attempts", "success", "loss"] as const).map((k) => (
            <React.Fragment key={k}>
              {triple(
                k === "attempts"
                  ? "Attempts per year"
                  : k === "success"
                    ? "Attack success probability"
                    : "Loss per successful event",
                draft.model[r].scenarios[s][k],
                k === "loss" ? 1e6 : 1,
                (x, t) => {
                  x.model[r].scenarios[s][k] = t;
                },
                k === "success",
              )}
            </React.Fragment>
          ))}
        </section>
      ))}
      <label className="scope-select">
        Additional departures in {r}
        <input
          type="number"
          min="0"
          step="any"
          value={
            Number.isFinite(draft.model[r].departures)
              ? draft.model[r].departures
              : ""
          }
          onChange={(e) =>
            edit((x) => {
              x.model[r].departures =
                e.target.value.trim() === "" ? NaN : +e.target.value;
            })
          }
        />
      </label>
      <p className="notice">
        Calculated employee replacement cost for {r}:{" "}
        <strong>
          {money(departureCost(draft, draft.model[r].departures))}
        </strong>
        . Cost is derived from departures, replacement rate, and cost per
        replacement.
      </p>
      {triple("Program cost", draft.model[r].program, 1e6, (x, t) => {
        x.model[r].program = t;
      })}
      {triple(
        "Annual enforcement probability",
        draft.model[r].enforcement,
        1,
        (x, t) => {
          x.model[r].enforcement = t;
        },
        true,
      )}
      {triple(
        "Shared penalty conditional on enforcement",
        draft.penalty,
        1e6,
        (x, t) => {
          x.penalty = t;
        },
      )}
      <details>
        <summary>Replacement costing assumptions</summary>
        <div className="cost-inputs">
          {Object.entries(draft.turnover)
            .filter(([k]) => k !== "workforce")
            .map(([k, v]) => (
              <label key={k}>
                {
                  (
                    {
                      replacementRate: "Replacement rate (0–1)",
                      hiring: "Hiring & ramp-up ($)",
                      vacancy: "Net vacancy cost ($)",
                      payDifference: "Annual pay difference ($)",
                      yearFraction: "First-year fraction (0–1)",
                    } as Record<string, string>
                  )[k]
                }
                <input
                  type="number"
                  step="any"
                  value={Number.isFinite(v) ? v : ""}
                  onChange={(e) =>
                    edit((x) => {
                      (x.turnover as unknown as Record<string, number>)[k] =
                        e.target.value.trim() === "" ? NaN : +e.target.value;
                    })
                  }
                />
              </label>
            ))}
        </div>
        <p className="muted">
          Changing replacement rates or unit costs keeps departure counts fixed.
          Apply recalculates employee replacement costs for A, B, and C
          automatically.
        </p>
      </details>
      {errors.length > 0 && (
        <div className="error" role="alert">
          <strong>Fix inputs to update results.</strong>
          <ul>
            {errors.map((e) => (
              <li key={e}>{e}</li>
            ))}
          </ul>
        </div>
      )}
      <div className="actions">
        <button
          className="primary"
          disabled={errors.length > 0}
          onClick={() => {
            const e = validate(draft);
            setErrors(e);
            if (!e.length) onApply(draft);
          }}
        >
          Apply all inputs
        </button>
        <button
          onClick={() => {
            setDraft(clone(input));
            setErrors([]);
          }}
        >
          Discard edits
        </button>
      </div>
    </details>
  );
}
function App() {
  const [state, setState] = useState<Snapshot>(initial);
  const [undo, setUndo] = useState<Snapshot | null>(null);
  const [r, setR] = useState<Regime>("B");
  const [tab, setTab] = useState<Scenario | "all">("all");
  const [focus, setFocus] = useState<Scenario>("S2");
  const [both, setBoth] = useState(true);
  const [incidentOnly, setIncidentOnly] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [live, setLive] = useState("");
  const [error, setError] = useState("");
  const [revision, setRevision] = useState(0);
  const [detail, setDetail] = useState(
    "Select or focus a chart segment to inspect its cost.",
  );
  const { input, anchor } = state;
  const result = evaluate(input);
  const s = tab === "all" ? focus : tab;
  const p = input.model[r].scenarios[s];
  const ar = anchor.model[r].scenarios[s];
  const compare = r === "B" ? "C" : "B";
  const gap = result[r].total - result[compare].total;
  const sorted = regimes.toSorted((a, b) => result[a].total - result[b].total);
  const tied = regimes.filter(
    (v) => result[v].total - result[sorted[0]].total < 10000,
  );
  const scopes: Scenario[] = tab === "all" && both ? ["S2", "S3"] : [s];
  const upliftDisabled = upliftReason(anchor, r, scopes);
  const maxMultiplier =
    ar.success[2] === 0 ? 200 : Math.min(200, 100 / ar.success[2]);
  const departures = departuresFor(input, r);
  const unit = costPerReplacement(input);
  const largest = keys.toSorted(
    (a, b) =>
      Math.abs(result[r].components[b] - result[compare].components[b]) -
      Math.abs(result[r].components[a] - result[compare].components[a]),
  )[0];
  function commit(
    next: Inputs,
    options: Partial<Snapshot> = {},
    message = "Your assumptions are applied.",
  ) {
    const errors = validate(next);
    if (errors.length) {
      setError(errors[0]);
      return;
    }
    setError("");
    setState({ ...state, input: next, ...options });
    setFeedback(message);
  }
  function reset() {
    setUndo(clone(state));
    setState(initial());
    setR("B");
    setTab("all");
    setFocus("S2");
    setBoth(true);
    setIncidentOnly(false);
    setError("");
    setRevision((v) => v + 1);
    setFeedback("Project baseline restored.");
  }
  function loadPreset(name: string) {
    const n = preset(name);
    setUndo(clone(state));
    setState({
      ...initial(),
      input: n,
      anchor: clone(n),
      applied: name !== "baseline",
    });
    setRevision((v) => v + 1);
    setR("B");
    setTab("all");
    setFocus("S2");
    setError("");
    setFeedback("Loaded project baseline + this change.");
  }
  function scaleSuccess(k: number) {
    commit(successScale(input, anchor, r, s, k), {
      multipliers: { ...state.multipliers, [`${r}-${s}-success`]: k * 100 },
    });
  }
  function scaleUplift(k: number) {
    const multipliers = { ...state.multipliers };
    scopes.forEach((v) => (multipliers[`${r}-${v}-attempts`] = k * 100));
    commit(withUplift(input, anchor, r, scopes, k), { multipliers });
  }
  const announce = () =>
    setLive(
      `Lowest modeled cost: ${tied.join(" and ")}, ${money(result[sorted[0]].total)}.`,
    );
  return (
    <>
      <header>
        <a className="brand" href="#main">
          <span className="brand-icon">
            M<span>↗</span>
          </span>
          <span>
            MONITORING
            <br />
            <b>TRADE-OFF EXPLORER</b>
          </span>
        </a>
        <div className="header-meta">
          <span className="pill">ATT&CK × FAIR</span>
        </div>
      </header>
      <main id="main" onPointerUp={announce} onKeyUp={announce}>
        <section className="hero">
          <div>
            <p className="eyebrow">INSIDER THREAT · INTERACTIVE MODEL</p>
            <h1>
              When is more monitoring
              <br />
              <em>worth the cost?</em>
            </h1>
            <p className="intro">
              Security gains. Human responses. Real trade-offs.
              <br />
              Change an assumption and see which strategy costs less.
            </p>
          </div>
          <div className="hero-note">
            <span className="small-label">THE QUESTION IS YOURS</span>
            <p>
              Which assumption
              <br />
              would you challenge?
            </p>
            <div className="hero-rule" />
            <span>
              Three strategies. Three threats.
              <br />
              One comparison you can change.
            </span>
          </div>
        </section>
        <div className="toolbar">
          <div className="tabs" aria-label="Threat scenario">
            {(["all", ...scenarios] as const).map((v) => (
              <button
                key={v}
                aria-pressed={tab === v}
                onClick={() => {
                  setTab(v);
                  setError("");
                }}
              >
                {v === "all" ? "All scenarios" : titles[v]}
              </button>
            ))}
          </div>
          <div className="actions">
            <button onClick={reset}>↺ Reset</button>
            {undo && (
              <button
                onClick={() => {
                  setState(undo);
                  setUndo(null);
                  setRevision((v) => v + 1);
                  setFeedback("Previous experiment restored.");
                }}
              >
                Undo reset / preset
              </button>
            )}
          </div>
        </div>
        <div className="workspace">
          <aside className="controls">
            <div className="section-heading">
              <div>
                <p className="eyebrow">YOUR ASSUMPTIONS</p>
                <h2>Explore the trade-off</h2>
              </div>
              <span className="step-badge">01 — 03</span>
            </div>
            <div className="regime-switch">
              <span>Edit strategy</span>
              <div className="segmented">
                {(["B", "C"] as const).map((v) => (
                  <button
                    key={v}
                    aria-pressed={r === v}
                    onClick={() => setR(v)}
                  >
                    {v} · {v === "B" ? "Extensive" : "Privacy-preserving"}
                  </button>
                ))}
              </div>
            </div>
            {tab === "all" && (
              <label className="scope-select">
                Focus scenario
                <select
                  value={focus}
                  onChange={(e) => setFocus(e.target.value as Scenario)}
                >
                  {scenarios.map((v) => (
                    <option value={v} key={v}>
                      {titles[v]}
                    </option>
                  ))}
                </select>
              </label>
            )}
            <div className="scope-note">
              <b>
                Editing {r} · {titles[s]}
              </b>
              <span>
                {desc[s]}{" "}
                <a
                  href={`https://attack.mitre.org/techniques/${techniques[s].replace(".", "/")}/`}
                  target="_blank"
                  rel="noreferrer"
                >
                  {techniques[s]} ↗
                </a>
              </span>
            </div>
            <section className="control-section">
              <div className="control-title">
                <span>01</span>
                <h3>Successful attacks remaining</h3>
              </div>
              <p className="muted">
                Lower values mean fewer attempts cause a loss.
              </p>
              <div className="big-readout">
                {number(mean(p.success) * 100)}
                <span> out of 100 attempts succeed</span>
              </div>
              <Range
                key={`${r}-${s}-success-${revision}`}
                label="Successful attacks remaining"
                value={state.multipliers[`${r}-${s}-success`] ?? 100}
                max={maxMultiplier}
                unit="%"
                onChange={(v) => scaleSuccess(v / 100)}
              />
              <p className="micro">
                100% ={" "}
                {state.applied ? "your applied inputs" : "project baseline"}
              </p>
              <div className="quick-actions">
                <button onClick={() => scaleSuccess(1)}>Baseline</button>
                <button onClick={() => scaleSuccess(0.75)}>
                  25% fewer successes
                </button>
                <button onClick={() => scaleSuccess(0.5)}>
                  50% fewer successes
                </button>
              </div>
              <div className="event-chain">
                <div>
                  <b>{number(mean(p.attempts))}</b>
                  <span>attempts / yr</span>
                </div>
                <i>→</i>
                <div>
                  <b>{number(result[r].events[s])}</b>
                  <span>successful events</span>
                </div>
                <i>→</i>
                <div>
                  <b>{money(result[r].components[s])}</b>
                  <span>expected loss</span>
                </div>
              </div>
            </section>
            <section className="control-section">
              <div className="control-title">
                <span>02</span>
                <h3>Additional attack attempts</h3>
              </div>
              <p className="muted">
                Explore whether monitoring leads to more attempts through other
                channels.
              </p>
              {s === "S1" ? (
                <p className="notice">
                  USB attempts are equal across regimes in this baseline. Use
                  Advanced inputs for custom rates.
                </p>
              ) : (
                <>
                  <div className="big-readout">
                    {number(mean(anchor.model.A.scenarios[s].attempts))} →{" "}
                    {number(mean(p.attempts))}
                    <span> attempts / year</span>
                  </div>
                  {tab === "all" && (
                    <label className="checkbox">
                      <input
                        type="checkbox"
                        checked={both}
                        onChange={(e) => setBoth(e.target.checked)}
                      />
                      Apply to email/cloud and admin sabotage
                    </label>
                  )}
                  <Range
                    key={`${r}-${s}-attempts-${revision}`}
                    label="Additional attack attempts"
                    value={state.multipliers[`${r}-${s}-attempts`] ?? 100}
                    max={200}
                    unit="%"
                    disabled={!!upliftDisabled}
                    onChange={(v) => scaleUplift(v / 100)}
                  />
                  <p className="micro">
                    0% = same attempts as A · 100% ={" "}
                    {state.applied ? "applied" : "project"} uplift
                  </p>
                  {upliftDisabled && <p className="error">{upliftDisabled}</p>}
                  <button
                    className="text-button"
                    disabled={!!upliftDisabled}
                    onClick={() => scaleUplift(0)}
                  >
                    Try no additional attempts →
                  </button>
                </>
              )}
            </section>
            <section className="control-section">
              <div className="control-title">
                <span>03</span>
                <h3>Additional employees who leave</h3>
              </div>
              <p className="muted">
                Extra departures relative to A during the first year. Shared
                across all three threats.
              </p>
              <div className="big-readout">
                ≈ {number(Math.round(departures))}
                <span> extra departures</span>
              </div>
              <Range
                key={`${r}-departures-${revision}`}
                label="Additional employees who leave"
                value={departures}
                max={Math.max(5000, Math.ceil(departures))}
                onChange={(v) =>
                  commit(
                    withDepartures(input, r, v),
                    {},
                    "Custom departure assumption applied.",
                  )
                }
              />
              <div className="quick-actions">
                {r === "B" && (
                  <button
                    onClick={() => {
                      const n = clone(input);
                      n.model.B.departures = n.model.C.departures;
                      commit(
                        n,
                        {},
                        "B now has the same number of additional departures as C.",
                      );
                    }}
                  >
                    Match C’s extra departures
                  </button>
                )}
                <button
                  onClick={() =>
                    commit(
                      withDepartures(input, r, 0),
                      {},
                      "No additional departures assumed.",
                    )
                  }
                >
                  No additional departures
                </button>
              </div>
              <div className="employee-ledger">
                <div>
                  <span>Extra departures</span>
                  <b>{number(departures)}</b>
                </div>
                <div>
                  <span>Replaced</span>
                  <b>{number(input.turnover.replacementRate * 100)}%</b>
                </div>
                <div>
                  <span>Replacement hires</span>
                  <b>{number(departures * input.turnover.replacementRate)}</b>
                </div>
                <div>
                  <span>Replacement cost</span>
                  <b>{money(departureCost(input, departures))}</b>
                </div>
              </div>
              <p className="micro">
                {number(departures)} ×{" "}
                {number(input.turnover.replacementRate * 100)}% × $
                {number(unit)} per replacement
              </p>
              <details>
                <summary>Where does this estimate come from?</summary>
                <p className="muted">
                  Baseline: 48,100 employees × additional intention to leave (
                  {r === "B" ? "7.3" : "5.5"} percentage points versus A) × 25%
                  assumed conversion to actual departures. These are scenario
                  assumptions. Editing departures creates a custom assumption.
                </p>
                <p className="muted">
                  Per replacement: hiring and ramp-up + net vacancy cost +
                  first-year compensation difference.
                </p>
              </details>
            </section>
          </aside>
          <section className="results" aria-label="Live comparison">
            <div className="section-heading">
              <div>
                <p className="eyebrow">LIVE COMPARISON</p>
                <h2>Follow the cost.</h2>
              </div>
              <span className="live-indicator">Live</span>
            </div>
            <p className="muted">
              Expected first-year cost · USD millions · All-scenario total
            </p>
            <div className="cards">
              {regimes.map((v) => (
                <article
                  className={`cost-card regime-${v} ${tied.includes(v) ? "lowest" : ""}`}
                  key={v}
                >
                  <div className="card-top">
                    <span className="regime-letter">{v}</span>
                    {tied.includes(v) && (
                      <span className="winner-label">
                        {tied.length > 1
                          ? "Approximately tied"
                          : "Lowest modeled cost"}
                      </span>
                    )}
                  </div>
                  <h3>{names[v]}</h3>
                  <strong className="total">{money(result[v].total)}</strong>
                  <span className="delta">
                    {result[v].total - original[v].total < 0 ? "−" : "+"}
                    {money(Math.abs(result[v].total - original[v].total))} vs
                    project baseline
                  </span>
                </article>
              ))}
            </div>
            <section className="chart-panel">
              <div className="chart-title">
                <h3>What makes up the cost?</h3>
                <div className="segmented small">
                  <button
                    aria-pressed={!incidentOnly}
                    onClick={() => setIncidentOnly(false)}
                  >
                    All costs
                  </button>
                  <button
                    aria-pressed={incidentOnly}
                    onClick={() => setIncidentOnly(true)}
                  >
                    Incident losses only
                  </button>
                </div>
              </div>
              <p className="micro">
                All three scenarios included.{" "}
                {incidentOnly
                  ? "Chart shows incident losses; cards still compare total costs."
                  : "Select a segment for details."}
              </p>
              <svg
                className="cost-chart"
                viewBox="0 0 660 230"
                role="group"
                aria-label="Expected cost composition by strategy"
              >
                <defs>
                  <pattern
                    id="sabotage"
                    width="7"
                    height="7"
                    patternUnits="userSpaceOnUse"
                  >
                    <rect width="7" height="7" fill={colors.S3} />
                    <path d="M0 7L7 0" stroke="white" strokeOpacity=".5" />
                  </pattern>
                  <pattern
                    id="penalty"
                    width="7"
                    height="7"
                    patternUnits="userSpaceOnUse"
                  >
                    <rect width="7" height="7" fill={colors.fine} />
                    <circle cx="3" cy="3" r="1" fill="white" />
                  </pattern>
                </defs>
                {(() => {
                  const shown: readonly Component[] = incidentOnly
                    ? keys.slice(0, 3)
                    : keys;
                  const max = Math.max(
                    1,
                    ...regimes.map((v) =>
                      shown.reduce<number>(
                        (sum, k) => sum + result[v].components[k],
                        0,
                      ),
                    ),
                  );
                  return (
                    <>
                      {regimes.map((v, i) => {
                        let x = 42;
                        return (
                          <g key={v}>
                            <text x="8" y={39 + i * 61} className="svg-regime">
                              {v}
                            </text>
                            {shown.map((k) => {
                              const val = result[v].components[k],
                                w = (val / max) * 530;
                              const pos = x;
                              x += w;
                              const text = `${v} · ${labels[k]}: ${money(val)}`;
                              return val > 0 ? (
                                <g
                                  key={k}
                                  tabIndex={0}
                                  role="button"
                                  aria-label={text}
                                  onFocus={() => setDetail(text)}
                                  onMouseEnter={() => setDetail(text)}
                                  onClick={() => setDetail(text)}
                                  onKeyDown={(e) => {
                                    if (e.key === "Enter" || e.key === " ") {
                                      e.preventDefault();
                                      setDetail(text);
                                    }
                                  }}
                                >
                                  <title>{text}</title>
                                  <rect
                                    x={pos}
                                    y={17 + i * 61}
                                    width={w}
                                    height="34"
                                    fill={
                                      k === "S3"
                                        ? "url(#sabotage)"
                                        : k === "fine"
                                          ? "url(#penalty)"
                                          : colors[k]
                                    }
                                    stroke="white"
                                    strokeWidth="1.2"
                                  />
                                  {w > 45 && k === "S1" && (
                                    <rect
                                      x={pos + w / 2 - 12}
                                      y={25 + i * 61}
                                      width={24}
                                      height={18}
                                      rx={3}
                                      fill="white"
                                      pointerEvents="none"
                                    />
                                  )}
                                  {w > 45 && (
                                    <text
                                      pointerEvents="none"
                                      x={pos + w / 2}
                                      y={38 + i * 61}
                                      textAnchor="middle"
                                      fill={
                                        ["S1", "program"].includes(k)
                                          ? "#212D74"
                                          : "white"
                                      }
                                      fontSize="11"
                                      fontWeight="700"
                                    >
                                      {k.startsWith("S") ? k : ""}
                                    </text>
                                  )}
                                </g>
                              ) : null;
                            })}
                            <text
                              x={x + 7}
                              y={39 + i * 61}
                              fontSize="13"
                              fill="#212D74"
                              fontWeight="700"
                            >
                              {money(
                                shown.reduce<number>(
                                  (sum, k) => sum + result[v].components[k],
                                  0,
                                ),
                              )}
                            </text>
                          </g>
                        );
                      })}
                      {[0, 0.25, 0.5, 0.75, 1].map((t) => (
                        <g key={t}>
                          <line
                            x1={42 + t * 530}
                            x2={42 + t * 530}
                            y1="195"
                            y2="200"
                            stroke="#212D74"
                          />
                          <text
                            x={42 + t * 530}
                            y="218"
                            textAnchor="middle"
                            fontSize="11"
                            fill="#212D74"
                          >
                            {((t * max) / 1e6).toFixed(0)}
                          </text>
                        </g>
                      ))}
                    </>
                  );
                })()}
              </svg>
              <div className="segment-detail">{detail}</div>
              <div className="legend">
                {(incidentOnly ? keys.slice(0, 3) : keys).map((k) => (
                  <span key={k}>
                    <i style={{ background: colors[k] }} />
                    {labels[k]}
                  </span>
                ))}
              </div>
              <details>
                <summary>View exact cost data</summary>
                <div className="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>Component</th>
                        {regimes.map((v) => (
                          <th key={v}>{v} ($M)</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {keys.map((k) => (
                        <tr key={k}>
                          <th>{labels[k]}</th>
                          {regimes.map((v) => (
                            <td key={v}>
                              {(result[v].components[k] / 1e6).toFixed(4)}
                            </td>
                          ))}
                        </tr>
                      ))}
                      <tr>
                        <th>Total</th>
                        {regimes.map((v) => (
                          <td key={v}>{(result[v].total / 1e6).toFixed(4)}</td>
                        ))}
                      </tr>
                    </tbody>
                  </table>
                </div>
              </details>
            </section>
            <section className="insight">
              <span className="eyebrow">WHAT CHANGED?</span>
              <h3>
                {Math.abs(gap) < 10000
                  ? `${r} and ${compare} are approximately tied.`
                  : `${gap < 0 ? r : compare} has the lower modeled cost.`}
              </h3>
              <p>
                {r}'s total is{" "}
                <b>
                  {money(Math.abs(gap))} {gap < 0 ? "below" : "above"} {compare}
                </b>
                . The largest component of their current difference is{" "}
                <b>{labels[largest].toLowerCase()}</b> (
                {money(
                  Math.abs(
                    result[r].components[largest] -
                      result[compare].components[largest],
                  ),
                )}
                ).
              </p>
              <p className="micro">
                {feedback ||
                  "Start with a preset or change one assumption. The ranking follows your inputs."}
              </p>
            </section>
            <section className="presets">
              <h3>Challenge an assumption.</h3>
              <p className="muted">
                Each experiment loads the project baseline + this change.
              </p>
              <div className="preset-grid">
                <button onClick={() => loadPreset("attempts")}>
                  <span>01 / BEHAVIOR</span>
                  <b>No additional attack attempts in B</b>
                  <i>Try this scenario ↗</i>
                </button>
                <button onClick={() => loadPreset("success")}>
                  <span>02 / PROTECTION</span>
                  <b>Stronger email/cloud protection in B</b>
                  <i>50% fewer successful attacks ↗</i>
                </button>
                <button onClick={() => loadPreset("people")}>
                  <span>03 / EMPLOYEES</span>
                  <b>Same number of employees leave in B and C</b>
                  <i>Set B’s extra departures to C’s level ↗</i>
                </button>
                <button onClick={() => loadPreset("baseline")}>
                  <span>04 / START AGAIN</span>
                  <b>Project baseline</b>
                  <i>Restore the original comparison ↗</i>
                </button>
              </div>
            </section>
            <details className="method">
              <summary>
                See the calculation <span>ATT&CK → FAIR → costs</span>
              </summary>
              <p>
                ATT&CK defines the scenario: {titles[s]} ({techniques[s]}). FAIR
                structures the calculation:
              </p>
              <div className="formula">
                Attempts / year × attack success probability × loss per event
              </div>
              <p>
                For {r} · {titles[s]}: {number(mean(p.attempts))} ×{" "}
                {number(mean(p.success) * 100)}% × {money(mean(p.loss))} ={" "}
                <b>{money(result[r].components[s])}</b> expected incident loss.
              </p>
              <p>
                Add the three scenario losses, employee replacement, program
                cost, and expected enforcement penalty. Triple means use
                (minimum + 4 × mode + maximum) / 6 under independent inputs.
              </p>
              <p>
                <a
                  href="https://www.fairinstitute.org/blog/3-steps-to-combine-mitre-attck-and-fair-to-focus-cyber-risk-management"
                  target="_blank"
                  rel="noreferrer"
                >
                  How ATT&CK and FAIR connect ↗
                </a>{" "}
                ·{" "}
                <a
                  href="https://www.bny.com/assets/corporate/documents/pdf/investor-relations/annual-report-2025.pdf"
                  target="_blank"
                  rel="noreferrer"
                >
                  BNY workforce context ↗
                </a>
              </p>
              <p className="micro">
                These are analytical expectations. No random simulation is
                needed for these means; P95 and cost-exceedance probabilities
                require simulation.
              </p>
            </details>

            {error && (
              <p className="error" role="alert">
                {error}
              </p>
            )}
          </section>
        </div>
        <Advanced
          key={revision}
          input={input}
          onApply={(next) => {
            setUndo(clone(state));
            commit(
              clone(next),
              { anchor: clone(next), multipliers: {}, applied: true },
              "Advanced inputs applied. Slider references now use your applied values.",
            );
            setRevision((v) => v + 1);
          }}
        />
        <footer>
          <span>BNY context · ATT&CK scenarios · FAIR-informed costs</span>
        </footer>
        <div className="sr-only" role="status" aria-live="polite">
          {live}
        </div>
      </main>
    </>
  );
}
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
