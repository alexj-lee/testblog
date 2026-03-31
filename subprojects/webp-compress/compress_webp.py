"""
Compress an animated WebP file using multiple strategies and report results.

Strategies tried:
1. Re-encode with lower quality (cwebp via ffmpeg)
2. Reduce frame rate (drop every other frame, double duration)
3. Downscale dimensions
4. Combinations of the above

The script extracts frames to PNG, then reassembles with various settings.
It reports file sizes for all variants so the user can pick the best tradeoff.
"""

import subprocess
import shutil
import os
from pathlib import Path

import typer


def run(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result


def get_size_mb(path: str) -> float:
    return os.path.getsize(path) / (1024 * 1024)


def extract_frames(input_path: str, frames_dir: str) -> int:
    """Extract all frames from animated WebP to PNGs using ffmpeg."""
    os.makedirs(frames_dir, exist_ok=True)
    # Use webpmux to extract frames, then dwebp to decode
    # Actually, ffmpeg can't read animated webp well. Use Python instead.
    from PIL import Image

    img = Image.open(input_path)
    n_frames = img.n_frames
    durations = []
    for i in range(n_frames):
        img.seek(i)
        frame = img.copy().convert("RGBA")
        frame.save(os.path.join(frames_dir, f"frame_{i:04d}.png"))
        durations.append(img.info.get("duration", 80))
    return n_frames, durations


def frames_to_webp(
    frames_dir: str,
    output_path: str,
    quality: int = 75,
    duration_ms: int = 80,
    scale: float = 1.0,
    skip: int = 1,
    method: int = 6,
) -> None:
    """Assemble PNG frames back into animated WebP using img2webp or cwebp+webpmux."""
    frame_files = sorted(Path(frames_dir).glob("frame_*.png"))

    # Apply frame skipping
    if skip > 1:
        frame_files = frame_files[::skip]
        duration_ms = duration_ms * skip

    # If we need to scale, do it with ffmpeg first
    if scale != 1.0:
        scaled_dir = frames_dir + f"_scaled_{scale}"
        os.makedirs(scaled_dir, exist_ok=True)
        for f in frame_files:
            out_f = os.path.join(scaled_dir, f.name)
            run(
                f'ffmpeg -y -i "{f}" -vf "scale=iw*{scale}:ih*{scale}:flags=lanczos" "{out_f}"'
            )
        frame_files = sorted(Path(scaled_dir).glob("frame_*.png"))

    # Use img2webp for animated WebP assembly
    # Build command: img2webp -loop 0 -d <duration> -q <quality> -m <method> frame1.png frame2.png ... -o output.webp
    frame_args = []
    for f in frame_files:
        frame_args.extend(["-d", str(duration_ms), "-lossy", "-q", str(quality), "-m", str(method), str(f)])

    cmd = ["img2webp", "-loop", "0"] + frame_args + ["-o", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"img2webp failed: {result.stderr}")
        raise RuntimeError("img2webp failed")


def main(
    input_path: str = "/Users/alex/projects/website/static/1jrj-d80_minsize.webp",
    work_dir: str = "/Users/alex/projects/website/subprojects/webp-compress/work",
    output_dir: str = "/Users/alex/projects/website/subprojects/webp-compress/variants",
) -> None:
    """Compress animated WebP with multiple strategies, reporting size for each."""
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    original_size = get_size_mb(input_path)
    print(f"Original: {original_size:.2f} MB")

    # Step 1: Extract frames
    frames_dir = os.path.join(work_dir, "frames")
    print("Extracting frames...")
    n_frames, durations = extract_frames(input_path, frames_dir)
    base_duration = durations[0] if durations else 80
    print(f"  {n_frames} frames, base duration={base_duration}ms")

    # Define compression variants
    variants = [
        # (name, quality, scale, skip, method)
        ("q50_full", 50, 1.0, 1, 6),
        ("q30_full", 30, 1.0, 1, 6),
        ("q20_full", 20, 1.0, 1, 6),
        ("q50_scale75", 50, 0.75, 1, 6),
        ("q30_scale75", 30, 0.75, 1, 6),
        ("q50_scale50", 50, 0.5, 1, 6),
        ("q30_scale50", 30, 0.5, 1, 6),
        ("q50_skip2", 50, 1.0, 2, 6),
        ("q30_skip2", 30, 1.0, 2, 6),
        ("q50_scale75_skip2", 50, 0.75, 2, 6),
        ("q30_scale75_skip2", 30, 0.75, 2, 6),
    ]

    results = []
    for name, quality, scale, skip, method in variants:
        out_path = os.path.join(output_dir, f"{name}.webp")
        print(f"\nBuilding variant: {name} (q={quality}, scale={scale}, skip={skip})...")
        try:
            frames_to_webp(
                frames_dir,
                out_path,
                quality=quality,
                duration_ms=base_duration,
                scale=scale,
                skip=skip,
                method=method,
            )
            size = get_size_mb(out_path)
            ratio = size / original_size * 100
            results.append((name, size, ratio))
            print(f"  => {size:.2f} MB ({ratio:.1f}% of original)")
        except Exception as e:
            print(f"  => FAILED: {e}")
            results.append((name, -1, -1))

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"{'Variant':<25} {'Size (MB)':>10} {'% of orig':>10}")
    print("-" * 45)
    print(f"{'ORIGINAL':<25} {original_size:>10.2f} {'100.0%':>10}")
    for name, size, ratio in sorted(results, key=lambda x: x[1]):
        if size > 0:
            marker = " ***" if size < 1.0 else (" **" if size < 2.0 else "")
            print(f"{name:<25} {size:>10.2f} {ratio:>9.1f}%{marker}")
        else:
            print(f"{name:<25} {'FAILED':>10}")


if __name__ == "__main__":
    typer.run(main)
