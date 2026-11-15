# Lamine Yamal - first fighter concept

User selected Lamine Yamal as the next fighter on October 16, 2026.
The initial visual design was approved and the user requested engine integration.
The first playable is now packaged under `sprite-fighter/characters/yamal`;
see its controls and runtime-validation report for delivered behavior. The
original design below remains a reference for further polish.

Identity: a fast football dribbler who controls space with a ball, changes pace,
and converts a clean opening into exaggerated cinematic shots. Lean athletic
proportions, recognizable face, blue/red football kit. Initial outfit is a visual
proposal; no exact season kit or squad number is assumed.

## Core play

Standing light is a quick inside-foot tap, medium a turning kick, and heavy a
committed left-foot drive. Crouching attacks use low toe pokes and a slide;
air attacks use volleys and a bicycle kick. A shoulder-to-shoulder challenge
provides the close throw. The ball is a gameplay prop, never a second fighter.

- Close Control: skill enters a short dribble with a visible ball at his feet.
  Light exits into a quick poke, medium performs a forward cut, and heavy commits
  to a rising flick. No automatic invulnerability or endless cancel loop.
- Cut Inside: toward + skill changes pace into a diagonal-looking grounded
  approach and left-foot strike. Travels only on the game's combat plane.
- Elastico: away + skill performs a retreating feint into a return kick.
- Nutmeg: down + skill sends a low rolling ball that knocks the opponent down
  on a clean hit. Guardable low with a clear startup.
- Curler: quarter-circle forward + attack launches a spinning ball. Strength
  controls speed and recovery. One ordinary ball projectile at a time; after it
  expires, a replacement appears during a visible foot-trap animation.
- Rainbow Flick: quarter-circle back + attack pops the ball upward as an
  anti-air, with a recovery window if it misses.

## Super: Left-Foot Lightning

Proposed cost: 1000 meter. Proposed confirmed damage: 620 against 1000 health.
A guardable opening volley confirms a four-second sequence: nutmeg, sprinting
stepovers, repeated wall-pass ricochets around the captured opponent, an aerial
volley, then a giant blue/red curling shot that crosses the arena. The opponent
remains visible, and damage resolves once. A blocked opener does not capture.

## Ultimate: The World Is My Pitch

Proposed cost: 2000 meter. Proposed confirmed damage: 950 against 1000 health.
A guardable cinematic starter converts the arena into a luminous stadium.
Oversized pitch markings sweep underfoot; rapid dribble afterimages surround
the opponent, a rainbow flick launches them, and Yamal follows with successive
air volleys. A huge spectral goal appears behind the victim for the final
left-foot shot: the ball becomes a blue/red comet, the net erupts with light,
and a stadium-wide GOAL finish holds briefly before normal play returns.
Target duration seven seconds. Intentionally exaggerated per the user's
existing preference for overpowered finishers. No real match footage or audio.

## Production state

Begin with one stance concept at gameplay size and keep proportions consistent
through crouch, jump and knockdown. Next art work is a dedicated movement and
kick set, followed by engine packaging, authored effects and native validation.
First playable uses nine transparent key poses, normals, football projectiles,
directional dribble specials and cancel branches, throws, guard and both
620/950-damage cinematic finishers. Some imagery in the original ultimate
description remains a polish target; current effects use an authored stadium,
goal, volleys, afterimages, comet, flash and GOAL title. No transformation has
been selected for this fighter.
