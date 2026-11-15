# Dave Chappelle as Prince — moveset draft

Status: first playable implemented October 16, 2026. The corrected roster
pairs Prince with Rick James as his transformation. See
`sprite-fighter/characters/prince/CONTROLS.md` and `review.html` for current
inputs, native results and actual engine replays. The design below remains
the longer-term reference. Current Royal Bounce uses an arcing projectile;
dedicated floor-bounce logic, air-special dunk, stance exit button, portraits
and full in-betweens remain future work. The current super/ultimate deal
620/950 damage for 1000/2000 meter, following the user's exaggerated finisher direction.

## Fighting identity

A mobile trickster who controls space with basketball bounces, changes his approach with quick footwork, and punishes opponents who chase recklessly. Calm, regal poses make the sudden athletic bursts funny. His attacks favor exaggerated basketball action and costume flourishes.

Strengths: movement, angled projectiles, corner pressure, whiff punishment.
Weaknesses: low damage without setup, punishable committed approaches, no meterless invincible reversal. Use standard roster health until playtesting supports a change.

## Proposed controls

Four attack buttons: Light (L), Medium (M), Heavy (H), Skill (S). Directions are relative to facing the opponent. Quarter-circle and down-down motions are proposals until the game's shared controls are finalized. Throw and universal defense should follow the eventual roster-wide system.

## Core attacks

| Attack | Animation and purpose | Limitation |
| --- | --- | --- |
| Standing L — Lace Flick | Quick jab with a flourish of the cuff; close-range check. | Short reach. |
| Standing M — Royal Backhand | Deliberate backhand for midrange poking. | Can be beaten by faster close attacks. |
| Standing H — Purple Heel | Long high side kick; rewards whiff punishment and converts into specials on hit. | Slow recovery on a miss. |
| Crouching L — Ankle Tap | Fast low toe tap. | Modest damage and reach. |
| Crouching M — Court Sweep | Sliding low kick that can start a combo. | Unsafe if blocked at close range. |
| Crouching H — Royal Rejection | Upward palm-and-ball swat; primary anti-air and launcher on grounded hit. | Vulnerable to grounded approaches. |
| Jumping L — Air Check | Quick airborne knee for close air exchanges. | Small hit area. |
| Jumping M — Floating Heel | Extended diagonal kick for jump-ins. | Loses to well-timed anti-airs. |
| Jumping H — Purple Descent | Dramatic downward heel strike with strong hit reaction. | Slow startup. |
| Forward + M — Crown Breaker | Clearly telegraphed overhead heel drop. | Slow; no automatic full combo without a resource or special setup. |
| Forward throw — Baseline Toss | Basketball-style pivot and shoulder toss. | Standard throw rules. |
| Back throw — Court Switch | Spins around the opponent and sends them behind him. | Prioritizes position over damage. |

## Specials

| Move | Proposed input | Behavior | Counterplay |
| --- | --- | --- | --- |
| Royal Bounce | Quarter-circle forward + L/M/H | A conjured basketball hits the floor once, then travels forward. L is short and fast; M travels farther; H is slower with a higher bounce to occupy jump space. | Only one Royal Bounce projectile may be active per fighter. Startup can be challenged; predictable bounces can be jumped or blocked. |
| Purple Slide | Quarter-circle back + L/M | A low, gliding approach. L stops short as a spacing feint; M ends in a low heel strike. | No invincibility. The attacking version is punishable if blocked close. The feint cannot cancel immediately into a throw. |
| Royal Rejection | Forward, down, down-forward + H | A rising basketball swat that counters predictable aerial approaches. | Anti-air protection only; no full-body invincibility. Blocked or missed attempts leave a large opening. |
| Ruffle Counter | Quarter-circle back + H | Brief high/mid strike counter: catches the attack with a lace flourish, then shoves the opponent away. | Loses to lows, throws, projectiles, and delayed attacks; long recovery if nothing triggers it. |
| Baseline Cut | Down, down + S | Quick basketball crossover step through a nearby opponent to switch sides. No attack is built in. | Visible startup and recovery, no invincibility, and no immediate throw afterward. A movement tool with a readable response window. |
| Purple Rain Dunk | In air, quarter-circle forward + H | A steep descending dunk strike; launches only when used as an airborne combo ender. | One use per jump, no instant landing cancel, punishable on block. An airborne overhead; cannot hit low. |

## Character skill: Check Ball

Press S to enter a short stationary dribble stance. The stance has visible startup, no armor, and no guard. During the stance, press L for a short bounce pass, M for a forward crossover that ends outside throw range, H for a committed overhead dunk, or S to stop dribbling with recovery. Getting hit cancels the stance. Jumping and guarding are unavailable until it ends.

This is a deliberate pressure choice after a knockdown or at safe distance. It does not grant free mix-ups in neutral. The stance's pass follows the same one-projectile limit as Royal Bounce.

## Supers

### Game, Blouses — one meter unit

Quarter-circle forward twice + H. A fast advancing basketball strike; on hit, transitions into an ankle-breaking crossover, a burst of purple stage light, and a towering slam dunk. Final impact launches the opponent away and leaves Prince posing under the hoop. Useful as a confirmed combo ender. Blocked activation stops before the cinematic and leaves him punishable. No free cinematic damage through guard.

### Breakfast Is Served — two meter units

Quarter-circle back twice + H. A short-range, clearly telegraphed strike starts the ultimate. On hit, the scene cuts to a moonlit basketball court: crossover, impossible leap, thunderous dunk, then a smash cut to Prince calmly presenting pancakes as the opponent lands in a chair at the breakfast table. A purple spotlight and a tiny satisfied nod finish the scene. No gore. If the starter misses or is blocked, there is no cinematic and the opponent gets a punish opportunity.

The pancake sequence is presentation only. Damage and positioning resolve once, with both fighters returning to the normal arena after the cinematic. Until a shared super system exists, meter costs above are relative design targets.

## Sample routes to prototype

- Simple confirm: standing L → standing M → Royal Bounce L. Test the timing so the projectile connects on hit; do not assume it is a true blockstring.
- Low starter: crouching L → crouching M → Purple Slide M. A short grounded route ending in knockdown if confirmed.
- Anti-air reward: crouching H → jump M → Purple Rain Dunk. Requires the launch and air-cancel rules to support it.
- Meter cash-out: standing M → standing H → Game, Blouses. Special/super cancel windows must be tested.

These routes are intended behaviors for the prototype, not verified combos. No numerical frame data or damage values are final.

## Animation personality

- Idle: one hand at the lace collar, unimpressed expression, weight on one hip.
- Walk: unhurried regal strut; dash: startlingly quick basketball footwork.
- Intro: slowly removes a purple coat, produces a basketball, and waits for the opponent to check it.
- Taunt: spins the basketball on one finger; no gameplay buff.
- Win: sets down a plate of pancakes and folds his hands.
- Keep the face consistent with the approved likeness study; visual approval is still pending.

## First playable scope

Build movement, basic attacks, throws, Royal Bounce, Purple Slide, Royal Rejection, and Game, Blouses first. Add Check Ball, side-switch movement, counter, air dunk, and the breakfast cinematic after the core combat loop works. Use placeholder animation and effects while validating readability and counterplay.
