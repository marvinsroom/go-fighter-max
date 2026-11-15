# Cid redesign and consistent JUS sizes

The user confirmed consistent JUS gameplay sizes: adults close in height with modest differences, and visibly shorter child/small forms. This replaces the earlier height-based gameplay sizing policy.

All 23 base fighters and the documented alternate bodies are calibrated from their installed sprite pixels, AIR scale, CNS scale and local coordinates. Forty-six additional walk cycles use one scale per complete sequence, matched to their standing bodies. Collision boxes follow body scale adjustments; animation IDs, timings, offsets and flags are preserved. Small slime, pet and child bodies remain smaller, and larger humanoid transformations stay close to ordinary fighters.

The previous JUS comparison multiplied the historical scale by the replacement scale, inflating eight fighters by 40–70% and slightly undersizing Edward. The viewer now uses live runtime values once.

Cid's 56 body drawings and both portrait slots use the new flat anime design. The [artwork, official reference URLs and exact built-in imagegen prompts](../characters/cid/art/redesign-v7/README.md) are preserved with his previous runtime. No API fallback was used.

Open [the current interactive comparison](review.html). All cards and the standing/walking player use the same world scale. [Policy](policy.json), [installed changes](installation.json), [201 file/size preservation checks](verification.json), and [desktop/narrow browser checks](browser-validation.json).

Brief production startup checks passed for Cid/Luffy and Goku/GT Goku. Fresh gameplay recordings and full recapture suites remain deferred at the user's request. Earlier recordings show previous artwork and sizes.
