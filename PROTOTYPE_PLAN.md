# First playable preparation

## Target

Side-view PC fighting game, 3D characters, fixed side-on camera, cel-shaded visual direction. Unreal 5.8.3 is installed. A Blueprint training prototype now exists at `SitcomFighter/SitcomFighter.uproject`; see `TRAINING_CONTROLS.md` for the current behavior and limits.

## First playable slice

Use Will and Prince as the first pair because their revised kits have distinct close-range and projectile roles, and both have saved face studies. This is an implementation proposal, not a reduction of the 11-character roster.

Begin with placeholder fighters in one flat training arena. Prove these behaviors before producing finished models or cinematic supers:

1. Two fighters move on a single gameplay plane, face each other, jump, land, and stop at arena edges.
2. Camera keeps both fighters visible with bounded zoom and no crossing behind the arena.
3. Grounded light, medium, and heavy attacks have explicit startup, active, and recovery phases. A hit connects once per intended strike.
4. Blocking, hitstun, blockstun, knockdown, and wake-up prevent invalid actions. Throws follow one shared rule set.
5. Health, timer, round reset, and win state work reliably. Reset clears projectiles and transient combat state.
6. Will gets one confirmed Three-Piece route; Prince gets Royal Bounce. Tune their interaction before adding full kits.
7. Test local two-player controls and a training dummy. Do not assume two physical controllers are available.

## Architecture notes for implementation

- Keep shared fighter behavior separate from character move data.
- Use explicit combat states and move phase timing; animations present the combat rules rather than silently defining them.
- Separate hit detection from character collision. Define hitboxes, hurtboxes, pushboxes, facing, and per-attack hit tracking.
- Put input actions, buffered commands, facing-relative directions, and action priority in a shared system.
- Store move definitions with stable IDs, phase durations, hit reaction, damage, block behavior, cancel rules, and presentation references.
- Keep simulation-facing move data free of cinematic camera logic. Start cinematics only after a confirmed hit.
- Treat current moveset documents as design proposals; do not invent final frame data or promise verified combos.
- Resolve input device availability and shared controller layout before mapping every character's specials.
- Decide online scope before committing to the combat timing architecture. Network play is not implemented or promised by this preparation.

## Asset preparation

Concept images are visual references, not rigged game characters or animations. After placeholder combat works, one fighter needs a model, skeleton, rig, materials, and animation set: idle, walk, jump, landing, attacks, guard, hit reactions, knockdown, recovery, and victory.

Use Will's approved v3 face reference. His older concept images still contain basketball imagery; the revised moveset supersedes that direction. Prince's latest face study and the full roster poster remain concepts for review. Preserve versioned originals when revising images.

## Once installation completes

Verify the installed engine version and launch the editor. Create the project in a dedicated subfolder of this workspace, then verify a clean project opens before adding combat. Choose the initial project template and Blueprint/C++ approach after checking available tooling. Keep roster art and design documents outside generated engine folders.

## Current prep status

- 11-character roster recorded in `design/roster.json`.
- Ensemble image: `concepts/full-roster-mockup-v1.png`.
- Detailed moveset drafts: Prince, Will, Chappelle as Negan, Homey, Sheneneh, Al, Dwight.
- Earlier Urkel, Carlton, Uncle Phil, and Rick James work is partly in recovered session history; consolidate it before implementing those characters.
- Engine project and a 17-actor training arena now exist, with two mannequin placeholders, fixed shared camera, keyboard movement, light/heavy strikes, guard, health, knockout, and manual reset. Runtime checks are recorded separately in the project's Saved folder. Final models, authored combat animations, character-specific moves, complete match flow, and a packaged executable remain pending.
