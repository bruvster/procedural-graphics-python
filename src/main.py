from pathlib import Path

import numpy as np
from PIL import Image


WIDTH = 512 
HEIGHT = 512

def create_image(width, height):
    # Each array contains the x or y coordinate for every pixel.
    x = np.arange(width, dtype=np.float32)
    y = np.arange(height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)

    # Distance of each pixel from the image center.
    dx = xx - width / 2
    dy = yy - height / 2
    distance = np.sqrt(dx * dx + dy * dy)

    # Use distance to make repeating rings, then map them to RGB channels.
    pattern = (np.sin(distance * 0.08) + 1) / 2
    red = pattern
    green = (np.sin(distance * 0.08 + 2.1) + 1) / 2
    blue = (np.sin(distance * 0.08 + 4.2) + 1) / 2

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "colors.txt").open("w") as file:
        for name, channel in (("red", red), ("green", green), ("blue", blue)):
            file.write(f"{name}:\n")
            np.savetxt(file, channel, fmt="%.6f")
            file.write("\n")

    # Stack the channels into an (height, width, 3) image array.
    image = np.stack((red, green, blue), axis=-1)
    return (image * 255).astype(np.uint8)

def main():
    img = create_image(WIDTH, HEIGHT)
    pil_img = Image.fromarray(img)
    pil_img.save("output/output.png")

if __name__ == "__main__":
    main()
