#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("tomllib is required (Python 3.11+)") from exc

TOKEN_RE = re.compile(r"\$\$\$([A-Z0-9_]+)\$\$\$")
DEFAULT_IGNORE_PATTERNS = {"**/.git/**", "**/.hg/**", "**/.svn/**", "**/__pycache__/**", "**/.venv/**"}


def git_root(start: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return Path(result.stdout.strip())


def load_palette(path: Path) -> dict[str, str]:
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    values = data.get("values", data)
    return {str(k).upper(): str(v) for k, v in values.items()}


def tokens_in(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text))


def find_templates(root: Path, ignore_patterns: set[str]) -> list[Path]:
    templates: list[Path] = []
    for tmpl in root.rglob("*.tmpl"):
        rel = tmpl.relative_to(root).as_posix()
        if any(fnmatch.fnmatch(rel, pat) for pat in ignore_patterns):
            continue
        templates.append(tmpl)
    return templates


def match_only(rel_path: str, patterns: list[str] | None) -> bool:
    if not patterns:
        return True
    return any(fnmatch.fnmatch(rel_path, pat) or rel_path.endswith(pat) for pat in patterns)


def render_template(text: str, mapping: dict[str, str], allow_missing: bool) -> tuple[str, set[str]]:
    missing: set[str] = set()

    def _replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in mapping:
            missing.add(key)
            return match.group(0) if allow_missing else match.group(0)
        return mapping[key]

    return TOKEN_RE.sub(_replace, text), missing


def write_if_changed(target: Path, content: str) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_text(encoding="utf-8") == content:
        return False
    target.write_text(content, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    git_top = git_root(here)
    root_default = git_top if git_top else here.parent

    parser = argparse.ArgumentParser(
        description="Render dotfile templates with $$$TOKENS$$$.",
        epilog="Exit codes: 0=success, 1=palette missing/error, 2=missing tokens",
    )
    parser.add_argument("--root", type=Path, default=root_default, help="Root directory to scan (default: git root or repo parent)")
    parser.add_argument("--palette", type=Path, default=root_default / "themegen" / "palette.toml", help="Palette TOML file")
    parser.add_argument("--only", nargs="*", help="Optional list of template path globs to render (relative to root)")
    parser.add_argument("--ignore", nargs="*", default=[], help="Additional ignore globs (relative to root)")
    parser.add_argument("--allow-missing", action="store_true", help="Leave unknown tokens untouched instead of failing")
    parser.add_argument("--dry-run", action="store_true", help="Render but do not write files")
    parser.add_argument("--verbose", action="store_true", help="Print every processed template")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root: Path = args.root.resolve()
    palette_path: Path = args.palette.resolve()

    if not palette_path.exists():
        print(f"Palette not found: {palette_path}", file=sys.stderr)
        return 1

    try:
        mapping = load_palette(palette_path)
    except Exception as exc:  # pragma: no cover
        print(f"Failed to load palette: {exc}", file=sys.stderr)
        return 1

    ignore_patterns = DEFAULT_IGNORE_PATTERNS | set(args.ignore)
    templates = find_templates(root, ignore_patterns)
    if not templates:
        print("No templates found.")
        return 0

    processed = 0
    updated: list[Path] = []
    missing_total: dict[Path, set[str]] = {}
    used_tokens: set[str] = set()

    for tmpl in templates:
        rel = tmpl.relative_to(root).as_posix()
        if not match_only(rel, args.only):
            continue

        target = tmpl.with_suffix("")
        text = tmpl.read_text(encoding="utf-8")
        referenced = tokens_in(text)
        used_tokens.update(referenced)

        rendered, missing = render_template(text, mapping, allow_missing=args.allow_missing)

        if missing and not args.allow_missing:
            missing_total[tmpl] = missing
            continue

        processed += 1
        if args.verbose or args.dry_run:
            print(f"Render {rel} -> {target.relative_to(root).as_posix()}")

        if args.dry_run:
            continue

        if write_if_changed(target, rendered):
            updated.append(target)

    if missing_total:
        print("Missing tokens detected:", file=sys.stderr)
        for path, tokens in missing_total.items():
            rel = path.relative_to(root)
            token_list = ", ".join(sorted(tokens))
            print(f"  {rel}: {token_list}", file=sys.stderr)
        return 2

    unused = sorted(k for k in mapping if k not in used_tokens)
    if unused and args.verbose:
        print("Unused palette entries:")
        for key in unused:
            print(f"  {key}")

    if args.dry_run:
        print(f"Dry run complete. Eligible templates: {processed}")
    else:
        if updated:
            print("Updated:")
            for path in updated:
                rel = path.relative_to(root)
                print(f"  {rel}")
        else:
            print("Already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
