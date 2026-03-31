"""
Animated WebP compression using Pillow for frame manipulation and img2webp for encoding.

Focuses on the strategies most likely to hit <1MB:
- Downscaling (the protein wiggle doesn't need 960x1201)
- Frame skipping (every 2nd or 3rd frame)
- Quality reduction
- Combinations of all three

Also tries Pillow's native animated WebP save which may handle
inter-frame optimization differently.
"""

import subprocess
import os
from pathlib import Path

import typer
from PIL import Image
import numpy as np


def get_size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


def scale_frames(src_dir: str, dst_dir: str, scale: float) -> None:
    """Scale all PNG frames using Pillow with high-quality Lanczos."""
    os.makedirs(dst_dir, exist_ok=True)
    for f in sorted(Path(src_dir).glob("frame_*.png")):
        img = Image.open(f)
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)
        img.save(os.path.join(dst_dir, f.name))


def build_with_img2webp(
    frames_dir: str,
    output_path: str,
    quality: int,
    method: int = 4,
    skip: int = 1,
    duration: int = 80,
) -> bool:
    """Assemble frames into animated WebP using img2webp."""
    frame_files = sorted(Path(frames_dir).glob("frame_*.png"))
    if skip > 1:
        frame_files = frame_files[::skip]
    actual_duration = duration * skip

    frame_args = []
    for f in frame_files:
        frame_args.extend([
            "-d", str(actual_duration),
            "-lossy", "-q", str(quality), "-m", str(method),
            str(f),
        ])

    cmd = ["img2webp", "-loop", "0", "-mixed"] + frame_args + ["-o", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def build_with_pillow(
    frames_dir: str,
    output_path: str,
    quality: int,
    skip: int = 1,
    duration: int = 80,
) -> bool:
    """Assemble frames into animated WebP using Pillow's native save."""
    frame_files = sorted(Path(frames_dir).glob("frame_*.png"))
    if skip > 1:
        frame_files = frame_files[::skip]
    actual_duration = duration * skip

    frames = [Image.open(f).convert("RGBA") for f in frame_files]
    if not frames:
        return False

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=actual_duration,
        loop=0,
        quality=quality,
        method=6,  # Pillow passes this to libwebp
        lossless=False,
        minimize_size=True,
    )
    return True


