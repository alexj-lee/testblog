"""
Add a forward-diffusion noise effect to an animated WebP of a protein.

Progressively adds per-channel Gaussian noise across frames using a cosine
schedule. Noise is applied only to non-transparent pixels so the background
stays clean. The result mimics the forward process of a diffusion model:
clean at frame 0, heavily noised by the last frame.

Input:  static/1jrj-d80_minsize.webp  (animated WebP, 84 frames)
Output: static/1jrj-d80_minsize_diffusion.webp
"""

import math
from pathlib import Path

import numpy as np
from PIL import Image

import typer


def main(
    input_path: str = "static/1jrj-d80_minsize.webp",
    output_path: str = "static/1jrj-d80_minsize_diffusion.webp",
    max_sigma: float = 180.0,
    quality: int = 5,
    seed: int = 42,
) -> None:
    """Apply forward-diffusion noise to an animated WebP.

    Args:
        input_path: Path to the input animated WebP.
        output_path: Path for the output animated WebP.
        max_sigma: Maximum noise standard deviation (out of 255) at the last frame.
        quality: WebP encoding quality (lower = smaller file).
        seed: Random seed for reproducibility.
    """
    root = Path(__file__).resolve().parents[2]
    inp = root / input_path
    out = root / output_path

    rng = np.random.default_rng(seed)

    img = Image.open(inp)
    n_frames = getattr(img, "n_frames", 1)
    duration = img.info.get("duration", 240)
    out_duration = 180

    print(f"Input: {inp} ({n_frames} frames, {duration}ms/frame)")
    print(f"Output frame duration: {out_duration}ms/frame")

    noised_frames: list[Image.Image] = []

    # Use a very high alpha threshold to kill semi-transparent fringe pixels
    alpha_threshold = 240

    # Extra frames of pure noise at the start (animated static, not frozen)
    hold_frames = 4
    for h in range(hold_frames):
        img.seek(0)
        frame = img.convert("RGBA")
        arr = np.array(frame, dtype=np.float32)
        is_bg = arr[:, :, 3] < alpha_threshold
        arr[:, :, 3] = np.where(is_bg, 0, 255)
        arr[is_bg, :3] = 0
        noise = rng.normal(0, max_sigma, arr[:, :, :3].shape).astype(np.float32)
        arr[:, :, :3] += noise
        arr[:, :, :3] = np.clip(arr[:, :, :3], 0, 255)
        arr[is_bg, 3] = 255
        noised_frames.append(Image.fromarray(arr.astype(np.uint8), "RGBA"))

    for i in range(n_frames):
        img.seek(i)
        frame = img.convert("RGBA")
        arr = np.array(frame, dtype=np.float32)

        # Snap alpha: >= threshold → 255 (protein), below → 0 (background)
        is_bg = arr[:, :, 3] < alpha_threshold
        arr[:, :, 3] = np.where(is_bg, 0, 255)
        # Zero out RGB on background pixels to kill white fringe
        arr[is_bg, :3] = 0

        # Reverse diffusion: starts noisy, ends clean
        t = i / max(n_frames - 1, 1)
        sigma = max_sigma * (1 - math.sin(math.pi * t / 2))

        if sigma > 0:
            # Per-channel additive Gaussian noise on all pixels (RGB)
            noise = rng.normal(0, sigma, arr[:, :, :3].shape).astype(np.float32)
            arr[:, :, :3] += noise
            arr[:, :, :3] = np.clip(arr[:, :, :3], 0, 255)
            # Fade out alpha on background pixels faster than protein denoises
            is_bg = arr[:, :, 3] == 0
            bg_t = min(t * 1.8, 1.0)  # 1.8x faster fade to transparent
            blend_t = (1 - bg_t) ** 2
            arr[is_bg, 3] = 255 * blend_t

        noised_frames.append(Image.fromarray(arr.astype(np.uint8), "RGBA"))

    # Save animated WebP
    noised_frames[0].save(
        out,
        save_all=True,
        append_images=noised_frames[1:],
        duration=out_duration,
        loop=0,
        quality=quality,
        method=4,
        lossless=False,
    )

    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"Output: {out} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    typer.run(main)
