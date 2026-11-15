SHREDDER by Dcat Power. http://www.mugen-infantry.net
                        http://mugenguild.com/




\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
===================< RETROMUTAGEN RAY CUSTOM STATE COMPATIBILITY >================================


Custom Animation
  ---------------------------------------
     Shredder uses the following animation numbers for Retro Mutation custom animations.

     19030 - Ground Idling animation
     19032 - Ground crouching animation
     19033 - Ground crouch get up animation (optional)
     19034 - Ground walk forwards animation
     19035 - Ground walk backwards animation
     19036 - Ground jump start animation
     19038 - Ground jump animation
     19039 - Ground jump land animation
     19040 - Ground get hit animation

     19050 - Flying Idling animation
     19052 - Flying crouching animation
     19053 - Flying crouch get up animation (optional)
     19054 - Flying walk forwards animation
     19055 - Flying walk backwards animation
     19056 - Flying jump start animation
     19058 - Flying jump animation
     19059 - Flying jump land animation
     19060 - Flying get hit animation

     Shredder uses the following sound numbers for Retro Mutation custom sounds.

     19030,0 - Get hit sound

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
/////////////////////////////////////////////////////////////////////////////////////////////////

UPDATE - 3/23/2017
====================
-Tweaked Normal Shredder A.I. -- Shredder should now use more Special Attacks and the SHADOW CLONE SUPER

UPDATE - 3/14/2017
====================
-Tweaked RETROMUTATION Anim for Jumping Backwards while RETROMUTATED/CURSED
-Fixed glitch that previously prevented Opponent from mutating back to their Normal state if you kept spamming the jumping Backwards movement while RETROMUTATED/CURSED

