import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


def bundled_roles(root):
    contract = root / "skills/setup-pstack/references/model-config.md"
    block = re.search(r"```text\n(.*?)\n```", contract.read_text(), re.DOTALL).group(1)
    roles = {}
    for line in block.splitlines():
        if line.startswith("#"):
            continue
        aliases, choices = line.split(": ", 1)
        entries = [tuple(part.strip() for part in choice.split("|")) for choice in choices.split(", ")]
        for alias in aliases.split(", "):
            if alias in roles:
                raise ValueError(f"duplicate role: {alias}")
            roles[alias] = entries
    return roles


class ModelContractTests(unittest.TestCase):
    def test_bundled_choices_and_original_panel_sizes(self):
        roles = bundled_roles(ROOT)
        ordinary = ["feature", "refactoring", "bug-fix", "perf-issue", "hillclimb",
                    "judgment and prose", "how explorer", "how explainer", "why investigators",
                    "why synthesizer", "reflect tooling", "reflect judgment", "divergent",
                    "synthesizer", "swarm workers"]
        for role in ordinary:
            with self.subTest(role=role):
                self.assertEqual(roles[role], [("gpt-6.1-sol", "max")])
        self.assertEqual(roles["hardest tasks"], [("gpt-6-astra", "max")])
        for role in ["arena runners", "architect runners"]:
            self.assertEqual(roles[role], [("gpt-6.1-sol", "max")] * 4)
        for role in ["arena cross-judge pool", "interrogate reviewers"]:
            self.assertEqual(roles[role], [("inherit-parent",)])

    def test_account_archive_contains_the_same_single_model_contract(self):
        import importlib.util
        import zipfile
        spec = importlib.util.spec_from_file_location("model_packager", ROOT / "scripts/package-plugin.py")
        packager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(packager)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "account.zip"
            packager.package(ROOT, output)
            with zipfile.ZipFile(output) as archive:
                names = [name for name in archive.namelist() if name.endswith("/model-config.md")]
                self.assertEqual(names, ["pstack-codex/skills/setup-pstack/references/model-config.md"])
                archive.extractall(directory)
            self.assertEqual(bundled_roles(Path(directory) / "pstack-codex"), bundled_roles(ROOT))

    def test_local_hook_reads_custom_codex_home_and_task_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, CODEX_HOME=directory)
            command = [sys.executable, str(ROOT / "hooks/load-pstack-models.py")]
            empty = subprocess.run(command, env=env, capture_output=True, text=True, check=True)
            self.assertEqual(empty.stdout, "")
            choices = "# budget: medium\nfeature: inherit-parent\nhardest tasks: gpt-6-astra | high\n"
            (Path(directory) / "pstack-models.md").write_text(choices)
            loaded = subprocess.run(command, env=env, capture_output=True, text=True, check=True)
            self.assertIn("explicit user instructions take precedence", loaded.stdout)
            self.assertTrue(loaded.stdout.endswith(choices))
            self.assertEqual((Path(directory) / "pstack-models.md").read_text(), choices)


if __name__ == "__main__":
    unittest.main()
