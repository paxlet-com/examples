#!/usr/bin/env python3
"""Test Taskand orchestration and complex multi-stage autonomy scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATION_DIR = ROOT / "examples" / "03-taskand-orchestration"
COMPLEX_DIR = ROOT / "examples" / "04-complex-scenarios"


class TestOrchestrationAndComplexScenarios(unittest.TestCase):
    """Verifies that orchestration examples and complex autonomy pipelines execute properly."""

    def test_01_orchestration_structures(self):
        network_scan = ORCHESTRATION_DIR / "network-scan" / "network-scan-task.mjs"
        self.assertTrue(network_scan.is_file())

        web_twin = ORCHESTRATION_DIR / "web-twin"
        self.assertTrue((web_twin / "web-twin-task.mjs").is_file())
        self.assertTrue((web_twin / "web-twin-github.json").is_file())
        self.assertTrue((web_twin / "web-twin-subactor.json").is_file())

        shell_wf = ORCHESTRATION_DIR / "shell-workflow"
        self.assertTrue((shell_wf / "hello.plan.json").is_file())
        self.assertTrue((shell_wf / "hello.permissions.json").is_file())

        with open(shell_wf / "hello.plan.json", encoding="utf-8") as f:
            plan = json.load(f)
            self.assertEqual(plan.get("name"), "Taskand hello")
            self.assertIn("steps", plan)

    def test_02_autonomous_devops_pipeline(self):
        script = COMPLEX_DIR / "autonomous-devops-pipeline" / "pipeline.py"
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("Pipeline executed successfully", res.stdout)
        self.assertIn("POLICY_GATE_PASSED", res.stdout)

    def test_03_heterogeneous_dag(self):
        script = COMPLEX_DIR / "multi-language-dag" / "heterogeneous_dag.py"
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("Heterogeneous pipeline executed", res.stdout)
        self.assertIn("CLEANUP_COMPLETED_SUCCESSFULLY", res.stdout)

    def test_04_digital_twin_browser_agent(self):
        script = COMPLEX_DIR / "digital-twin-browser-agent" / "browser_agent.py"
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("Digital Twin Browser Agent scenario generated", res.stdout)
        self.assertIn("bubblewrap", res.stdout)


if __name__ == "__main__":
    unittest.main()
