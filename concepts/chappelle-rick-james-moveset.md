# Dave Chappelle as Rick James / Tyrone Biggums

The user explicitly corrected the layout to two fighters: **Prince transforms
into Rick James**, and **Tyrone Biggums transforms into Negan**. This supersedes
the initial three-slot implementation. See `chappelle-paired-fighters.md`.

Rick James: theatrical ringed slaps, platform-boot kicks, Cold Blooded palm
strengths, Unity Slap, Platform Rush, Couch Surf retreat, Couch Crusher and
Funk Flash anti-air. Supers: Unity Tour and Couch Demolition.

Tyrone Biggums: nervous scrapper with Quick Rush, Panic Lunge, Backpedal,
Floor Scramble and Rising Flail. Supers: Scramble City and Midnight Mayhem.
Basic attacks share timing/damage with Rick, with separate artwork for the
entire movement, attack and reaction set. Specials and finisher animations
use his own form and fixed inputs rather than random moves.

W as Player 1 / ] as Player 2 toggles within the assigned pair, free while grounded and controllable.
42-tick activation, change at tick 18, 90-tick cooldown from reveal. Health and
meter stay shared. Persistent form across moves, incoming captures, falls,
recovery and finishers. Reset returns to Prince or Tyrone respectively. Supers cost 1000/deal 620;
ultimates cost 2000/deal 950, with guardable hit-confirm starters. First pass
uses nine key poses per look, no recorded dialogue or finished portraits.

Current controls, renderer replays and native validation live under
`sprite-fighter/characters/prince` and `sprite-fighter/characters/tyrone`. Further animation, cinematic staging,
effects detail and competitive balance remain.
