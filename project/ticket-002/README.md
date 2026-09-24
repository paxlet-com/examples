# Ticket 002: Import, verify, and expand Paxlet ecosystem examples

- **ID**: ticket-002
- **Owner**: Tom Softreck
- **Status**: IN_PROGRESS
- **Workflow state**: VALIDATION
- **Created**: 2026-09-24

## Goal and scope

Import, verify, and document the baseline Paxlet ecosystem examples (`01-paxlet-basics`: `hello`, `science-fasta-gc`, `sensor-calibrate`, `statistics-mean`, `text-wordcount`), and provide automated test suite `tests/test_paxlet_basics.py` verifying manifests and execution.

## Acceptance criteria

- [x] AC-01: Import and verify baseline Paxlet examples in `examples/01-paxlet-basics/`.
- [x] AC-02: Verify manifest validation and cryptographic package digests for all 5 baseline examples.
- [x] AC-03: Implement automated test suite `tests/test_paxlet_basics.py` asserting clean execution and valid output.
- [x] AC-04: Provide root `examples/README.md` catalog documentation.
- [x] AC-05: Governance check passes cleanly with 0 errors and 0 warnings.

