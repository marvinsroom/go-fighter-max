# Character work in progress

Current custom model passes:

- `will/integration-v1/`: current detailed head fitted to Will's weighted body/outfit, preserved detailed master and a 96,376-triangle runtime version. Imported into Unreal under `/Game/Characters/WillV2` with duplicated/retargeted locomotion assets. See its README and validation reports for current test results and limitations.
- `will/reference-reconstruction/detailed-v4/`: current detailed head source and portable skin maps; no separate eyeballs or facial rig. Earlier eye-socket experiments were rejected.
- `will/v1/`: first generic face, patterned open shirt, tee, shorts, shoes and modeled hair. User rejected facial likeness. Hair placement and outfit waist also needed correction.
- `will/v2/`: corrected hair placement/materials, separate shirt/trouser components, revised face proportions and finer moustache geometry. **Still not an approved Will likeness.**
- `prince/v1/`: distinct face targets, purple suit, custom coat tails, modeled ivory jabot/cuffs, buttons and curly wig. First visual review found overly shiny hair/clothing, a wig fitting problem, exposed skin at the chest/shoes, and needed silhouette refinement. **Not finished or approved.**

The original modeled passes contain editable Blender source, skeletal FBX, renders and model-report.json. These are real meshes with a 53-bone MPFB game-engine rig, not final production assets. The current integration pass has separate assembly, FBX, Unreal import and runtime validation reports. FBX export alone does not establish animation compatibility.

The generation script is `scripts/model-roster-characters.py`. It refuses to overwrite saved models; use a new revision for experiments. Its current source includes material/garment/hair changes made after the first renders, so reproducing v1 would require restoring earlier values.

The generic MPFB face and the Sketchfab candidate were rejected. Current Will uses the generated reference head, locally refined and textured, fitted to the original body/outfit. Likeness and outfit polish remain subject to user review. Prince's custom model is still unfinished.
