# Homey the Clown — moveset draft

Status: original game moveset concept for the requested character. Not implemented or playtested; invented attacks are not claims about a television sketch.

## Fighting identity

A stubborn close-to-midrange disruptor with a knotted sock weapon, deadpan expression, and reluctant clown theatrics. Homey uses awkward sock arcs, low kicks, and a single unreliable-looking party prop to interrupt predictable approaches. His comedy comes from refusing to entertain anyone while the fight accidentally becomes a clown routine.

Strengths: awkward attack angles, close-range interruption, knockdown setups, strong anti-approach reads.
Weaknesses: modest mobility, limited long-range reach, setup commitments, no meterless invincible reversal. Standard roster health initially. His sock has shorter maximum reach than Negan's bat; he gets faster close attacks rather than matching its heavy damage.

Four-button proposal: Light (L), Medium (M), Heavy (H), Skill (S). Inputs are relative to facing and provisional until the shared control scheme is settled.

## Core attacks

| Attack | Name and animation | Purpose and limit |
| --- | --- | --- |
| Standing L | Quit It — short free-hand jab. | Fast close check. |
| Standing M | Sock Check — quick horizontal sock swipe. | Main poke; limited disjoint at the knot, hittable hand and arm. |
| Standing H | Party's Over — wide, looping sock swing. | Whiff punish and knockdown; noticeable startup and recovery. |
| Crouching L | Big Shoe Tap — quick low toe poke. | Low check. |
| Crouching M | Clown Shoe Sweep — exaggerated low sweep. | Low starter; punishable close on block. |
| Crouching H | Up You Go — upward sock flick. | Primary anti-air; loses to well-spaced grounded attacks. |
| Jumping M | Big Foot — descending oversized-shoe kick. | Standard jump-in. |
| Jumping H | Bad Birthday — slow downward sock swing. | Heavy air attack with a clear wind-up. |
| Forward + M | Look Up — raises a party hat, then chops downward with the sock. | Slow overhead; no large meterless conversion. |
| Forward throw | Take Your Present — forces an empty gift box into the opponent's hands, then shoves them away. | Standard breakable throw; box is cinematic dressing. |
| Back throw | Wrong Party — pivots and tosses the opponent behind him. | Standard throw rules and position swap. |

## Specials

### Sock It to You

Quarter-circle forward + L/M/H. A single sock strike with different trajectories: L is a quick short mid, M swings farther horizontally, and H makes a slower upward arc intended to catch jumps. The upward version hits mid against grounded opponents and cannot become a disguised overhead. No armor or invincibility. M and H have enough recovery for a spaced whiff punish; H is punishable on block nearby.

### Homey Don't Play That

Quarter-circle back + H. Brief counter stance: folds his arms, tilts his head, then answers a caught high or mid melee strike with one emphatic sock bonk. Lows, throws, projectiles, and delayed attacks beat it. Long recovery when it fails. Not an escape from an already-confirmed combo, and no automatic counter against every attack type.

### Get Off My Shoes

Quarter-circle back + M. Stomps forward with an oversized shoe, hitting low at short range. Knocks down on a clean hit but is punishable on block. No armor. Provides a grounded threat underneath opponents waiting for the sock arcs.

### Party Favor

Quarter-circle forward + S. Places a small wind-up jack-in-the-box a short distance ahead. After a fixed visible wind-up, it opens once with a short-range spring-glove mid strike, then disappears. The glove does not track, launch projectiles, or move the opponent by itself without contact.

Only one box per Homey may be active. The opponent can destroy it with one attack, jump over the strike, or block it. Homey can be interrupted during placement, and the box disappears if he is hit or the round ends. Its strike cannot trigger throws, unblockables, or repeated box loops. Start with low damage and pushback, no combo extension until testing supports one.

The box gives him a small temporary area to defend after knockdown, rather than full-screen zoning. Keep it visually distinct from Urkel's elaborate inventions: one cheap clown prop with one predictable action.

### No Refunds

Quarter-circle back + L. Steps backward and sweeps the sock across the space he just left. One mid strike, limited reach, no invincibility or side switch. Used to bait a short poke; forward movement and longer attacks can catch the retreat. Punishable if blocked at close range.

## Character skill: Balloon Business

Press S to begin visibly twisting a long balloon. Startup and completion have fixed durations; Homey cannot move, guard, or attack during the preparation. On completion he holds one balloon animal. No passive buff, random outcome, stacking resource, or permanent reward.

With a balloon held, press S again for Balloon Pop: Homey squeezes it into a short, close-range mid pop that deals negligible damage and pushes the opponent away on hit or block. It does not stun, blind, mute inputs, create a free throw, or guarantee another balloon setup. It is not a projectile and does not beat projectiles. The balloon is consumed on use and lost if Homey is hit. The pop's startup is visible, with no invincibility; balance recovery so it ends his turn on block.

This is an optional prepared spacing tool with a funny payoff. Keep Party Favor and Balloon Pop pushback modest enough that neither creates guaranteed setup loops.

## Supers

### Nobody's Laughing — one meter unit

Quarter-circle forward twice + H. A short-range sock strike confirms into a rapid series of alternating sock swipes and big-shoe kicks. He pauses with an irritated stare, then finishes with one huge looping sock swing that sends the opponent sliding away. No cinematic on block or miss; starter is punishable. No invincible startup by default.

### Worst Birthday Ever — two meter units

Quarter-circle back twice + H. A telegraphed close-range strike confirms into a shabby birthday-party stage. The opponent lands in a folding chair, a banner droops, and a party horn produces one sad note. Homey reluctantly offers a balloon animal; it pops, the opponent springs upright in surprise, and he delivers an exaggerated body-level sock wallop that launches them into a pile of empty presents. He sits down, folds his arms, and glares as confetti falls late.

No gore or realistic injury. The chair and presents are cinematic props, not persistent arena objects. Resolve damage once and return both fighters to predictable positions. The starter must connect; block or miss gives the defender a punish opportunity. Use original recorded audio and dialogue.

## Intended prototype routes

- Standing L → standing M → Sock It to You L: simple close confirm.
- Crouching L → crouching M → Get Off My Shoes: low route into knockdown if cancel rules support it.
- Whiff punish standing H → Sock It to You M: spacing-based conversion if the cancel window permits.
- Standing M → Nobody's Laughing: straightforward meter cash-out.
- Knockdown → Party Favor placement: setup only where recovery and wake-up timing actually allow it; never assume it is guaranteed.

Routes are design targets, not verified combos. No frame data, damage, counter windows, or setup safety is final.

## Visual and animation direction

- Preserve the recognizable Homey character silhouette: bright clown wig, round red nose, clown makeup, loose colorful costume, oversized shoes, and knotted sock.
- Facial reference should be Damon Wayans portraying Homey, with a fed-up deadpan expression. Keep him distinct from the Chappelle characters.
- Idle: sock hanging at his side, slumped shoulders, unimpressed stare.
- Walk: heavy, reluctant steps; sock trails with a readable arc.
- Intro: checks an imaginary party booking, looks at the opponent, and slowly drops the paper.
- Taunt: starts to smile, immediately gives up. No gameplay effect.
- Win: sits on a folding chair as a balloon slowly deflates beside him.
- No background children, crowd interaction, or forced laughter mechanic needed for combat.

## First playable scope

Start with movement, normals, throws, Sock It to You, Get Off My Shoes, and No Refunds. Validate sock animation readability and hurtboxes. Add the counter, Party Favor, Balloon Business, and supers after the basic spacing game works. Prototype props with simple shapes before producing cinematic assets.
