"""Turn a flat-magenta imagegen atlas into a clean transparent sprite atlas."""
from pathlib import Path
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


source = Path(sys.argv[1])
target = Path(sys.argv[2])
image = Image.open(source).convert("RGBA")
pixels = np.asarray(image).copy()
rgb = pixels[:, :, :3].astype(np.int16)

# Key the generated hot-magenta field, including antialiased fringe pixels.
magenta_score = rgb[:, :, 0] + rgb[:, :, 2] - 2 * rgb[:, :, 1]
background = (rgb[:, :, 0] > 185) & (rgb[:, :, 2] > 150) & (magenta_score > 170)
background = ndimage.binary_closing(background, iterations=1)
distance = ndimage.distance_transform_edt(~background)
alpha = np.clip(distance * 255, 0, 255).astype(np.uint8)
alpha[distance >= 1.75] = 255
pixels[:, :, 3] = alpha

# Remove keyed color from partially transparent edge pixels to prevent pink halos.
a = pixels[:, :, 3].astype(np.float32) / 255.0
edge = (a > 0) & (a < 1)
for channel in (0, 2):
    values = pixels[:, :, channel].astype(np.float32)
    values[edge] = np.clip((values[edge] - 255 * (1 - a[edge])) / np.maximum(a[edge], .01), 0, 255)
    pixels[:, :, channel] = values.astype(np.uint8)

target.parent.mkdir(parents=True, exist_ok=True)
Image.fromarray(pixels).save(target)
print(target)
