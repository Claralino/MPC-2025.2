from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    github_token: str
    owner: str
    repo: str
    group_number: str = ""
    participants: Optional[list[str]] = None


    @staticmethod
    def from_env() -> "Settings":
        token = os.getenv("GITHUB_TOKEN", "").strip()
        if not token:
            raise RuntimeError(
            "GITHUB_TOKEN não definido. Configure no .env ou variável de ambiente."
            )
        owner = os.getenv("GITHUB_OWNER", "TheAlgorithms").strip()
        repo = os.getenv("GITHUB_REPO", "Python").strip()
        pr_limit = int(os.getenv("PR_LIMIT", 50))
        group_number = os.getenv("GROUP_NUMBER", "").strip()
        participants_raw = os.getenv("PARTICIPANTS", "").strip()
        participants = [p.strip() for p in participants_raw.split(";") if p.strip()] if participants_raw else []
        return Settings(
            github_token=token,
            owner=owner,
            repo=repo,
            pr_limit=pr_limit,
            group_number=group_number,
            participants=participants,
        )