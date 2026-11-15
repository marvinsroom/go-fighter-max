
RAPHAEL by Dcat Power. http://www.mugen-infantry.net
                       http://mugenguild.com/



+++++++++++++++++++++

What's here:
UPDATE - 4/12/2019
====================
-Added SKY-RIPPER Special, while In The Air: [QCB + Any Punch Button]
-Added CLAW HAMMER Air Super, while In The Air: [QCF , QCF + Any Punch Button]
-Added JAMBOREE Specials, while On the Ground [ QCB + Any Punch Button]
-Added 	EX JAMBOREE Specials, while On the Ground [ QCB + Any 2 Punch Buttons]
-Remapped HEARTBREAKER Special to [QCB + Any Kick Button]

UPDATE - 1/17/2019
====================
-Added CHESTBUSTER Special Attack [Hold Back, then press Forward + Any Kick Button]
-Added Chain Combos to Raph's Air Normals
UPDATE - 10/31/2018
====================
-Added 2nd supine variety EX HEARTBREAKER Attack [QCB, MP + HP]
-Changed SUPER HEARTBREAKER into Supermove [QCB, QCB + Any Punch Button] 

UPDATE - 9/14/2018
====================
-Added 2nd Vaulting Counter for COUNTER ATTACK [StateDef 1050] Hold Back Direction while pressing HP + HK 
-Added EX HEARTBREAKER Attack [QCB, LP + MP]
-Added SUPER HEARTBREAKER Attack Inspired by Injustice 2 [QCB, MP + HP]

UPDATE - 8/18/2018
====================
-Updated Pallette Names
-Added Auto Launcher attack to StateDef 221

UPDATE - 8/3/2018
====================
-Added Simple ENEMY Bound FX coding for helper opponents
-Updated COUNTER ATTACK [StateDef 1050] 

UPDATE - 2/2/2013
====================
-Added custom AI by Veanko
-Increased Super & Hyper damage against Super Shredder

UPDATE - 9/10/2012
====================
-Prevented change to crouching state from run (StateDef 100)

UPDATE - 9/6/2012
====================
-Added TMNT 1 ARCADE  APRIL'S APARTMENT Intro vs DcatShredder

UPDATE - 6/24/2012
====================
-Fixed error that prevented Hyper Move from performing correctly in Simul Mode

