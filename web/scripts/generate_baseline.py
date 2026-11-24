"""Copy authoritative Python parameters into the browser's versioned baseline."""
import hashlib
import json
import runpy
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root.parent / "simulation" / "run_validation.py"
module = runpy.run_path(str(source))
turnover = root.parent / "simulation" / "turnover_sensitivity.py"
# Read constants without importing plotting dependencies.
import ast
constants = {}
for node in ast.parse(turnover.read_text()).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        try:
            constants[node.targets[0].id] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            pass
unit_cost = constants["HIRING_COST"] + constants["NET_VACANCY_COST"] + constants["ANNUAL_PAY_DIFFERENCE"] * constants["FIRST_YEAR_FRACTION"]
cost_per_departure = constants["REPLACEMENT_RATE"] * unit_cost
if cost_per_departure <= 0:
    raise ValueError("A positive baseline unit cost is required to initialize departures")
model = {}
for regime, values in module["PARAMETERS"].items():
    model[regime] = {"scenarios": {s: {"attempts": values[s][0], "success": values[s][1], "loss": values[s][2]} for s in ("S1", "S2", "S3")}, "departures": module["pert_mean"](values["people"]) / cost_per_departure, "program": values["program"], "enforcement": values["oc"]}
output = {"schemaVersion": 2, "source": "simulation/run_validation.py", "sourceHash": hashlib.sha256(source.read_bytes()).hexdigest(), "turnoverSourceHash": hashlib.sha256(turnover.read_bytes()).hexdigest(), "model": model, "penalty": [1e7, 4e7, 1e8], "turnover": {"workforce": constants["WORKFORCE"], "replacementRate": constants["REPLACEMENT_RATE"], "hiring": constants["HIRING_COST"], "vacancy": constants["NET_VACANCY_COST"], "payDifference": constants["ANNUAL_PAY_DIFFERENCE"], "yearFraction": constants["FIRST_YEAR_FRACTION"]}, "pythonExpected": {r: module["analytic_expected_mean"](p) for r, p in module["PARAMETERS"].items()}}
(root / "src" / "baseline.json").write_text(json.dumps(output, indent=2) + "\n")
print("Updated src/baseline.json from Python inputs")
