#!/usr/bin/env python3
"""Assemble a TRTT vertical short from a presenter clip, cutaways and captions.

Usage:
    python3 tools/stitch_short.py edit.json

edit.json:
{
  "presenter": "presenter.mp4",            # base clip with the voice track
  "cuts": [["station.mp4", 1.5, 5.0], ...],  # file, start, end (seconds on the timeline)
  "captions": [[0.5, 14.5, "Line one\\nLine two"], ...],
  "label": null,                          # optional on-screen line; null for none
  "end_card": null,                       # optional closing card; null for none
  "end_seconds": 3.5,
  "output": "short.mp4"
}

Output is 1080x1920, 25 fps, H.264 and AAC. Needs ffmpeg on PATH (or FFMPEG env var)
and Pillow. Captions are rendered to PNG with Pillow and overlaid, so the ffmpeg build
does not need drawtext.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NAVY = (0, 46, 71)
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def card(path, text, size, y_of, alpha=150, pad=22, spacing=12):
    font = ImageFont.truetype(FONT, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = text.split("\n")
    widths = [d.textlength(l, font=font) for l in lines]
    lh = size + spacing
    tw, th = max(widths), lh * len(lines) - spacing
    y = y_of(th)
    x0 = (W - tw) / 2 - pad
    d.rounded_rectangle([x0, y - pad, x0 + tw + 2 * pad, y + th + pad], radius=14, fill=NAVY + (alpha,))
    for line, w in zip(lines, widths):
        d.text(((W - w) / 2, y), line, font=font, fill="white")
        y += lh
    img.save(path)


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = spec.get("output", "short.mp4")
    with tempfile.TemporaryDirectory() as tmp:
        p = lambda n: os.path.join(tmp, n)
        label = spec.get("label")
        if label:
            card(p("label.png"), label, 34, lambda th: 90)
        caps = spec.get("captions", [])
        for i, (a, b, text) in enumerate(caps, 1):
            card(p(f"c{i}.png"), text, 50, lambda th: H - th - 300)

        cuts = spec.get("cuts", [])
        cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", spec["presenter"]]
        for f, a, b in cuts:
            cmd += ["-itsoffset", str(a), "-i", f]
        n = 1 + len(cuts)
        if label:
            cmd += ["-i", p("label.png")]
        for i in range(1, len(caps) + 1):
            cmd += ["-i", p(f"c{i}.png")]

        fc = "[0:v]scale=-2:1920,crop=1080:1920,setsar=1,fps=25[base];"
        prev = "base"
        for i, (f, a, b) in enumerate(cuts, 1):
            fc += (f"[{i}:v]scale=1080:1920,setsar=1,fps=25[b{i}];"
                   f"[{prev}][b{i}]overlay=eof_action=pass:enable='between(t,{a},{b})'[v{i}];")
            prev = f"v{i}"
        cap_base = n
        if label:
            fc += f"[{prev}][{n}:v]overlay=0:0[l0];"
            prev = "l0"
            cap_base = n + 1
        for i, (a, b, _) in enumerate(caps, 1):
            fc += f"[{prev}][{cap_base + i - 1}:v]overlay=0:0:enable='between(t,{a},{b})'[l{i}];"
            prev = f"l{i}"
        fc = fc.rstrip(";")
        fc = fc[: fc.rfind(f"[{prev}]")] + "[vout]"
        cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", "0:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "1", "-movflags", "+faststart", p("main.mp4")]
        run(cmd)

        end_text = spec.get("end_card")
        if not end_text:
            os.replace(p("main.mp4"), out)
            print(out)
            return
        font = ImageFont.truetype(FONT, 52)
        img = Image.new("RGB", (W, H), NAVY)
        d = ImageDraw.Draw(img)
        lines = end_text.split("\n")
        lh = 66
        y = (H - lh * len(lines)) / 2
        for line in lines:
            w = d.textlength(line, font=font)
            d.text(((W - w) / 2, y), line, font=font, fill="white")
            y += lh
        img.save(p("end.png"))
        secs = str(spec.get("end_seconds", 3.5))
        run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", p("end.png"),
             "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", secs, "-r", "25",
             "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
             "-ar", "44100", "-ac", "1", "-shortest", p("end.mp4")])
        with open(p("list.txt"), "w") as f:
            f.write(f"file '{p('main.mp4')}'\nfile '{p('end.mp4')}'\n")
        run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", p("list.txt"), "-c", "copy", "-movflags", "+faststart", out])
    print(out)


if __name__ == "__main__":
    main()
