# Sheneneh — moveset draft

Status: original fighting-game moveset for Sheneneh from Martin. Not implemented or playtested; invented moves are not claims about specific television scenes.

## Fighting identity

An assertive close-range fighter with sharp backhands, heel kicks, expressive gestures, and salon-themed flourishes. She controls the pace with a brief two-step stance and a strong choice between advancing mids and a committed low. Her personality comes through confident posing, facial reactions, and deliberately theatrical finishing animations.

Strengths: quick close checks, advancing pressure, grounded conversions, corner positioning.
Weaknesses: short reach, no projectile, no meterless invincible reversal, and interruptible stance transitions. Standard roster health initially.

Differentiate her from Will's branching punch strings: Sheneneh uses separate attacks from a stationary two-step stance with explicit commitments, rather than a repeating attack chain. Avoid copying Prince's side-switch dash or Homey's prepared prop setups.

## Proposed controls

Shared four-button proposal: Light (L), Medium (M), Heavy (H), Skill (S). Directions are relative to facing. Inputs and meter costs remain provisional until shared combat rules exist.

## Core attacks

| Attack | Name and animation | Purpose and limit |
| --- | --- | --- |
| Standing L | Excuse Me — sharp open-hand check. | Fast close-range interrupt. |
| Standing M | Talk to the Hand — stepping palm strike. | Main grounded starter. |
| Standing H | Backhand Business — committed turning backhand. | Heavy punish; visible wind-up and whiff recovery. |
| Crouching L | Heel Tap — short low toe kick. | Low check. |
| Crouching M | Step Aside — low shin kick with an exaggerated hip turn. | Low starter; unsafe nearby on block. |
| Crouching H | Chin Up — rising palm strike. | Primary anti-air; modest horizontal reach. |
| Jumping M | Heel First — diagonal heel kick. | Standard jump-in. |
| Jumping H | Make an Entrance — descending two-handed palm strike. | Slow heavy jump-in with conspicuous startup. |
| Forward + M | Look at Me — slow raised-hand palm drop. | Readable overhead; no large free conversion. |
| Forward throw | Move Along — catches the wrist, turns the opponent, and shoves them away. | Standard breakable throw and forward positioning. |
| Back throw | Wrong Door — pivots and sends the opponent behind her. | Standard throw rules and position swap. |

## Specials

### Oh No You Didn't

Quarter-circle forward + L/M/H. An advancing open-hand strike. L is short and quick; M travels farther and pushes back; H adds a slow turning follow-through that knocks down on hit. All versions hit mid and have clear recovery. H is interruptible during startup and punishable on block. No armor, invincibility, auto-counter, or forced side switch.

### Heel, Please

Quarter-circle back + M. A planted low heel sweep. Strong knockdown reward at close range, but slower than her crouching low checks and punishable on block. It cannot cancel freely into a safe stance follow-up.

### Fresh Set

Quarter-circle back + L. A short flurry of palm and backhand strikes, ending with Sheneneh checking her nails. All hits are mids. A close-range combo ender that pushes the opponent away; finishing pose is part of its recovery, not a cancelable taunt. Insufficient reach to be a neutral approach tool.

### Make Some Room

Forward, down, down-forward + H. A rising heel kick with a small backward lean. Anti-air protection only; no full-body invincibility. Misses against grounded opponents at close range and leaves a large opening if baited. Her normal rising palm remains the lower-commitment anti-air.

### Salon Spin

Quarter-circle forward + H in the air. One descending turning heel kick per jump. Must begin above a minimum height; no instant overhead from the ground. Punishable on block, no bounce into another air special, no invincibility. A single-hit air combo ender rather than Prince's dunk-style launcher.

## Character skill: Two-Step Attitude

Press S to enter a short stationary two-step stance, hands on hips, with visible startup. No attack occurs on entry. During a fixed window choose one follow-up:

- L — Say It Again: quick short-range mid backhand. Ends her turn on block.
- M — Coming Through: advancing double-palm mid strike. Greater reach, slower startup, and a punishable blocked finish.
- H — Watch Your Step: slow low heel sweep. Clear leg animation; punishable on block. No overhead option in this stance.
- S — Fix the Look: ends the stance with a hair adjustment and recovery. No instant guard or immediate throw.

She cannot guard, jump, counter, or cancel back into the stance while it is active. No follow-up grants invincibility or armor. Avoid forced mix-ups on entry; opponents can challenge startup and delayed follow-ups. Nothing tracks through the opponent or automatically switches sides.

The stance is a deliberate timing and distance choice after a knockdown or a successful pushback. It must not repeat true blockstrings indefinitely. Keep the stance animation distinct from attack startup so the defender can read the commitment.

## Supers

### Full-Service Makeover — one meter unit

Quarter-circle forward twice + H. A close palm strike confirms into a rapid sequence of backhands, heel kicks, and a turning palm finish. Graphic salon-mirror panels reflect her expressions between hits; she checks her nails as the opponent slides away. No cinematic on block or miss; starter is punishable. Use original sound and dialogue.

### Queen of the Salon — two meter units

Quarter-circle back twice + H. A clearly telegraphed close-range strike confirms into a stylized salon cinematic. The opponent spins into a salon chair. Sheneneh turns the chair with a dramatic flourish, a hood dryer drops into frame, and a burst of harmless theatrical steam reveals an absurd towering hairstyle. The opponent staggers upright; a final spinning heel kick sends them through a curtain into a pile of towels. Sheneneh turns to the mirror, fixes her hair, and poses.

The joke is the over-the-top salon routine, not injury or personal identity. No hot-tool burns, chemical attacks, eye attacks, gore, or persistent appearance changes. Chair, dryer, hairstyle, and towels exist only in the cinematic. Damage resolves once; both fighters return to predictable arena positions. Blocked or missed starter never triggers the cinematic and gives a punish opportunity.

## Intended prototype routes

- Standing L → standing M → Fresh Set: close confirm and separation.
- Crouching L → crouching M → Heel, Please: low starter into knockdown if cancel rules support it.
- Standing H whiff punish → Oh No You Didn't M: grounded punish and corner carry.
- Standing M → Full-Service Makeover: straightforward meter conversion.
- Knockdown → Two-Step Attitude: spacing-dependent pressure setup, never assumed guaranteed.

Routes are design targets, not verified combos. Frame data, damage, cancel windows, anti-air protection, and setup timing require prototype testing.

## Visual and animation direction

- Preserve Sheneneh's recognizable appearance as portrayed by Martin Lawrence, using a character-specific reference before final modeling. Do not reuse the Chappelle facial reference.
- Bold patterned outfit, styled hair, expressive makeup, hoop earrings, nails, and heeled footwear should create a readable side-view silhouette. Final costume needs visual review.
- Attacks use palms, backhands, elbows, and heels; nails are character detail, not cutting weapons.
- Idle: weight on one hip, hand on hip, alert and unimpressed expression.
- Walk: confident measured strut; dash: quick purposeful steps with controlled hair movement.
- Intro: checks a compact mirror, shuts it, then gestures for the opponent to approach.
- Taunt: examines her nails and gives the opponent a skeptical look. No gameplay buff.
- Win: turns away, glances back, and gives a satisfied shoulder pose.
- Keep dialogue original and the comedy rooted in confidence, timing, and expressive reactions.

## First playable scope

Start with movement, normals, throws, Oh No You Didn't, Fresh Set, and Heel, Please. Validate pressure gaps and reach. Add the stance, anti-air special, air heel kick, and supers after the grounded kit works. Prototype cinematic props only after confirmed-hit transitions and arena return positions are reliable.