UPDATE - 6/20/2012
====================
-Added animation numbers to correspond to "Pharoah's Curse/Retromutagen" special states
-Added animation numbers [8055000-8055999] for Messatsu's Character trait identifiers
-Added Burned, Frozen, Midnight Bliss special animations
-Fixed DiagUp/DiagDown animations
-Fixed Dizzy and Dizzy Stars animations
-Added Dizzy Helper [Statedef 5305] to create Dizzy Stars effect universally
-Changed sprites for (5010,20) (5011,20) & (5012,20) in .SFF file
-Added EVENING NEWS Intro against Krang (StateNo 196)
-Fixed issue with EX THOUSAND STAB passing through Helper Opponents
-Added rotation to Opponent hitstate for EX Thousand Stab: (compatible with Cybaster & Balthazar's Flip Knockout anim)
-Recoded EX THOUSAND STAB so that it's more reliable
-Added new Fall Back State (StateNo 651) for if the Opponent blocks some of Raph's special attacks
-Fixed issue with Counter Atack spawning clones against Helper opponents
-RAMPAGING TURTLE Hyper (StateNo 3300) is now unblockable
-Increased velocity on RAMPAGING TURTLE Hyper

UPDATE - 3/20/2011
====================
-Increased volume of voice audio
-Fixed Damage Output for RAMPAGING TURTLE & both POWER DRILL SUPERS
-Fixed Super KO Finish display details
-Increased damage of all Specials and EX Specials
-Removed Ininite possibility from Heavy Punch THOUSAND STAB Special
-Removed command glitch where AIR POWERDRILL Super would result from inputting the Dive Kick command immediately after a Super Jump  
-Added block damage to those atacks which were previously lacking
-Added startup frame to Dive Kick

UPDATE - 1/28/2011
====================
-Tweaked Body Slam Throw
-Added additional voice sound to CRIMSON TIDE
-Adjusted damage calculation on CRIMSON TIDE to use (Target, LifeMax)
-Invulnerable Frame parameters edited for Crimson Tide
(Raph Can be hit by all Air Attacks or if opponent is behind Raphael  during Startup)
-Hitbox altered on Crimson Tide
-added additional Triggers to the .CMD for Crimson Tide

UPDATE - 1/24/2011
===================
-Special Thanks to KojiroBADNESS for fixing the Special Intro glitch
Intros now work in Winmugen as well as Mugen 1.0!! Many thanks to him for fixing that pesky little issue, it was driving me nuts.

UPDATE - 1/23/2011
===================
-Added Winposes
-Added Special Intros with the other Turtles
-Added HEARTBREAKER Special (QCB + Any Punch)
-Varied THOUSAND STAB Properties

UPDATE - 1/02/2011
===================
-Increased damage dealt
-Added sliding stop to all turtles for dash-in standing & crouching attacks
-Afterimages on dash and super jump
-Added velocities to air attacks following a launcher pursuit for fewer whiffed chances
-Fixed opponent positions on custom states
-Fixed Posset bug with Turtles appearing beneath the floor

UPDATE - 12/25/2010
===================
-fixed CLSN's
-updated sprites
-tweaked Supercancel Damage
-Added custom land state
-Added longer cool down to all Normals and Specials
-Added limiter to Thousand Stab & EX Thousand Stab to prevent infinites
-changed Crouching MP (StateDef 410) to Sweep attack
-improved chaining from air normals into Stab Shoot Special
-improved Stab Shoot Special timing & execution
-Changed the Counter attack to an EX move 
-Added CRIMSON RAIN Hyper Move
-Combo Tweaking

UPDATE - 1/30/2010
===================
-added EX Dive Kick move
-fixed position of dizzy stars for liedead and lose states
-Intros with other turtles
-fixed targetstate issues with some moves

UPDATE - 9/12/2009
===================
-Added Voice & Sound Effects to misc. attacks
-Added Slash sparks to slashing attacks
-Added Dash Dust Effects to jump, superjump, runback, floor bounce, floor recover states
-Fixed the spamming Wall Hit glitch
-Intros with other turtles
-Better scaled dimensions
-More Palettes
-CVS Lifebars Portrait 
-Counter move Added (QCB + Any punch button)
-Advancing Guard Added (any 2 punches during a blocked hit)
-Super KO Finish

UPDATE - 7/30/2009
===================
-Removed juggling on downed opponent from standing LK, crouching LP, crouching MP, crouching LK, crouching MK
-Rampage super no longer hits downed opponent on the first hit for fairness
-tweaked triggerall for the wall hit to prevent inifinite spark/&combo generation
-added anglesets to powerdrill to prevent sprite shifting during scaling

UPDATE - 7/29/2009
===================
-Increased general damage for normals
-Improved the OTG chaining with more velSets & changestates
-Improved launcher setups & chaining from crouching MP > crouching HP
-Added Velset to jumping LK to help with range for air combos 
-Added sound effect to the run state
-fixed the PosSet for PowerDrill: Now more towards the middle of the screen instead of at the floor
-tweaked wall hit
-added hitDefs to moves that put p2 into custom states so they will at least damage chars that can't be put into custom states
-made equal possibility (1/3) for getting each of the 3 taunts


What's missing:
====================== 
add AI

+++++++++++++++++++++++++++++++
** Sprites & Sounds ripped from TMNT Hyperstone Heist, TMNT IV Arcade, TMNT 3 Manhattan Project
** TMNT 2 Secret of the Ooze Sound Rips by DJ TRACK
** TMNT IV SNES Sprite sheets by Cabanaman 
** TMNT TF SNES Sprite sheets by
** Sounds rpped from TMNT Movie(1990), TMNT II: Secret of the Ooze, 
             TMNT(4Kids cartoon 2003), TMNT III Movie

CREDITS:
========
*** Cybaster, Shwa, & RajaaBoy for thoroughly beta testing each turtle ad nauseum &
    the various gameplay fixes and suggestions throughout
*** Cyanide for Helper binding fix 
*** RicePigeon, Cyanide, Caddie for fall.defence_up/damage dampener workarounds
*** Special thanks to N-Mario for his command grapple coding
    
    Cybaster's Office    : http://mugenguild.com/cybaster	

    Rajaa's website      : http://justnopoint.com/RajaaBoy/

    Shwa on youtube      : http://youtube.com/user/Shwa

    N-Mario's website    : http://gcnmario.free.fr/

    Cyanide's website    : http://www.mugenguild.com/cyanide/

    RicePigeon's website : http://ricepigeon.webs.com/

    Caddie's website     : http://caddie.smeenet.org/


*** Special thanks to Quetzalcoatl88 for letting me use his Screen Splatter coding

** Mugen Fighters Guild Mugen Newb Walkthrough by P.o.t.S. 
           : http://mugenguild.com/forumx/index.php?topic=99092.0 

** MvC2 sprites from Infinity Mugen Team
           ; http://www.infinitymugenteam.com/

** SF3 Third Strike sprites ripped by Zweifuss
           : http://www.zweifuss.com/

** Capcom vs SNK sounds rpped by Just No Point
           : http://www.drunkduck.com/The_Devon_Legacy_Prologue/ 

*** Sound FX for the sewer lid scrape by the Recordist 
           : http://www.therecordist.com/pages/downloads.html

*** Super Smash Bros Melee Link sound rips from the Spriter Database
           : http://sdb.drshnaps.com/

*** TMNT 3 - Mutant Nightmare DS sound rips by Enscripture:

           : http://www.mediafire.com/?sc3o9wjjucotee8

           : http://membres.multimania.fr/enscripture/

*** MvC1 Slash sparks ripped by KONG:

           http://mugenguild.com/forumx/index.php?topic=118366.msg1156941#msg1156941

*** Special thanks to Seurat, Oldmanwinters, R-iZZy, The Ninjinister
    from the Technodrome Forums for Idea Engineering

           : http://forums.thetechnodrome.com

*** Peter Laird & Kevin Eastman's MIRAGE studios for first developing the 
Teenage Mutant Ninja Turtles and bringing joy to millions of kids 
and adults alike through the franchise




======================
- 6 buttons
- 3 taunts 
- 3 Specials
- 5 EX Special attacks
- 5 Supers 
- 2 Super Cancels
- 2 Hypers

Other Basic Moves
=================
Taunt  -      Start 
Crouch -      Down
Jump -        Up
Super Jump -  Down, Up
Run Forward-  Forward,Forward
Run Back -    Back,Back
Dodge Forward- LP + LK
Dodge Back   - Back, LP + LK



Alternate Launcher ("ROCKET PUNCH")
-(From Standing states On the Ground)
============================
- HP, HP

Guard Push/Advancing Guard
============================
Advancing Guard - Any 2 Punches while blocking


Throws (while next to the opponent)
======
Body Slam Throw       - F + HP 
Screen Splatter Throw - F + HK or B + HK


Crouching Attacks
=================
Down + LP - Crouching Light Punch
Down + MP - Crouching Sai Sweep
Down + HP - Launcher (press up after movehits for the air pursuit)
Down + LK - Crouching Shin Stab
Down + MK - Crouching Medium Kick
Down + HK - Crouching Slide Tackle


--------SPECIAL MOVES----------
+++++++++++++++++++++++++++++++
===============================
-------------------------------
CHESTBUSTER- (On the Ground )
------------------------------
Hold Back, Then Press Forward + Any Kick Button

-------------------------------
HEARTBREAKER- (On the Ground or In The Air)
------------------------------
QCB, + Any Punch Button

-------------------------------
EX HEARTBREAKER Type 1- (On the Ground or In The Air)
------------------------------(-500 power cost)
QCB, LP + MP (Fury Stab)

-------------------------------
EX HEARTBREAKER Type 2- (On the Ground)
------------------------------(-500 power cost)
QCB, MP + HP (Goon Bomber -- Enemy is used as a Projectile to hit Opposing Team)

-------------------------------
THOUSAND STAB - (On the Ground)
------------------------------
QCF + LP (long   range)
QCF + MP (middle range)
QCF + HP (short  range)

-----------------------
EX THOUSAND STAB      -(On the Ground)
------------------------------(-500 power cost)
QCF , any two punches

QCF, LP + MP (Sai Spread)
QCF, MP + HP (Wall Bounce)


-----------------------
JAMBOREE      -(On the Ground)
------------------------------
QCB + LP (Crouch-type)
QCB + MP (Launcher-Type)
QCB + HP (Knockdown-Type)
-----------------------
EX JAMBOREE      -(On the Ground)
------------------------------(-500 power cost)
QCB , any two punches 

QCB, LP + MP (I Got Skill) ; Hold Back to do a Side-Switch
QCB, MP + HP (Back Drop); Hold Back/Down to do a Suplex
QCB, MP + HP (Hold These); Press Punch Buttons for Full 3 Hit melee Combo

-----------------------
EX COUNTER             -(On the Ground)
------------------------------(-500 power cost)
HP + HK or Forward/Back + HP + HK

*note Raph can be hit by any crouching attack, throw, 
or super attack that's coded with the proper hitdef attributes.


-----------------------
EX AGRO-COUNTER             -(In the Air, Once per Combo string)
------------------------------(-500 power cost)
HP + HK or Forward/Back + HP + HK

*note Raph will perform an Offensive Counter attack that flings
the Enemy to the ground for extended Combos.

-------------------------
STAB SHOOT- (In the Air)
-------------------------
QCF + LP (short  range)
QCF + MP (middle range)
QCF + HP (long   range)

----------------------------
EX STAB SHOOT               (In the Air)
----------------------------------(-500 power cost)
QCF , any two punches


-------------------------
SKYSURGE- (In the Air, Hold down the Punch Button if attack Connects to float higher)
-------------------------
QCB + LP (short  range)
QCB + MP (middle range)
QCB + HP (long   range)

*note Can only be performed TWICE during a Combo String
-------------------------
DIVE KICK - (In the Air)
-------------------------
Hold Down & press HK in the air

----------------------------
EX DIVE KICK (In the Air)
----------------------------------(-500 power cost)
QCF , any two kicks


----------SUPER MOVES-------------
++++++++++++++++++++++++++++++++++
==================================
1.)RAMPAGING TURTLE
----------------------------------(-1000 power cost)
QCF, QCF + any Punch Button

