#!/usr/bin/env python3
"""Finish the chosen takes with ffmpeg: trim edge silence, optionally slow down, and optionally join.

  # one clean file per line, for placing on a video timeline → final/s1.flac, final/s2.flac, ...
  python finish.py takes/s1_seed7.wav takes/s2_seed21.wav takes/s3_seed7.wav --out final

  # one narration track: lines in the order given, 750 ms between them, 0.90x speed, -16 LUFS
  python finish.py takes/s1_seed7.wav takes/s2_seed21.wav --join narration.m4a --gap-ms 750 --tempo 0.90

Per-line files keep the model's 48 kHz and get trim (+ tempo). The joined file also gets loudness
normalisation (--lufs, default -16). The output format follows the extension: .m4a .wav .flac .mp3.
Needs ffmpeg and ffprobe on PATH.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

TRIM = ("silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05,areverse,"
        "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.08,areverse")
CODECS = {".m4a": ["-c:a", "aac", "-b:a", "192k"], ".mp3": ["-c:a", "libmp3lame", "-b:a", "192k"],
          ".wav": ["-c:a", "pcm_s16le"], ".flac": ["-c:a", "flac"]}


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def codec_for(path: Path) -> list[str]:
    c = CODECS.get(path.suffix.lower())
    if c is None:
        sys.exit(f"unsupported output type {path.suffix}; use one of {', '.join(CODECS)}")
    return c


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("takes", nargs="+", type=Path, help="chosen takes, in script order")
    p.add_argument("--out", type=Path, help="folder for one trimmed file per line")
    p.add_argument("--join", type=Path, help="one file with every line in order")
    p.add_argument("--gap-ms", type=int, default=750, help="silence between lines in --join (default 750)")
    p.add_argument("--tempo", type=float, default=1.0, help="pitch-preserving speed, e.g. 0.90 (keep >= 0.85)")
    p.add_argument("--lufs", type=float, default=-16.0, help="loudness of --join (default -16)")
    p.add_argument("--rate", type=int, default=48000, help="sample rate of --join (default 48000)")
    a = p.parse_args()

    if not a.out and not a.join:
        sys.exit("give --out folder (one file per line) and/or --join file")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg and ffprobe must be on PATH")
    missing = [str(t) for t in a.takes if not t.is_file()]
    if missing:
        sys.exit(f"not found: {', '.join(missing)}")
    if not 0.5 <= a.tempo <= 2.0:
        sys.exit("--tempo must be between 0.5 and 2.0")
    if a.tempo < 0.85:
        print("note: below 0.85 the slow-down starts to sound stretched", file=sys.stderr)

    tempo = f",atempo={a.tempo:.3f}" if abs(a.tempo - 1.0) > 1e-3 else ""

    if a.out:
        a.out.mkdir(parents=True, exist_ok=True)
        for t in a.takes:
            m = re.match(r"s(\d+)", t.name)
            dst = a.out / (f"s{m.group(1)}.flac" if m else f"{t.stem}.flac")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(t), "-af", TRIM + tempo, "-c:a", "flac", str(dst)],
                           check=True)
            print(f"{t.name} {duration(t):5.2f}s → {dst.name} {duration(dst):5.2f}s", flush=True)

    if a.join:
        a.join.parent.mkdir(parents=True, exist_ok=True)
        ins, chains, labels = [], [], []
        gap = a.gap_ms / 1000
        for i, t in enumerate(a.takes):
            ins += ["-i", str(t)]
            chains.append(f"[{i}:a]aresample={a.rate},aformat=sample_fmts=fltp:channel_layouts=mono,{TRIM}[t{i}]")
            labels.append(f"[t{i}]")
            if i < len(a.takes) - 1 and gap > 0:
                chains.append(f"anullsrc=r={a.rate}:cl=mono,atrim=0:{gap:.3f}[g{i}]")
                labels.append(f"[g{i}]")
        graph = ";".join(chains) + ";" + "".join(labels) + (
            f"concat=n={len(labels)}:v=0:a=1{tempo},loudnorm=I={a.lufs}:TP=-1.5:LRA=11,aresample={a.rate}[out]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", graph, "-map", "[out]",
                        *codec_for(a.join), str(a.join)], check=True)
        print(f"joined {len(a.takes)} lines → {a.join} {duration(a.join):.2f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
