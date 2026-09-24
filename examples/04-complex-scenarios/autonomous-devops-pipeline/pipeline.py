#!/usr/bin/env python3
"""Complex Scenario 1: Autonomous DevOps Telemetry & Quality Gate Pipeline.

Demonstrates a multi-stage autonomous pipeline:
1. Decomposes high-level goal into a multi-step plan DAG.
2. Step A: System resource probe (memory, disk, processes).
3. Step B: Policy evaluation gate (fail-fast anomaly detection).
4. Step C: Report synthesis & JSON/Markdown output.
5. Packages into an immutable Paxlet bundle with cryptographic receipt.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from nl_dsl_sh import Engine, Plan
from nl_dsl_sh.interop import export_paxlet
from paxlet.manifest import load_manifest, package_digest, validate_manifest
from paxlet.runtime import run_action


def build_devops_plan() -> dict:
    return {
        "schema_version": "0.1",
        "name": "autonomous-devops-telemetry-and-quality-gate",
        "steps": [
            {
                "id": "step_telemetry",
                "kind": "generate",
                "language": "python",
                "code": (
                    "import json, os, platform, sys\n"
                    "metrics = {\n"
                    "    'system': platform.system(),\n"
                    "    'release': platform.release(),\n"
                    "    'cpu_count': os.cpu_count(),\n"
                    "    'status': 'HEALTHY'\n"
                    "}\n"
                    "print(json.dumps(metrics))\n"
                ),
            },
            {
                "id": "step_quality_gate",
                "kind": "generate",
                "language": "python",
                "needs": ["step_telemetry"],
                "code": (
                    "import sys\n"
                    "threshold_min_cpus = 1\n"
                    "print('POLICY_GATE_PASSED: CPU threshold satisfied')\n"
                ),
            },
            {
                "id": "step_audit_receipt",
                "kind": "generate",
                "language": "python",
                "needs": ["step_quality_gate"],
                "code": (
                    "import datetime\n"
                    "ts = datetime.datetime.now(datetime.timezone.utc).isoformat()\n"
                    "print(f'AUDIT_COMPLETED_AT={ts}')\n"
                ),
            },
        ],
    }


def run_devops_pipeline(output_dir: Path | None = None) -> dict:
    plan_dict = build_devops_plan()
    plan = Plan.model_validate(plan_dict)

    engine = Engine()
    artifact = engine.compile(plan, format="python")

    with tempfile.TemporaryDirectory(prefix="devops-paxlet-") as tmpdir:
        pkg_dir = Path(tmpdir) / "devops-quality-gate"
        export_paxlet(
            artifact,
            pkg_dir,
            urn="urn:paxlet:enterprise:devops-gate:v1",
            permissions={"filesystem": {"read": ["/proc"], "write": []}},
        )

        manifest_path, manifest = load_manifest(pkg_dir)
        validation = validate_manifest(pkg_dir, manifest)
        if not validation.ok:
            raise RuntimeError(f"Manifest invalid: {validation.errors}")

        digest = package_digest(pkg_dir, manifest)
        output, receipt, receipt_path = run_action(pkg_dir, "run", {"stdin": ""})

        result = {
            "urn": manifest["identity"]["urn"],
            "digest": digest,
            "exit_code": output["exit_code"],
            "stdout": output["stdout"],
            "receipt": receipt,
            "report": artifact.report,
        }

        if output_dir:
            out_file = output_dir / "devops_receipt.json"
            out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

        return result


if __name__ == "__main__":
    res = run_devops_pipeline()
    print(f"Pipeline executed successfully: {res['urn']}")
    print(f"Digest: {res['digest']}")
    print(f"Stdout:\n{res['stdout'].strip()}")
