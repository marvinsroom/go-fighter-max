# Lloyd and Jin Mori proportion redesigns

Open [review.html](review.html) for before/after standing and walking at identical live gameplay scales, including Monkey King. Full sheets and exact prompt sets are linked in the review. Built-in imagegen artwork is saved in each character's `art/proportions-v9` directory.

Lloyd has 56 drawings across movement, combat, story and walk. Jin Mori has 120 across seven body/transition sheets and two form-specific walks. Smaller heads, longer limbs and leaner silhouettes replace the squat builds. Lloyd remains 53 world units; both Mori forms remain 52.

Prior runtime files are preserved in each character's `art/proportions-v9/before` directory. AIR, CNS, CMD, DEF, ZSS and SND are byte-identical. All replacement sprites were decoded and compared; unrelated headers remain unchanged. Raster scale is uniform per sequence, preserving natural crouch/jump height changes.

Validation: 201 roster checks pass; new review passes 80 assertions each in desktop/narrow Edge; roster review passes 299 each. Lloyd versus Mori starts with the production configuration. Recordings remain deferred.

Scripts: `install-proportions-v9.py`, `build-proportions-v9-review.py`, `verify-proportions-v9-review.py`, `publish-proportions-v9-links.py`, `check-proportions-v9-startup.ps1`. Earlier character builders and JUS packers restore obsolete baselines; do not rerun them blindly.
