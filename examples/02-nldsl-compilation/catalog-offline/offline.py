"""Run from any directory after pip install -e .; no model/API required."""
from pathlib import Path
from nl_dsl_sh import Catalog, Engine, Plan, run

root = Path(__file__).parent
catalog = Catalog()
catalog.import_script(root / "scripts/hello.sh", script_id="urn:nl-dsl-sh:example:hello",
                      description="Przywitanie / greeting; positional arg 1: name",
                      aliases=["przywitaj się", "say hello"])
engine = Engine(catalog)
assert engine.plan("przywitaj sie").steps[0].kind == "reuse"
plan = Plan.model_validate_json((root / "plan.json").read_text(encoding="utf-8"))
artifact = engine.compile(plan)
result = run(artifact, expected_sha256=artifact.sha256)
print(result.stdout, end="")
print(result.receipt)
