import requests
import csv

TOKEN = ""
OWNER = "TheAlgorithms"
REPO = "Python"
URL = "https://api.github.com/graphql"

headers = {"Authorization": f"Bearer {TOKEN}"}

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
    raise Exception(f"Erro na API: {response.status_code}, {response.text}")

data = response.json()
prs = data["data"]["repository"]["pullRequests"]["nodes"]

with open("pr_comments.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerow(["PR Number", "Comments"])
    for pr in prs:
        number = pr["number"]
        comments = "; ".join([c["body"].replace("\n", " ").replace('"', "'") for c in pr["comments"]["nodes"]])
        writer.writerow([number, comments])

print("CSV gerado: pr_comments.csv")
