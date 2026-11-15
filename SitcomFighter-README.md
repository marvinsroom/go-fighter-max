# SitcomFighter Unreal project

Project entry point: `SitcomFighter/SitcomFighter.uproject`.

Created from the locally installed Unreal Engine 5.8 Third Person Blueprint template and its Side Scroller shared content. Includes the shared mannequin, input, and level-prototyping packs. The default map is now the smaller `Prototype/L_TrainingArena`, with a fixed shared camera and custom training game mode. The original platforming map is preserved. Split screen is disabled.

The training map contains two mannequin placeholders labeled Will and Prince. Generated runtime Blueprints provide keyboard movement and jumping, light/heavy strikes with startup and recovery, ground guarding, health labels/bars, knockout, and manual round reset. These are shared basic attacks; unique roster moves and finished combat animations still need to be built. No AI, controller bindings, timer, match scoring, character selection, or online play exists yet. See `TRAINING_CONTROLS.md` in the workspace root.

The Python and Editor Scripting Utilities plugins are enabled for editor automation only. Gameplay is Blueprint-based. The original template validation used `scripts/validate-unreal-project.py`. The new training build uses `scripts/build-training-prototype.py`; runtime checks use `scripts/test-training-pie.py`. Reports are written to the project's Saved folder. Automated checks do not substitute for a visual and physical-keyboard playtest.

Rendering defaults now target a lighter prototype: DirectX 11, low scalability, and Lumen/distance-field generation/virtual shadow maps disabled. Restart the editor to apply them. This is a development preset, not final art direction or a measured performance guarantee.

Design and art references remain in the workspace's `concepts` and `design` folders.