UPDATE - 3/12/2017
====================
-Fixed RETROMUTATED Animation so that players no longer go into crouching anim when jumping backwards
(Thanks to Toni from Mugen Fighter's Guild Forums for pointing this out)
-Fixed RETROMUTATION frog states for Battletoads
-Added Streets of Rage Adam, Axel, & Blaze to RETROMUTATION

UPDATE - 3/4/2017
====================
-Prevented April and Splinter lose states from freezing the round
-Added explosion fx to final hit of NINJA FOOT STORM
UPDATE - 5/7/2015
====================
-Removed additional Power cost from several FOOT SOLDIER helpers during the FOOT STORM Air supermove
UPDATE - 5/5/2015
====================
-Added Tylor the Hedgehog's Death Fix .CNS Patch to fix deathpause glitch
-Added Dizzy Stars to non turtle opponents for EX CLAWS Attack

UPDATE - 2/2/2013
====================
-Added Air Super FOOT STORM (QCF, QCF + Any Punch)
-Added Ooze Pollution Winpose
-Added Killing Blow winpose

UPDATE - 1/15/2013
====================
-Prevented SUPER SHREDDER from being killed while in Training Mode
-Decreased the startup walking delay while in SUPER SHREDDER MODE
-Added additional SUPER SHREDDER Winpose inspired by SNES Tournament Fighters
-Prevented SUPER SHREDDER MODE from ending prematurely if Super Shredder wins but has Power <=0
-Added GAUNTLET BLUR SUPER to SUPER SHREDDER MODE (QCF,QCF + Any Punch button / Rapidly Press any Punch Button)
-Re-mapped SUPER SHREDDER's THUNDER WAVE SUPER to (QCF,QCF, Any Kick Button)
-Changed braking animation
-Added alternate command for special Kick techniques (QCF + Any Kick button) 
-Removed ability into chain Aura Crusher from Gauntlet Blur
-Shredder's mid level roundhouse (no knockdown) is once again the default Heavy Kick
-Changed input for High (knockdown) Roundhouse kick to (Back/Forward + HK. Or HK while running)
-Shredder will automatically perform High Roundhouse if the opponent is in the air 
-Updated palettes
-Can now perform Foot Assists by pressing (QCF + Any 2 Kicks) or (QCB + Any 2 Kicks); -500 power cost 
-Added cape effects to all Foot Assists
-Added second attack to Sansetsukon Foot Assist (QCB, LP + MP) 
-Added wall bounce and floor bounce effects to Super Shredder normals
-Sprited new Heavy Kick for Super Shredder

UPDATE - 1/2/2013
====================
-Adjusted alignment for Shredder vs Krang introductions
-Added missing arcade beam pillar effects from intro statedef 193
-Adjusted animation alignments for crouching normals and specials as per RobotMonkeyHead's suggestions
-Added custom Super Shredder Breathing animation by RobotMonkeyHead to Super Shredder's idle animation

UPDATE - 12/23/2012
====================
-Reduced scaling of Foot Soldier sprites
-Added Katana Foot Soldier to Foot Soldier Assists
-Foot Soldier Assists now have varied chains when comboed from/during Shredder's (standing/crouching/air) normal attacks
-Adjusted input timings for Gauntlet Blur (Mash any Punch Button), Foot Soldier Assists (QCF + Any 2 Kicks), Hyper (QCB, QCF + Any Punch / Any Kick)
They should be less restrictive now
-PosSet Armor Helper to Shredder while in Super Shredder mode instead of the opposite. Super Shredder should be less pushable now
-Added Medium Punch, Light Kick attacks to Super Shredder
-Added RemoveExplod sctrls for Super Shredder's Energy Auras to prevent them from remaining if Shredder is dead or outside of Roundstate 2
-Added an Opponent Bind code by SYN & Cybaster for Frozen / Burned / My Toe Custom States. Now these special hit effects should be correctly applied to all enemies regardless of Mugen game mode


UPDATE - 12/19/2012
====================
-Fixed Shredder's normal attack sprite alignments thanks to RobotMonkeyHead's specifications feedback
-Added sound to Super Shredder laugh winpose
-Added effects to Super Shredder Thunder winpose
-Fixed Super Shredder options thanks to YagamiBrando for pointing these errors out:
-Now gain powerbar when Shredder transforms into Super Shredder during his intros
-Powerbar is cleared to 0 at the start of the next round if defeated while in Super Shredder mode
-Super Shredder now only automatically triggers on the final round if you alter config option 2
-Super Shredder intro transformations no longer function improperly during other character intros
-Super Shredder no longer instantly de-transforms if the transformation intro is skipped

UPDATE - 12/15/2012
====================
-Hold Start during Shredder's Laughter Taunt / Winpose to do Maniacal Laughter
-Added FOOT CLAN ASSIST (QCF + Any 2 kicks)
-FOOT CLAN ASSIST Can be performed mid-combo during all ground / air normals
-Added AURA CRUSHER Special (Hold Back then Forward + Any Punch or QCB + Any Punch)
-Added TMNT 1 SPLINTER KIDNAPPEd Intro vs Dcat's Ninja Turtles
-Re-coded Super Shredder's ICE SHOT SPECIAL using Projecile sctrller.
-Fixed bug with MY Toe! sound not playing in Simul Mode

UPDATE - 11/20/2012
====================
-Added THUNDER WAVE SUPER (QCF, QCF + Any Punch) to SUPER SHREDDER Mode
-Added 2OS's Training Mode detection code
-Improved transitional animations from normal attack states
-Sprited new Dizzy animation
-Fixed coding of DiveKick so that Shredder can't infinitely juggle the opponent
-Dive Kick Shuriken now hits air bound opponents more frequently

UPDATE - 11/18/2012
====================
-Added Super Shredder controls to the Readme
-Added Configuration file for Super Shredder mode options
-Made Super Shredder Normal Attacks Into Helper Attacks to prevent HitOverride glitch with opponents
-Added Burned, Frozen, My TOE! Special States

UPDATE - 11/11/2012
====================
-Added SUPER SHREDDER HYPER (QCB , QCF + Any Punch)
-Added combo finishers to certain normal attacks
-Made the special standing kick normals accessible via a one-stop alternate command (MP + MK). 
  note: The different kicks will trigger depending on the hitcount & randomization
-Added Pink energy pillar aura to SHADOW CLONE SUPER

UPDATE - 11/1/2012
====================
-Fixed varset bug with ENERGY CLAW special if a SHURIKEN is active 
-Removed EX GROUND CLAW > DIVE KICK SHURIKEN inifinite loop
-Fixed Recover near Ground & in Mid-Air animations

UPDATE - 10/25/2012
====================
-Added Hyper Portrait
-Fixed Knocked Back, Hit up animations
-Re-sprited Hit Up/Diagonal animations

UPDATE - 10/19/2012
====================
-Updated Readme
-Remapped EX ENERGY WAVE to QCF + Any 2 Punches
-Remapped OTG SHURIKEN projectile to HP + HK 
-Added Basic Combo Tutorial to the Readme
-Added FOOT TECHNIQUE KICKS Tutorial to the Readme
-Fixed FOOT CLAN KICK Command Normals chaining
-Added RETROMUTAGEN RAY COMPATIBILITY INFO to the Readme
-RETROMUTAGEN RAY can now transform both opponents if used in Simul Mode

UPDATE - 10/11/2012
====================
-Fixed Shocked bug with SFII WORLD WARRIOR M.Bison by N64Mario84

UPDATE - 10/10/2012
====================
-Added Compatibility with N-Mario's STreet Fighter 2 World Warrior M.Bison's AIR Winquote System
-Consolidated TMNT I ARCADE : APRIL'S APARTMENT Intro (Statedef 199) into a single state,deleted helper
-Added April O'Neil to the followup intro portion.

UPDATE - 10/5/2012
====================
-Added Far hit properties to Standing Light Kick (Statedef 230)
-Added Standing Reverse Kick (Statedef 260)
-Can now chain Standing Heavy Kick (Statedef 250) into Crouching Sweep Kick (Statedef 450)
-Added RETROMUTAGEN Animation for Mousers / Robots
-Added RETROMUTAGEN Animation for Rat King / Rodents
-Added RETROMUTAGEN Animation for Tokka
-Added RETROMUTAGEN Animation for BattleToads / Amphibians

UPDATE - 10/1/2012
====================
-Coded EX ENERGY WAVE

UPDATE - 9/26/2012
====================
-Remapped SHURIKEN Special to QCB + Any Punch
-Remapped ENERGY WAVE Special to QCF + Any Punch
-Added EX ENERGY WAVE Special : QCF, Same Strength Punch + Kick Button

UPDATE - 9/21/2012
====================
-Changed anim & hit properties for Jumping HK (Knockdown if far, normal stun if performed during a cross-up)
-Prevented chaining from Jumping HK [StateDef 650]
-Added Pos Y restrictions to Jumping Normals to prevent startup whiffs / infinites
-Can no longer chain Dive Kick from Jumping HK
-Added Automatic Shuriken Throw to Dive Kick Special if opponent dist is far.(Does not activate if performed during a cross-up)
-Prevented opponent from being infinitely juggled while in RETROMUATION states
-Fixed AngleDraw scaling for RETROMUTAGEN Animations
-Added RETROMUTAGEN Animation for Sonic the Hedgehog
-Added RETROMUTAGEN Animation for Ninja Turtles / Hero Turtles 
-Added RETROMUTAGEN Animation for Jinmen / Evil Turtles 
-Added RETROMUTAGEN Animation for Rahzar / Dogs 
-Added RETROMUTAGEN Animation for Pterodactyl / Dinosaurs
-Added RETROMUTAGEN Animation for Spiderman / Ananzi/ Viuda Negra
-Added RETROMUTAGEN Animation for Duck King


UPDATE - 9/17/2012
====================
-Added Width Scrtl to Startup of TWIN SHADOW to prevent Shredder from leaping over opponent
-Added additional QCB + Any Punch Button command to GAUNTLET BLUR special
-Remapped SHURIKEN special to QCF , Any 2 Punch Buttons Command
-Remapped ENERGY CLAW special to QCF , Punch + Kick command
-Remapped SILENT STEEL specials & DESPERATION STEEL SUPER to utilize Kick Button Commands
-Turned RETROMUTAGEN RAY into a super attack (-1000 Power Stock to perform)
-Fixed RETROMUTAGEN RAY Super so that it turns players that lack Retromutation Anims into the default Monkey from Shredder's .sff

UPDATE - 9/10/2012
====================
-Reduced the scale of x and y character dimensions  
-Prevented change to crouching state from run (StateDef 100)
-Reduced Shredder's life from 1300 to 1000
-Tweaked damage dampener for specials and supers
-Extended red CLSN for Standing MK & Followup Crouching HP
-Added Enemy Dizzy Anim for characters lacking anim 5300
-Added Enemy Dizzy Stars Helper
-Fixed Dizzy bug with Shin Gouki by Phantom.of.the.Server
-Fixed Dizzy bug with War Machine by One Winged Angel
UPDATE - 9/6/2012
====================
-Added TMNT I ARCADE : APRIL'S APARTMENT Intro vs Donatello, Leonardo, Michelangelo, Raphael 
-Added TMNT IV ARCADE : FINAL BOSS Intro vs Donatello, Leonardo, Michelangelo, Raphael

CREDITS:
========
*** Various sprite rips by BadBatman3, Daisy Of The Wolves, Dazz, Lexou, Code-E, Hioushi, Nitratez, Smithygon, goron0000
    MAneko & Davias, Nightowl35
*** Cenobite53, Cybaster, Iced, psychoripper,Saikoro,Toshio,O Ilusionista,Ruben, RobotMonkeyHead for beta testing 
*** Rukifelith's and MalaDingDong's palettes
*** Jmorphman for his extensive help with implementing optional animation standards
    
    Cybaster's Office    : http://network.mugenguild.com/cybaster

    Cenobite's Mugen     : http://cenobite53.mugengermany.com/index.html

    Shwa on youtube      : http://youtube.com/user/Shwa

    Jmorphman's website  : http://network.mugenguild.com/jmorphman

    Cyanide's website    : http://network.mugenguild.com/cyanide/

    RicePigeon's website : http://ricepigeon.webs.com/

    Caddie's website     : http://caddie.smeenet.org/


*** Special thanks to psychoripper for DVD quality audio rips
*** Special thanks to Enscripture & MaxBeta for extensive ripped resources for the inital Shredder sprites, additional audio resources, your guys's contributions were essential 

*** Special thanks to Enscripture for his numerous TMNT sprite rips also for lending his knowledge old toon via research and screencaptures for reference material 

           :  http://membres.multimania.fr/enscripture/

*** Special thanks to BowserKoopa for ripping audio resources
*** Special thanks to Iced, Saikoro, Rukifelith,for Idea Engineering
*** Special thanks to Saikoro & RobotMonkeyHead for Idea Engineering
*** Special thanks to Oldmanwinters, R-iZZy, The Ninjinister
    from the Technodrome Forums for Idea Engineering
*** Special thanks to mh77 for letting me use his April's Apartment sprites

           : http://forums.thetechnodrome.com

*** Peter Laird & Kevin Eastman's MIRAGE studios for first developing the 
Teenage Mutant Ninja Turtles and bringing joy to millions of kids 
and adults alike through the franchise


What's Here:
======================
- 6 buttons
- 1 taunt
- 3 Specials
- 3 Supers 
- 1 Hyper

Other Basic Moves
-------------------------
Taunt  -      Start 
Crouch -      Down
Jump -        Up (Double Jump)
Super Jump -  Down, Up
Run Forward-  Forward,Forward
Run Back -    Back,Back

Crouching Attacks
-------------------------
Down + LP - Crouching Light Punch
Down + MP - Crouching Medium Punch
Down + HP - Crouching Fierce Punch (press HP again after movehits for the Launcher. Press up after Launcher connects for air pursuit)
Down + LK - Crouching Light Kick
Down + MK - Crouching Medium Kick
Down + HK - Crouching Sweep Kick

Guard Push/Advancing Guard
============================
Advancing Guard - Any 2 Punches while blocking

Throws (Within Throw Distance)
-------------------------
HIKKOKI NAGE (Shoulder Throw) - Any Direction + MP or HP
TSUKI NAGE   (Impaling Throw) - Any Direction + MK or HK


\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////<FOOT TECHNIQUE KICKS -(OTG Command Normal Kicks)>////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

NOTE: 
     -each kick is intended as a single use per combo.
     -depending on combo conditions, some kicks can be accessed automatically via button press.
     


1.) TOE SMASH KICK [Combo extender]
    ----------------------(On the Ground)
    Forward  + LK    alt.command: [ LK > LK ] or [ MK > MK ] or [ LK , Forward + MK ]

