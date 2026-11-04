"""Character and word error rates against a verified ground truth."""

from __future__ import annotations

import re


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def edit_distance(a: list | str, b: list | str) -> int:
    """Levenshtein distance using linear memory."""
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, left in enumerate(a, start=1):
        current = [i]
        for j, right in enumerate(b, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (left != right),
                )
            )
        previous = current
    return previous[-1]


def cer(reference: str | None, hypothesis: str) -> float | None:
    """CER = character edit distance / number of reference characters.

    Normalization collapses whitespace but keeps punctuation and case.
    A missing or blank reference returns None, never a fabricated score.
    """
    if reference is None:
        return None
    target = normalize(reference)
    if not target:
        return None
    return edit_distance(target, normalize(hypothesis)) / len(target)


def wer(reference: str | None, hypothesis: str) -> float | None:
    if reference is None:
        return None
    target = normalize(reference).split()
    if not target:
        return None
    return edit_distance(target, normalize(hypothesis).split()) / len(target)
