#!/usr/bin/env python3
"""Heuristic voice check for TRTT social drafts.

It encodes the rules in the RobinReach brand tone brief. It cannot judge
accuracy, tone or sources, so treat WARN lines as prompts for a human edit.

Usage:
    python3 tools/voice_lint.py drafts.txt --platform linkedin
    cat draft.txt | python3 tools/voice_lint.py - --platform x

Several drafts can share one file, separated by a line containing only ---.
Exit status is 1 when any ERROR is found.
"""
import argparse
import re
import sys

LIMITS = {
    "x": 280,
    "twitter": 280,
    "instagram": 2200,
    "tiktok": 2200,
    "linkedin": 3000,
    "facebook": 5000,
    "youtube": 5000,
}

BANNED_PHRASES = [
    "delve", "unlock", "leverage", "tapestry", "game-changer", "game changer",
    "in today's fast-paced world", "here's the thing", "let me be clear",
    "the truth is", "and that matters", "that's the part everyone misses",
    "which is exactly the point", "in short", "at the end of the day",
]
FORMULA_OPENERS = ("picture this", "here's a common one", "quick question")
SCENARIO_LABEL = re.compile(r"\b(illustrative|made-up|made up|example|imagine)\b", re.I)
DISCLAIMER_TRIGGER = re.compile(
    r"\b(HVNL|NHVR|heavy vehicle|chain of responsibility|CoR)\b", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
TRIPLET = re.compile(r"\b(3|three)\s+(things|questions|checks|steps|rules|points)\b", re.I)
CONTRAST = re.compile(
    r"\b(?:that's|that is|this is|it's|it is|isn't|is not|aren't|are not|not)\b"
    r"[^.\n]{0,60}\.\s+(?:that's|that is|it's|it is|this is)\b",
    re.I)


def normalise(text):
    return text.replace("’", "'").replace("‘", "'")


def word_list(s):
    return re.findall(r"[\w$%']+", s)


def sentences(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or re.fullmatch(r"(#\w+\s*)+", line):
            continue
        out.extend(p for p in re.split(r"(?<=[.!?])\s+", line) if p.strip())
    return out


def syllables(word):
    w = word.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(n, 1)


def grade_level(sents):
    words = [w for s in sents for w in word_list(s)]
    if not words or not sents:
        return 0.0
    wps = len(words) / len(sents)
    spw = sum(syllables(w) for w in words) / len(words)
    return 0.39 * wps + 11.8 * spw - 15.59


def check(text, platform, max_grade):
    text = normalise(text)
    low = text.lower()
    findings = []

    limit = LIMITS.get(platform)
    if limit and len(text) > limit:
        findings.append(("ERROR", f"{len(text)} characters, {platform} limit is {limit}"))
    if "—" in text:
        findings.append(("ERROR", "em-dash found (brief: never use em-dashes)"))
    if "!" in text:
        findings.append(("ERROR", "exclamation mark found"))
    if EMOJI.search(text):
        findings.append(("ERROR", "emoji found"))
    for phrase in BANNED_PHRASES:
        if re.search(rf"\b{re.escape(phrase)}\b", low):
            findings.append(("ERROR", f"banned phrase: '{phrase}'"))

    opener = low.lstrip()
    for o in FORMULA_OPENERS:
        if opener.startswith(o):
            findings.append(("WARN", f"formula opener '{o}': vary the hook (scene, flat fact, real question)"))
            if not SCENARIO_LABEL.search(low):
                findings.append(("WARN", "invented scenario is not labelled as an example"))
            break

    if TRIPLET.search(text):
        findings.append(("WARN", "'3 things' style list: brief bans lists of exactly three matched items"))
    if CONTRAST.search(text):
        findings.append(("WARN", "possible contrast verdict ('That's not X. That's Y.'): say the second half only"))

    sents = sentences(text)
    for s in sents:
        n = len(word_list(s))
        if n > 25:
            findings.append(("WARN", f"{n}-word sentence (max 25): {s[:60]}..."))
        if n <= 10 and re.search(r"\b(is|are) not\b", s, re.I):
            findings.append(("WARN", f"short 'is not' sentence, possible contrast verdict: {s}"))
    if sents:
        avg = sum(len(word_list(s)) for s in sents) / len(sents)
        if avg > 15:
            findings.append(("WARN", f"average sentence length {avg:.1f} words (target 15)"))
        for a, b in zip(sents, sents[1:]):
            if len(word_list(a)) <= 3 and len(word_list(b)) <= 3:
                findings.append(("WARN", f"fragment pair: '{a}' '{b}'"))
        g = grade_level(sents)
        if g > max_grade:
            findings.append(("WARN", f"reading grade about {g:.1f} (target Year 7 to 8, limit {max_grade})"))

    if (platform not in ("x", "twitter") and DISCLAIMER_TRIGGER.search(text)
            and "not legal advice" not in low):
        findings.append(("WARN", "regulatory content without the 'General information, not legal advice' line"))

    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="file with drafts, or - for stdin")
    ap.add_argument("--platform", default="linkedin", choices=sorted(LIMITS))
    ap.add_argument("--max-grade", type=float, default=9.0)
    args = ap.parse_args()

    raw = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    drafts = [d.strip() for d in re.split(r"^---\s*$", raw, flags=re.M) if d.strip()]

    errors = 0
    for i, draft in enumerate(drafts, 1):
        findings = check(draft, args.platform, args.max_grade)
        print(f"Draft {i}: {len(word_list(draft))} words, {len(draft)} characters")
        if not findings:
            print("  OK")
        for level, msg in findings:
            print(f"  {level}: {msg}")
            errors += level == "ERROR"
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
