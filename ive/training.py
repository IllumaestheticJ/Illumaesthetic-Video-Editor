"""The learning loop that "trains" future editing agents.

There is no model fine-tuning here. Agents improve through retrieval: every project
leaves behind structured artifacts that the next agent reads before it starts.

  projects/<name>/editlog.jsonl   every editorial decision + why (written while editing)
  projects/<name>/feedback.jsonl  every reviewer note, timecoded and categorised
  knowledge/lessons.md            feedback promoted to standing rules (`--rule`)
  training/examples/<name>/       frozen snapshot of a finished project: manifest,
                                  camera solves, overlay, log, feedback, QA scores
  training/references/*.json|md   numeric + written breakdowns of reference edits

CLAUDE.md tells every agent to read lessons.md, the style guide and the 2 most recent
examples before touching footage. That is the training.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LESSONS = REPO / "knowledge" / "lessons.md"
EXAMPLES = REPO / "training" / "examples"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def log_decision(project_dir: str, decision: str, why: str) -> dict:
    rec = {"ts": _now(), "decision": decision, "why": why}
    _append(Path(project_dir) / "editlog.jsonl", rec)
    return rec


def add_feedback(project_dir: str, note: str, at: str | None = None, category: str = "general",
                 rule: bool = False, by: str = "reviewer") -> dict:
    p = Path(project_dir)
    rec = {"ts": _now(), "project": p.name, "at": at, "category": category, "note": note, "by": by, "promoted": rule}
    _append(p / "feedback.jsonl", rec)
    if rule:
        LESSONS.parent.mkdir(parents=True, exist_ok=True)
        with open(LESSONS, "a") as f:
            where = f" @ {at}s" if at else ""
            f.write(f"\n- **[{category}]** {note}  _(from {p.name}{where}, {rec['ts'][:10]}, {by})_\n")
    return rec


def archive(project_dir: str) -> str:
    """Freeze a finished project as a worked example (small text artifacts only - no media)."""
    p = Path(project_dir)
    dst = EXAMPLES / p.name
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for f in p.rglob("*"):
        if f.is_file() and f.suffix.lower() in (".yaml", ".yml", ".json", ".jsonl", ".md", ".txt"):
            rel = f.relative_to(p)
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst / rel)
    idx = EXAMPLES / "INDEX.md"
    lines = idx.read_text().splitlines() if idx.exists() else ["# Worked examples", "",
                                                                "Newest first. Read the top two before starting a new edit.", ""]
    entry = f"- [{p.name}]({p.name}/) - archived {_now()[:10]}"
    lines = [l for l in lines if not l.startswith(f"- [{p.name}]")]
    head = lines[:4]
    lines = head + [entry] + lines[4:]
    idx.write_text("\n".join(lines) + "\n")
    return str(dst)
