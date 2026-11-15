# Al Bundy — moveset draft

Status: original fighting-game concept for Al Bundy from Married... with Children. Not implemented or playtested. Invented attacks and cinematics are game concepts, not claims about particular episodes.

## Fighting identity

A weary scrapper who suddenly finds his old football energy. Al fights with short punches, work-shoe kicks, and committed shoulder charges. His central mechanic is converting a successful football tackle into a choice between field position and damage.

Strengths: punishing mistakes, grounded knockdowns, corner carry, simple hard-hitting confirms.
Weaknesses: slow walking, modest poke reach, vulnerable charge recovery, no projectile, no meterless invincible reversal. Standard roster health initially. He is not a dedicated grappler like Uncle Phil; tackle follow-ups require a successful strike rather than an unblockable grab.

## Proposed controls

Shared four-button layout: Light (L), Medium (M), Heavy (H), Skill (S). Directions are relative to facing. Inputs, meter units, and cancel rules remain provisional.

## Core attacks

| Attack | Name and animation | Purpose and limit |
| --- | --- | --- |
| Standing L | Clock In — tired-looking quick jab. | Fast close check. |
| Standing M | Working Stiff — compact body hook. | Reliable grounded starter. |
| Standing H | Overtime — heavy overhand punch with a weary grunt. | Strong punish; slow whiff recovery. |
| Crouching L | Bargain Kick — short low shoe tap. | Low check. |
| Crouching M | Last Pair — low shin kick. | Low starter; unsafe on block nearby. |
| Crouching H | Not Today — rising forearm. | Primary anti-air; limited horizontal reach. |
| Jumping M | Road Game — descending work-shoe kick. | Standard jump-in. |
| Jumping H | Old Glory — committed airborne forearm strike. | Slow heavy jump-in; no tackle follow-up. |
| Forward + H | Top Shelf — slow downward double-fist strike. | Clearly telegraphed overhead; no large free conversion. |
| Forward throw | Store's Closed — grabs the collar and shoves the opponent away. | Standard breakable throw; favors separation. |
| Back throw | Returns Counter — pivots and dumps the opponent behind him. | Standard throw rules and position swap. |

## Specials

### Polk High Power

Quarter-circle forward + L/M/H. A grounded shoulder charge that hits mid. L travels a short distance with quicker startup; M carries farther; H has the longest visible wind-up and carries toward the corner. No invincibility or armor by default. All versions are punishable when blocked nearby; H also has long whiff recovery.

Only on a clean grounded hit, the opponent enters a brief tackle reaction and Al may choose one follow-up:

- L — First Down: a short shove, giving separation and less damage.
- M — Extra Yard: drives forward a little farther before knocking the opponent down; modest damage, better corner carry.
- H — End Zone: plants his feet and finishes with a heavy body shove; more damage, less carry, greater recovery before Al can approach.

No follow-up on block, miss, or an airborne hit. If no input arrives, use First Down automatically. The initial charge and follow-up form one resolved strike sequence; these are not command grabs and cannot bypass guard. One tackle sequence per combo, no repeated carry loops. Start without wall bounce or armor to keep it distinct from Negan's heavy swings.

### Minimum Wage

Quarter-circle back + L. Two compact body punches followed by a tired elbow. All mids, short reach, modest damage; close-range combo ender. Negative on block and cannot reset into the tackle or repeat itself without a punishable gap. No meter stealing or resource drain.

### Size Twelve

Quarter-circle back + M. A deliberate forward boot to the stomach. Mid attack with pushback; creates breathing room on hit. No low hit, guard break, or armor. Slow startup lets opponents interrupt, and a whiff leaves him exposed.

### Off the Clock

Quarter-circle back + H. Al visibly ducks and shifts backward before swinging a short hook. During a defined portion of the duck, his lowered hurtbox can avoid sufficiently high attacks; mids, lows, throws, and properly aimed projectiles still hit him. No automatic counter, invincibility, or hit confirmation on the opponent's attack. This is a spacing read with long recovery if baited.

### Shoe Fits