(Note: TOE SMASH Alt. commands yield BACK HEEL KICK if TOE SMASH has been used in a combo already)


+++++++++++++++++++++++
2.) BACK HEEL KICK [Combo Finisher]
    ----------------------------------------(On the Ground) 
    (QCF + MK) or (Backward + MK)   alt.command if TOE SMASH not performed: [ MK > MK > MK ]
                     alt.command if TOE SMASH was performed: [ Forward + MK ] or [ MK > MK ]
                     
                     (randomized) alt.command if Combo Counter is mid-high value: [ MP + MK ] 

+++++++++++++++++++++++
3.) FRONT BOOT KICK [Mae Geri]
    ----------------------------------------(On the Ground) 
    (QCF + HK) or (LK > LK > LK)     alt.command if TOE SMASH was performed: [ LK ]
                     
                     (randomized) alt.command if Combo Counter is mid-high value: [ MP + MK ]

+++++++++++++++++++++++
4.) SIDE THRUST KICK [Yoko Geri]
    ----------------------(On the Ground)
    Press Medium Kick While running forward (has Wall bounce properties)
                     
                     alt.command if Combo Counter is zero-low value: [ MP + MK ]


+++++++++++++++++++++++
5.) DOUBLE ROUNDHOUSE [Mawashi Geri Baizo]
    ----------------------(On the Ground)
     If close by a standing opponent press HK>HK,  Shredder will do a high/low roundhouse combo

    
