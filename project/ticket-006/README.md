# Ticket 006: Demonstrate autonomous cluster gossip replication and distributed Paxlet execution

- **ID**: ticket-006
- **Owner**: antigravity
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-09-24

## Goal and scope

Add a comprehensive demonstration scenario showcasing natural language planning, compilation to Paxlet, autonomous background gossip propagation across a Taskand cluster, and concurrent multi-node execution with tamper-evident receipts.

## Acceptance criteria

- [x] AC-01: Example directory `examples/04-complex-scenarios/cluster-gossip-replication/` created with `demo_cluster_gossip.py`, `plan_distributed_audit.json`, and `README.md`.
- [x] AC-02: Support both simulated standalone execution (`--mock`) and live 3-node cluster execution (`--nodes ...`).
- [x] AC-03: Unit test suite `tests/test_cluster_gossip_example.py` added and passing.
- [x] AC-04: Catalog index updated in `examples/README.md`.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
