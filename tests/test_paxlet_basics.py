#!/usr/bin/env python3
"""Test Paxlet Basics examples."""

from __future__ import annotations

from pathlib import Path
import unittest

from paxlet.manifest import load_manifest, package_digest, validate_manifest
from paxlet.runtime import run_action

ROOT = Path(__file__).resolve().parents[1]
BASICS_DIR = ROOT / "examples" / "01-paxlet-basics"


class TestPaxletBasics(unittest.TestCase):
    """Verifies that all 01-paxlet-basics examples are valid and functional."""

    def test_01_manifests_and_digests(self):
        self.assertTrue(BASICS_DIR.is_dir())
        expected_examples = ["hello", "science-fasta-gc", "sensor-calibrate", "statistics-mean", "text-wordcount"]
        for name in expected_examples:
            pkg_dir = BASICS_DIR / name
            self.assertTrue(pkg_dir.is_dir(), f"Missing example directory: {name}")

            m_path, manifest = load_manifest(pkg_dir)
            validation = validate_manifest(pkg_dir, manifest)
            self.assertTrue(validation.ok, f"Manifest invalid for {name}: {validation.errors}")

            digest = package_digest(pkg_dir, manifest)
            self.assertTrue(digest.startswith("sha256:"), f"Invalid digest for {name}: {digest}")

    def test_02_execution_and_receipts(self):
        scenarios = {
            "hello": {"input": {"name": "TestUser"}, "expected_key": "message"},
            "science-fasta-gc": {"input": {"fasta_path": "data/sample.fasta"}, "expected_key": "gc_fraction"},
            "sensor-calibrate": {"input": {"values": [1.0, 2.0, 3.0], "gain": 2.0, "offset": 1.0}, "expected_key": "values"},
            "statistics-mean": {"input": {"values": [5.0, 15.0, 25.0]}, "expected_key": "mean"},
            "text-wordcount": {"input": {"text": "One two three four"}, "expected_key": "words"},
        }

        for name, spec in scenarios.items():
            pkg_dir = BASICS_DIR / name
            m_path, manifest = load_manifest(pkg_dir)
            action = list(manifest["actions"].keys())[0]

            output, receipt, receipt_path = run_action(pkg_dir, action, spec["input"])
            self.assertEqual(receipt["exit_code"], 0, f"Non-zero exit for {name}: {output}")
            self.assertIn(spec["expected_key"], output, f"Missing output key {spec['expected_key']} in {name}")
            self.assertEqual(receipt["action"], action)
            self.assertTrue(Path(receipt_path).is_file())


if __name__ == "__main__":
    unittest.main()