2.)POWER DRILL (On the Ground)
----------------------------------(-1000 power cost)
QCF, QCF + any Kick Button

3.)POWER DRILL (In the Air)
----------------------------------(-1000 power cost)
*note: can hit a downed opponent
---------------------------------
QCF, QCF + any Kick Button

4.)OGRE RUSH (On the Ground)
----------------------------------(-1000 power cost)
QCB, QCB + any Kick Button

----------HYPER MOVE-------------
++++++++++++++++++++++++++++++++++
==================================
CRIMSON BLITZ
----------------------------------(-3000 power cost)
QCB, QCB, + Any two punches



-----SUPER CANCELS-----
+++++++++++++++++++++++
=======================
----------------------------------------------------------
1;) RAMPAGING TURTLE > POWER DRILL (On The Ground)
---------------------------------------------------------
Must input 'POWER DRILL (OTG)' command before the leap

----------------------------------------------------------
2;) RAMPAGING TURTLE > POWER DRILL (In the Air)
---------------------------------------------------------
Must input 'POWER DRILL (ITA)' command after the leap


Basic Combos
++++++++++++
============
LP, LP, LP
MP, MP
HP, HP

LK, LK, LK
MK, MK, MK
HK, HK, HK

LP, LP, MK, MK, HK, Down + HK
LP, LP, MK, MK, MK, Down + HK

LP, LP, LP, LK, LK, LK
LP, LP, MK, MK, MK
LP, LP, MK, MK, HK, HK, HK

LP, LP, LP, Down + MP, HP, HP
LP, LP, LP, Down + MP, Down + HP > AIR COMBO

MP, Down + MP, HP, Down + HP
MP, Down + MP, HP, Down + HP > AIR COMBO

Down + MP, Down + MK
Down + MP, MK, MK, HP
Down + MP, MK, MK, Down + HP > AIR COMBO


----------------------
Jump-In (In the air jumping towards the opponent who's on the ground)
===============
--------------------------------
Jump-In (On a smaller Opponents, i.e.: other Turtles)
--------------------------------
LP, MP, HK > Land

LK, MK, HK > Land

MP, MK > Land

MP, MK, HK > Land

HP, HK > Land

LP, MP > Land

MP, HK > Land

--------------------------------
Jump-In (On a Tall Opponent, i.e.: HUGO)
--------------------------------
LP, LK, MK, MP > Land



