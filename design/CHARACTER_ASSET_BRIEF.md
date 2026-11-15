# Current milestone: Will sprite combat

Player 2 is now Steve Urkel with a malfunctioning-gadget super, Urkelbot ultimate
and a Stefan Urquelle transformation with a separate close-combat kit. Built-in
imagegen supplied 16 original transparent key poses/robot drawings. The native
52-case suite passed, including robot continuity and cross-character costume
preservation. See `sprite-fighter/characters/urkel/CONTROLS.md` and `review.html`.
Other Will transformations remain on hold at the user's request.

The approved 2D Will now has a first-pass `will_full` combat package in IKEMEN GO.
Launch `sprite-fighter/Play Will.cmd`; controls are in `sprite-fighter/WILL_CONTROLS.md`.
Includes normals, crouch/jump/air attacks, throws, branching Three-Piece, feint,
Fresh Step upright kick, Windmill, Taxi, meter reset, super and a two-backdrop ultimate. Both
cinematics require an unguarded hit. Will has no basketball moves or hat.
First-pass shared key-pose animation, portraits and competitive balance remain
unfinished. Earlier direction and asset experiments follow for history.

# Will and Chappelle-as-Prince character assets

## Current direction: IKEMEN GO sprites

The user switched to a 2D sprite fighter in IKEMEN GO after rejecting the 3D
likeness attempts. The historical Unreal requirements below describe the former
approach. Keep the Guilty Gear inspired illustration direction, expressed in 2D.

Will's first stance at `sprite-fighter/characters/will/art/will-stance-v1.png` is
user-approved. The latest `will_motion` study runs forward/backward keyboard
movement in IKEMEN GO, with three new step drawings and a fixed-pattern idle
using a tiny engine breathing scale. The earlier redrawn idle is preserved as
`will_idle`. Backward uses reversed forward frames; foot contact and walk garment
details need cleanup. No combat, jumping, crouching or portraits yet. See the
character README and motion review. Preserve the approved face and outfit.

User preference: full character faces and outfits, rather than recoloring the mannequin. Character appearance is the next priority before adding unique moves.

## Required visual direction — user correction

Guilty Gear inspired, cel-shaded 3D anime fighting-game presentation is an original
project requirement, reaffirmed by the user after seeing Will's integrated model.
The user explicitly rejected the current model's likeness: it looks nothing like
Will. The integrated `/Game/Characters/WillV2` is a technical rigging/movement
prototype, NOT an approved skin or an acceptable art target.

Use recognizable young Will facial anatomy from the approved reference, designed
as sculpted graphic planes with crisp outlines and two or three hard shadow
bands. Favor expressive brows/mouth, deliberate hair masses, angular cloth folds
and a strong fighting silhouette. Avoid projected photographic skin, pore noise,
realistic PBR shading and generic mannequin anatomy as a likeness shortcut.
The white tee should reach the waistband; no exposed midriff. Keep Will's moves
and character poses free of basketball props.

Next art work: establish a corrected cel-shaded concept sheet, then reconstruct
the head silhouette, features and outfit to that target and build the appropriate
Unreal materials. A shader change alone will not repair the rejected likeness.
Concept art is a design reference, not evidence of completed game geometry.

Corrected concept: `concepts/will-cel-design-target-v1.png`, generated with the
built-in imagegen tool from the approved Will face study. It shows recognizable
young Will features with graphic outlines, angular folds and cel-style shadows.
User review pending. This is a concept sheet, not the current in-game model.
Exact generation prompt is saved beside it in `.prompt.txt`.

## Existing references

- Will: `concepts/will-face-study-v3.png` is the approved facial likeness. Young adult Will Smith as the Fresh Prince, high-top fade, prominent ears, expressive smile. Teal/purple/yellow open short-sleeve shirt over a white tee, dark loose shorts, colorful high-top sneakers. Exclude basketball from his combat identity and final hero pose.
- Prince: `concepts/chappelle-prince-face-study-v2.png` is the latest concept for review. Dave Chappelle's facial anatomy in the Prince parody costume: curled black wig, purple satin outfit, lace jabot and cuffs, boots. Preserve Chappelle's face rather than substituting the musician's. Basketball remains his move theme, but a separate prop should not be fused into the character mesh.
- `concepts/full-roster-mockup-v1.png` establishes the overall crossover presentation, not a final modeling turnaround.

## Required model deliverables

Two full-body 3D characters with separate readable face, hair, skin, outfit, and footwear materials. Neutral pose appropriate for rigging, clean topology around shoulders/elbows/hips/knees, and skin weights that survive walking, crouching, jumping, punches, and kicks. Hair and cloth must work without expensive simulations for the first pass.

For this PC prototype, favor one 2K texture set per character where practical, compact material counts, and a lower-detail mesh option. These are initial art-budget proposals for the MX150 test machine, not measured limits or final acceptance criteria.

Preferred handoff: a skeletal FBX plus texture files and source model. An unrigged mesh is only an intermediate asset. Animation reuse requires a compatible skeleton or a verified retargeting setup; merely naming bones like the mannequin does not establish compatibility.

## Unreal integration after assets exist

1. Import into separate character folders; retain the working mannequin assets.
2. Check scale, upright orientation, facing, root/pelvis placement, skeleton, materials, and missing textures.
3. Verify skinning with existing movement animations or establish a retargeting setup.
4. Swap one fighter's visual mesh while retaining its capsule, movement, combat rules, and input bindings.
5. Review facial likeness and outfit both close up and through the actual side-view camera.
6. Test deformation during movement, guarding, and strikes, then check GPU memory and frame time on the target PC.

## Current asset blocker

Blender 5.2.2 and MPFB 2.0.18 are installed, with the free CC0 MakeHuman system assets. A generic clothed, rigged starter and tested skeletal FBX now exist under `characters/modeling-starter/`. These establish the modeling/export workflow; they do not provide Will or Chappelle's finished likenesses or costumes. See `design/FREE_CHARACTER_MODELING.md`. Meshy's free tier does not allow downloading newly generated models, so no subscription was purchased. Full likenesses and Unreal animation retargeting remain required before replacing the fighters in the game.
