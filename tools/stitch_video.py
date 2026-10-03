#!/usr/bin/env python3
"""Assemble a TRTT video of any frame size from presenter takes, cutaways and captions.

Usage:
    python3 tools/stitch_video.py edit.json

edit.json:
{
  "width": 1920, "height": 1080, "fps": 25,
  "takes": ["take1.mp4", "take2.mp4"],          # presenter clips, played back to back; their audio is the voice track
  "gap": 0.4,                                   # seconds of held frame between takes (default 0.4)
  "cuts": [["clip.mp4", 12.0, 16.5], ["graphic.png", 20.0, 28.0]],   # video or still image, start, end on the timeline
  "captions": [[a, b, "text"], ...],            # lower-third caption cards
  "titles": [[a, b, "text"], ...],              # optional larger centred cards (for numbered points)
  "output": "out.mp4"
}

Needs ffmpeg (or FFMPEG env var) and Pillow. The ffmpeg build does not need drawtext.
Cutaways keep the presenter audio underneath; cutaway audio is dropped.
Any input whose shape differs from the frame is fitted inside it over a blurred, filled copy of itself.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NAVY = (0, 46, 71)
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
IMG_EXT = (".png", ".jpg", ".jpeg")


def fit_chain(W, H, fps, src, out):
    """Filter graph: scale src to fit inside WxH over a blurred, filled copy of itself."""
    return (f"[{src}]split=2[{out}a][{out}b];"
            f"[{out}a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:5,setsar=1[{out}bg];"
            f"[{out}b]scale={W}:{H}:force_original_aspect_ratio=decrease,setsar=1[{out}fg];"
            f"[{out}bg][{out}fg]overlay=(W-w)/2:(H-h)/2,fps={fps}[{out}]")


def run(cmd):
    subprocess.run(cmd, check=True)


def probe_duration(path):
    out = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError("no duration for " + path)


def card(path, text, W, H, size, y_of, alpha=150, pad=22, spacing=12):
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


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    W, H, fps = spec.get("width", 1920), spec.get("height", 1080), spec.get("fps", 25)
    gap = float(spec.get("gap", 0.4))
    out = spec.get("output", "video.mp4")
    with tempfile.TemporaryDirectory() as tmp:
        p = lambda n: os.path.join(tmp, n)

        # 1. Normalise each take to the frame and chain them with a short held frame between.
        parts = []
        t = 0.0
        for i, take in enumerate(spec["takes"], 1):
            dur = probe_duration(take)
            fc1 = fit_chain(W, H, fps, "0:v", "f") + f";[f]tpad=stop_duration={gap}[vo]"
            run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", take,
                 "-filter_complex", fc1, "-map", "[vo]", "-map", "0:a",
                 "-af", f"apad=pad_dur={gap}", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "1", p(f"t{i}.mp4")])
            parts.append(p(f"t{i}.mp4"))
            print(f"take {i}: starts {t:.2f}s, runs {dur:.2f}s")
            t += dur + gap
        with open(p("list.txt"), "w") as f:
            for part in parts:
                f.write(f"file '{part}'\n")
        run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", p("list.txt"), "-c", "copy", p("base.mp4")])
        print(f"presenter track: {t:.2f}s")

        # 2. Caption and title cards.
        caps = spec.get("captions", [])
        titles = spec.get("titles", [])
        for i, (a, b, text) in enumerate(caps, 1):
            card(p(f"c{i}.png"), text, W, H, int(H * 0.042), lambda th: H - th - int(H * 0.10))
        for i, (a, b, text) in enumerate(titles, 1):
            card(p(f"T{i}.png"), text, W, H, int(H * 0.06), lambda th: (H - th) / 2, alpha=200)

        # 3. Overlay cutaways, then cards.
        cuts = spec.get("cuts", [])
        cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", p("base.mp4")]
        for f, a, b in cuts:
            if f.lower().endswith(IMG_EXT):
                cmd += ["-loop", "1", "-framerate", str(fps), "-t", str(b - a + 0.5), "-itsoffset", str(a), "-i", f]
            else:
                cmd += ["-itsoffset", str(a), "-i", f]
        n = 1 + len(cuts)
        for i in range(1, len(caps) + 1):
            cmd += ["-i", p(f"c{i}.png")]
        for i in range(1, len(titles) + 1):
            cmd += ["-i", p(f"T{i}.png")]

        fc = "[0:v]setsar=1[base];"
        prev = "base"
        for i, (f, a, b) in enumerate(cuts, 1):
            fc += (fit_chain(W, H, fps, f"{i}:v", f"b{i}") + ";"
                   f"[{prev}][b{i}]overlay=eof_action=pass:enable='between(t,{a},{b})'[v{i}];")
            prev = f"v{i}"
        idx = n
        for i, (a, b, _) in enumerate(caps, 1):
            fc += f"[{prev}][{idx}:v]overlay=0:0:enable='between(t,{a},{b})'[l{i}];"
            prev = f"l{i}"
            idx += 1
        for i, (a, b, _) in enumerate(titles, 1):
            fc += f"[{prev}][{idx}:v]overlay=0:0:enable='between(t,{a},{b})'[m{i}];"
            prev = f"m{i}"
            idx += 1
        fc = fc.rstrip(";")
        fc = fc[: fc.rfind(f"[{prev}]")] + "[vout]"
        cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", "0:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "1", "-movflags", "+faststart", out]
        run(cmd)
    print(out)


if __name__ == "__main__":
    main()
