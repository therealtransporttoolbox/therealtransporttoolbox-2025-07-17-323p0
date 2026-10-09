#!/usr/bin/env python3
"""Scaffold a TRTT AI video episode folder under drafts/.

Usage:
    python3 tools/new_episode.py gosford-steer-axle --title "Gosford steer axle" \
        --source "https://www.nhvr.gov.au/law-policies/prosecutions/court-outcomes" \
        --characters presenter_a,big_red

Creates drafts/<slug>/ with script.txt, captions.txt, shotlist.md and checklist.md.
Characters are checked against production/characters.json.
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "production" / "characters.json"


def load_registry():
    with REGISTRY.open(encoding="utf-8") as f:
        return json.load(f)["characters"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="lowercase words joined by hyphens")
    ap.add_argument("--title", required=True)
    ap.add_argument("--source", required=True, help="primary source URL for every fact")
    ap.add_argument("--characters", default="presenter_a", help="comma separated keys from production/characters.json")
    ap.add_argument("--platform", default="tiktok", help="platform for voice_lint")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit("slug must be lowercase letters, digits and hyphens")

    registry = load_registry()
    chosen = [c.strip() for c in args.characters.split(",") if c.strip()]
    unknown = [c for c in chosen if c not in registry]
    if unknown:
        sys.exit(f"unknown character(s): {', '.join(unknown)}. Known: {', '.join(registry)}")

    folder = ROOT / "drafts" / args.slug
    if folder.exists():
        sys.exit(f"{folder} already exists")
    folder.mkdir(parents=True)

    today = datetime.date.today().isoformat()
    voice_lines = []
    for c in chosen:
        v = registry[c].get("voice", {})
        voice_lines.append(f"- {c}: voice {v.get('name', 'NOT DECIDED')} ({v.get('status', 'unknown')})")

    (folder / "script.txt").write_text(
        "Write the spoken script here. One draft per block; separate drafts with a line containing only ---.\n",
        encoding="utf-8")
    (folder / "captions.txt").write_text(
        "On-screen captions, one per block, separated by a line containing only ---.\n", encoding="utf-8")
    (folder / "shotlist.md").write_text(
        f"# {args.title}: shot list\n\nDraft for owner approval. Not published.\n\n"
        f"Source: {args.source} (checked {today})\n\n"
        "Characters and voices:\n" + "\n".join(voice_lines) + "\n\n"
        "| Time | Voice | Picture | On-screen text |\n|---|---|---|---|\n| | | | |\n\n"
        "Labels: persistent AI or fiction label, end card, platform AI label. See production/RUNBOOK.md.\n",
        encoding="utf-8")
    (folder / "checklist.md").write_text(
        f"# {args.title}: checklist\n\n"
        "- [ ] Facts match the source; source line and date recorded\n"
        f"- [ ] python3 tools/voice_lint.py drafts/{args.slug}/script.txt --platform {args.platform}\n"
        f"- [ ] python3 tools/voice_lint.py drafts/{args.slug}/captions.txt --platform {args.platform}\n"
        "- [ ] Approved voice used for each character\n"
        "- [ ] Trucks left of road, driver on the right, no couplings, no stray vehicles\n"
        "- [ ] Characters match approved stills and are friendly\n"
        "- [ ] Labels and end card present\n"
        "- [ ] Owner has watched and listened\n"
        "- [ ] Saved as a draft only\n",
        encoding="utf-8")
    print(f"Created {folder.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