def main(
    input_path: str = "/Users/alex/projects/website/static/1jrj-d80_minsize.webp",
    work_dir: str = "/Users/alex/projects/website/subprojects/webp-compress/work",
    output_dir: str = "/Users/alex/projects/website/subprojects/webp-compress/variants",
) -> None:
    """Compress animated WebP aggressively, targeting <1MB."""
    os.makedirs(output_dir, exist_ok=True)

    original_size = get_size_mb(input_path)
    print(f"Original: {original_size:.2f} MB (960x1201, 250 frames, 80ms/frame)")

    # Ensure full-res frames exist
    frames_dir = os.path.join(work_dir, "frames")
    n_frames = len(list(Path(frames_dir).glob("frame_*.png")))
    if n_frames == 0:
        print("Extracting frames...")
        os.makedirs(frames_dir, exist_ok=True)
        img = Image.open(input_path)
        for i in range(img.n_frames):
            img.seek(i)
            img.copy().convert("RGBA").save(
                os.path.join(frames_dir, f"frame_{i:04d}.png")
            )

    # Create scaled frame directories
    scales = {
        "s75": 0.75,  # 720x901
        "s60": 0.6,   # 576x721
        "s50": 0.5,   # 480x601
        "s40": 0.4,   # 384x480
    }

    for label, scale in scales.items():
        scaled_dir = os.path.join(work_dir, f"frames_{label}")
        if not os.path.exists(scaled_dir) or len(list(Path(scaled_dir).glob("*.png"))) == 0:
            print(f"Scaling frames to {scale}x ({label})...")
            scale_frames(frames_dir, scaled_dir, scale)

    print()

    # Define all variants to try
    # (name, frames_subdir, quality, skip, method, engine)
    variants = [
        # Full res, aggressive quality + skip
        ("fullres_q20_skip2", "frames", 20, 2, 4, "img2webp"),
        ("fullres_q15_skip2", "frames", 15, 2, 4, "img2webp"),
        ("fullres_q10_skip2", "frames", 10, 2, 4, "img2webp"),
        ("fullres_q20_skip3", "frames", 20, 3, 4, "img2webp"),
        ("fullres_q10_skip3", "frames", 10, 3, 4, "img2webp"),

        # 75% scale
        ("s75_q30", "frames_s75", 30, 1, 4, "img2webp"),
        ("s75_q20", "frames_s75", 20, 1, 4, "img2webp"),
        ("s75_q30_skip2", "frames_s75", 30, 2, 4, "img2webp"),
        ("s75_q20_skip2", "frames_s75", 20, 2, 4, "img2webp"),

        # 60% scale
        ("s60_q30", "frames_s60", 30, 1, 4, "img2webp"),
        ("s60_q20", "frames_s60", 20, 1, 4, "img2webp"),
        ("s60_q30_skip2", "frames_s60", 30, 2, 4, "img2webp"),
        ("s60_q20_skip2", "frames_s60", 20, 2, 4, "img2webp"),

        # 50% scale
        ("s50_q50", "frames_s50", 50, 1, 4, "img2webp"),
        ("s50_q30", "frames_s50", 30, 1, 4, "img2webp"),
        ("s50_q20", "frames_s50", 20, 1, 4, "img2webp"),
        ("s50_q30_skip2", "frames_s50", 30, 2, 4, "img2webp"),

        # 40% scale - most aggressive
        ("s40_q50", "frames_s40", 50, 1, 4, "img2webp"),
        ("s40_q30", "frames_s40", 30, 1, 4, "img2webp"),

        # Pillow engine variants (may optimize inter-frame better)
        ("pillow_s60_q30", "frames_s60", 30, 1, 0, "pillow"),
        ("pillow_s50_q30", "frames_s50", 30, 1, 0, "pillow"),
        ("pillow_s50_q20", "frames_s50", 20, 1, 0, "pillow"),
        ("pillow_s50_q30_skip2", "frames_s50", 30, 2, 0, "pillow"),
    ]

    results = []
    for name, fdir, quality, skip, method, engine in variants:
        full_fdir = os.path.join(work_dir, fdir)
        out_path = os.path.join(output_dir, f"{name}.webp")

        n = len(list(Path(full_fdir).glob("frame_*.png")))
        effective_frames = n // skip if skip > 1 else n
        print(f"  {name:<30} ({effective_frames} frames, q={quality})...", end=" ", flush=True)

        try:
            if engine == "img2webp":
                ok = build_with_img2webp(full_fdir, out_path, quality, method, skip)
            else:
                ok = build_with_pillow(full_fdir, out_path, quality, skip)

            if ok:
                size = get_size_mb(out_path)
                ratio = size / original_size * 100
                results.append((name, size, ratio))
                marker = " ***" if size < 1.0 else ""
                print(f"{size:.2f} MB ({ratio:.1f}%){marker}")
            else:
                print("FAILED")
                results.append((name, -1, -1))
        except Exception as e:
            print(f"ERROR: {e}")
            results.append((name, -1, -1))

    # Summary
    print("\n" + "=" * 65)
    print("RESULTS SUMMARY (sorted by size)")
    print("=" * 65)
    print(f"{'Variant':<35} {'Size (MB)':>10} {'% orig':>8}")
    print("-" * 55)
    print(f"{'ORIGINAL':<35} {original_size:>10.2f} {'100.0%':>8}")
    for name, size, ratio in sorted(results, key=lambda x: x[1] if x[1] > 0 else 999):
        if size > 0:
            marker = " <-- TARGET" if size < 1.0 else ""
            print(f"{name:<35} {size:>10.2f} {ratio:>7.1f}%{marker}")

    under_1 = [(n, s, r) for n, s, r in results if 0 < s < 1.0]
    under_2 = [(n, s, r) for n, s, r in results if 0 < s < 2.0]

    print()
    if under_1:
        best = min(under_1, key=lambda x: abs(x[1] - 0.8))  # closest to 0.8MB = good balance
        print(f"BEST UNDER 1MB: {best[0]} at {best[1]:.2f} MB")
    elif under_2:
        best = min(under_2, key=lambda x: x[1])
        print(f"BEST UNDER 2MB: {best[0]} at {best[1]:.2f} MB")
    else:
        best_overall = min(results, key=lambda x: x[1] if x[1] > 0 else 999)
        print(f"SMALLEST: {best_overall[0]} at {best_overall[1]:.2f} MB")


if __name__ == "__main__":
    typer.run(main)
