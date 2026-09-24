#!/usr/bin/env python3
"""Test NL-DSL-SH compilation and bundle examples."""

from __future__ import annotations

from pathlib import Path
import unittest

from paxlet.manifest import load_manifest, validate_manifest
from paxlet.runtime import run_action

ROOT = Path(__file__).resolve().parents[1]
NLDSL_DIR = ROOT / "examples" / "02-nldsl-compilation"


class TestNldslCompilation(unittest.TestCase):
    """Verifies that NL-DSL-SH compilation examples and bundles function properly."""

    def test_01_catalog_offline_structure(self):
        catalog_dir = NLDSL_DIR / "catalog-offline"
        self.assertTrue((catalog_dir / "catalog.json").is_file())
        self.assertTrue((catalog_dir / "plan.json").is_file())
        self.assertTrue((catalog_dir / "permissions.json").is_file())
        self.assertTrue((catalog_dir / "offline.py").is_file())

        scripts_dir = catalog_dir / "scripts"
        self.assertTrue((scripts_dir / "hello.sh").is_file())
        self.assertTrue((scripts_dir / "lib.sh").is_file())
        self.assertTrue((scripts_dir / "with_library.sh").is_file())

    def test_02_modular_scripts_structure(self):
        modular_dir = NLDSL_DIR / "modular-scripts"
        self.assertTrue((modular_dir / "hello.sh").is_file())
        self.assertTrue((modular_dir / "lib.sh").is_file())
        self.assertTrue((modular_dir / "with_library.sh").is_file())

    def test_03_compiled_bundle_execution(self):
        bundle_dir = NLDSL_DIR / "compiled-bundle"
        m_path, manifest = load_manifest(bundle_dir)
        validation = validate_manifest(bundle_dir, manifest)
        self.assertTrue(validation.ok, f"Bundle manifest invalid: {validation.errors}")

        output, receipt, receipt_path = run_action(bundle_dir, "run", {"stdin": ""})
        self.assertEqual(receipt["exit_code"], 0)
        self.assertIn("Witaj, Tom!", output.get("stdout", ""))
        self.assertTrue(Path(receipt_path).is_file())


if __name__ == "__main__":
    unittest.main()
