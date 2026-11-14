#!/usr/bin/env python3
"""Check that this machine can run the voxcpm2-voiceover skill, and say how to fix what is missing.

  python3 doctor.py --find                       # look for venvs that already have voxcpm (run this first)
  python3 doctor.py --python .venv-voxcpm/bin/python   # check that venv, ffmpeg, the model cache and memory
  python3 doctor.py --python ... --json          # the same, as JSON

Standard library only, so any python3 can run it. Exit 0 when everything required is ready, 1 when not.
Run it when installing, or after a script fails; there is no need to run it before every job.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

TESTED_VOXCPM = "2.0.3"
MODEL_REPO = "models--openbmb--VoxCPM2"
WHISPER_REPO = "models--mlx-community--whisper-large-v3-mlx"
FILTERS = ["silenceremove", "areverse", "atempo", "loudnorm", "anullsrc", "concat", "aresample", "aformat", "atrim"]
MIN_FREE_GB = 16
SKIP_DIRS = {"Library", "node_modules", ".git", ".cache", ".Trash", "Pictures", "Movies", "Music", ".npm",
             ".cargo", ".rustup", "site-packages", "__pycache__", ".pyenv", ".local", "Applications"}
INSTALL = ("python3.12 -m venv .venv-voxcpm && .venv-voxcpm/bin/pip install -r "
           "<skill-dir>/requirements.txt")

PROBE = r"""
import json, sys, importlib.metadata as m, importlib.util as u
out = {"python": sys.version.split()[0], "executable": sys.executable}
for pkg in ("voxcpm", "mlx-whisper", "soundfile", "torch"):
    try:
        out[pkg] = m.version(pkg)
    except m.PackageNotFoundError:
        out[pkg] = None
if out["torch"]:
    try:
        import torch
        out["mps"] = bool(torch.backends.mps.is_available())
        out["cuda"] = bool(torch.cuda.is_available())
    except Exception as e:
        out["torch_error"] = repr(e)
