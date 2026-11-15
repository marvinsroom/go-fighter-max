# Dave Chappelle as Negan — moveset draft

Status: first playable implemented October 16, 2026. The corrected roster
makes Negan the transformation of Tyrone Biggums. See
`sprite-fighter/characters/negan/CONTROLS.md` and `review.html` for current
inputs, validation and actual engine replays. The original design below remains
the longer-term reference. Current kit includes the three bat swings, low kick,
feint, anti-air, whistle branches, command grab and 620/950-damage finishers.
Counter-hit wall bounce, extra attack in-betweens, portraits and competitive
balance remain future work. These are original invented game moves.

## Fighting identity

A deliberate midrange bully with a theatrical grin, a leather jacket, red scarf, and a barbed-wire-wrapped bat. He wins by making opponents hesitate at the edge of his reach, then punishing movement with heavy swings. Dave Chappelle's likeness and comic delivery should remain apparent beneath the costume.

Strengths: grounded reach, whiff punishment, corner carry, strong single-hit conversions.
Weaknesses: slow committed swings, weak close-range scramble defense, limited mobility, no projectile, no meterless invincible reversal. Standard roster health initially; strength comes from reach rather than extra durability.

Keep combat stylized: blunt impact flashes, knockback, bent scenery, and comic reactions. No blood, dismemberment, or head-crushing sequences.

## Proposed controls

Shared proposed four-button layout: Light (L), Medium (M), Heavy (H), Skill (S). Directions are relative to facing. Inputs and meter costs are provisional until shared combat rules exist.

## Core attacks

| Attack | Name and animation | Purpose and limit |
| --- | --- | --- |
| Standing L | Personal Space — quick free-hand palm jab. | Close check; short range. |
| Standing M | Handle That — short jab with the bat handle. | Reliable midrange check; less reach than heavy swings. |
| Standing H | Big Introduction — broad horizontal bat swing. | Long-range punish; substantial whiff recovery. |
| Crouching L | Boot Check — quick low toe kick. | Low check. |
| Crouching M | Kneecap Notice — low boot sweep while the bat stays over his shoulder. | Readable low attack; punishable close on block. |
| Crouching H | Heads Up — upward bat swat. | Primary anti-air; vulnerable to grounded attacks. |
| Jumping M | Leather Sole — descending boot kick. | Standard jump-in. |
| Jumping H | Heavy Baggage — slow diagonal bat swing. | Strong air reach; large startup and landing commitment. |
| Forward + H | Knock Knock — clearly telegraphed overhead bat strike. | Slow overhead; large combo requires meter or a specific counter-hit route. |
| Forward throw | Friendly Chat — grabs the lapel, leans in to grin, then shoves the opponent away with a boot. | Standard breakable throw; distance over damage. |
| Back throw | Your Seat's Over There — pivots and tosses the opponent behind him. | Standard throw rules and position swap. |

The bat's business end can have limited disjointed reach, but the hands and arms remain hittable. Avoid making every poke impossible to challenge.

## Specials

### Meet Lucille

Quarter-circle forward + L/M/H. A committed horizontal bat swing. L is short and quicker; M reaches farther and knocks down; H has the longest wind-up and carries the opponent toward the corner on hit. All versions are mids. Only a clean H counter-hit near the corner causes a wall bounce, once per combo. H is interruptible on startup and punishable on block. No armor on these swings.

### Take a Knee

Quarter-circle back + M. A short stepping boot to the shin, followed on hit by a bat-handle body shove. The first hit is low. If the kick is blocked, the shove does not automatically trap the opponent: the move stops with punishable recovery. Shorter reach than Meet Lucille, allowing the opponent to manage the threat through spacing.

### Swing and a Miss

Quarter-circle back + L. Starts the wind-up silhouette of Meet Lucille, then pulls the bat back onto his shoulder. No attack, armor, invincibility, or automatic counter. Recovery prevents immediate throw or guard. A prediction-based feint with a different silhouette from the overhead, so it cannot hide every attack behind one animation.

### Back Off

