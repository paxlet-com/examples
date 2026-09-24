# Autonomous Cluster Gossip Replication & Distributed Paxlet Execution

Demonstrates the distributed multi-node architecture of Taskand and Paxlet running across independent nodes.

## Architecture

```
[ Natural Language Request ]
            │
            ▼
[ nl-dsl-sh Compiler ]
            │
            ▼
[ Paxlet Package ] ──> (Immutable manifest & SHA-256 digest)
            │
            ▼
[ Node 1: Taskand Procedure ]
            │
    (Background Gossip Daemon)
            ├─── Continuous poll (/healthz, /.well-known/catalog.json)
            ├─── Autonomous pull (package transfer)
            └─── Automatic activation (auto-approve)
            │
      ┌─────┴─────┐
      ▼           ▼
  [ Node 2 ]  [ Node 3 ]
      │           │
      └─────┬─────┘
            ▼
[ Concurrent Execution & Tamper-Evident Receipts ]
```

## Running the Demo

### Simulated / Standalone Mode

Run directly from any environment without spinning up the full Docker cluster:

```bash
python3 examples/04-complex-scenarios/cluster-gossip-replication/demo_cluster_gossip.py --mock
```

### Live 3-Node Cluster Mode

When the Taskand 3-node Docker Compose cluster is running (e.g. from `paxlet-com/tests`):

```bash
python3 examples/04-complex-scenarios/cluster-gossip-replication/demo_cluster_gossip.py \
  --nodes http://127.0.0.1:8071 http://127.0.0.1:8072 http://127.0.0.1:8073
```

## Key Capabilities Demonstrated

1. **Zero-Operator Replication**: The background gossip worker in each Taskand gateway discovers new procedures on peer nodes and replicates them without needing an operator to trigger sync.
2. **Deterministic Cryptographic Verification**: Every replicated package has its SHA-256 manifest and action digest checked before entry into `generated/`.
3. **Multi-Node Concurrency**: Tasks run on independent nodes with node-specific isolation and emit tamper-evident execution receipts.
