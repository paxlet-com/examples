# Ticket 001: Configure governance manifest for examples catalog

- **ID**: ticket-001
- **Owner**: Tom Softreck
- **Status**: IN_PROGRESS
- **Workflow state**: VALIDATION
- **Created**: 2026-09-24

## Goal and scope

Configure `.governance/manifest.json` to allow the `application` workstream to own `examples/**`.

## Acceptance criteria

- [x] AC-01: Update `manifest.json` so `application.ownedPaths` includes `examples/**`.
- [x] AC-02: Governance check passes with 0 errors and 0 warnings.
