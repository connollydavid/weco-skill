---
name: local-mode
description: Running Weco in local mode — no Weco endpoints, no credits, the harness provides the intelligence
metadata:
  tags: ["local", "privacy", "containers"]
---

# Local Mode

Local mode is the default (`WECO_MODE` unset or `local`): the CLI never
talks to Weco's cloud. No login, no credits, no event reporting, no
installation identifier, no update pings. Opt into the cloud explicitly
with `WECO_MODE=weco` (plus `weco login`) when you want it.

## What changes

- **`weco run` (the cloud optimizer) is unavailable.** Use the local loop:
  `weco local run --eval-command "..." --metric <name> --goal min|max --steps N`.
  The configured agent harness (opencode) improves the code each step; the
  eval command measures it; the best result and every step land in
  `.weco/local-loop/`.
- **`weco observe` records locally** under `.weco/observe/` (append-only
  JSONL). `weco observe list` and `weco observe show --run-id <id>` read it
  back; nothing posts to the cloud and no dashboard opens.
- **`weco start <harness>` needs no login**: the dashboard relay stays
  offline. Claude Code runs on your own auth (`--billing claude` is the
  only billing); opencode runs on its own configured providers.
- **Evaluation execution can be sandboxed on your own infrastructure**:
  systemd user container units (Quadlet) via the `weco.local` container
  driver, or a reproducible chroot (hash-verified rootfs entered with
  `systemd-run --user`; a rootful fallback exists where direct GPU device
  access requires it).

## Privacy posture

Local mode makes no outbound connections. The no-phone-home contract is
enforced by the CLI's own test suite: any HTTP or socket egress during a
local-mode command is a bug.
