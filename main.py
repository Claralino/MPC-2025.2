import os
import requests
import csv
import sys
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "TheAlgorithms"
REPO = "Python"
URL = "https://api.github.com/graphql"

if not GITHUB_TOKEN.strip():
    sys.exit("Erro: o Token do GitHub não foi definido. Configure a variável GITHUB_TOKEN.")

headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

query = """
query {
  repository(owner: "%s", name: "%s") {
    pullRequests(first: 50, orderBy: {field: CREATED_AT, direction: ASC}) {
      nodes {
        number
        comments(first: 100) {
          nodes {
            body
          }
        }
      }
    }
  }
}
""" % (OWNER, REPO)

response = requests.post(URL, json={"query": query}, headers=headers)

if response.status_code != 200:
    raise requests.exceptions.HTTPError(f"Erro na API: {response.status_code}, {response.text}")

data = response.json()


if "errors" in data:
    sys.exit(f"Erro retornado pela API: {data['errors']}")

prs = data["data"]["repository"]["pullRequests"]["nodes"]

with open("pr_comments.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerow(["PR Number", "Comments"])
    for pr in prs:
        number = pr["number"]
        comment_nodes = pr["comments"]["nodes"]
        if not comment_nodes:
            continue 

        comments = "; ".join(
            [c["body"].replace("\n", " ").replace('"', "'") for c in comment_nodes]
        )
        writer.writerow([number, comments])

print("CSV gerado: pr_comments.csv")
