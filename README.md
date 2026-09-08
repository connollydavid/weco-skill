# Weco AI Skill

AI-powered code optimization skill for Claude Code, Cursor, opencode, and ZCode. Runs locally: no cloud service, no account, no telemetry.

## What is this?

This skill teaches your AI coding assistant the local Weco optimization workflow. When you ask to "make this faster" or "improve accuracy", the assistant will:

1. Analyze your code and environment
2. Set up an evaluation benchmark
3. Run the local optimization loop (the assistant's harness provides the intelligence)
4. Present results with the numbers against the baseline
5. Apply changes (with your approval)

## Installation

### Recommended: Weco CLI

The easiest way to install is via the Weco CLI, which sets up the skill and trigger rules for your agent.

**Install the CLI (from this fork):**

```bash
uv tool install "weco @ git+https://github.com/connollydavid/weco-cli.git"
```

**Install the skill:**

```bash
weco setup cursor       # For Cursor
weco setup claude-code  # For Claude Code
weco setup opencode     # For opencode
weco setup zcode        # For ZCode (also wires the z.ai MCP servers)
```

### What Gets Installed

**Claude Code:**
```
~/.claude/skills/weco/
├── CLAUDE.md          # Trigger snippet (Claude reads this)
├── SKILL.md           # Full optimization workflow
├── references/        # Advanced documentation
└── assets/            # Template evaluation scripts
```

**Cursor:**
```
~/.cursor/
├── rules/
│   └── weco.mdc        # Always-on trigger rule
└── skills/
    └── weco/
        ├── SKILL.md       # Full optimization workflow
        ├── references/    # Advanced documentation
        └── assets/        # Template evaluation scripts
```

**opencode:**
```
~/.config/opencode/skills/weco/
├── SKILL.md           # Full workflow; opencode advertises the skill from
│                      # the frontmatter description (no trigger file needed)
├── references/        # Advanced documentation
└── assets/            # Template evaluation scripts
```

## Usage

Once installed, just ask your AI assistant to optimize code:

- "Make this function faster"
- "Optimize this for speed"
- "Improve the accuracy of this model"

The skill guides the local workflow: baseline, evaluation setup, the loop
(`weco local run`) or manual tracking (`weco observe`), and a numbered
report. See `references/local-mode.md` for the contract.

## Requirements

- The Weco CLI (from this fork; the upstream PyPI package carries the cloud CLI)
- Claude Code, Cursor, opencode, or ZCode

## Files

```
weco-skill/
├── .cursor-plugin/       # Cursor plugin manifest
│   └── plugin.json
├── SKILL.md              # Full skill instructions (source of truth)
├── CLAUDE.md             # Trigger snippet for Claude Code (ships with skill)
├── install.sh            # Interactive installer
├── README.md             # This file
├── rules/                # Cursor plugin rules
│   └── weco.mdc          # Always-on trigger rule for Cursor
├── snippets/             # Trigger snippets (used by weco-cli installer)
│   ├── claude.md         # Claude Code trigger
│   ├── claude-global.md  # Claude Code global trigger
│   ├── cursor.md         # Cursor trigger (.mdc rule)
│   ├── opencode.md       # opencode trigger (frontmatter description is primary)
│   └── zcode.md          # ZCode trigger
├── references/           # Advanced documentation
│   ├── benchmarking.md
│   ├── ml-evaluation.md
│   ├── gpu-profiling.md
│   └── ...
└── assets/               # Template evaluation scripts
    ├── evaluate-speed.py
    ├── evaluate-accuracy.py
    └── ...
```

## Learn More

- [Weco Documentation](https://weco.ai/docs)
- [Claude Code](https://claude.ai/code)
- [Cursor](https://cursor.sh)
