import csv
import json
from pathlib import Path
from src.csv_export import export_comments_csv

def test_export_comments_json_handles_semicolon(tmp_path: Path):
    data = {42: ["Comentário com ; ponto e vírgula"]}
    out = tmp_path / "pr_comments.csv"
    export_comments_csv(data, out, use_json=True)

    with out.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    assert rows[0] == ["PR Number", "Comments"]

    arr = json.loads(rows[1][1])
    assert arr == ["Comentário com ; ponto e vírgula"]


def test_export_comments_join_mode_handles_semicolon(tmp_path: Path):
    data = {99: ["Comentário com ; dentro", "Outro comentário"]}
    out = tmp_path / "pr_comments.csv"
    export_comments_csv(data, out, use_json=False, inner_sep="; ")

    with out.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    assert rows[0] == ["PR Number", "Comments"]

    cell = rows[1][1]

    assert cell.count(";") >= 2

    assert "Comentário com ; dentro" in cell
