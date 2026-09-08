---
name: local-mode
description: The local contract — what runs where, and what never runs
metadata:
  tags: ["local", "privacy"]
---

# The Local Contract

Weco is local-only: no cloud service, no account, no credits, no
telemetry, no update pings. The intelligence is the configured agent
harness (driven by `weco local run`); the CLI provides the loop, the
measurement discipline, and the run history under `.weco/`.

- **`weco local run`** drives the configured harness each step against
  the metric-name eval contract; every step lands in
  `.weco/local-loop/` (steps.jsonl and report.json).
- **`weco observe`** records manual runs under `.weco/observe/` as
  append-only JSONL; `list` and `show` read it back.
- **`weco start <harness>`** launches claude (offline bridge), opencode,
  or codex headlessly; no login exists to require.
- **Evaluation execution** can be sandboxed with the container and
  chroot drivers (`weco.local`): systemd user container units, or a
  reproducible hash-verified chroot entered with systemd-run --user.

The no-phone-home contract is enforced by the CLI's own test suite:
any HTTP or socket egress during any command is a bug.
