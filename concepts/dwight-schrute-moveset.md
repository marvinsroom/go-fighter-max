# Dwight Schrute — moveset draft

Status: original fighting-game concept for Dwight Schrute from The Office. Not implemented or playtested. Invented moves and cinematic events are not claims about particular episodes.

## Fighting identity

A methodical setup fighter with stiff martial-arts poses, office equipment, and beet-farm preparations. Dwight places one clearly visible tripline, then uses modest pokes and an arcing beet toss to guide opponents toward it. His confidence is absolute; his plan is only as good as his ability to protect the setup.

Strengths: prepared space control, grounded approach denial, situational trap conversions.
Weaknesses: vulnerable setup animation, limited mobility, mediocre close-range scramble tools, no meterless invincible reversal. Standard roster health initially. Traps have fixed behavior and visible counterplay; no random items, hidden inventory, or compulsory planning minigame.

Differentiate him from Homey's timed jack-in-the-box: Dwight's tripline stays dormant until crossed on the ground, is tied to a fixed location, and must be guarded. Keep Urkel's elaborate inventions and robot summons reserved for Urkel.

## Proposed controls

Shared four-button layout: Light (L), Medium (M), Heavy (H), Skill (S). Directions are relative to facing. Inputs and meter costs remain proposals until shared combat rules exist.

## Core attacks

| Attack | Name and animation | Purpose and limit |
| --- | --- | --- |
| Standing L | Fact — stiff quick palm jab. | Close-range check. |
| Standing M | Assistant to the Strike — straight karate punch with overly formal posture. | Grounded starter; moderate reach. |
| Standing H | Disciplinary Action — two-handed clipboard swing. | Heavy punish; slow recovery. |
| Crouching L | Desk Check — short low toe kick. | Low check. |
| Crouching M | Sweep Protocol — deliberate low leg sweep. | Low starter; punishable nearby on block. |
| Crouching H | Threat Assessment — rising forearm under a rigid guard. | Primary anti-air; limited horizontal reach. |
| Jumping M | Field Exercise — diagonal kick. | Standard jump-in. |
| Jumping H | Mandatory Training — slow downward double-palm strike. | Committed heavy air attack. |
| Forward + H | Performance Review — clearly telegraphed overhead clipboard drop. | Slow overhead; no free large conversion. |
| Forward throw | Security Escort — wrist turn into a firm shove. | Standard breakable throw; forward separation. |
| Back throw | Reassigned — pivots and sends the opponent behind him. | Standard throw rules and position swap. |

## Specials

### Schrute Strike

Quarter-circle forward + L/M/H. A formal advancing palm-and-elbow sequence. L is one short palm strike; M adds forward movement and an elbow; H uses a slower committed step and ends in knockdown. All hits are mids, no armor or invincibility. M and H have punishable blocked recovery; H startup is interruptible. Its role is converting a grounded hit rather than endlessly safe pressure.

### Beet Delivery

Quarter-circle back + L/M/H. Tosses one beet on a fixed arc: L lands nearby, M at midrange, H farther away with longer startup. It hits mid, never as an overhead, and disappears on hit, block, or first ground contact. Only one beet projectile per Dwight may be active. It does not roll, bounce, grow, leave a stain hazard, or replenish a resource.

The arc leaves approach routes underneath or around it depending on spacing. Throw recovery prevents simultaneous guaranteed projectile coverage and trap placement. Opponents can block, evade, or use eventual universal projectile rules. Do not make the beet an automatic answer to every jump.

### Fire Drill

Down, down + L. A short shoulder-led rush with a paper evacuation sign held overhead; one mid strike, knockdown on hit, substantial recovery on block or miss. No armor, invincibility, teleport, flame, or screen-wide distraction. Intended to punish a whiff, not bypass neutral for free.

### False Alarm

Down, down + M. Dwight briefly raises the same evacuation sign but stays in place, then puts it away. No hitbox, stun, input disruption, or automatic counter. Recovery prevents immediate throw or instant guard. A readable feint to bait an anticipated Fire Drill response.

### Black Belt Procedure

Forward, down, down-forward + H. Rising palm strike into a high kick. Anti-air protection only, no full-body invincibility. Both hits are mids against grounded opponents, with no hidden overhead. Punishable when baited or blocked; his normal forearm remains the lower-risk anti-air.

## Character skill: Perimeter Protocol

