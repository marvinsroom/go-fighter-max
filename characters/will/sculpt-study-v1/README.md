# Will head-only shape study

This is a local, editable 3D proportion study, not an approved Will likeness.
It uses a human topology cage from the earlier MPFB body as starting topology,
with explicit vertex-region edits. The rejected generated head and photographic
skin projection are not used. No landmark fitting, external uploads, paid tools,
or Unreal changes are involved.

Files:

- `head-baseline.blend`: isolated starting topology, before this shape study.
- `will-head-shape-study.blend`: reshaped head, separate eyes with procedural
  irises, brows, fine moustache strips and a simplified high-top hair mass.
- `will-head-toon-review.blend`: Blender Eevee material study using diffuse light
  through Shader-to-RGB, three constant shading bands, and a reversed mesh hull
  for the outline. Includes the approved concept as an unrendered reference.
- `clay-front.png`, `clay-profile.png`: actual geometry review renders.
- `toon-front.png`, `toon-three-quarter.png`, `toon-profile.png`: actual 3D toon
  review renders, not image-generated concepts or in-game captures.

All images used on surfaces are absent; flat colors, procedural eye masks and
vertex fade values supply material colors. A separate reference image object in
the toon file is for editing guidance only. The toon nodes are Blender-specific;
an equivalent Unreal material has not been implemented.

The first iterations exposed excessive hair height, scalp clipping and faceted
iris edges. These were revised before the final views. Facial proportions still
need deliberate likeness work and user review. No facial rig, expressions,
body fitting or animation acceptance is claimed. Keep the head review separate
from rig/body integration until the user accepts its likeness.

Scripts: `build-will-head-study.py`, `refine-will-head-study.py`,
`render-will-toon-study.py`. They write this study folder and preserve original
body, concept, generated-mesh and Unreal assets. Baseline images are historical;
use the clay/toon views for the current study.
