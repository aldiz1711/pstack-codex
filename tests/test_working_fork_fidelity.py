import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BASELINE = json.loads((ROOT / "tests/fixtures/working-fork-files.json").read_text())
HOST_ONLY = {
    ".codex-plugin/plugin.json", ".codex/agents/comment-sicko.toml", ".codex/agents/poteto-agent.toml",
    ".gitignore", "README.md", "docs/guide/01-setup.md", "skills/how/SKILL.md", "skills/no-comments/SKILL.md",
    "skills/interrogate/SKILL.md", "skills/poteto-mode/playbooks/multi-phase-plan.md",
    "skills/poteto-mode/playbooks/orchestrate.md",
    "skills/poteto-mode/SKILL.md", "skills/setup-pstack/SKILL.md",
}


class WorkingForkFidelityTests(unittest.TestCase):
    def test_complete_baseline_inventory_is_preserved(self):
        self.assertEqual(BASELINE["baseline"], "ffb1958178011f532a2e1ee2376844120fcc0ce0")
        self.assertEqual(len(BASELINE["files"]), 202)
        for name, expected in BASELINE["files"].items():
            with self.subTest(resource=name):
                file = ROOT / name
                self.assertTrue(file.is_file())
                if name not in HOST_ONLY:
                    self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), expected["sha256"])
                self.assertEqual(bool(file.stat().st_mode & 0o111), expected["mode"] == "100755")

    def test_unchanged_playbooks_and_helpers_have_no_new_behavior(self):
        original = BASELINE["files"]
        for prefix in ["skills/poteto-mode/playbooks/", "skills/poteto-mode/scripts/"]:
            paths = sorted(path for path in original if path.startswith(prefix))
            self.assertTrue(paths)
            for path in paths:
                if path not in HOST_ONLY:
                    self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), original[path]["sha256"])
        for forbidden in ["host-runtime.md", "model-config.md", "skill-index.json"]:
            self.assertEqual(list((ROOT / "skills").rglob(forbidden)), [])

    def test_all_skill_models_frontmatter_and_workflow_headings_match(self):
        self.assertEqual(len(BASELINE["skill_contracts"]), 49)
        for path, contract in BASELINE["skill_contracts"].items():
            with self.subTest(skill=path):
                text = (ROOT / path).read_text()
                self.assertEqual(hashlib.sha256(text.split("---", 2)[1].encode()).hexdigest(), contract["frontmatter_sha256"])
                self.assertEqual(re.findall(r"`gpt-[^`]+`", text), contract["models"])
                self.assertEqual(re.findall(r"^#{1,6} .+", text, re.MULTILINE), contract["headings"])

    def test_inline_default_map_and_panels_without_setup(self):
        text = (ROOT / "skills/setup-pstack/SKILL.md").read_text()
        block = re.search(r"```text\n(.*?)\n```", text, re.DOTALL).group(1)
        roles = {}
        for line in block.splitlines():
            if line.startswith("#"):
                continue
            aliases, choices = line.split(": ", 1)
            entries = [tuple(part.strip() for part in value.split("|")) for value in choices.split(", ")]
            for alias in aliases.split(", "):
                roles[alias] = entries
        for role in ["feature", "refactoring", "bug-fix", "perf-issue", "hillclimb", "how explorer", "why investigators", "swarm workers"]:
            self.assertEqual(roles[role], [("gpt-6-luna", "xhigh")])
        for role in ["judgment and prose", "hardest tasks", "how explainer", "why synthesizer", "reflect judgment", "divergent", "synthesizer"]:
            self.assertEqual(roles[role], [("gpt-6-astra", "max")])
        self.assertEqual(roles["reflect tooling"], [("gpt-6-sol", "max")])
        for role in ["arena runners", "architect runners"]:
            self.assertEqual(roles[role], [("gpt-6-astra", "max")] * 4)
        for role in ["interrogate reviewers", "arena cross-judge pool"]:
            self.assertEqual(roles[role], [("inherit-parent",)])
        self.assertIn("# budget: unlimited (max)", block)

    def test_packaged_role_fallbacks_keep_the_original_prompt(self):
        for source, target in [("agents/poteto-agent.md", "skills/poteto-mode/references/poteto-agent.md"),
                               ("agents/comment-sicko.md", "skills/no-comments/references/comment-sicko.md")]:
            self.assertEqual((ROOT / source).read_bytes(), (ROOT / target).read_bytes())

    def test_local_hook_needs_no_map_and_retains_custom_home(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, CODEX_HOME=directory)
            command = [sys.executable, str(ROOT / "hooks/load-pstack-models.py")]
            result = subprocess.run(command, env=env, capture_output=True, text=True, check=True)
            self.assertEqual(result.stdout, "")
            map_file = Path(directory) / "pstack-models.md"
            choices = "# budget: small\nfeature: inherit-parent\nhardest tasks: gpt-6-astra | medium\n"
            map_file.write_text(choices)
            loaded = subprocess.run(command, env=env, capture_output=True, text=True, check=True)
            self.assertTrue(loaded.stdout.endswith(choices))
            self.assertIn("explicit user instructions take precedence", loaded.stdout)
            self.assertEqual(map_file.read_text(), choices)


if __name__ == "__main__":
    unittest.main()
