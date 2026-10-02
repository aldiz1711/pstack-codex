import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import subprocess
import unittest
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("packager", ROOT / "scripts/package-plugin.py")
PACKAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGER)


class PackagingTests(unittest.TestCase):
    def test_complete_pack_and_local_invocation_contract(self):
        result = PACKAGER.validate(ROOT)
        self.assertEqual((result["skills"], result["playbooks"]), (49, 23))
        metadata = json.loads((ROOT / "tests/fixtures/local-invocation-metadata.json").read_text())
        for relative, expected in metadata.items():
            with self.subTest(resource=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)

    def test_reproducible_account_archive_and_resource_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first.zip", Path(directory) / "second.zip"
            report = PACKAGER.package(ROOT, first)
            PACKAGER.package(ROOT, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                names = archive.namelist()
                self.assertNotIn("pstack-codex/.agents/plugins/marketplace.json", names)
                self.assertIn("pstack-codex/.codex-plugin/plugin.json", names)
                self.assertEqual(len([name for name in names if name.endswith("/SKILL.md")]), 49)
                self.assertEqual(len(names), len(set(names)))
                for name in names:
                    relative = name.removeprefix("pstack-codex/")
                    self.assertEqual(archive.read(name), (ROOT / relative).read_bytes())
            self.assertTrue(report["excluded_marketplace"])

    def test_source_archive_retains_only_the_intended_registration_difference(self):
        with tempfile.TemporaryDirectory() as directory:
            account, source = Path(directory) / "account.zip", Path(directory) / "source.zip"
            PACKAGER.package(ROOT, account)
            PACKAGER.package(ROOT, source, account=False)
            with zipfile.ZipFile(account) as a, zipfile.ZipFile(source) as s:
                self.assertEqual(set(s.namelist()) - set(a.namelist()), {"pstack-codex/.agents/plugins/marketplace.json"})
                for name in a.namelist():
                    self.assertEqual(a.read(name), s.read(name))

    def test_manual_only_sibling_resolution_with_sparse_catalog(self):
        namespace = "skill://verified-pstack"
        catalog = {"poteto-mode": namespace + "/poteto-mode"}
        def read(package, resource="SKILL.md"):
            name = package.removeprefix(namespace + "/")
            self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file())
            relative = Path(resource)
            file = (ROOT / "skills" / name / relative).resolve()
            self.assertTrue(file.is_relative_to(ROOT / "skills" / name))
            return file.read_text()
        prefix = catalog["poteto-mode"].rsplit("/", 1)[0]
        how = prefix + "/how"
        self.assertNotIn("how", catalog)
        self.assertIn("# How", read(how))
        self.assertIn("explore", read(how, "references/explorer-prompt.md").lower())
        self.assertIn("explain", read(how, "references/explainer-prompt.md").lower())
        with self.assertRaises(AssertionError):
            read(how, "../poteto-mode/SKILL.md")

    def test_archive_excludes_untracked_and_ignored_user_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            extras = [".env.local", ".codex/pstack-models.md", "private-build.log"]
            for name in extras:
                (root / name).write_text("private fixture\n")
            output = Path(directory) / "account.zip"
            PACKAGER.package(root, output)
            with zipfile.ZipFile(output) as archive:
                for name in extras:
                    self.assertNotIn("pstack-codex/" + name, archive.namelist())
                self.assertIn("pstack-codex/skills/setup-pstack/SKILL.md", archive.namelist())

    def test_archive_rejects_required_prompt_missing_from_export(self):
        for remove_from_disk in [False, True]:
            with self.subTest(remove_from_disk=remove_from_disk), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "source"
                shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
                subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
                subprocess.run(["git", "add", "."], cwd=root, check=True)
                prompt = "skills/no-comments/references/comment-sicko.md"
                subprocess.run(["git", "rm", "--cached", "--quiet", prompt], cwd=root, check=True)
                if remove_from_disk:
                    (root / prompt).unlink()
                output = Path(directory) / "account.zip"
                with self.assertRaisesRegex(ValueError, "required package resources.*comment-sicko"):
                    PACKAGER.package(root, output)
                self.assertFalse(output.exists())

    def test_symlink_and_output_inside_source_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            PACKAGER.package(ROOT, ROOT / "invalid.zip")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "fixture"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            (root / "unsafe-link").symlink_to(root / "LICENSE")
            with self.assertRaisesRegex(ValueError, "symlink"):
                PACKAGER.validate(root)


if __name__ == "__main__":
    unittest.main()
