"""Isolate the accepted Ash illustration and build a usable transparent pose bank."""
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

root=Path(__file__).resolve().parents[1]
source=root/'sprite-fighter/style-wave2/ash-ketchum/candidates/design-reference-v1-rejected-background.png'
out=root/'sprite-fighter/style-wave2/ash-ketchum/conversion-v1/trainer-v1.png'
image=Image.open(source).convert('RGBA');pixels=np.asarray(image).copy();rgb=pixels[:,:,:3]
light=rgb.max(axis=2)
mask=light>38
labels,count=ndimage.label(mask)
areas=np.bincount(labels.ravel());areas[0]=0
# The central subject and its soft aura form the dominant non-black component.
subject=labels==areas.argmax()
subject=ndimage.binary_closing(subject,iterations=3)
subject=ndimage.binary_fill_holes(subject)
subject=ndimage.binary_opening(subject,iterations=1)
box=ndimage.find_objects(subject.astype(np.uint8))[0]
crop=pixels[box].copy();alpha=(subject[box]*255).astype(np.uint8)
alpha=ndimage.gaussian_filter(alpha.astype(float),.65).clip(0,255).astype(np.uint8)
crop[:,:,3]=alpha
figure=Image.fromarray(crop)

canvas=Image.new('RGBA',(1600,1600))
for row in range(4):
 for col in range(4):
  cell=figure.copy()
  scale=(.88,.92,.96,.90)[col]
  cell.thumbnail((int(350*scale),int(350*scale)),Image.Resampling.LANCZOS)
  x=col*400+(400-cell.width)//2;y=row*400+(400-cell.height)//2
  canvas.alpha_composite(cell,(x,y))
out.parent.mkdir(parents=True,exist_ok=True);canvas.save(out);print(out)
