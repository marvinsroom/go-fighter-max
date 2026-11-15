# Will character integration

`will-fitted-master.blend` retains the detailed head on the weighted body/outfit.
`will-runtime.blend` is the lighter editable character in metres.
`will-runtime.fbx` exports that character in centimetres for Unreal retargeting.
`full-body-review.png` shows the assembled runtime geometry in Blender.

The runtime model has 96,376 triangles and a 53-bone body rig (Unreal also imports
the armature container). The original detailed head and body files are preserved.
Skin uses the baked 2048px colour, normal and roughness maps. Fine curl geometry
is thinned deterministically; the head skin is reduced to about 44k triangles.

`assembly-report.json` records geometry counts, weights and neck seam checks for
rest, left/right head turns and up/down nods. This checks attachment continuity;
it does not establish finished likeness or a production facial rig.

Unreal assets are under `/Game/Characters/WillV2`. The first metre-scale import
under `/Game/Characters/Will` is an unused diagnostic version with bad retarget
scale, retained until the corrected version passes the rendered checks.
`unreal-import-report.json` records the current import and retarget mappings.
The mannequin-specific Control Rig is bypassed on Will's duplicated animation
blueprint because its bone hierarchy differs. Prince retains his existing mesh.

`runtime-validation.json` contains the latest rendered PIE test result and
same-scene frame measurements. Performance numbers are editor preview results,
not a guarantee for a packaged game. The arena's normal 60 FPS cap is restored
after testing. `level-visual-backup.json` records the original Will visual.
The final run passed all 27 checks. See `PERFORMANCE.md`: about 57 FPS with Will
versus 60 FPS with the original mannequin at the measured low preview settings.
`arena-runtime.png` and `close-up-runtime.png` are the final Unreal captures.
The saved arena includes a movable, shadow-free fill light so faces remain visible.

Known art limitations: first-pass outfit, simplified side/rear head texture,
stylized hair clumps, no facial expressions or independent eyeballs. Combat uses
the existing prototype gameplay and debug hitboxes; authored punches are separate
work. Likeness still needs user review.
