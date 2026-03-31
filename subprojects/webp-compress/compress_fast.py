"""
Fast animated WebP compression using ffmpeg for re-encoding.

Tries several strategies:
1. Quality reduction only (q values from 10-50)
2. Scale down to 75% and 50%
3. Frame decimation (half the frames, double the duration)
4. Combinations

Uses ffmpeg's libwebp_anim encoder which is much faster than img2webp -m 6.
"""

import subprocess
import os
from pathlib import Path

import typer


def get_size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


def ffmpeg_webp(
    input_path: str,
    output_path: str,
    quality: int = 50,
    scale: float = 1.0,
    fps: float = 0,
    lossless: bool = False,
) -> bool:
    """Re-encode animated WebP via ffmpeg.

    ffmpeg's libwebp_anim uses -quality (0-100, higher=better but slower encoding)
    and -qscale (0-100 for lossy, where 0=worst, 100=best visual quality).
    We use -compression_level 6 for max compression effort.
    """
    # First extract to raw frames, then re-encode
    # ffmpeg can't read animated webp directly, so use Pillow to create intermediate
    vf_filters = []
    if scale != 1.0:
        vf_filters.append(f"scale=iw*{scale}:ih*{scale}:flags=lanczos")

    vf = ",".join(vf_filters) if vf_filters else None

    # Build ffmpeg command using Pillow frames as input
    # Since ffmpeg can't read animated webp, let's use the extracted frames
    frames_dir = os.path.dirname(output_path) + "/../work/frames"
    if fps > 0:
        input_fps = fps
    else:
        input_fps = 12.5  # 80ms per frame = 12.5 fps

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(input_fps),
        "-i", f"{frames_dir}/frame_%04d.png",
    ]

    if fps > 0 and fps != input_fps:
        vf_filters.append(f"fps={fps}")

    if vf_filters:
        cmd += ["-vf", ",".join(vf_filters)]

    cmd += [
        "-c:v", "libwebp_anim",
        "-lossless", "1" if lossless else "0",
        "-compression_level", "6",
        "-quality", str(quality),
        "-loop", "0",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg error: {result.stderr[-500:]}")
        return False
    return True


def main(
    input_path: str = "/Users/alex/projects/website/static/1jrj-d80_minsize.webp",
    output_dir: str = "/Users/alex/projects/website/subprojects/webp-compress/variants",
) -> None:
    """Compress animated WebP with multiple strategies using ffmpeg."""
    os.makedirs(output_dir, exist_ok=True)

    original_size = get_size_mb(input_path)
    print(f"Original: {original_size:.2f} MB (960x1201, 250 frames, 80ms/frame)")
    print()

    # Ensure frames are extracted
    frames_dir = os.path.join(os.path.dirname(output_dir), "work", "frames")
    n_frames = len(list(Path(frames_dir).glob("frame_*.png")))
    if n_frames == 0:
        print("No frames found - extracting...")
        from PIL import Image
        os.makedirs(frames_dir, exist_ok=True)
        img = Image.open(input_path)
        for i in range(img.n_frames):
            img.seek(i)
            img.copy().convert("RGBA").save(os.path.join(frames_dir, f"frame_{i:04d}.png"))
        n_frames = img.n_frames
    print(f"Using {n_frames} extracted frames from {frames_dir}")
    print()

    # Also try img2webp with lower -m for speed, for the most promising combos
    variants = [
        # (name, quality, scale, fps)
        # Quality-only variants (full res, full framerate)
        ("q50", 50, 1.0, 0),
        ("q30", 30, 1.0, 0),
        ("q20", 20, 1.0, 0),
        ("q10", 10, 1.0, 0),

        # Scale variants
        ("q50_s75", 50, 0.75, 0),
        ("q30_s75", 30, 0.75, 0),
        ("q50_s50", 50, 0.5, 0),
        ("q30_s50", 30, 0.5, 0),

        # FPS reduction (halve framerate)
        ("q50_half", 50, 1.0, 6.25),
        ("q30_half", 30, 1.0, 6.25),

        # Combo: scale + fps
        ("q50_s75_half", 50, 0.75, 6.25),
        ("q30_s75_half", 30, 0.75, 6.25),
    ]

    results = []
    for name, quality, scale, fps in variants:
        out_path = os.path.join(output_dir, f"{name}.webp")
        desc = f"q={quality}"
        if scale != 1.0:
            desc += f", scale={scale}"
        if fps > 0:
            desc += f", fps={fps}"
        print(f"Building {name} ({desc})...", end=" ", flush=True)

        ok = ffmpeg_webp(input_path, out_path, quality=quality, scale=scale, fps=fps)
        if ok:
            size = get_size_mb(out_path)
            ratio = size / original_size * 100
            results.append((name, size, ratio, desc))
            print(f"{size:.2f} MB ({ratio:.1f}%)")
        else:
            print("FAILED")
            results.append((name, -1, -1, desc))

    # Now try img2webp with -m 4 (faster than 6) for the best candidates
    print("\n--- img2webp variants (higher compression) ---")
    for m_val, q_val, skip in [(4, 30, 1), (4, 20, 1), (4, 30, 2), (4, 20, 2)]:
        name = f"img2webp_q{q_val}_m{m_val}" + (f"_skip{skip}" if skip > 1 else "")
        out_path = os.path.join(output_dir, f"{name}.webp")
        duration = 80 * skip

        frame_files = sorted(Path(frames_dir).glob("frame_*.png"))
        if skip > 1:
            frame_files = frame_files[::skip]

        frame_args = []
        for f in frame_files:
            frame_args.extend(["-d", str(duration), "-lossy", "-q", str(q_val), "-m", str(m_val), str(f)])

        cmd = ["img2webp", "-loop", "0"] + frame_args + ["-o", out_path]
        print(f"Building {name} ({len(frame_files)} frames, d={duration}ms)...", end=" ", flush=True)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            size = get_size_mb(out_path)
            ratio = size / original_size * 100
            results.append((name, size, ratio, f"img2webp m={m_val} q={q_val} skip={skip}"))
            print(f"{size:.2f} MB ({ratio:.1f}%)")
        else:
            print("FAILED")

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"{'Variant':<30} {'Size (MB)':>10} {'% orig':>8} {'Settings'}")
    print("-" * 70)
    print(f"{'ORIGINAL':<30} {original_size:>10.2f} {'100.0%':>8}")
    for name, size, ratio, desc in sorted(results, key=lambda x: x[1] if x[1] > 0 else 999):
        if size > 0:
            marker = " <-- UNDER 1MB" if size < 1.0 else (" <-- UNDER 2MB" if size < 2.0 else "")
            print(f"{name:<30} {size:>10.2f} {ratio:>7.1f}% {desc}{marker}")
        else:
            print(f"{name:<30} {'FAILED':>10}")

    # Recommendation
    print()
    good = [(n, s, r, d) for n, s, r, d in results if 0 < s < 2.0]
    if good:
        best = min(good, key=lambda x: x[1])
        print(f"RECOMMENDATION: {best[0]} at {best[1]:.2f} MB ({best[2]:.1f}% of original)")
        print(f"  Settings: {best[3]}")
        print(f"  File: {output_dir}/{best[0]}.webp")


if __name__ == "__main__":
    typer.run(main)