+++++++++++++++++++++++
6.) SINGLE ROUNDHOUSE 
    ----------------------(On the Ground) 
    Forward + HK or Backward + HK, Shredder will do a high Roundhouse that knocks the enemy into the air 


==================================================================================



Follow-Up Attacks / Extra Strikes
--------------------------------
(Press buttons in succession for additional hit)


(In the Air) LP > LP      
(In the Air) MP > MP      
(In the Air) Hold Down + LK > LK or Hold Forward + LK > LK
(In the Air) Hold Down + HP
(In the Air) Hold Forward + HK



--------SPECIAL MOVES----------
+++++++++++++++++++++++++++++++
===============================
----------------------------------------
1. GAUNTLET BLUR - (On the Ground)
----------------------------------------
Rapidly press Any Punch button


----------------------------------------
2. AURA CRUSHER - (On the Ground)
----------------------------------------
Hold Back then press Forward + Any Punch button or QCB + Any Punch button


----------------------------------------
3. ENERGY CLAW / ENERGY WAVE - (On the Ground)
----------------------------------------
QCF , LP  (Ground Wave)
QCF , MP  (Medium Wave)
QCF , HP  (Anti-Air Wave)

----------------------------------------
4. EX ENERGY CLAW / ENERGY WAVE - (On the Ground)
----------------------------------(-500 power cost)
QCF , LP + MP (EX Ground Wave)
QCF , MP + HP (EX Medium Wave)
QCF , LP + HP (EX Anti-Air Wave)


