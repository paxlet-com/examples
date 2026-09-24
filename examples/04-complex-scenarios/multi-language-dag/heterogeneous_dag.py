#!/usr/bin/env python3
"""Complex Scenario 2: Multi-Language Heterogeneous DAG Pipeline.

Combines:
- Step 1 (Bash): Prepares input dataset and text processing.
- Step 2 (Python): Statistical aggregation and data synthesis.
- Step 3 (Bash): Final output packaging and checksumming.

Compiles into a single verifiable standalone bundle packaged as a Paxlet.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from nl_dsl_sh import Engine, Plan
from nl_dsl_sh.interop import export_paxlet
from paxlet.manifest import load_manifest, package_digest, validate_manifest
from paxlet.runtime import run_action


def build_heterogeneous_plan() -> dict:
    return {
        "schema_version": "0.1",
        "name": "heterogeneous-multi-language-pipeline",
        "steps": [
            {
                "id": "step1_bash_source",
                "kind": "generate",
                "language": "bash",
                "code": (
                    "printf '42\\n100\\n256\\n512\\n' > /tmp/paxlet-numbers.dat\n"
                    "printf 'GENERATED_DATASET_OK\\n'\n"
                ),
            },
            {
                "id": "step2_python_analytics",
                "kind": "generate",
                "language": "python",
                "needs": ["step1_bash_source"],
                "code": (
                    "from pathlib import Path\n"
                    "nums = [int(line.strip()) for line in Path('/tmp/paxlet-numbers.dat').read_text().splitlines() if line.strip()]\n"
                    "avg = sum(nums) / len(nums)\n"
                    "print(f'NUMBERS_COUNT={len(nums)}')\n"
                    "print(f'NUMBERS_AVERAGE={avg}')\n"
                ),
            },
            {
                "id": "step3_bash_cleanup",
                "kind": "generate",
                "language": "bash",
                "needs": ["step2_python_analytics"],
                "code": (
                    "rm -f /tmp/paxlet-numbers.dat\n"
                    "printf 'CLEANUP_COMPLETED_SUCCESSFULLY\\n'\n"
                ),
            },
        ],
    }


def run_heterogeneous_pipeline() -> dict:
    plan_dict = build_heterogeneous_plan()
    plan = Plan.model_validate(plan_dict)

    engine = Engine()
    artifact = engine.compile(plan, format="python")

    with tempfile.TemporaryDirectory(prefix="hetero-paxlet-") as tmpdir:
        pkg_dir = Path(tmpdir) / "hetero-pipeline"
        export_paxlet(
            artifact,
            pkg_dir,
            urn="urn:paxlet:enterprise:multi-language:v1",
            permissions={"filesystem": {"read": ["/tmp"], "write": ["/tmp"]}},
        )

        manifest_path, manifest = load_manifest(pkg_dir)
        validation = validate_manifest(pkg_dir, manifest)
        if not validation.ok:
            raise RuntimeError(f"Manifest invalid: {validation.errors}")

        digest = package_digest(pkg_dir, manifest)
        output, receipt, receipt_path = run_action(pkg_dir, "run", {"stdin": ""})

        return {
            "urn": manifest["identity"]["urn"],
            "digest": digest,
            "exit_code": output["exit_code"],
            "stdout": output["stdout"],
            "receipt": receipt,
            "report": artifact.report,
        }


if __name__ == "__main__":
    res = run_heterogeneous_pipeline()
    print(f"Heterogeneous pipeline executed: {res['urn']}")
    print(f"Digest: {res['digest']}")
    print(f"Stdout:\n{res['stdout'].strip()}")
