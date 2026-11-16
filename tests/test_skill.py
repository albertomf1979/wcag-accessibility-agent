"""
Local checks for the portable skill, the Claude Code plugin manifests,
the Claude.ai package and the Python CLI prompt loading.
No API key or network access required: python -m unittest discover -s tests
"""

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "wcag-accessibility"
SKILL_MD = SKILL_DIR / "SKILL.md"


def frontmatter(text: str) -> dict:
    """Parse the flat `key: value` frontmatter used by SKILL.md."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, "SKILL.md must start with a YAML frontmatter block"
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


class SkillTests(unittest.TestCase):
    def test_frontmatter_follows_agent_skills_spec(self):
        fields = frontmatter(SKILL_MD.read_text(encoding="utf-8"))
        self.assertEqual(fields["name"], "wcag-accessibility")
        self.assertEqual(fields["name"], SKILL_DIR.name)
        self.assertRegex(fields["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(fields["name"]), 64)
        self.assertTrue(0 < len(fields["description"]) <= 1024)
        self.assertLessEqual(len(fields.get("compatibility", "")), 500)
        self.assertLessEqual(set(fields), {"name", "description", "license", "compatibility", "metadata", "allowed-tools"})

    def test_internal_references_exist(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        paths = set(re.findall(r"(?:references|scripts)/[\w.-]+\.(?:md|mjs)", text))
        self.assertTrue(paths)
        for rel in paths:
            self.assertTrue((SKILL_DIR / rel).is_file(), f"missing {rel}")
        # Every bundled reference is reachable from SKILL.md.
        for ref in (SKILL_DIR / "references").glob("*.md"):
            self.assertIn(f"references/{ref.name}", paths)

    def test_wcag21_catalog_counts(self):
        text = (SKILL_DIR / "references" / "criterios-wcag21.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| (\d\.\d+\.\d+) [^|]*\| (A{1,3}) \|", text, re.M)
        wcag22 = set(re.findall(r"^\| (\d\.\d+\.\d+) [^|]*\[2\.2\]", text, re.M))
        levels = [lvl for sc, lvl in rows if sc not in wcag22]
        self.assertEqual((levels.count("A"), levels.count("AA"), levels.count("AAA")), (30, 20, 28))
        self.assertEqual(len(wcag22), 9)


class PluginTests(unittest.TestCase):
    def test_manifests(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["name"], "wcag")
        self.assertEqual(market["name"], "wcag-accessibility")
        [entry] = market["plugins"]
        self.assertEqual(entry["name"], plugin["name"])
        self.assertTrue((ROOT / entry["source"] / "skills" / "wcag-accessibility" / "SKILL.md").is_file())


class PackageTests(unittest.TestCase):
    def test_claude_ai_package_matches_skill_dir(self):
        with zipfile.ZipFile(ROOT / "wcag-accessibility.skill") as zf:
            packaged = {n: zf.read(n) for n in zf.namelist() if not n.endswith("/")}
        expected = {
            f"wcag-accessibility/{p.relative_to(SKILL_DIR).as_posix()}": p.read_bytes()
            for p in SKILL_DIR.rglob("*")
            if p.is_file() and p.name != ".DS_Store"
        }
        self.assertEqual(sorted(packaged), sorted(expected), "run `make skill-package`")
        self.assertEqual(packaged, expected, "wcag-accessibility.skill is stale: run `make skill-package`")


class CliTests(unittest.TestCase):
    def test_system_prompt_builds_from_any_working_directory(self):
        code = (
            "import sys; sys.path.insert(0, sys.argv[1]);"
            "from system_prompt import build_system_prompt, build_initial_prompt;"
            "[build_system_prompt(d, 'AA') for d in ('ux', 'ui', 'desarrollo', 'dev', 'todos')];"
            "p = build_system_prompt('todos', 'AA');"
            "print(len(p), len(build_initial_prompt()))"
        )
        with tempfile.TemporaryDirectory() as cwd:
            out = subprocess.run([sys.executable, "-c", code, str(ROOT)], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_system_prompt_includes_skill_and_references(self):
        sys.path.insert(0, str(ROOT))
        from system_prompt import build_system_prompt

        prompt = build_system_prompt("todos", "AA")
        self.assertIn("name: wcag-accessibility", prompt)
        for ref in (SKILL_DIR / "references").glob("*.md"):
            first_heading = next(l for l in ref.read_text(encoding="utf-8").splitlines() if l.startswith("#"))
            self.assertIn(first_heading, prompt, ref.name)

    @unittest.skipUnless(importlib.util.find_spec("httpx") and importlib.util.find_spec("bs4"), "CLI deps not installed")
    def test_cli_axe_tool_uses_skill_script(self):
        sys.path.insert(0, str(ROOT))
        import tools

        self.assertTrue(tools.AXE_SCAN_SCRIPT.is_file())


if __name__ == "__main__":
    unittest.main()
