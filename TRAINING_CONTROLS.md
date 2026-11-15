# Training prototype

Open `SitcomFighter/SitcomFighter.uproject`. The startup map is `Prototype/L_TrainingArena`.

Press the green Play button or Alt+P, then click inside the viewport. Esc stops the session; Shift+F1 releases the mouse while playing.

| Action | Will placeholder (P1) | Prince placeholder (P2) |
| --- | --- | --- |
| Move | A / D | Left / Right arrow |
| Jump | W | Up arrow |
| Light attack | J | Comma |
| Heavy attack | K | Period |
| Hold guard | Left Shift | Right Shift |
| Reset round | R | R |

Both fighters use one keyboard. P2 stays idle without input; no opponent AI is present. Physical keyboard rollover may limit simultaneous key combinations. Controller bindings have not been implemented for this prototype.

Each starts at 100 health. Light attacks deal 10 and heavy attacks 20 when within range. Attacks have startup and recovery, cannot hit twice, and are interrupted by an unblocked hit during startup. Guarding on the ground blocks damage. At zero health, the round stops; R restores health and starting positions. There is no timer, score tracking, best-of-three flow, or character-select screen yet.

These are mannequin stand-ins labeled Will and Prince. Their full unique movesets, finished models, attack animations, hit effects, sound, and online play are not implemented. Attacks currently show a short debug impact box when they connect; the health bars provide the main feedback. Movement uses the template's animation blueprint.

## Performance changes

The prototype uses a small flat 17-actor arena, a fixed shared camera, and simple materials. Project settings switch from DirectX 12 to DirectX 11, disable Lumen/distance-field generation/virtual shadow maps, set low scalability, reduce render resolution, cap rendering at 60 FPS, and set a 512 MB texture streaming pool. These are prototype defaults for the detected MX150, not a promise of a measured frame rate or final visual quality.

Restart Unreal after changing rendering settings. The old platforming template is preserved under `Content/Variant_SideScroller`; this map replaces it as the startup level. Art and design references remain outside the engine Content folder.

## Automation

`scripts/build-training-prototype.py` generates ordinary runtime Blueprint assets. Python is used only during editor asset creation and tests, not to run the game rules. The generator refuses to overwrite a completed build. `scripts/test-training-pie.py` checks combat and camera behavior in Play-in-Editor and writes its results to `SitcomFighter/Saved/training-pie-tests.json`.
