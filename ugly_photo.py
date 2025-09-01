"""Simple script to make a photo look slightly ugly by adding noise and blur.

Requires Pillow and NumPy.
"""

from PIL import Image, ImageFilter
import numpy as np
import random


def make_ugly(input_path: str, output_path: str) -> None:
    """Add mild noise and blur to degrade the image."""
    image = Image.open(input_path).convert("RGB")
    arr = np.asarray(image).astype(np.int16)
    noise = np.random.randint(0, 40, arr.shape, dtype="int16")
    arr = arr - noise
    arr = np.clip(arr, 0, 255).astype("uint8")
    degraded = Image.fromarray(arr)
    degraded = degraded.filter(ImageFilter.GaussianBlur(radius=1))
    degraded.save(output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Make a photo a little ugly.")
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Path to save the uglified image")
    args = parser.parse_args()

    make_ugly(args.input, args.output)

