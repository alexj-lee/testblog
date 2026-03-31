"""Fine-tune compression parameters around the 1MB target."""
import subprocess
import os
from pathlib import Path

work_dir = "/Users/alex/projects/website/subprojects/webp-compress/work"
output_dir = "/Users/alex/projects/website/subprojects/webp-compress/final"

configs = [
    ("s50_q25_skip3", "frames_s50", 25, 3),
    ("s50_q22_skip3", "frames_s50", 22, 3),
    ("s50_q18_skip3", "frames_s50", 18, 3),
    ("s40_q15_skip2", "frames_s40", 15, 2),
    ("s40_q10_skip2", "frames_s40", 10, 2),
    ("s40_q25_skip2", "frames_s40", 25, 2),
    # Try s50 skip2 with very low quality
    ("s50_q10_skip2", "frames_s50", 10, 2),
    ("s50_q15_skip2", "frames_s50", 15, 2),
]

for name, fdir, quality, skip in configs:
    full_fdir = os.path.join(work_dir, fdir)
    out_path = os.path.join(output_dir, f"{name}.webp")
    ff = sorted(Path(full_fdir).glob("frame_*.png"))[::skip]
    duration = 80 * skip

    frame_args = []
    for f in ff:
        frame_args.extend(["-d", str(duration), "-lossy", "-q", str(quality), "-m", "4", str(f)])

    cmd = ["img2webp", "-loop", "0", "-mixed"] + frame_args + ["-o", out_path]
    print(f"{name:<25} ({len(ff)} frames)...", end=" ", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(out_path) / (1024 * 1024)
        marker = " ***" if size < 1.0 else ""
        print(f"{size:.2f} MB{marker}")
    else:
        print("FAILED")
