# Will — combat prototype controls

Double-click **Play Will.cmd** for a two-player match with full starting meter.
The build implements Will's revised, basketball-free kit from
`concepts/will-moveset.md`. These are first-pass combat timings and key-pose
animations, not finished animation or competitively balanced frame data.

| Action | Player 1 | Player 2 |
| --- | --- | --- |
| Move / crouch / jump | Arrow keys | J/L left/right, K down, I up |
| Light (L) | Z | F |
| Medium (M) | X | G |
| Heavy (H) | C | H |
| Skill / Run It Back | A | R |
| Super shortcut | S | T |
| Ultimate shortcut | D | Y |
| Throw | Q, close to opponent | Left bracket, close to opponent |

Hold **back** to block mids and aerial/overhead attacks. Hold **down + back** to
block lows. Throws bypass guard. Directions below are relative to facing the
opponent; the quarter-circle directions reverse when you face left.

## Normals and movement

- Standing L: Fresh Jab. Standing M: Philly Straight. Standing H: Punchline.
- Down + L: Sneaker Tap. Down + M: Floor Sweep, knocks down.
- Down + H: High-Top Saver, anti-air elbow. The approved design has no cap.
- Forward + M: High Five, a slower overhead palm strike.
- Jump + L: air jab. Jump + M: Fresh Sole kick. Jump + H: Double Take, two hits.
- Q: Fresh Handshake throw. Back + Q: After You, the side-switch throw.
- Light can cancel into medium/heavy on hit, and medium into heavy. Normals
  can cancel into specials on hit. These routes still need balance testing.

## Specials

| Move | Facing-right motion | Behavior |
| --- | --- | --- |
| West Philly Three-Piece | Down, down-right, right + L | Shoulder/elbow entry. Tap an attack for the body punch, then L/M/H for palm/low sweep/slow overhead kick ending. |
| Psyche! | Down, down-left, left + L | Fake entry with no hitbox or invulnerability. |
| Fresh Step | Down, down-left, left + M | Upright side kick with punishable recovery. |
| Windmill Remix | Down, down-right, right + H | Two mid leg hits with knockdown; can be blocked standing or crouching. |
| Taxi! | Down, down-left, left + H | Committed elbow lunge, with a once-per-combo corner-bounce rule. |

**Run It Back:** press Skill during the body-punch recovery window of Three-Piece.
It spends **1000 meter**, adds no hit or invincibility, and gives a visible
recovery gap. Three-Piece cannot cancel back into its own opener.

## Super and ultimate

**Summertime Remix — 1000 meter:** quarter-circle forward twice + H, or the
super shortcut. A fake handshake and shoulder feint lead into a quick punch
string, an airborne chase, afterimages and a finishing launch kick. Will ends
with a comic shrug. The opening strike must hit; a blocked or missed starter recovers
normally and still spends meter.

**Fresh to Bel-Air — 2000 meter:** quarter-circle back twice + H, or the ultimate
shortcut. Will whistles for a moving cab, chases it through the street-to-mansion
transition, kicks the opponent toward a pile of luggage, then shrugs at the viewer.
The ultimate's damage is applied once at the final
impact. A blocked or missed starter never starts the cinematic. This is a
sprite cinematic with animated positions and props; pose-to-pose animation still
needs additional in-betweens.

Maximum meter is **3000**. Attacks build meter through the engine's hit/guard
rules. The sample launcher starts full so both finishers can be tried immediately.

## Practice helpers

- **F3:** refill both players' meter using the engine's existing debug helper.
- **Space:** restore both players' life and meter using the existing debug helper.
- **F4:** restart the round.
- **Escape:** match menu when launched with the supplied Play Will launcher.

There are no basketball moves, sampled celebrity voices or licensed songs.
Sound cues are synthesized for this prototype. Some attacks reuse key poses;
additional animation in-betweens, HUD portraits and competitive balance remain.
