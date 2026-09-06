"""Package invariants for the weco skill package.

Stdlib-only (no dependencies): validates the skill frontmatter against the
constraints the consuming harnesses apply, keeps the per-harness trigger
snippets consistent, checks recorded executable bits, and exercises the
interactive installer's placement for every supported harness against a
throwaway HOME.
"""

from __future__ import annotations

import re
import subprocess
import pathlib
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"

# opencode validates the skill name against this; keep the package conformant.
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _frontmatter() -> dict[str, str]:
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "SKILL.md must open with YAML frontmatter"
    end = text.index("\n---\n", 4)
    block = text[4:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def test_skill_frontmatter_name() -> None:
    name = _frontmatter().get("name")
    assert name == "weco"
    assert SKILL_NAME_RE.match(name or "")


def test_skill_frontmatter_description_length() -> None:
    # The consuming harnesses accept 1..1024 characters of description.
    fields = _frontmatter()
    assert "description" in fields
    body = SKILL.read_text(encoding="utf-8")
    start = body.index("description:")
    end = body.index("\n---\n", start)
    description = body[start + len("description:") : end].strip()
    assert 1 <= len(description) <= 1024


def test_version_file_is_three_component() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert re.fullmatch(r"\d+\.\d+\.\d+", version)


def test_trigger_snippets_are_consistent() -> None:
    snippets = ROOT / "snippets"
    claude = (snippets / "claude.md").read_bytes()
    for name in ("cursor.md", "opencode.md", "zcode.md"):
        assert claude == (snippets / name).read_bytes(), name


def test_recorded_executable_bits() -> None:
    def mode(path: str) -> str:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-s", "--", path],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
        assert out, f"{path} is not tracked"
        return out[0]

    assert mode("install.sh") == "100755"
    assert mode("assets/evaluate-wrapper.sh") == "100755"


@pytest.mark.parametrize(
    ("choice", "expected"),
    [
        ("1", [".claude/skills/weco/SKILL.md", ".claude/skills/weco/CLAUDE.md"]),
        ("2", [".cursor/skills/weco/SKILL.md", ".cursor/rules/weco.mdc"]),
        ("3", [".config/opencode/skills/weco/SKILL.md"]),
        ("4", [".zcode/skills/weco/SKILL.md"]),
        (
            "5",
            [
                ".claude/skills/weco/SKILL.md",
                ".cursor/skills/weco/SKILL.md",
                ".config/opencode/skills/weco/SKILL.md",
                ".zcode/skills/weco/SKILL.md",
            ],
        ),
    ],
)
def test_installer_placement(choice: str, expected: list[str]) -> None:
    with tempfile.TemporaryDirectory() as home:
        subprocess.run(
            ["bash", str(ROOT / "install.sh")],
            input=f"{choice}\n",
            capture_output=True,
            text=True,
            env={"HOME": home, "PATH": "/usr/bin:/bin"},
            check=True,
        )
        for rel in expected:
            assert (pathlib.Path(home) / rel).is_file(), rel


def test_installer_syntax() -> None:
    subprocess.run(["bash", "-n", str(ROOT / "install.sh")], check=True)
