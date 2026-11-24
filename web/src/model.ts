import raw from "./baseline.json";
export type Triple = [number, number, number];
export const regimes = ["A", "B", "C"] as const;
export const scenarios = ["S1", "S2", "S3"] as const;
export type Regime = (typeof regimes)[number];
export type Scenario = (typeof scenarios)[number];
export type ScenarioInput = { attempts: Triple; success: Triple; loss: Triple };
export type Inputs = {
  model: Record<
    Regime,
    {
      scenarios: Record<Scenario, ScenarioInput>;
      departures: number;
      program: Triple;
      enforcement: Triple;
    }
  >;
  penalty: Triple;
  turnover: {
    workforce: number;
    replacementRate: number;
    hiring: number;
    vacancy: number;
    payDifference: number;
    yearFraction: number;
  };
};
export const clone = <T>(v: T): T => structuredClone(v);
export const baseline = raw as unknown as Inputs & {
  sourceHash: string;
  turnoverSourceHash: string;
  pythonExpected: Record<Regime, number>;
};
export const names: Record<Regime, string> = {
  A: "Reference baseline",
  B: "Extensive monitoring",
  C: "Privacy-preserving monitoring",
};
export const titles: Record<Scenario, string> = {
  S1: "USB theft",
  S2: "Email / cloud",
  S3: "Admin sabotage",
};
export const techniques = { S1: "T1052.001", S2: "T1567.002", S3: "T1485" };
export const keys = ["S1", "S2", "S3", "people", "program", "fine"] as const;
export type Component = (typeof keys)[number];
export const labels: Record<Component, string> = {
  S1: "S1 · USB theft",
  S2: "S2 · Email / cloud",
  S3: "S3 · Admin sabotage",
  people: "Employee replacement",
  program: "Program",
  fine: "Expected enforcement penalty",
};
export const mean = (t: Triple) => (t[0] + 4 * t[1] + t[2]) / 6;
export const money = (n: number) => `$${(n / 1e6).toFixed(2)}M`;
export const number = (n: number) =>
  n.toLocaleString("en-US", { maximumFractionDigits: 1 });
export function evaluate(input: Inputs) {
  return Object.fromEntries(
    regimes.map((r) => {
      const p = input.model[r];
      const events = Object.fromEntries(
        scenarios.map((s) => [
          s,
          mean(p.scenarios[s].attempts) * mean(p.scenarios[s].success),
        ]),
      ) as Record<Scenario, number>;
      const components = {
        ...Object.fromEntries(
          scenarios.map((s) => [s, events[s] * mean(p.scenarios[s].loss)]),
        ),
        people: departureCost(input, p.departures),
        program: mean(p.program),
        fine: mean(p.enforcement) * mean(input.penalty),
      } as Record<Component, number>;
      return [
        r,
        {
          events,
          components,
          total: keys.reduce((sum, k) => sum + components[k], 0),
        },
      ];
    }),
  ) as Record<
    Regime,
    {
      events: Record<Scenario, number>;
      components: Record<Component, number>;
      total: number;
    }
  >;
}
export function costPerReplacement(input: Inputs) {
  const t = input.turnover;
  return t.hiring + t.vacancy + t.payDifference * t.yearFraction;
}
export function departureCost(input: Inputs, departures: number) {
  return (
    departures * input.turnover.replacementRate * costPerReplacement(input)
  );
}
export function departuresFor(input: Inputs, r: Regime) {
  return input.model[r].departures;
}
export function withDepartures(input: Inputs, r: Regime, departures: number) {
  const next = clone(input);
  next.model[r].departures = departures;
  return next;
}
export function successScale(
  input: Inputs,
  anchor: Inputs,
  r: Regime,
  s: Scenario,
  multiplier: number,
) {
  const next = clone(input);
  next.model[r].scenarios[s].success = anchor.model[r].scenarios[s].success.map(
    (v) => v * multiplier,
  ) as Triple;
  return next;
}
export function upliftReason(anchor: Inputs, r: Regime, selected: Scenario[]) {
  for (const s of selected) {
    if (
      anchor.model[r].scenarios[s].attempts.some(
        (v, i) => v < anchor.model.A.scenarios[s].attempts[i],
      )
    )
      return "Applied attempts are below A. Edit the attempt triples directly in Advanced inputs.";
  }
  return "";
}
export function withUplift(
  input: Inputs,
  anchor: Inputs,
  r: Regime,
  selected: Scenario[],
  k: number,
) {
  const next = clone(input);
  for (const s of selected)
    next.model[r].scenarios[s].attempts = anchor.model.A.scenarios[
      s
    ].attempts.map(
      (a, i) => a + k * (anchor.model[r].scenarios[s].attempts[i] - a),
    ) as Triple;
  return next;
}
export function preset(name: string): Inputs {
  let next: Inputs = clone(baseline);
  if (name === "attempts")
    next = withUplift(next, baseline, "B", ["S2", "S3"], 0);
  if (name === "success") next = successScale(next, baseline, "B", "S2", 0.5);
  if (name === "people") next.model.B.departures = next.model.C.departures;
  return next;
}
export function validate(input: Inputs): string[] {
  const errors: string[] = [];
  const check = (t: Triple, path: string, probability = false) => {
    if (
      t.length !== 3 ||
      !t.every(Number.isFinite) ||
      t[0] < 0 ||
      t[0] > t[1] ||
      t[1] > t[2] ||
      (probability && t[2] > 1)
    )
      errors.push(
        `${path}: enter finite values with 0 ≤ minimum ≤ mode ≤ maximum${probability ? " ≤ 1" : ""}.`,
      );
  };
  for (const r of regimes) {
    for (const s of scenarios)
      for (const k of ["attempts", "success", "loss"] as const)
        check(
          input.model[r].scenarios[s][k],
          `${r} ${s} ${k}`,
          k === "success",
        );
    if (
      !Number.isFinite(input.model[r].departures) ||
      input.model[r].departures < 0
    )
      errors.push(`${r} departures: enter a finite nonnegative number.`);
    check(input.model[r].program, `${r} program cost`);
    check(input.model[r].enforcement, `${r} enforcement probability`, true);
  }
  check(input.penalty, "Penalty");
  for (const [k, v] of Object.entries(input.turnover))
    if (
      !Number.isFinite(v) ||
      v < 0 ||
      (["replacementRate", "yearFraction"].includes(k) && v > 1)
    )
      errors.push(
        `Turnover ${k}: enter a finite nonnegative value${["replacementRate", "yearFraction"].includes(k) ? " no greater than 1" : ""}.`,
      );
  return errors;
}
