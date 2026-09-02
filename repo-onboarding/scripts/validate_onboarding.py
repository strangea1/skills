#!/usr/bin/env python3

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

PLACEHOLDER_PATTERN = re.compile(r"\{\{[^{}]+\}\}")
FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^\s)]+)")
SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
WINDOWS_ABSOLUTE_PATTERN = re.compile(r"^[A-Za-z]:[\\/]")
CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
RAW_REPOMAP_MARKERS = (
    "Rank value:",
    '"definitionMatches"',
    '"referenceMatches"',
    '"totalFilesConsidered"',
    '"tokenLimit"',
    '"excludeUnranked"',
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a concise agent-oriented repository overview."
    )
    parser.add_argument("document", type=Path)
    parser.add_argument("--max-tokens", type=int, default=3000)
    parser.add_argument("--target-tokens", type=int, default=2500)
    parser.add_argument("--max-lines", type=int, default=250)
    parser.add_argument("--min-local-links", type=int, default=3)
    return parser.parse_args()


def without_fenced_code(text: str) -> str:
    visible_lines: list[str] = []
    active_fence: str | None = None

    for line in text.splitlines():
        match = FENCE_PATTERN.match(line)
        if match:
            marker = match.group(1)[0]
            if active_fence is None:
                active_fence = marker
            elif active_fence == marker:
                active_fence = None
            visible_lines.append("")
        elif active_fence is None:
            visible_lines.append(line)
        else:
            visible_lines.append("")

    return "\n".join(visible_lines)


def estimate_tokens(text: str) -> int:
    cjk_count = len(CJK_PATTERN.findall(text))
    without_cjk = CJK_PATTERN.sub("", text)
    ascii_count = sum(
        character.isascii() and not character.isspace() for character in without_cjk
    )
    other_count = sum(
        not character.isascii() and not character.isspace() for character in without_cjk
    )
    return cjk_count + math.ceil(ascii_count / 4) + math.ceil(other_count / 2)


def local_link_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in LINK_PATTERN.finditer(without_fenced_code(text)):
        target = match.group("target").strip("<>")
        if target.startswith("#"):
            continue
        if not WINDOWS_ABSOLUTE_PATTERN.match(target) and SCHEME_PATTERN.match(target):
            continue
        targets.append(target)
    return targets


def validate(args: argparse.Namespace) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not args.document.is_file():
        return [f"document does not exist: {args.document}"], warnings, {}

    text = args.document.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    token_estimate = estimate_tokens(text)

    if not re.search(r"(?m)^#\s+\S", text):
        errors.append("document must contain one level-1 title")

    headings = [
        re.sub(r"\s+", " ", heading).strip().casefold()
        for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", without_fenced_code(text))
    ]
    duplicate_headings = sorted(
        heading for heading, count in Counter(headings).items() if count > 1
    )
    if duplicate_headings:
        errors.append("duplicate headings: " + ", ".join(duplicate_headings))

    placeholders = sorted(set(PLACEHOLDER_PATTERN.findall(text)))
    if placeholders:
        preview = ", ".join(placeholders[:5])
        errors.append(f"unfinished template placeholders: {preview}")

    leaked_markers = [marker for marker in RAW_REPOMAP_MARKERS if marker in text]
    if leaked_markers:
        errors.append(
            f"raw repomap output leaked into document: {', '.join(leaked_markers)}"
        )

    if token_estimate > args.max_tokens:
        errors.append(
            f"estimated token count {token_estimate} exceeds maximum {args.max_tokens}"
        )
    elif token_estimate > args.target_tokens:
        warnings.append(
            f"estimated token count {token_estimate} exceeds target {args.target_tokens}"
        )

    if line_count > args.max_lines:
        errors.append(f"line count {line_count} exceeds maximum {args.max_lines}")

    local_targets = local_link_targets(text)
    if len(local_targets) < args.min_local_links:
        errors.append(
            f"found {len(local_targets)} local links; expected at least {args.min_local_links}"
        )

    repeated_targets = sorted(
        target for target, count in Counter(local_targets).items() if count > 3
    )
    if repeated_targets:
        warnings.append(
            "local link targets repeated more than three times: "
            + ", ".join(repeated_targets)
        )

    missing_targets: list[str] = []
    for target in local_targets:
        path_text = unquote(re.split(r"[?#]", target, maxsplit=1)[0])
        if not path_text:
            continue
        if WINDOWS_ABSOLUTE_PATTERN.match(path_text) or Path(path_text).is_absolute():
            errors.append(f"local link must be relative: {target}")
            continue
        resolved = (args.document.parent / Path(path_text)).resolve()
        if not resolved.exists():
            missing_targets.append(target)

    if missing_targets:
        errors.append(
            "missing local link targets: " + ", ".join(sorted(set(missing_targets)))
        )

    metrics = {
        "estimated_tokens": token_estimate,
        "lines": line_count,
        "local_links": len(local_targets),
    }
    return errors, warnings, metrics


def main() -> int:
    args = parse_args()
    errors, warnings, metrics = validate(args)

    if metrics:
        print(
            f"{args.document}: ~{metrics['estimated_tokens']} tokens, "
            f"{metrics['lines']} lines, {metrics['local_links']} local links"
        )

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
