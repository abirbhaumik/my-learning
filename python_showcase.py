"""A small, polished example of Python fundamentals and clean CLI design."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Iterable


WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*")


@dataclass(frozen=True, slots=True)
class TextStats:
    """A summary of useful measurements for a piece of text."""

    words: int
    characters: int
    lines: int
    unique_words: int
    longest_word: str
    most_common_word: str

    def to_dict(self) -> dict[str, int | str]:
        """Return a dictionary suitable for JSON-like output."""
        return asdict(self)


def extract_words(text: str) -> list[str]:
    """Extract normalized words from text."""
    return [match.group(0).lower() for match in WORD_PATTERN.finditer(text)]


def analyze_text(text: str) -> TextStats:
    """Analyze text safely and return its key statistics."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    words = extract_words(text)
    word_counts = Counter(words)
    longest_word = max(words, key=len, default="")
    most_common_word = (
        min(word_counts, key=lambda word: (-word_counts[word], word))
        if word_counts
        else ""
    )

    return TextStats(
        words=len(words),
        characters=len(text),
        lines=len(text.splitlines()),
        unique_words=len(word_counts),
        longest_word=longest_word,
        most_common_word=most_common_word,
    )


def iter_source_files(paths: Iterable[Path]) -> Iterable[tuple[Path, str]]:
    """Read UTF-8 text files, reporting invalid paths with a clear error."""
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f"Not a file: {path}")
        yield path, path.read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze words and text statistics."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Optional UTF-8 text files to analyze.",
    )
    parser.add_argument(
        "--text",
        help="Analyze text supplied directly instead of reading a file.",
    )
    return parser


def print_stats(label: str, stats: TextStats) -> None:
    print(f"\n{label}")
    print("-" * len(label))
    for name, value in stats.to_dict().items():
        print(f"{name.replace('_', ' ').title():20}: {value}")


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.text is not None:
            print_stats("Direct text", analyze_text(args.text))

        if args.files:
            for path, text in iter_source_files(args.files):
                print_stats(str(path), analyze_text(text))

        if args.text is None and not args.files:
            print_stats("Standard input", analyze_text(input()))
    except (FileNotFoundError, UnicodeDecodeError) as error:
        print(f"Error: {error}", file=__import__("sys").stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