----------------------------------------
5. SHURIKEN - (On the Ground)
----------------------------------(-500 power cost)
HP + HK

----------------------------------------
6. TSUKI NAGE - (On the Ground)
----------------------------------------
QCB + LK (Front type)
QCB + MK (Side-Switch type)
QCB + HK (Air type)


----------------------------------------
7. FOOT CLAN SUMMON - (On the Ground or In the Air) 
----------------------------------(-500 power cost)
QCF , Any 2 Kicks   SPECIAL NOTE: 
QCB , Any 2 Kicks   Can be performed mid-combo during all ground / air normals


----------------------------------------
8. DIVE KICK - (In the Air)

(Has an Additional SHURIKEN TOSS effect depending on EnemyDistance)
----------------------------------------

Hold Down & press HK in the air

or QCF + HK while in the air


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////------------< SUPER MOVES >-------------//////////////////////////////////
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1.) RETROMUTAGEN RAY  - (On the Ground)
----------------------------------(-1000 power cost)
QCF, QCF + any Punch Button 

2.) SHADOW cLONE [KAGE BUNSHIN] - (On the Ground)
----------------------------------(-1000 power cost)
QCF, QCF + any Kick Button

3.) VORPAL CUTTER  - (On the Ground)
----------------------------------(-1000 power cost)
QCB, QCB + any Kick Button 

