"""
Add a forward-diffusion noise effect to an animated WebP of a protein.

Progressively adds per-channel Gaussian noise across frames using a cosine
schedule. Noise is confined to a soft ellipsoid region around the protein
so edges feather smoothly into transparent background.

Input:  static/1jrj-d80_minsize.webp  (animated WebP, 84 frames)
Output: static/1jrj-d80_minsize_diffusion.webp
"""

import math
from pathlib import Path

import numpy as np
from PIL import Image

import typer


def make_ellipsoid_mask(h: int, w: int, cy: int, cx: int, ry: float, rx: float, feather: float) -> np.ndarray:
    """Create a soft ellipsoid mask (0-1) with feathered edges.

    Args:
        h, w: Image dimensions.
        cy, cx: Ellipsoid center.
        ry, rx: Ellipsoid radii (inner edge where mask is 1.0).
        feather: Width of the soft falloff zone beyond the radii.
    """
    yy, xx = np.mgrid[:h, :w]
    # Normalized distance from center (1.0 = on the ellipse edge)
    dist = np.sqrt(((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2)
    # 1.0 inside ellipse, smooth falloff in feather zone, 0.0 outside
    mask = np.clip(1.0 - (dist - 1.0) / (feather / min(ry, rx)), 0, 1)
    return mask.astype(np.float32)


def main(
    input_path: str = "static/1jrj-d80_minsize.webp",
    output_path: str = "static/1jrj-d80_minsize_diffusion.webp",
    max_sigma: float = 180.0,
    quality: int = 5,
    seed: int = 42,
    ellipse_pad: float = 1.15,
    feather_px: float = 45.0,
) -> None:
    """Apply forward-diffusion noise to an animated WebP.

    Args:
        input_path: Path to the input animated WebP.
        output_path: Path for the output animated WebP.
        max_sigma: Maximum noise standard deviation (out of 255) at the last frame.
        quality: WebP encoding quality (lower = smaller file).
        seed: Random seed for reproducibility.
        ellipse_pad: Multiplier on protein bounding box to set ellipse radii.
        feather_px: Width in pixels of the soft edge falloff.
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

    alpha_threshold = 240

    # Compute protein bounding box from first frame
    img.seek(0)
    first = np.array(img.convert("RGBA"))
    ys, xs = np.where(first[:, :, 3] >= alpha_threshold)
    cx = (xs.min() + xs.max()) // 2
    cy = (ys.min() + ys.max()) // 2
    rx = (xs.max() - xs.min()) / 2 * ellipse_pad
    ry = (ys.max() - ys.min()) / 2 * ellipse_pad

    h, w = first.shape[:2]

    # Compute padding needed so ellipse + feather fits within canvas
    pad_margin = 24  # extra pixels to avoid edge clipping
    pad_left = max(0, int(math.ceil(-(cx - rx - feather_px))) + pad_margin)
    pad_right = max(0, int(math.ceil((cx + rx + feather_px) - w)) + pad_margin)
    pad_top = max(0, int(math.ceil(-(cy - ry - feather_px))) + pad_margin)
    pad_bottom = max(0, int(math.ceil((cy + ry + feather_px) - h)) + pad_margin)
    # Adjust center for padding offset
    cx += pad_left
    cy += pad_top
    h_pad = h + pad_top + pad_bottom
    w_pad = w + pad_left + pad_right
    print(f"Padding: left={pad_left}, right={pad_right}, top={pad_top}, bottom={pad_bottom}")
    print(f"Padded canvas: {w_pad}x{h_pad}")

    ellipse_mask = make_ellipsoid_mask(h_pad, w_pad, cy, cx, ry, rx, feather_px)
    print(f"Ellipse center=({cx},{cy}), radii=({rx:.0f},{ry:.0f}), feather={feather_px}px")

    noised_frames: list[Image.Image] = []

    def pad_frame(arr: np.ndarray) -> np.ndarray:
        """Pad frame array with transparent pixels to fit ellipse."""
        if pad_top == 0 and pad_bottom == 0 and pad_left == 0 and pad_right == 0:
            return arr
        return np.pad(arr, ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), constant_values=0)

    # Extra frames of pure noise at the start (animated static, not frozen)
    hold_frames = 4
    for h_i in range(hold_frames):
        img.seek(0)
        frame = img.convert("RGBA")
        arr = pad_frame(np.array(frame, dtype=np.float32))
        is_bg = arr[:, :, 3] < alpha_threshold
        arr[:, :, 3] = np.where(is_bg, 0, 255)
        arr[is_bg, :3] = 0
        noise = rng.normal(0, max_sigma, arr[:, :, :3].shape).astype(np.float32)
        arr[:, :, :3] += noise
        arr[:, :, :3] = np.clip(arr[:, :, :3], 0, 255)
        # BG alpha modulated by ellipse mask
        arr[is_bg, 3] = 255 * ellipse_mask[is_bg]
        noised_frames.append(Image.fromarray(arr.astype(np.uint8), "RGBA"))

    for i in range(n_frames):
        img.seek(i)
        frame = img.convert("RGBA")
        arr = pad_frame(np.array(frame, dtype=np.float32))

        # Snap alpha: >= threshold → 255 (protein), below → 0 (background)
        is_bg = arr[:, :, 3] < alpha_threshold
        arr[:, :, 3] = np.where(is_bg, 0, 255)
        arr[is_bg, :3] = 0

        # Reverse diffusion: starts noisy, ends clean
        t = i / max(n_frames - 1, 1)
        sigma = max_sigma * (1 - math.sin(math.pi * t / 2))

        if sigma > 0:
            noise = rng.normal(0, sigma, arr[:, :, :3].shape).astype(np.float32)
            arr[:, :, :3] += noise
            arr[:, :, :3] = np.clip(arr[:, :, :3], 0, 255)
            # BG alpha: ellipse mask * temporal fade
            is_bg = arr[:, :, 3] == 0
            bg_t = min(t * 1.8, 1.0)
            blend_t = (1 - bg_t) ** 2
            arr[is_bg, 3] = 255 * ellipse_mask[is_bg] * blend_t

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
