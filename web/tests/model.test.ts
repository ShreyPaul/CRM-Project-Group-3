import { test } from "node:test";
import assert from "node:assert/strict";
import {
  baseline,
  clone,
  evaluate,
  regimes,
  preset,
  withDepartures,
  departuresFor,
  departureCost,
  validate,
  withUplift,
  successScale,
} from "../src/model";
const close = (a: number, b: number) =>
  assert.ok(Math.abs(a - b) < 1, `${a} != ${b}`);
test("analytical model agrees with authoritative Python evaluator", () => {
  for (const r of regimes)
    close(evaluate(baseline)[r].total, baseline.pythonExpected[r]);
});
test("specified sensitivity cases retain their expected totals and unaffected regimes", () => {
  for (const [p, total] of [
    ["success", 58909154.074074],
    ["attempts", 61139431.851852],
    ["people", 83417707.407407],
  ] as const) {
    const result = evaluate(preset(p));
    close(result.B.total, total);
    close(result.A.total, evaluate(baseline).A.total);
    close(result.C.total, evaluate(baseline).C.total);
  }
});
test("turnover formula preserves exact baseline departures and fixed costs", () => {
  close(departureCost(baseline, 877.825), 14396330);
  close(departureCost(baseline, 661.375), 10846550);
  close(evaluate(withDepartures(baseline, "B", 0)).B.total, 72571157.407407);
  assert.ok(Math.abs(departuresFor(baseline, "B") - 877.825) < 1e-8);
});
test("scaling uses a stable anchor and does not compound or alter other inputs", () => {
  const once = successScale(baseline, baseline, "B", "S2", 0.5);
  assert.deepEqual(successScale(once, baseline, "B", "S2", 0.5), once);
  assert.deepEqual(once.model.C, baseline.model.C);
  const attempts = withUplift(baseline, baseline, "B", ["S2"], 0);
  assert.deepEqual(
    attempts.model.B.scenarios.S2.attempts,
    baseline.model.A.scenarios.S2.attempts,
  );
  assert.deepEqual(
    attempts.model.B.scenarios.S3,
    baseline.model.B.scenarios.S3,
  );
});
test("validation catches missing, unordered, negative, and out-of-bounds probability inputs", () => {
  for (const t of [
    [NaN, 1, 2],
    [2, 1, 3],
    [-1, 0, 1],
    [0, 1, 1.1],
  ]) {
    const x = clone(baseline);
    x.model.B.scenarios.S2.success = t as [number, number, number];
    assert.ok(validate(x).length);
  }
  assert.deepEqual(validate(baseline), []);
});
test("presets are independent", () => {
  const a = preset("people");
  a.model.B.program = [0, 0, 0];
  const b = preset("people");
  assert.deepEqual(b.model.B.program, baseline.model.B.program);
});
test("unit-cost edits recalculate replacement costs while preserving every departure count", () => {
  const input = clone(baseline);
  input.turnover.hiring += 1000;
  const before = evaluate(baseline),
    after = evaluate(input);
  for (const r of regimes) {
    assert.equal(departuresFor(input, r), departuresFor(baseline, r));
    close(
      after[r].components.people - before[r].components.people,
      baseline.model[r].departures * 0.8 * 1000,
    );
    close(
      after[r].total - before[r].total,
      baseline.model[r].departures * 0.8 * 1000,
    );
  }
});
test("zero replacement costs preserve departures and recover correctly when costing resumes", () => {
  const input = clone(baseline);
  input.turnover.replacementRate = 0;
  assert.equal(evaluate(input).B.components.people, 0);
  assert.equal(departuresFor(input, "B"), baseline.model.B.departures);
  const changed = withDepartures(input, "B", 1000);
  assert.equal(evaluate(changed).B.components.people, 0);
  changed.turnover.replacementRate = 0.8;
  close(evaluate(changed).B.components.people, 16_400_000);
});
test("departure inputs validate independently of unit costs and remain authoritative", () => {
  for (const n of [NaN, -1, Infinity]) {
    const input = withDepartures(baseline, "B", n);
    assert.ok(validate(input).some((e) => e.includes("B departures")));
  }
  const input = withDepartures(baseline, "B", 123);
  assert.equal(input.model.B.departures, 123);
  assert.equal("people" in input.model.B, false);
  close(evaluate(input).B.components.people, 123 * 0.8 * 20500);
});
