from __future__ import annotations
import argparse
import logging
from pathlib import Path

from .config import Settings
from .github_client import GitHubClient
from .processing import analyze
from .csv_export import export_comments_csv
from .reporting import build_pdf


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Coleta comentários de PRs e gera CSV+PDF")
    p.add_argument("--owner", type=str, help="Dono do repositório", default=None)
    p.add_argument("--repo", type=str, help="Nome do repositório", default=None)
    p.add_argument("--limit", type=int, help="Quantidade de PRs", default=None)
    p.add_argument("--outdir", type=str, help="Diretório de saída", default="data/outputs")
    p.add_argument("--verbose", action="store_true", help="Log detalhado")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")


    cfg = Settings.from_env()
    owner = args.owner or cfg.owner
    repo = args.repo or cfg.repo
    limit = args.limit or cfg.pr_limit


    client = GitHubClient(cfg.github_token)


    logging.info("Buscando primeiros %d PRs de %s/%s...", limit, owner, repo)
    pr_numbers = client.get_first_pr_numbers(owner, repo, limit)


    logging.info("Coletando comentários (com paginação) para %d PRs...", len(pr_numbers))
    comments_by_pr = client.get_comments_for_prs(owner, repo, pr_numbers)


    outdir = Path(args.outdir)
    csv_path = outdir / "pr_comments.csv"
    export_comments_csv(comments_by_pr, csv_path)
    logging.info("CSV gerado: %s", csv_path)


    metrics = analyze(comments_by_pr)
    repo_url = f"https://github.com/{owner}/{repo}"
    pdf_path = outdir / "report.pdf"
    build_pdf(
    out_path=pdf_path,
    repo_url=repo_url,
    metrics=metrics,
    group_number=cfg.group_number,
    participants=cfg.participants or [],
    )
    logging.info("PDF gerado: %s", pdf_path)


if __name__ == "__main__":
    main()