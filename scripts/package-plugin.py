#!/usr/bin/env python3
"""Validate and reproducibly package the complete PStack plugin."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import zipfile


EXCLUDED_PARTS = {".git", "node_modules", "__pycache__", "dist"}
MARKETPLACE = ".agents/plugins/marketplace.json"


def validate(root: Path) -> dict:
    portable = json.loads((root / "plugin.json").read_text())
    local = json.loads((root / ".codex-plugin/plugin.json").read_text())
    name = portable["name"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError("invalid plugin name")
    if portable["version"] != local["version"] or name != local["name"]:
        raise ValueError("manifest identity or version differs")
    if any(key in portable for key in ("skills", "mcpServers", "apps", "interface")):
        raise ValueError("non-portable root manifest field")
    interface = portable["extensions"]["com.openai"]["interface"]
    if interface != local["interface"] or len(interface["shortDescription"]) > 30:
        raise ValueError("manifest interface differs or subtitle is too long")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if len(skills) != 49:
        raise ValueError("the complete pack requires 49 skills")
    names = []
    for file in skills:
        text = file.read_text()
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            raise ValueError(f"missing frontmatter in {file}")
        frontmatter = text.split("---", 2)[1]
        match = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
        if match is None or match[1] != file.parent.name:
            raise ValueError(f"skill name mismatch in {file}")
        if not re.search(r"^description:\s*\S", frontmatter, re.MULTILINE):
            raise ValueError(f"missing skill description in {file}")
        names.append(file.parent.name)
    index = json.loads((root / "skills/poteto-mode/references/skill-index.json").read_text())
    if index["plugin"] != name or index["skills"] != {value: value for value in names}:
        raise ValueError("skill index differs from the complete pack")
    playbooks = list((root / "skills/poteto-mode/playbooks").glob("*.md"))
    if len(playbooks) != 23:
        raise ValueError("the complete pack requires 23 playbooks")
    for file in root.rglob("*"):
        if EXCLUDED_PARTS.intersection(file.relative_to(root).parts):
            continue
        if file.is_symlink():
            raise ValueError(f"symlink cannot be packaged: {file}")
    for file in (root / "skills").rglob("*.md"):
        for link in re.findall(r"\]\(([^\s)]+)", file.read_text()):
            if link == "url" or link.startswith("#") or re.match(r"[a-z][a-z0-9+.-]*:", link):
                continue
            destination = (file.parent / link.split("#", 1)[0]).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                raise ValueError(f"unresolved resource in {file}: {link}")
    return {"name": name, "version": portable["version"], "skills": len(skills), "playbooks": len(playbooks)}


def tracked_source(root: Path) -> list[Path]:
    try:
        checkout = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=root, text=True, stderr=subprocess.PIPE
        ).strip()
        if Path(checkout).resolve() != root:
            raise ValueError("package from the repository root checkout")
        names = subprocess.check_output(["git", "ls-files", "-z", "--cached"], cwd=root)
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        raise ValueError("packaging requires Git and a source checkout") from error
    files = []
    for name in names.decode("utf-8").split("\0"):
        if not name:
            continue
        file = root / name
        if not file.resolve().is_relative_to(root):
            raise ValueError(f"tracked source escapes the checkout: {name}")
        if not EXCLUDED_PARTS.intersection(Path(name).parts):
            files.append(file)
    return sorted(set(files))


def package(root: Path, output: Path, account: bool = True) -> dict:
    root, output = root.resolve(), output.resolve()
    if output.is_relative_to(root):
        raise ValueError("write the archive outside the plugin source directory")
    report = validate(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    files = []
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in tracked_source(root):
            relative = file.relative_to(root)
            if not file.is_file():
                raise ValueError(f"tracked source is missing: {relative}")
            if account and relative.as_posix() == MARKETPLACE:
                continue
            info = zipfile.ZipInfo(f"{report['name']}/{relative.as_posix()}", (1980, 1, 1, 0, 0, 0))
            mode = 0o755 if file.stat().st_mode & stat.S_IXUSR else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, file.read_bytes())
            files.append(relative.as_posix())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("archive integrity check failed")
    return {
        **report,
        "kind": "account" if account else "source",
        "files": len(files),
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "excluded_marketplace": account,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source", action="store_true", help="keep local marketplace registration")
    args = parser.parse_args()
    root = args.root.resolve()
    report = package(root, args.output, not args.source) if args.output else validate(root)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