Forward, down, down-forward + H. A rising bat-handle shove and upward swing. Anti-air protection only; no full-body invincibility. Useful against predictable jumps, but leaves a large opening if blocked or baited. It should not replace his normal anti-air in every situation.

### Business Meeting

Half-circle back + H. A short-range command grab: hooks the opponent's arm with the bat handle, turns them around, and plants a boot into their back to send them forward. No head strike. Cannot grab airborne opponents or opponents in blockstun; no invincible startup. A missed grab has long recovery. This is a secondary threat, with less damage and reach than dedicated grappler Uncle Phil's primary grabs.

## Character skill: The Whistle

Press S for a brief whistle while resting the bat on his shoulder. The whistle has no hitbox and does not freeze or debuff the opponent. During a short follow-up window:

- L — Early Exit: cancel into an in-place recovery pose sooner than the attack options. This is still a commitment, not instant guard.
- M — Collection Time: a forward step into a mid bat-handle body strike. Advances farther than his normal poke but can be interrupted.
- H — Final Warning: a slow planted bat swing with one hit of armor against eligible grounded mids/highs during the visible wind-up only. Lows, throws, projectiles, and multiple hits beat it. Absorbed damage still applies; armor disappears before the active swing. Punishable on block or whiff.

The stance cannot move, jump, block, or loop back into itself. All attack follow-ups are mids; no unreactable low/overhead guess from the same startup. Use it after a knockdown or at carefully chosen distance. Do not add an invisible intimidation meter or input restriction.

## Supers

### Collection Day — one meter unit

Quarter-circle forward twice + H. A forward bat-handle body strike confirms into three heavy, theatrically spaced blows ending with a sweeping knockback. Between hits, he adjusts the scarf and flashes a disbelieving grin. Treat pauses as cinematic presentation after a confirmed hit. On block or miss, the cinematic never starts and the starter is punishable. No invincible startup by default.

### The Last Laugh — two meter units

Quarter-circle back twice + H. A clearly telegraphed close-range strike confirms into an abandoned warehouse cinematic. He whistles, slowly points the bat, and begins a huge theatrical wind-up. The opponent braces; he pauses to adjust his jacket, then suddenly lands a body-level bat strike that launches them through a stack of empty supply crates. He rests the bat over his shoulder and gives the camera an amused look as a single crate lid falls behind him.

No kneeling execution, head crushing, blood, or gore. Damage resolves once. The cinematic returns to the normal arena with predictable separation. On block or miss, no cinematic triggers and recovery is punishable. Use original dialogue and audio.

## Intended prototype routes

- Standing L → standing M → Meet Lucille L: close confirm into separation.
- Crouching L → crouching M → Take a Knee: low route if the final cancel rules permit it.
- Standing H whiff punish → Meet Lucille M: reach-based punish and knockdown.
- Meet Lucille H counter-hit wall bounce → standing M → Collection Day: corner meter conversion; enforce one wall bounce per combo.

These are targets, not verified combos. Frame data, damage, protection windows, cancel rules, and spacing need playtesting.

## Animation and visual direction

- Likeness: Dave Chappelle's facial structure, expressive eyes, long face, and mischievous delivery in the Negan costume. Do not substitute Jeffrey Dean Morgan's face.
- Costume: black leather jacket, red scarf, dark trousers, boots; bat silhouette clear from the side camera.
- Idle: bat across shoulder, relaxed lean, watchful grin.
- Walk: measured forward steps; limited speed reinforces grounded control.
- Intro: slow whistle, jacket adjustment, then a casual bat-point toward the opponent.
- Taunt: checks an imaginary appointment on his wrist, then gestures for the opponent to hurry. No gameplay buff.
- Win: sits on an empty crate with the bat across his knees; the crate creaks under the dramatic pose.
- Keep voice and facial comedy original rather than copying dialogue from a show.

## First playable scope

Build movement, normals, standard throws, Meet Lucille, Take a Knee, and Swing and a Miss first. Validate bat hurtboxes and punish windows. Add the anti-air special, command grab, whistle stance, and supers after the core spacing game works. Delay cinematic production until hit confirmation and return positioning are reliable.
