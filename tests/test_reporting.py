from pathlib import Path
from src.reporting import build_pdf
from src.processing import Metrics


def test_build_pdf_smoke(tmp_path: Path):
    pdf_path = tmp_path / "report.pdf"
    metrics = Metrics(
        total_comments=3,
        avg_comments_per_pr=1.5,
        avg_chars_per_comment=12.0,
        avg_words_per_comment=2.5,
        thank_like_count=2,
    )
    build_pdf(
        out_path=pdf_path,
        repo_url="https://github.com/owner/repo",
        metrics=metrics,
        group_number="42",
        participants=["Alice", "Bob"],
    )
    assert pdf_path.exists() and pdf_path.stat().st_size > 1000