Forward, down, down-forward + H. A rising elbow with his other hand still holding a work shoe as a comic prop. Anti-air protection only, no full-body invincibility. Punishable on block or miss. The shoe is not thrown and does not add a separate hitbox.

## Character skill: Glory Days

Press S after a successful Polk High Power follow-up to perform a brief victory fist pump and spend one shared meter unit to reduce Al's post-tackle recovery. It deals no extra damage, gives no invincibility, and does not erase the defender's wake-up options. Position after First Down usually remains too distant for immediate close pressure; Extra Yard trades meter for a possible approach; End Zone still retains enough recovery to prevent guaranteed repeat tackles.

Cannot activate on block, miss, airborne hit, normal throw, or a cinematic super. No stacking touchdown counter, passive damage buff, or penalty for failing to activate it. This is a simple choice between saving meter and improving position after a confirmed tackle. The exact recovery reduction must be established through wake-up testing; no guaranteed safe-jump or throw loop is assumed.

## Supers

### Employee of the Month — one meter unit

Quarter-circle forward twice + H. A short body punch confirms into a flurry of exhausted-looking hooks, an elbow, and a shoulder shove that sends the opponent through a graphic burst of empty shoeboxes. Al briefly straightens a crooked name badge before the final hit. No cinematic on block or miss; starter is punishable. No invincible startup by default.

### Four Touchdowns, One Game — two meter units

Quarter-circle back twice + H. A clearly telegraphed shoulder strike confirms into a stylized Polk High football field. Al suddenly looks energized as stadium lights switch on and a scoreboard marks four scoring beats:

1. A driving shoulder check sends the opponent skidding downfield.
2. A quick sidestep and stiff-arm spins them toward the sideline.
3. A dramatic hurdle leads into a body-level forearm impact.
4. A final charging tackle sends them into padded end-zone equipment as the fourth touchdown lights up.

Hard cut to Al dropping onto his battered couch, proudly raising four fingers, then wincing as he rubs his back. The opponent remains on the field; the couch is his closing reaction shot, not another impact. No gore, head-first spike, or realistic injury sequence. Use original stadium audio and dialogue.

The scoring beats are cinematic presentation, not four separately escapable attacks after confirmation. Resolve damage once, return both fighters to predictable arena positions, and trigger no cinematic on block or miss. No actual football projectile or dunk imagery.

## Intended prototype routes

- Standing L → standing M → Minimum Wage: simple close confirm.
- Crouching L → crouching M → Polk High Power L → First Down: low starter into separation if cancel rules permit.
- Standing H whiff punish → Polk High Power M → Extra Yard: corner-carry route.
- Confirmed tackle → End Zone → Glory Days: spend meter to recover sooner, with wake-up timing verified before enabling pressure.
- Standing M → Employee of the Month: straightforward meter cash-out.

These routes are design targets, not verified combos. Frame data, damage, tackle timing, cancel rules, and wake-up advantage require playtesting.

## Visual and animation direction

- Use Al Bundy's appearance as portrayed by Ed O'Neill as the likeness reference for a future mockup.
- Everyday shoe-salesman outfit, loosened tie, worn trousers and shoes; reserve football uniform changes for the ultimate cinematic.
- Idle: slumped shoulders, tired stare, occasional lower-back stretch.
- Walk: reluctant steps. Charge: surprising burst of old football form.
- Intro: drops a shoebox, looks at the opponent, and sighs before raising his fists.
- Taunt: proudly raises four fingers. No passive buff or resource gain.
- Win: collapses into his couch, reaches for a remote, and finds the batteries missing.
- Shoe-store props remain background or cinematic elements; no odor cloud, shoe projectile, or automatic opponent debuff.
- Keep comedy focused on his exhaustion, pride, football nostalgia, and thankless work.

## First playable scope

Build movement, normals, standard throws, Polk High Power with its three confirmed-hit finishes, Minimum Wage, and Size Twelve first. Validate charge punishability and return positioning. Add Off the Clock, Shoe Fits, Glory Days, and supers once the grounded game is stable. Produce cinematics only after hit-confirm transitions and round-state handling work.
