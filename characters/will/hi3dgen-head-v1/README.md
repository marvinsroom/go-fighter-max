# Free Hi3DGen head candidate

The user explicitly approved sending the existing isolated Will head reference
to Stable-X/Hi3DGen after an automatic approval review required destination-specific
permission. One free public generation succeeded. No account token, subscription,
payment or paid endpoint was used. Free service quotas may affect future attempts.

Source demo: https://huggingface.co/spaces/Stable-X/Hi3DGen
Input: ../reference-reconstruction/will-head-input-v1.png
Seed: 2718. Sparse structure guidance 3 / 50 steps; latent guidance 3 / 6 steps.

`will-head-raw.glb` is the unaltered 22,211,224-byte downloaded model.
`will-hi3dgen-geometry-review.blend` contains the actual mesh, uniformly scaled
to 34cm height and centered for review. No face reshaping or photo projection.
The four `clay-*.png` files are neutral Blender Workbench geometry renders.
`downloads/` preserves the returned normal bridge and service preview images.
`review.html` compares input and actual geometry.

Import and rendering succeeded: one mesh, 462,706 vertices, 925,436 triangles,
no UVs, no separate eyes and no rig. The raw topology is not game-ready.
Visual inspection found an exaggerated brow/nose and unwanted wrinkles, making
the face appear older than the input. Likeness is NOT approved. No Guilty Gear
style or Unreal integration is claimed; no Unreal assets were changed.

Scripts: scripts/generate-will-hi3dgen.py, scripts/inspect-hi3dgen-head.py.
Generation script submits an external upload; do not rerun casually or retry
automatically. Model and output-use license review is still needed before any
distribution; free service access alone does not establish reuse terms.