print(json.dumps(out))
"""


def hf_hub() -> Path:
    if os.environ.get("HF_HUB_CACHE"):
        return Path(os.environ["HF_HUB_CACHE"]).expanduser()
    if os.environ.get("HF_HOME"):
        return Path(os.environ["HF_HOME"]).expanduser() / "hub"
    return Path("~/.cache/huggingface/hub").expanduser()


def snapshot_size(repo_dir: Path, needed: list[str]) -> tuple[Path | None, float]:
    """Newest snapshot holding every needed file (any one of a|b), and its size in GB."""
    snaps = sorted((repo_dir / "snapshots").glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for snap in snaps:
        files = []
        for want in needed:
            hit = next((snap / w for w in want.split("|") if (snap / w).exists()), None)
            if hit is None:
                break
            files.append(hit)
        else:
            size = sum(f.resolve().stat().st_size for f in snap.iterdir() if f.is_file() or f.is_symlink())
            return snap, size / 1e9
    return None, 0.0


def free_memory_gb() -> tuple[float | None, float | None]:
    """(total, roughly available) in GB."""
    try:
        if sys.platform == "darwin":
            total = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=False).stdout)
            vm = subprocess.run(["vm_stat"], capture_output=True, text=True, check=False).stdout
            page = int(re.search(r"page size of (\d+)", vm).group(1))
            pages = {k.strip(): int(v.strip(" .")) for k, v in re.findall(r"^([^:]+):\s+(\d+)\.?$", vm, re.MULTILINE)}
            free = sum(pages.get(k, 0) for k in ("Pages free", "Pages inactive", "Pages speculative",
                                                   "Pages purgeable"))
            return total / 2**30, free * page / 2**30
        info = dict(line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines() if ":" in line)
        return int(info["MemTotal"].split()[0]) / 2**20, int(info["MemAvailable"].split()[0]) / 2**20  # kB -> GiB
    except (OSError, ValueError, KeyError, AttributeError, subprocess.SubprocessError):
        return None, None


def find_venvs(root: Path, max_depth: int = 6) -> list[dict]:
    found = []
    root_depth = len(root.parts)
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath)
        if "pyvenv.cfg" in filenames:
            dirnames[:] = []
            for sp in here.glob("lib/python*/site-packages"):
                dist = sorted(sp.glob("voxcpm-*.dist-info"))
                if dist:
                    found.append({"python": str(here / "bin" / "python"),
                                  "voxcpm": dist[-1].name.removesuffix(".dist-info").split("-", 1)[1],
                                  "mlx-whisper": bool(list(sp.glob("mlx_whisper-*.dist-info")))})
            continue
        if len(here.parts) - root_depth >= max_depth:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".") or d.startswith(".venv")]
    return found


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--python", default=sys.executable, help="interpreter of the VoxCPM2 venv (default: this one)")
    p.add_argument("--find", action="store_true", help="look for existing venvs with voxcpm under --root")
    p.add_argument("--root", default="~", help="where --find looks (default: home folder)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    checks: list[dict] = []

    def add(name: str, status: str, detail: str, fix: str = "") -> None:
        checks.append({"name": name, "status": status, "detail": detail, "fix": fix})

    venvs = find_venvs(Path(a.root).expanduser()) if a.find else None

    # 1. the interpreter that will run synth.py / check_takes.py
    py = shutil.which(a.python) or a.python
    info: dict = {}
    if not Path(py).exists():
        add("python", "fail", f"{a.python} not found", INSTALL)
    else:
        r = subprocess.run([py, "-c", PROBE], capture_output=True, text=True, timeout=180, check=False)
        if r.returncode != 0 or not r.stdout.strip():
            add("python", "fail", f"{py} did not run: {r.stderr.strip()[-200:]}", INSTALL)
        else:
            info = json.loads(r.stdout.strip().splitlines()[-1])
            ver = tuple(int(x) for x in info["python"].split(".")[:2])
            add("python", "ok" if ver >= (3, 10) else "fail", f"{info['python']} ({info['executable']})",
                "" if ver >= (3, 10) else "use Python 3.10 or newer (tested with 3.12)")
    if info:
        v = info.get("voxcpm")
        if not v:
            add("voxcpm", "fail", "not installed in this interpreter", INSTALL)
        else:
            add("voxcpm", "ok" if v == TESTED_VOXCPM else "warn", f"{v} (tested {TESTED_VOXCPM})",
                "" if v == TESTED_VOXCPM else f"pip install voxcpm=={TESTED_VOXCPM} if a script fails")
        if info.get("torch"):
            dev = "mps" if info.get("mps") else "cuda" if info.get("cuda") else "cpu"
            add("device", "ok" if dev != "cpu" else "warn", f"torch {info['torch']} · {dev}",
                "" if dev != "cpu" else "no GPU: it runs on CPU, many times slower")
        mw = info.get("mlx-whisper")
        add("mlx-whisper", "ok" if mw else "warn", mw or "not installed (only check_takes.py needs it)",
            "" if mw else "pip install mlx-whisper==0.4.3 (Apple Silicon only)")

    # 2. model weights
    offline = os.environ.get("HF_HUB_OFFLINE") in ("1", "true", "True")
    snap, gb = snapshot_size(hf_hub() / MODEL_REPO, ["model.safetensors", "audiovae.pth", "config.json"])
    if snap:
        add("VoxCPM2 weights", "ok", f"{gb:.1f} GB in {snap}")
    else:
        add("VoxCPM2 weights", "fail" if offline else "warn",
            "not downloaded yet" + (" and HF_HUB_OFFLINE is set" if offline else ""),
            "unset HF_HUB_OFFLINE for the first run" if offline
            else "the first synth.py run downloads about 5 GB from Hugging Face (no token needed)")
    wsnap, wgb = snapshot_size(hf_hub() / WHISPER_REPO, ["weights.npz|weights.safetensors", "config.json"])
    add("Whisper weights", "ok" if wsnap else "warn", f"{wgb:.1f} GB in {wsnap}" if wsnap else "not downloaded yet",
        "" if wsnap else "the first check_takes.py run downloads about 3 GB")

    # 3. ffmpeg
    ff, fp = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ff or not fp:
        add("ffmpeg", "fail", "ffmpeg/ffprobe not on PATH",
            "brew install ffmpeg (macOS) · sudo apt install ffmpeg (Ubuntu)")
    else:
        out = subprocess.run([ff, "-hide_banner", "-filters"], capture_output=True, text=True, check=False).stdout
        have = {ln.split()[1] for ln in out.splitlines() if len(ln.split()) > 2 and ln.startswith(" ")}
        missing = [f for f in FILTERS if f not in have]
        ver = subprocess.run([ff, "-hide_banner", "-version"], capture_output=True, text=True, check=False).stdout.split()[2]
        add("ffmpeg", "fail" if missing else "ok", f"{ver} ({ff})" + (f" · missing {missing}" if missing else ""),
            "install a full ffmpeg build" if missing else "")

    # 4. memory
    total, free = free_memory_gb()
    if total is None:
        add("memory", "warn", "could not read", f"VoxCPM2 needs about {MIN_FREE_GB} GB free")
    else:
        add("memory", "ok" if free >= MIN_FREE_GB else "warn", f"{free:.0f} GB free of {total:.0f} GB",
            "" if free >= MIN_FREE_GB else f"close other apps: the model needs about {MIN_FREE_GB} GB")

    ready = all(c["status"] != "fail" for c in checks)
    if a.json:
        print(json.dumps({"ok": ready, "platform": platform.platform(), "checks": checks, "venvs": venvs},
                         ensure_ascii=False, indent=1))
        return 0 if ready else 1

    if venvs is not None:
        print("venvs with voxcpm:" if venvs else f"no venv with voxcpm under {a.root}")
        for v in venvs:
            print(f"  {v['python']}  voxcpm {v['voxcpm']}  mlx-whisper {'yes' if v['mlx-whisper'] else 'no'}")
        print()
    print(f"checking {a.python}")
    for c in checks:
        print(f"  {c['status']:4s}  {c['name']:16s} {c['detail']}")
        if c["fix"]:
            print(f"        {'':16s} → {c['fix']}")
    print("\nready" if ready else f"\nnot ready: {sum(c['status'] == 'fail' for c in checks)} problem(s)")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
