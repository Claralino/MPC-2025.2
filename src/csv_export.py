from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Dict, List
from .processing import normalize_comment

def export_comments_csv(
    comments_by_pr: Dict[int, List[str]],
    out_path: Path,
    *,
    use_json: bool = True,        
    inner_sep: str = "; "     
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)  
        writer.writerow(["PR Number", "Comments"])
        for pr, comments in sorted(comments_by_pr.items()):
            if not comments:
                writer.writerow([pr, ""])
                continue

            cleaned = [normalize_comment(c).replace('"', "'") for c in comments]

            if use_json:
                cell = json.dumps(cleaned, ensure_ascii=False)
            else:
                cell = inner_sep.join(cleaned)

            writer.writerow([pr, cell])
