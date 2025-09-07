from __future__ import annotations
import logging
from typing import Dict, List
import requests
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

GQL_ENDPOINT = "https://api.github.com/graphql"

class GitHubError(Exception):
    pass

class GitHubClient:
    def __init__(self, token: str) -> None:
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((requests.RequestException, GitHubError)),
        reraise=True,
    )
    def _post(self, query: str, variables: dict | None = None) -> dict:
        resp = self.session.post(GQL_ENDPOINT, json={"query": query, "variables": variables or {}}, timeout=30)
        if resp.status_code != 200:
            raise GitHubError(f"Erro HTTP {resp.status_code}: {resp.text}")
        data = resp.json()
        if "errors" in data:
            raise GitHubError(str(data["errors"]))
        return data["data"]
    
    def get_first_pr_numbers(self, owner: str, repo: str, limit: int = 50) -> List[int]:
        query = """
        query($owner: String!, $repo: String!, $limit: Int!) {
            repository(owner: $owner, name: $repo) {
                pullRequests(first: $limit, orderBy: {field: CREATED_AT, direction: ASC}) {
                    nodes { number }
                }
            }
        }
        """
        data = self._post(query, {"owner": owner, "repo": repo, "limit": limit})
        nodes = data["repository"]["pullRequests"]["nodes"]
        return [n["number"] for n in nodes]
    
    def get_pr_comments(self, owner: str, repo: str, pr_number: int) -> List[str]:
        comments: List[str] = []
        cursor = None
        has_next = True
        query = """
        query($owner: String!, $repo: String!, $number: Int!, $after: String) {
            repository(owner: $owner, name: $repo) {
                pullRequest(number: $number) {
                    comments(first: 100, after: $after) {
                        nodes { body }
                        pageInfo { hasNextPage endCursor }
                    }
                }
            }
        }
        """
        while has_next:
            variables = {"owner": owner, "repo": repo, "number": pr_number, "after": cursor}
            data = self._post(query, variables)
            c = data["repository"]["pullRequest"]["comments"]
            comments.extend([n.get("body", "") or "" for n in c["nodes"]])
            has_next = c["pageInfo"]["hasNextPage"]
            cursor = c["pageInfo"]["endCursor"]
        logging.debug("PR #%s: %d comentários", pr_number, len(comments))
        return comments
    
    def get_comments_for_prs(self, owner: str, repo: str, pr_numbers: List[int]) -> Dict[int, List[str]]:
        result: Dict[int, List[str]] = {}
        for num in pr_numbers:
            try:
                result[num] = self.get_pr_comments(owner, repo, num)
            except Exception as e:
                logging.exception("Falha ao buscar comentários do PR #%s: %s", num, e)
                result[num] = []
        return result
