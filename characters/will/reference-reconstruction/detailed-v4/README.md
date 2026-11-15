# Detailed Will head — current version

This is the current detail pass on the generated head, built entirely locally from the existing Hunyuan mesh and reference texture. No additional images were uploaded and no paid services were used.

## Files

- `will-head-detailed.blend`: editable master, including the skin shader and separate curl/facial-hair/lash meshes.
- `will-head-detailed-export.blend`: source with portable baked skin maps.
- `will-head-detailed.glb`: verified portable export with embedded textures.
- `three-quarter.png`, `front.png`, `profile.png`: actual Blender review renders.
- `will-head-basecolor.png`, `will-head-normal.png`, `will-head-roughness.png`: 2048px skin maps.
- `export-validation.json`: reimport checks.

## Changes

Reduced the inflated rear skull, broadened the lower jaw slightly and softened the high-top corners. Made a subtle eye-opening adjustment on the existing head and separated smoother eye shading from the skin pore effect. Added fine upper lashes, brow/moustache fibers, 20,000 curl clusters and 500 curl loops. Replaced the stretched side/rear projection with blended skin/scalp color, added a scalp fade and skin micro-normal detail, and used softer lighting for review.

Separate eyeball/socket experiments in `detailed-v1` through `detailed-v3` were rejected during visual inspection because they introduced clipping and unnatural eyelid edges. They are not the current model. This version retains the reference eye surfaces; it does not have separate riggable eyeballs or a facial-animation rig.

## Validation and limits

The GLB was reimported in Blender: all five mesh objects and 550,080 triangles survived, as did skin UV coordinates and embedded base-color, normal and roughness maps. These checks establish mesh/material portability, not approved likeness or animation quality.

This is a detailed **head study**, not a finished playable fighter. It is unrigged, not fitted to Will's body and not integrated into Unreal. Its higher-detail hair geometry is a source asset; runtime detail levels and target-PC performance still need to be established during integration. Side/rear color is an approximation from a single front image. The front image alone does not define an exact likeness from every angle.

Generation/edit scripts: `scripts/detail-will-head.py`, `scripts/render-detailed-head.py`, `scripts/export-detailed-head.py`. Earlier versions are preserved. The generation script refuses to overwrite this source.
