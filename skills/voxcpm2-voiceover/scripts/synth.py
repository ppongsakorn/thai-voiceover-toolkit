#!/usr/bin/env python3
"""Generate voiceover takes with VoxCPM2 (openbmb/VoxCPM2, Apache-2.0): one WAV per line per seed.

The mode follows from the arguments:

  hifi    --ref voice.wav                 voice.txt next to it holds the exact words spoken in voice.wav.
                                          Closest to the reference and copies its pace. Ignores "(instructions)".
  clone   --ref voice.wav --no-transcript timbre from the reference only. An "(instruction)" at the start of a
                                          line, or --style, steers the delivery. Use it for emotions and for
                                          speaking another language than the reference.
  design  --design "description"          no reference: a new voice from a description. Use it to make a reference.

Examples:

  python synth.py --lines script.txt --ref voices/narrator.wav --out takes
  python synth.py --lines script.txt --ref voices/narrator.wav --no-transcript --style "cheerful, bright and happy tone" --out takes
  python synth.py --lines ref_line.txt --design "warm, gentle Thai woman, storyteller" --seeds 1,2,3,4 --out takes
  python synth.py ... --only 2,5          # redo lines 2 and 5

Lines file: .txt (one line per take, blank lines and lines starting with # are skipped) or .json (a list of
strings, or {"lines": [...]}). Output: <out>/s<line>_seed<seed>.wav plus <out>/takes.json describing every take.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import warnings
from pathlib import Path

os.environ.setdefault("TQDM_DISABLE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore")

INSTRUCTION = re.compile(r"^\s*\(([^)]*)\)\s*(.*)$", re.DOTALL)


def read_lines(path: Path) -> list[str]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        lines = data["lines"] if isinstance(data, dict) else data
        return [str(x).strip() for x in lines]
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if s and not s.startswith("#"):
            out.append(s)
    return out


def split_instruction(line: str) -> tuple[str, str]:
    """'(sad, slow)ข้อความ' -> ('sad, slow', 'ข้อความ'); 'ข้อความ' -> ('', 'ข้อความ')."""
    m = INSTRUCTION.match(line)
    return (m.group(1).strip(), m.group(2).strip()) if m else ("", line.strip())


def build_text(line: str, mode: str, style: str, design: str) -> str:
    inline, body = split_instruction(line)
    if mode == "hifi":
        return body
    parts = [p for p in (design if mode == "design" else "", style, inline) if p]
    return f"({', '.join(parts)}){body}" if parts else body


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--lines", required=True, type=Path, help="script: .txt or .json")
    p.add_argument("--out", required=True, type=Path, help="folder for the takes")
    p.add_argument("--ref", type=Path, help="reference voice .wav (10-15 s, one speaker, quiet room)")
    p.add_argument("--ref-text", type=Path, help="transcript of --ref (default: the .txt next to it)")
    p.add_argument("--no-transcript", action="store_true", help="clone from the audio only (allows instructions)")
    p.add_argument("--style", default="", help='instruction for every line, in English, e.g. "warm, gentle tone"')
    p.add_argument("--design", default="", help="describe a new voice (no --ref)")
    p.add_argument("--seeds", default="7,21", help="one take per seed (default 7,21)")
    p.add_argument("--only", default="", help="line numbers to make, e.g. 2,5 (1-based)")
    p.add_argument("--cfg", type=float, default=2.0, help="guidance (default 2.0)")
    p.add_argument("--steps", type=int, default=10, help="diffusion steps (default 10)")
    p.add_argument("--model", default="openbmb/VoxCPM2", help="Hugging Face id or a local snapshot folder")
    p.add_argument("--device", default="auto", help="auto | mps | cuda | cpu")
    p.add_argument("--optimize", action="store_true", help="torch.compile (CUDA only; leave off on Mac)")
    return p.parse_args()


def main() -> int:
    a = parse_args()

    if a.design and a.ref:
        sys.exit("--design makes a new voice; do not give --ref with it")
    if not a.design and not a.ref:
        sys.exit("give --ref voice.wav (clone) or --design 'description' (new voice)")

    ref = ref_text = None
    if a.ref:
        ref = a.ref.expanduser().resolve()
        if not ref.is_file():
            sys.exit(f"reference not found: {ref}")
        txt = (a.ref_text or ref.with_suffix(".txt")).expanduser()
        if not a.no_transcript:
            if txt.is_file():
                ref_text = txt.read_text(encoding="utf-8").strip()
            else:
                print(f"note: no transcript at {txt}; cloning from the audio only", file=sys.stderr)

    mode = "design" if a.design else ("hifi" if ref_text else "clone")
    lines = read_lines(a.lines)
    if not lines:
        sys.exit(f"no lines in {a.lines}")
    only = {int(i) for i in a.only.split(",") if i.strip()}
    seeds = [int(s) for s in a.seeds.split(",") if s.strip()]

    if mode == "hifi":
        if a.style:
            sys.exit("--style has no effect in Hi-Fi mode (reference + transcript). Add --no-transcript to use it.")
        with_instr = [i for i, ln in enumerate(lines, 1) if split_instruction(ln)[0] and (not only or i in only)]
        if with_instr:
            print(f"note: Hi-Fi mode ignores instructions; dropped them from lines {with_instr}. "
                  "Use --no-transcript to apply them.", file=sys.stderr)

    import numpy as np
    import soundfile as sf
    import torch
    from voxcpm import VoxCPM

    a.out.mkdir(parents=True, exist_ok=True)
    model_id = str(Path(a.model).expanduser()) if Path(a.model).expanduser().is_dir() else a.model
    t0 = time.time()
    model = VoxCPM.from_pretrained(model_id, load_denoiser=False, optimize=a.optimize,
                                   device=None if a.device == "auto" else a.device)
    sr = int(model.tts_model.sample_rate)
    print(f"mode {mode} · model loaded in {time.time() - t0:.0f}s · {sr} Hz", flush=True)

    manifest = {"mode": mode, "model": a.model, "cfg": a.cfg, "steps": a.steps, "sample_rate": sr,
                "ref": str(ref) if ref else None, "ref_text": ref_text, "style": a.style, "design": a.design,
                "takes": []}
    man_path = a.out / "takes.json"
    if man_path.is_file() and only:  # keep earlier takes of the lines we are not redoing
        try:
            old = json.loads(man_path.read_text(encoding="utf-8"))
            manifest["takes"] = [t for t in old.get("takes", []) if t["line"] not in only]
        except (json.JSONDecodeError, KeyError):
            pass

    for i, line in enumerate(lines, 1):
        if only and i not in only:
            continue
        text = build_text(line, mode, a.style, a.design)
        spoken = split_instruction(line)[1]
        for seed in seeds:
            torch.manual_seed(seed)
            np.random.seed(seed)
            kw = {"text": text, "cfg_value": a.cfg, "inference_timesteps": a.steps}
            if ref:
                kw["reference_wav_path"] = str(ref)
                if ref_text:
                    kw["prompt_wav_path"] = str(ref)
                    kw["prompt_text"] = ref_text
            t1 = time.time()
            wav = np.asarray(model.generate(**kw), dtype=np.float32).reshape(-1)
            took = time.time() - t1
            name = f"s{i}_seed{seed}.wav"
            sf.write(a.out / name, wav, sr)
            secs = len(wav) / sr
            cps = len(re.sub(r"\s", "", spoken)) / secs if secs else 0.0
            print(f"s{i} seed {seed}: {secs:5.2f}s audio in {took:5.1f}s (RTF {took / secs:.2f}) · "
                  f"{cps:.1f} chars/s · {name}", flush=True)
            manifest["takes"].append({"file": name, "line": i, "seed": seed, "script": line, "sent": text,
                                      "seconds": round(secs, 3), "gen_seconds": round(took, 2)})

    manifest["takes"].sort(key=lambda t: (t["line"], t["seed"]))
    man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"done in {time.time() - t0:.0f}s → {a.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
