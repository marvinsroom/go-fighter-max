# Will head from our approved reference

This route uses a new, isolated head image derived from `concepts/will-face-study-v3.png`, then Tencent's Hunyuan3D demo to create an actual 3D mesh. The generated image is a reconstruction input, not a mesh or game character. Image prepared with the built-in imagegen tool; exact prompt is saved in `will-head-input-v1.prompt.txt`.

The user rejected the generic MPFB likeness and the Sketchfab head candidate. The user initially declined sending an image to Tencent, then explicitly reversed that choice with **“actually send it”**. The Will head input was then sent only to Tencent's official Hunyuan3D Spaces. No account, paid inference, subscription or game-project upload was used.

## Generation result

- Hunyuan3D 2.0 textured generation failed with a server-side NameError.
- Hunyuan3D 2.1 textured generation was rejected because the requested GPU duration exceeded the free service allowance. No subscription was started.
- **Hunyuan3D 2.1 shape-only generation succeeded**, returning a GLB with 809,880 vertices and 1,619,864 triangles. Inference metadata reports about 32 seconds of processing. The actual raw mesh is preserved in the `downloads` subfolder. Its exact local path and service parameters are in `generation-result.json`.

The raw mesh is untextured and unrigged. `scripts/inspect-generated-head.py` makes a lighter review mesh, saves an editable Blender file and renders review views. Any resemblance assessment must use those actual mesh renders, not the input photograph. This head has not been fitted to the body, given facial animation, or integrated into Unreal.

## Current review files

The latest detail pass is now in **`detailed-v4/`**. It adds actual curl and facial-hair geometry, skin normal/roughness detail, a subtler eye-opening sculpt and a corrected rear silhouette. See its README and export-validation.json. The files below describe the earlier first textured pass.

- `will-head-textured-v2.blend`: latest editable head study, 90,000 triangles, with packed 2048px base-color texture.
- `will-head-textured-v2.glb`: portable mesh and embedded texture.
- `will-head-basecolor-v2.png`: the locally baked UV texture.
- `v2-textured-front.png`, `v2-textured-three-quarter.png`, `v2-textured-profile.png`: actual Blender renders of that mesh.
- `front.png`, `three-quarter.png`, `profile.png`: geometry-only renders.

`scripts/texture-generated-head.py` projects the isolated front reference onto the generated geometry, blends into simple procedural color at the back, then bakes a standard UV atlas. It does not use the rejected landmark-fitting method or send further images elsewhere. Version 2 masks transparent reference pixels to avoid pale seams at the hair edge. Side/rear color and hair detail still need finishing; frontal projection does not establish accurate unseen views. Geometry is still an unrigged first head study. `scripts/verify-generated-head.py` checks GLB reimport, triangle count, UV coordinates and embedded texture; it does not evaluate likeness or animation quality.

## Reproduction and sources

- Script: `scripts/generate-reference-head.py --version 2.1 --shape-only`, using the workspace `tooling/mesh-client-venv` Python interpreter.
- Official demo: https://huggingface.co/spaces/tencent/Hunyuan3D-2.1
- Official source: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
- Model license: https://huggingface.co/tencent/Hunyuan3D-2.1/blob/main/LICENSE

This is a generated starting mesh; clean deformation topology, texture finishing and likeness review remain necessary for the game character.
