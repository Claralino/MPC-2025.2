import pytest
from src.processing import normalize_comment, analyze, THANK_REGEX

def test_normalize_comment_spaces_and_newlines():
    assert normalize_comment("Hello   \nWorld ! ") == "Hello World !"


def test_analyze_basic_metrics():
    comments_by_pr = {1: ["Thanks!; Valeu", "Ok"], 2: ["Obrigado!"], 3: []}
    m = analyze(comments_by_pr)
    assert m.total_comments == 3
    assert m.avg_comments_per_pr == pytest.approx(1.0) # 3 comments / 3 PRs
    assert m.avg_words_per_comment > 0
    assert m.avg_chars_per_comment > 0
    assert m.thank_like_count == 2 # "Thanks" + "Obrigado"

def test_thanks_regex_variants():
    samples = [
        "thank you for the fix",
        "Thanks!!",
        "tks",
        "obg",
        "valeu demais",
        "vlw",
    ]
    assert sum(1 for s in samples if THANK_REGEX.search(s)) == len(samples)