Press S to place a short, bright safety-orange tripline between two small freestanding desk stands just ahead of Dwight. Long visible placement animation, no armor or guard. Only one tripline per Dwight may exist. It never attaches to arena geometry or changes with stage layout.

- Remains at a fixed position for a fixed short lifetime; its expiry is shown with a flashing indicator.
- Triggers only when the opponent crosses it while grounded and vulnerable to being hit. One low strike, then it disappears.
- Does not trigger on airborne travel, throws, cinematics, invincible movement, or opponents already in knockdown. Guarding low blocks its strike.
- The opponent can jump over it, destroy either stand with one attack, or wait out its lifetime. Attacking the prop does not create a projectile hit against the opponent.
- Disappears immediately if Dwight is hit, on a round transition, or when triggered/destroyed/expired. No persistent hazards after a super.
- S while a line is active begins a short remote cancel animation that removes it; no damage, explosion, refund, or simultaneous replacement.

Outside a combo, a clean trigger gives brief hitstun rather than a full cinematic knockdown, allowing Dwight a modest nearby confirm. In a combo, it adds only a small scaled hit: no launch, ground bounce, hitstun refresh, or repeat setup loop. Disable placement during offensive cancel windows initially. Prototype trap interactions against blocking, movement, wake-up, hitstop, and side switches before enabling stronger conversions.

This is a visible spacing tool, not a grab, unblockable, bear trap, or random status effect. Dwight has no second trap type in the initial kit.

## Supers

### Mandatory Combat Training — one meter unit

Quarter-circle forward twice + H. A close palm strike confirms into an overly formal karate demonstration: stiff punches, a pivoting elbow, a high kick, then Dwight straightening his glasses as the opponent slides away. Graphic instructional arrows punctuate the impacts without obscuring the fighters. No cinematic on block or miss; starter is punishable. No invincible startup by default.

### Schrute Farms Field Trip — two meter units

Quarter-circle back twice + H. A clearly telegraphed clipboard strike confirms into a stylized farm training course. Dwight blows a whistle, the opponent stumbles through swinging padded training bags, and he charges in with a shoulder check that launches them into a stack of empty beet crates. A tractor rolls slowly through the distant background, well away from the fighters. Dwight checks a clipboard, stamps the test as failed, and offers the camera a satisfied nod.

No collision with machinery, animal attack, sharp trap, burns, gore, or realistic injury sequence. Obstacles and farm props exist only in the cinematic. Damage resolves once; both fighters return to predictable arena positions. Any active tripline is cleared when the cinematic begins. No cinematic on block or miss. Use original dialogue, sound, and music.

## Intended prototype routes

- Standing L → standing M → Schrute Strike L: simple close confirm.
- Crouching L → crouching M → Schrute Strike H: low starter into knockdown if cancel rules permit.
- Nearby tripline hit → standing M → Schrute Strike M: situational trap confirm with scaling.
- Standing H whiff punish → Mandatory Combat Training: meter conversion if the super-cancel rules support it.
- Knockdown → Perimeter Protocol: setup only where placement and wake-up timing actually allow it. Never assume guaranteed protection from Beet Delivery.

Routes are design targets, not verified combos. Frame data, trap lifetime, hitstun, damage, cancel windows, and placement advantage require playtesting.

## Visual and animation direction

- Future likeness reference: Rainn Wilson as Dwight Schrute, with recognizable glasses, center-parted hair, serious expression, mustard shirt, tie, and office trousers.
- Keep the side-view silhouette readable; glasses and facial expressions should survive the intended cel-shaded presentation.
- Idle: rigid ready stance, occasional glasses adjustment.
- Walk: deliberate patrol steps; dash: awkward committed sprint.
- Intro: checks the arena against a laminated checklist, then assumes an excessively formal fighting stance.
- Taunt: raises one finger and begins a lecture. No gameplay effect.
- Win: stamps a form, files it, then looks directly toward the camera.
- Office supplies are blunt stylized props; no staple-gun projectiles, pepper spray, or realistic weapon handling.
- Comedy should come from procedural certainty, preparation, and the contrast between confidence and awkward movement.

## First playable scope

Start with movement, normals, throws, Schrute Strike, and Beet Delivery. Add one simple tripline and test its lifecycle thoroughly before adding trap confirms. Then add Fire Drill, False Alarm, the anti-air special, and supers. Use placeholder props while checking visibility, cleanup, collision, and repeated setups.