4.) NINJA FOOT STORM  - (In the Air)
----------------------------------(-1000 power cost)
QCF, QCF + any Punch Button 


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////------------< HYPER MOVE >-------------//////////////////////////////////
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1.) SUPER SHREDDER  - (On the Ground)
----------------------------------(-3000 power cost)
QCB, QCF + any Punch Button 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////<SUPER SHREDDER MODE CONTROLS -(OTG HYPER MODE)>////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
RULES/ STIPULATIONS:

(DRAWBACKS / CONS - )
As Super Shredder you cannot run, backdash, jump crouch or block.
Depending on the settings in the config.st file, Super Shredder's powerbar will gradually depelete.
Once the powerbar reaches 0 Super shredder will transform back into his normal character states.
Ending the transformation takes a toll on Shredder and he will be stunned if the timer runs out before the round ends.

(BENEFITS / PROS + )
Super Shredder cannot be pushed, knocked down, thrown, or put into custom states by the opponent.
Super Shredder mode has additional normal and special moves unavailable in normal mode.
Super Shredder mode has super armor; all damage Shredder takes while transformed is halved.

--------NORMAL MOVES----------
+++++++++++++++++++++++++++++++
===============================
----------------------------------------
1. HEAVY CHOP - (On the Ground)
----------------------------------------
LP       (Vertical Karate Chop)
MP       (Downward Thrust Punch)
HP       (Horizontal Karate Chop)
----------------------------------------
2. SIDE KICK - (On the Ground)
----------------------------------------
LK       (Forward Knee Thrust)
MK       (Horizontal Side Kick)

--------SPECIAL MOVES----------
+++++++++++++++++++++++++++++++
===============================
----------------------------------------
1. AURA ATTACKS - (On the Ground)
----------------------------------------
QCF , LP  (Ground Flame Wave)
QCF , MP  (Medium Retro Blast)
QCF , HP  (Anti-Air Ice Wave)

----------------------------------------
2. LEVITATION - (On the Ground)
----------------------------------(-100 power cost)
LP + LK (Forward or Back movement, Super Shredder is temporarily invulnerbale to attacks)

----------------------------------------
3. LIGHTNING PRESSURE - (On the Ground)
----------------------------------------
HP + HK (Breaks Enemy Combo)

or Start



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////------------< SUPER MOVES >-------------//////////////////////////////////
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
1.) GAUNTLET BLUR  - (On the Ground)
----------------------------------
QCF, QCF + Any Punch Button or Rapidly press Any Punch button

2.) THUNDER WAVE  - (On the Ground)
----------------------------------
QCF, QCF + Any Kick Button 


;//////////////////////////////////////////////////////////////////////////////////////////////////
------------
Basic Combos
++++++++++++
============

(Any Distance) LK, MK, HK, Down + HK
(Any Distance) MK, MK, MK

(In the Corner) Down + LP, Down + MP, HP, MK, MK

(Close Distance) LP, LP, LP, LP
(Close Distance) LP, LP, MP, HP, HK

(Close Distance) LP, LK, MK
(Close Distance) LP, LK, MK, Down + LP, Down + MP, HP

(Close Distance) LP, LK, Down + LP, Down + MP, HP, HK
(Close Distance) LP, MP, Down + LP, Down + MP, HP, HK

(Mid-Range/ Far Distance) MP, HP
(Mid-Range/ Far Distance) HP, MP, HP
(Mid-Range/ Far Distance) LP, MP, HP
(Mid-Range/ Far Distance) LP, MP, HP > TSUKI NAGE


Down + LP, Down + MP, HP 
Down + LP, Down + MP, HP > GAUNTLET BLUR
Down + LP, Down + MP, HP > TSUKI NAGE

Down + LP, Down + LK, Down + MK, Down + MP 
Down + LP, Down + MP, Down + LK, Down + MK 
Down + LP, Down + MP, Down + HP, Down + HK 
Down + LP, Down + MP, LK, MK, MP, HP

Down + LP, Down + LP, Down + LK, Down + MK, Down + HK
Down + LP, Down + LK, Down + MK, Down + HK

-------------------
Ground > Air Combos
+++++++++++++++++++
===================
Down + LP, Down + LP, Down + MP, Down + HP, Down + HP > AIR COMBO

LP, MP, Down + MP, Down + HP, Down + HP > AIR COMBO



