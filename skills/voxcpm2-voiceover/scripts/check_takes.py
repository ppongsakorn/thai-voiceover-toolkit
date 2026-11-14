#!/usr/bin/env python3
"""Transcribe takes with Whisper large-v3 (mlx-whisper, Apple Silicon) and score each against its script line.

  python check_takes.py --lines script.txt takes/*.wav      # character error rate (CER) per take + best per line
  python check_takes.py --words final/s*.flac               # word start times (for syncing visuals to words)

A take is matched to its line by its file name: s<line>_... or s<line>.<ext> (what synth.py writes).
An "(instruction)" at the start of a script line is not counted. CER is a hint, not a verdict: it misses wrong
tones, and words spelled phonetically in Thai (e.g. "โคไพล็อต") score as errors when Whisper writes them in English.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

PUNCT = re.compile(r"[\s,.\-!?·:;\"'“”‘’()\[\]…/]")
INSTRUCTION = re.compile(r"^\s*\([^)]*\)\s*")


def read_lines(path: Path) -> list[str]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        lines = data["lines"] if isinstance(data, dict) else data
        return [str(x).strip() for x in lines]
    return [s.strip() for s in path.read_text(encoding="utf-8").splitlines() if s.strip() and not s.strip().startswith("#")]


def norm(s: str) -> str:
    return PUNCT.sub("", s.lower())


def cer(ref: str, hyp: str) -> float:
    r, h = norm(ref), norm(hyp)
    prev = list(range(len(h) + 1))
    for i, rc in enumerate(r, 1):
        cur = [i]
        for j, hc in enumerate(h, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rc != hc)))
        prev = cur
    return prev[-1] / max(1, len(r))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("--lines", type=Path, help="the script given to synth.py (for CER)")
    p.add_argument("--words", action="store_true", help="print word start times instead of CER")
    p.add_argument("--lang", default="th", help="language of the speech (default th)")
    p.add_argument("--model", default="mlx-community/whisper-large-v3-mlx", help="mlx-whisper model id or folder")
    a = p.parse_args()
    if not a.words and not a.lines:
        sys.exit("give --lines script.txt (CER) or --words (word timings)")

    import mlx_whisper

    lines = read_lines(a.lines) if a.lines else []
    best: dict[int, tuple[float, str]] = {}
    width = max(len(str(f)) for f in a.files)
    for f in sorted(a.files, key=lambda x: (x.name, str(x))):
        r = mlx_whisper.transcribe(str(f), path_or_hf_repo=a.model, language=a.lang, temperature=0.0,
                                   word_timestamps=a.words)
        if a.words:
            ws = [w for s in r["segments"] for w in s.get("words", [])]
            print(str(f), " ".join(f"{w['word'].strip()}@{w['start']:.2f}" for w in ws), flush=True)
            continue
        text = r["text"].strip()
        m = re.match(r"s(\d+)", f.name)
        if not m or not (1 <= int(m.group(1)) <= len(lines)):
            print(f"{f!s:{width}s} (no matching line) {text}", flush=True)
            continue
        n = int(m.group(1))
        score = cer(INSTRUCTION.sub("", lines[n - 1]), text)
        flag = "  ← listen closely" if score > 0.05 else ""
        print(f"{f!s:{width}s} CER {score:.2f} | {text}{flag}", flush=True)
        if n not in best or score < best[n][0]:
            best[n] = (score, str(f))

    if best:
        print("\nlowest CER per line (listen before choosing):")
        for n in sorted(best):
            print(f"  s{n}: {best[n][1]} (CER {best[n][0]:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
