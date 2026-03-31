"""
Final pass at animated WebP compression for protein wiggle animation.

Key insight: animated WebP (like GIF) encodes frames mostly independently.
For a wiggling protein that changes slowly between frames, we can:
1. Skip frames aggressively (3-5x) since the wiggle is subtle
2. Scale down since hero images are often displayed at CSS-constrained sizes
3. Use lowest quality that still looks good for a protein visualization

Also tries: converting to looping MP4/WebM video for comparison, since
video codecs (H.264, VP9) do real inter-frame prediction.
"""

import subprocess
import os
from pathlib import Path

import typer
from PIL import Image


def get_size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


def main(
    input_path: str = "/Users/alex/projects/website/static/1jrj-d80_minsize.webp",
    work_dir: str = "/Users/alex/projects/website/subprojects/webp-compress/work",
    output_dir: str = "/Users/alex/projects/website/subprojects/webp-compress/final",
) -> None:
    """Try the most promising compression strategies."""
    os.makedirs(output_dir, exist_ok=True)

    original_size = get_size_mb(input_path)
    print(f"Original: {original_size:.2f} MB")

    # Ensure frames are extracted
    frames_dir = os.path.join(work_dir, "frames")
    frame_files = sorted(Path(frames_dir).glob("frame_*.png"))
    n_frames = len(frame_files)
    print(f"Working with {n_frames} extracted frames")

    # Create scaled variants we need
    for scale_label, scale_val in [("s50", 0.5), ("s40", 0.4)]:
        d = os.path.join(work_dir, f"frames_{scale_label}")
        if not os.path.exists(d) or len(list(Path(d).glob("*.png"))) < n_frames:
            print(f"Creating {scale_label} frames...")
            os.makedirs(d, exist_ok=True)
            for f in frame_files:
                img = Image.open(f)
                new_size = (int(img.width * scale_val), int(img.height * scale_val))
                img.resize(new_size, Image.LANCZOS).save(os.path.join(d, f.name))

    results = []

    # Strategy 1: img2webp with aggressive settings
    # -m 4 is a good speed/quality tradeoff
    configs = [
        # (name, frame_dir, quality, skip, method)
        ("s50_q20_skip2", "frames_s50", 20, 2, 4),
        ("s50_q15_skip3", "frames_s50", 15, 3, 4),
        ("s50_q20_skip3", "frames_s50", 20, 3, 4),
        ("s50_q30_skip3", "frames_s50", 30, 3, 4),
        ("s50_q20_skip4", "frames_s50", 20, 4, 4),
        ("s50_q20_skip5", "frames_s50", 20, 5, 4),
        ("s40_q20_skip2", "frames_s40", 20, 2, 4),
        ("s40_q20_skip3", "frames_s40", 20, 3, 4),
        ("s40_q30_skip2", "frames_s40", 30, 2, 4),
    ]

    for name, fdir, quality, skip, method in configs:
        full_fdir = os.path.join(work_dir, fdir)
        out_path = os.path.join(output_dir, f"{name}.webp")
        ff = sorted(Path(full_fdir).glob("frame_*.png"))[::skip]
        duration = 80 * skip

        frame_args = []
        for f in ff:
            frame_args.extend(["-d", str(duration), "-lossy", "-q", str(quality), "-m", str(method), str(f)])

        cmd = ["img2webp", "-loop", "0", "-mixed"] + frame_args + ["-o", out_path]
        print(f"  {name:<30}", end=" ", flush=True)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            size = get_size_mb(out_path)
            ratio = size / original_size * 100
            results.append((name, size, ratio, "webp"))
            marker = " ***" if size < 1.0 else ""
            print(f"{size:.2f} MB ({ratio:.1f}%){marker}")
        else:
            print("FAILED")

    # Strategy 2: Pillow animated WebP with minimize_size (but use method=4 for speed)
    print("\n--- Pillow variants ---")
    pillow_configs = [
        ("pil_s50_q15_skip2", "frames_s50", 15, 2),
        ("pil_s50_q20_skip2", "frames_s50", 20, 2),
        ("pil_s50_q20_skip3", "frames_s50", 20, 3),
        ("pil_s40_q20_skip2", "frames_s40", 20, 2),
        ("pil_s40_q30_skip2", "frames_s40", 30, 2),
    ]

    for name, fdir, quality, skip in pillow_configs:
        full_fdir = os.path.join(work_dir, fdir)
        out_path = os.path.join(output_dir, f"{name}.webp")
        ff = sorted(Path(full_fdir).glob("frame_*.png"))[::skip]
        duration = 80 * skip

        print(f"  {name:<30} ({len(ff)} frames)", end=" ", flush=True)
        frames = [Image.open(f).convert("RGBA") for f in ff]
        frames[0].save(
            out_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            quality=quality,
            method=4,
            lossless=False,
            minimize_size=True,
        )
        size = get_size_mb(out_path)
        ratio = size / original_size * 100
        results.append((name, size, ratio, "webp"))
        marker = " ***" if size < 1.0 else ""
        print(f"{size:.2f} MB ({ratio:.1f}%){marker}")

    # Strategy 3: Convert to video formats (much better inter-frame compression)
    print("\n--- Video format variants (for comparison) ---")

    # VP9 WebM - can be used as <video> with autoplay loop
    for scale_label, fdir in [("s50", "frames_s50"), ("s40", "frames_s40")]:
        for crf in [35, 40, 45]:
            name = f"vp9_{scale_label}_crf{crf}"
            full_fdir = os.path.join(work_dir, fdir)
            out_path = os.path.join(output_dir, f"{name}.webm")

            cmd = [
                "ffmpeg", "-y",
                "-framerate", "12.5",
                "-i", f"{full_fdir}/frame_%04d.png",
                "-c:v", "libvpx-vp9",
                "-crf", str(crf),
                "-b:v", "0",
                "-pix_fmt", "yuva420p",
                "-auto-alt-ref", "0",
                out_path,
            ]
            print(f"  {name:<30}", end=" ", flush=True)
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size = get_size_mb(out_path)
                ratio = size / original_size * 100
                results.append((name, size, ratio, "webm"))
                marker = " ***" if size < 1.0 else ""
                print(f"{size:.2f} MB ({ratio:.1f}%){marker}")
            else:
                print(f"FAILED: {result.stderr[-200:]}")

    # H.264 MP4 (no alpha but tiny files, can use poster image for alpha)
    for scale_label, fdir in [("s50", "frames_s50")]:
        for crf in [28, 32, 36]:
            name = f"h264_{scale_label}_crf{crf}"
            full_fdir = os.path.join(work_dir, fdir)
            out_path = os.path.join(output_dir, f"{name}.mp4")

            cmd = [
                "ffmpeg", "-y",
                "-framerate", "12.5",
                "-i", f"{full_fdir}/frame_%04d.png",
                "-c:v", "libx264",
                "-crf", str(crf),
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                out_path,
            ]
            print(f"  {name:<30}", end=" ", flush=True)
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size = get_size_mb(out_path)
                ratio = size / original_size * 100
                results.append((name, size, ratio, "mp4"))
                marker = " ***" if size < 1.0 else ""
                print(f"{size:.2f} MB ({ratio:.1f}%){marker}")
            else:
                print("FAILED")

    # Summary
    print("\n" + "=" * 70)
    print("ALL RESULTS (sorted by size)")
    print("=" * 70)
    print(f"{'Variant':<35} {'Size':>8} {'%':>7} {'Format'}")
    print("-" * 60)
    print(f"{'ORIGINAL':<35} {'8.13MB':>8} {'100.0%':>7} {'webp'}")
    for name, size, ratio, fmt in sorted(results, key=lambda x: x[1] if x[1] > 0 else 999):
        if size > 0:
            marker = " <--" if size < 1.0 else ""
            print(f"{name:<35} {size:>7.2f}M {ratio:>6.1f}% {fmt}{marker}")

    # Pick the best WebP variant
    webp_results = [(n, s, r) for n, s, r, f in results if f == "webp" and s > 0]
    if webp_results:
        best_webp = min(webp_results, key=lambda x: x[1])
        print(f"\nBest WebP: {best_webp[0]} at {best_webp[1]:.2f} MB ({best_webp[2]:.1f}%)")
        print(f"  -> {output_dir}/{best_webp[0]}.webp")

    video_results = [(n, s, r, f) for n, s, r, f in results if f in ("webm", "mp4") and s > 0]
    if video_results:
        best_vid = min(video_results, key=lambda x: x[1])
        print(f"\nBest video: {best_vid[0]} at {best_vid[1]:.2f} MB ({best_vid[2]:.1f}%)")
        ext = best_vid[3]
        print(f"  -> {output_dir}/{best_vid[0]}.{ext}")
        print(f"  Use as: <video autoplay loop muted playsinline src=\"{best_vid[0]}.{ext}\">")


if __name__ == "__main__":
    typer.run(main)
