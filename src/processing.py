from __future__ import annotations
from dataclasses import dataclass
from pydoc import text
from typing import Dict, List
import re


THANK_PATTERNS = [
    r"\bthank\s*you\b",
    r"\bthanks\b",
    r"\btks\b",
    r"\bobrigado\b",
    r"\bvaleu\b",
    r"\bobg\b",
    r"\bvlw\b",
    ]
THANK_REGEX = re.compile("|".join(THANK_PATTERNS), flags=re.IGNORECASE)

@dataclass
class Metrics:
    total_comments: int
    avg_comments_per_pr: float
    avg_chars_per_comment: float
    avg_words_per_comment: float
    thank_like_count: int


def normalize_comment(text: str) -> str:
# Mantém pontuação, normaliza espaços e quebras de linha
    return re.sub(r"\s+", " ", (text or "").strip())


def analyze(comments_by_pr: Dict[int, List[str]]) -> Metrics:
    all_comments = [c for comments in comments_by_pr.values() for c in comments]
    total = len(all_comments)
    avg_per_pr = (total / max(len(comments_by_pr), 1)) if comments_by_pr else 0.0
    if total == 0:
        return Metrics(0, avg_per_pr, 0.0, 0.0, 0)


    norm = [normalize_comment(c) for c in all_comments]
    char_lens = [len(c) for c in norm]
    word_lens = [len(c.split()) for c in norm]
    thank_count = sum(1 for c in norm if THANK_REGEX.search(c))


    return Metrics(
        total_comments=total,
        avg_comments_per_pr=avg_per_pr,
        avg_chars_per_comment=sum(char_lens) / total,
        avg_words_per_comment=sum(word_lens) / total,
        thank_like_count=thank_count,
    )