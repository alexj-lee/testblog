"""Check if the animated WebP frames actually use transparency."""
from PIL import Image
import numpy as np

img = np.array(Image.open("/Users/alex/projects/website/subprojects/webp-compress/work/frames/frame_0000.png"))
print(f"Shape: {img.shape}")
if img.shape[2] == 4:
    alpha = img[:, :, 3]
    print(f"Alpha min={alpha.min()}, max={alpha.max()}")
    transparent = (alpha < 255).sum()
    total = alpha.size
    print(f"Transparent pixels: {transparent}/{total} ({transparent/total*100:.1f}%)")
    # Check corners
    print(f"Top-left corner alpha: {alpha[0, 0]}")
    print(f"Center alpha: {alpha[alpha.shape[0]//2, alpha.shape[1]//2]}")
