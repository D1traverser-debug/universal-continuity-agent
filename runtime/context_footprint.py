from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ContextFootprint:
    paths: tuple[str, ...]
    utf8_bytes: int
    approximate_tokens: int
    file_count: int


def approximate_tokens_from_utf8_bytes(utf8_bytes: int) -> int:
    """Return a coarse planning estimate, never a tokenizer claim.

    The 4-bytes/token ratio is deliberately labeled approximate. It is useful for
    regression/budget comparisons when a model tokenizer is not part of the harness,
    but it must not be reported as an exact model token count.
    """

    if utf8_bytes < 0:
        raise ValueError("utf8_bytes must be non-negative")
    return ceil(utf8_bytes / 4)


def measure_context_footprint(root: str | Path, relative_paths: Iterable[str]) -> ContextFootprint:
    root = Path(root)
    paths = tuple(str(path) for path in relative_paths)
    if not paths:
        raise ValueError("at least one context path is required")

    total = 0
    for relative in paths:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        total += len(path.read_bytes())

    return ContextFootprint(
        paths=paths,
        utf8_bytes=total,
        approximate_tokens=approximate_tokens_from_utf8_bytes(total),
        file_count=len(paths),
    )


def footprint_within_budget(footprint: ContextFootprint, *, max_utf8_bytes: int) -> bool:
    if max_utf8_bytes < 0:
        raise ValueError("max_utf8_bytes must be non-negative")
    return footprint.utf8_bytes <= max_utf8_bytes
