# Will — revised moveset

Status: first-pass IKEMEN GO combat prototype implemented. Current controls and
verified behavior are in `sprite-fighter/WILL_CONTROLS.md`; detailed animation
descriptions below remain art targets. User rejected the handstand: Fresh Step
replaces Fresh Freeze, and finishers use upright kick poses. The approved Will
sprite is bareheaded. Animation polish and balance remain unfinished.

## Character identity

Will is a close-range freestyle fighter: loose dance steps, exaggerated fake-outs, fast punches, and breakdance kicks. His personality comes from his grin, jokes, confident poses, and playful recovery animations. His mechanics revolve around branching attack strings and changing timing.

Strengths: close-range pressure, varied string endings, grounded combo routes.
Weaknesses: short reach, no projectile, no meterless invincible reversal. Delaying or resetting a string gives the defender a chance to interrupt. Standard roster health initially.

No basketballs, bounce passes, dunks, basketball-named attacks, or court props in his combat animations. Basketball remains Prince's character theme. Will also avoids Prince's dribble stance, side-switch special, counter, and aerial dunk mechanics.

## Proposed controls

Use Light, Medium, Heavy and Skill. On Player 1's keyboard these are Z/X/C and A;
S and D are the super and ultimate shortcuts. Directions are relative to facing
the opponent. See the current controls document for motion inputs.

## Basic attacks

| Attack | Name and animation | Purpose |
| --- | --- | --- |
| Standing L | Fresh Jab — quick jab with the other hand keeping his cap in place. | Fast close-range check. |
| Standing M | Philly Straight — long stepping straight punch. | Grounded combo starter. |
| Standing H | Punchline — exaggerated wind-up into a committed swinging punch. | Heavy punish; slow recovery on a miss. |
| Crouching L | Sneaker Tap — quick low kick. | Low check. |
| Crouching M | Floor Sweep — low leg sweep from a dance crouch. | Low starter; unsafe at close range on block. |
| Crouching H | Cap Saver — rising elbow, free hand gripping his cap. | Primary anti-air. |
| Jumping M | Fresh Sole — extended sideways sneaker kick. | Jump-in. |
| Jumping H | Double Take — two alternating airborne kicks. | Slower committed jump-in with a clear silhouette. |
| Forward + M | High Five! — conspicuous raised-hand feint flowing into a downward palm strike. | Slow overhead; resource required for a large conversion. |
| Forward throw | Fresh Handshake — elaborate handshake that becomes an arm-drag toss. | Close-range throw with comic personality. |
| Back throw | After You — bows and pulls the opponent past him. | Position swap under standard throw rules. |

## Specials

### West Philly Three-Piece

Quarter-circle forward + L, then up to two follow-up attack presses. A branching three-hit sequence with a shoulder-led entry, quick body punch, and one chosen ending:

- L: short palm strike that pushes the opponent out and ends pressure. Safest ending, but gives up the turn.
- M: low sweep that knocks down on hit. Punishable on block.
- H: slow overhead heel kick. Visually distinct startup and an interruptible gap; punishable on block.

Follow-up timing can vary within a limited window. Delays create real defensive opportunities. No automatic low/overhead sequence with identical timing and no endless loops back into the opener. The first two attacks are mids.

### Psyche!

Quarter-circle back + L. Will starts the same shoulder animation as Three-Piece, then pulls back with a grin. No hitbox, invincibility, parry, or automatic retreat through attacks. Recovery prevents immediate throw or instant guard. Used sparingly to bait an anticipated response; opponents can chase it down.

### Fresh Step

Quarter-circle back + M. An upright side kick replaces the rejected handstand.
One grounded mid strike that creates space on hit. His hurtbox stays vulnerable;
this is not a counter or an invincible escape. Unsafe when blocked nearby.

### Windmill Remix

Quarter-circle forward + H. A short breakdance spin with two sweeping leg hits. Both hits are mids despite the low animation, so the move is not a hidden low. Grounded combo ender with knockdown; ends with Will springing to his feet. Long enough recovery to punish on block. No projectile immunity.

### Taxi!

Quarter-circle back + H. Whistles, then lunges forward with an elbow as though hailing a cab. A committed midrange punish that wall-bounces only on a clean hit near the corner, once per combo. The whistle telegraphs it; blocking or jumping it exposes the recovery. No taxi vehicle appears in normal combat.

## Character skill: Run It Back

Press Skill (Player 1: A) during the recovery window after the second hit of
Three-Piece to cancel into a short dance reset. Costs 1000 meter. The reset adds
no attack and grants no invincibility. Treat it as a pressure reset with a
visible, interruptible gap.

Its purpose is a resource-based choice between ending a string and taking a risky extra turn. It must not let Will repeat a true blockstring indefinitely. No rhythm minigame or audio-timing requirement; all information is visible in the animation.

## Supers

### Summertime Remix — one meter unit

Quarter-circle forward twice + H. A short-range opening strike confirms into a freestyle dance-combat sequence: shoulder pop, rapid body punches, spinning kick, and a freeze pose as the opponent slides away. Graffiti-like teal, yellow, and purple impact accents pulse through the sequence. Use original audio. On block or miss, the cinematic does not trigger and the starter is punishable.

### Fresh to Bel-Air — two meter units

Quarter-circle back twice + H. A clearly telegraphed close-range strike starts the ultimate. The camera swings through a stylized West Philly street as Will strings together quick punches, dance-step dodges, and a final spinning heel kick. A comic yellow taxi transition carries the scene into a Bel-Air mansion driveway, where the opponent lands in a luggage pile. Will straightens his cap and poses at the gate.

The taxi is a stylized scene transition, not a repeated attack or drivable gameplay object. Resolve damage once and return to the normal arena at the end. No cinematic on block or miss; no basketball imagery anywhere in the sequence. Keep the final impact a kick so it stays visually separate from Prince's dunk and Uncle Phil's doorway throw.

Meter costs are provisional relative units and must be aligned with the eventual shared combat system.

## Prototype routes

- Standing L → standing M → Three-Piece with L ending: simple confirm and pushback.
- Crouching L → crouching M → Windmill Remix: low starter into knockdown.
- Whiff punish with standing H → Taxi!: corner conversion only if spacing allows the wall bounce.
- Standing M → Three-Piece second hit → Summertime Remix: meter conversion if super-cancel rules support it.

These are intended routes, not verified combos. Frame data, damage, cancel windows, and wall-bounce limits require prototype testing.

## Art and animation changes

Use the approved sprite likeness and colorful 1990s outfit, with no hat. Replace
basketball hero poses with a dance stance. Bank Shot becomes Three-Piece, the
alley-oop becomes Fresh Step, and the dunk ultimate becomes Fresh to Bel-Air.
Reinterpret Fresh Footwork as dance motion within attacks. Future action boards
should use a graffiti-accented street or mansion driveway setting.

Existing `will-concept.png`, `will-concept-v2.png`, and the small full-body panel in `will-face-study-v3.png` still show basketball imagery. They remain historical visual references; this document supersedes their combat direction. A revised action board has not yet been generated.

## First playable scope

The first-pass package implements movement, normals, throws, Three-Piece,
Psyche!, Fresh Step, Windmill Remix, Taxi!, the meter reset and both finishers.
Next work is animation consistency, readability and balance refinement.
