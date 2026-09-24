# Ticket 004: Import and verify NL-DSL-SH compilation examples

- **ID**: ticket-004
- **Owner**: Tom Softreck
- **Status**: IN_PROGRESS
- **Workflow state**: VALIDATION
- **Created**: 2026-09-24

## Goal and scope

Import, verify, and validate NL-DSL-SH compilation examples (`02-nldsl-compilation`), including modular shell scripts (`modular-scripts`), offline catalog generation (`catalog-offline`), and compiled standalone executable Paxlet packages (`compiled-bundle`), supported by automated test suite `tests/test_nldsl_compilation.py`.

## Acceptance criteria

- [x] AC-01: Import modular bash library scripts (`hello.sh`, `lib.sh`, `with_library.sh`).
- [x] AC-02: Import offline catalog definition with plans and permissions (`catalog.json`, `plan.json`, `permissions.json`, `offline.py`).
- [x] AC-03: Import compiled standalone Paxlet bundle (`action.py`, `task.py`, `paxlet.json`, `compile-report.json`).
- [x] AC-04: Implement automated test suite `tests/test_nldsl_compilation.py` asserting clean execution and valid outputs.
- [x] AC-05: Governance checks pass cleanly with 0 errors and 0 warnings.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
