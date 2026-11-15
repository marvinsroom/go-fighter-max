# Free character modeling setup

Installed Blender 5.2.2 LTS and the official Blender Extensions MPFB 2.0.18 add-on. Installed the MakeHuman system asset pack (140 material/asset definitions, plus textures and meshes). No account or paid service is required.

MPFB makes editable human bodies and faces, fits clothing and body parts, and adds a skeleton with weights. It does not automatically reproduce Will Smith or Dave Chappelle from our concept pictures.

## Open the starter

Open `characters/modeling-starter/male-character-starter.blend` in Blender. It contains an editable male base, eyes, short hair, a generic outfit, shoes, and a 53-bone game-engine rig. This is a workflow starter, not a finished roster character. The preview uses solid viewport colors rather than the final skin textures.

In Blender's 3D viewport press **N** to open the sidebar, then select **MPFB**. Select `EditableMaleBase` to access human controls. For a new character, use **New human > From scratch**. Set body proportions and face controls before adding the rig. Add the rig before clothing so fitted assets receive weights. Asset libraries are under **Apply assets**. See the official getting-started guide below for the current panel layout.

## Will and Prince workflow

1. Save a separate character file for each fighter. Keep the generic starter intact.
2. Match head shape, jaw, ears, nose, lips, and eyes against the approved Will reference and latest Chappelle-as-Prince concept. Use MPFB face targets first, then Blender sculpt/edit tools for remaining differences. Review front, side, and three-quarter views; a single concept does not define every angle.
3. Model Will's high-top fade, open colorful shirt, tee, shorts, and sneakers. Model Chappelle-as-Prince's curled wig, purple satin costume, lace details, and boots. Generic library clothes are fitting examples; they are not the requested costumes.
4. Finalize proportions, rig, then fit and weight the custom clothing. Check shoulders, elbows, hips, and knees in pose mode.
5. Export a skeletal FBX, establish Unreal animation retargeting, and test one fighter at a time in the working arena. The MPFB skeleton is not automatically compatible with the Unreal mannequin.

## Verification

`scripts/create-character-starter.py` builds the starter and exports FBX. It refuses to overwrite the starter to protect edits. `scripts/verify-character-starter.py` packs source textures and reimports the FBX to verify bones, meshes, and skin weights. Results are in `characters/modeling-starter/validation.json`. No Unreal import, animation retarget, likeness approval, or in-game performance validation has been completed for this starter.

## Official sources

- Free software/assets explanation: https://static.makehumancommunity.org/mpfb/faq/is_it_really_free.html
- Getting started: https://static.makehumancommunity.org/mpfb/docs/getting_started.html
- Asset pack and item licenses (CC0): https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html
- Extension: https://extensions.blender.org/add-ons/mpfb/

MPFB software uses GPL; the core human assets and this system asset pack are CC0. Other community asset packs can have different licenses; check the actual asset before adopting it.
