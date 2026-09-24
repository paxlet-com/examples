"""Unit tests for the cluster gossip demonstration example."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

demo_path = Path(__file__).resolve().parent.parent / "examples" / "04-complex-scenarios" / "cluster-gossip-replication" / "demo_cluster_gossip.py"
spec = importlib.util.spec_from_file_location("demo_cluster_gossip", demo_path)
demo_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo_module)


class TestClusterGossipExample(unittest.TestCase):
    def test_paxlet_builder(self):
        paxlet = demo_module.build_audit_paxlet()
        self.assertIn("urn:paxlet:", paxlet["urn"])
        self.assertIn("manifest", paxlet)
        self.assertEqual(len(paxlet["manifest_sha256"]), 64)
        self.assertEqual(paxlet["manifest"]["entrypoint"], "audit_action.py")
        self.assertIn("audit_verified", paxlet["action_source"])

    def test_run_demo_mock_mode(self):
        report = demo_module.run_demo(mock=True)
        self.assertTrue(report.get("ok"))
        self.assertEqual(report.get("mode"), "simulated")
        self.assertEqual(report.get("nodes_reported"), 3)
        self.assertIn("taskand-node1", report.get("results", {}))
        self.assertIn("taskand-node2", report.get("results", {}))
        self.assertIn("taskand-node3", report.get("results", {}))


if __name__ == "__main__":
    unittest.main()
