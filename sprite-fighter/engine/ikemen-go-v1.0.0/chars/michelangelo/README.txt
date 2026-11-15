MICHELANGELO by Dcat Power. http://www.mugen-infantry.net
                       http://mugenguild.com/



+++++++++++++++++++++

What's here:
UPDATE - 11/21/2019
====================
- Improved Mikey's AI

UPDATE - 4/12/2019
====================
- Changed Inputs for RISING THUNDER Special (Hold Back, then Forward + Any Punch)
- Added AIR MIKEY SUPER While In The Air : ( QCF, QCF + Any Punch In The Air)
- Added BREAKDANCE Special inspired by Injustice 2: (QCB + Any Kick On The Ground)

UPDATE - 12/24/2018
====================
-Changed ALTERNATE LAUNCHER "HEADS UP!" Input From HP > HP to HK > HK
-Added Follow-Up Button Press Combos for All of Mikey's Punch Attacks 
-LIGHT PUNCH COMBO  = LP > LP or Press Back + LP to just do the follow-Up Light Punch Move
-MEDIUM PUNCH COMBO = MP > MP or Press Back + MP to just do the follow-Up Medium Punch Move
-HEAVY PUNCH COMBO  = HP > HP can only perform the follow-up attack if normal standing HP connects

-Added RISING THUNDER Special Inspired by SNES and SEGA Tournament Fighters
  QCF + MP = SEGA Type w/ Side-Switch Properties
  QCF + HP = SNES Type w/ Standard Hit Properties + Greater Damage +  Greater Travel Distance

-Can Now perform CUSTOM THROWS (QCB + Any Punch) While in the Air or During Air Combos
-Added New LIGHT PUNCH CUSTOM AIR THROW (QCB + LP)

-Added EX ELBOW DROP (HP + HK while On the Ground)


UPDATE - 8/2/2018
====================
-Fixed TargetBind Positions for Helper Opponents hit by Throws
-Added AIR COMMAND THROW [Statedef 830] QCB + Any Punch in the Air
-Removed limiter for AIR LAUNCHER [StateDef 660]
-Fixed Height issue with Launched Opponents

UPDATE - 2/2/2013
====================
-Increased Super & Hyper damage against Super Shredder

UPDATE - 11/16/2012
====================
-Added Custom AI by Veanko

UPDATE - 9/10/2012
====================
-Prevented change to crouching state from run (StateDef 100)

UPDATE - 9/6/2012
====================
-Added TMNT 1 ARCADE  APRIL'S APARTMENT Intro vs DcatShredder

UPDATE - 6/17/2012
====================
-Added Dizzy Helper [Statedef 5305] to create Dizzy Stars effect universally
-Added EVENING NEWS Intro against Krang (StateNo 196)
-Recoded "Pizza Time" Intro
-Improved audio for "Not So Fast Homeboy" Intro
-Fixed issue with grappling hook helper improperly reaching its destroyself
-Fixed issue with Standing Heavy Kick (Statedef 250) going to an idle state prematurely
-Fixed Dizzy and Dizzy Stars animations
-Fixed DiagUp/DiagDown animations
-Added animation numbers [8055000-8055999] for Messatsu's Character trait identifiers

UPDATE - 3/20/2011
====================
-Increased volume of voice audio
-Fixed Super KO Finish display details
-Removed command glitch where AIR FOOT UPRISING Super would result from inputting the Dive Kick command immediately after a Super Jump 
-NINJA KNEE SLAPPER (In the Corner) Now works as it was initially intended
-Added PosAdds to EX & Normal KANGAROO KICKS
-Now able to chain EX & Normal KANGAROO KICKS from all standing normals
-Now able to chain EX & Normal KANGAROO KICKS from most crouching attacks
-Now able to chain EX KANGAROO KICKS from normal KANGAROO KICK Front Type 
-Now able to chain EX KANGAROO KICK front type into itself
-Increased damage of all Specials and EX Specials
-Added Guard velocity to Final hit of CHUCK IT OUT Super. Prevents Mikey from grabbing a pushed opponent.
-Made both FOOT UPRISING Supers change to State 890 once complete
-Added more hit velocity to final hit of FOOT UPRISING AIR
-Added block damage to those atacks which were previously lacking
-Added startup frame to Dive Kick

UPDATE - 1/28/2011
===================
-Tweaked Body Slam Throw
-Tweaked Screen Splatter Throw
-Added Voice Audio to Screen Splatter Throw
-Fixed oversight that prevented GRAPPLE HOOK HURRICANE from being chained into by MP

UPDATE - 1/25/2011
===================
-shortened the length of delay between inputs for Mikey's QCB + LP command grapple
-added additional conditions for removal of the delay helper as well.
-Updated the ReadMe

UPDATE - 1/24/2011
===================
-Special Thanks to KojiroBADNESS for fixing the Special Intro glitch
Intros now work in Winmugen as well as Mugen 1.0!! Many thanks to him for fixing that pesky little issue, it was driving me nuts.

-fixed issue with Air Launcher Delay Helper sprouting incorrectly on State 440.
details: search for the line:

   trigger2=numtarget(441)=1&&movehit=1

and changed it to :

   trigger1=numtarget(441)=1&&movehit=1 


UPDATE - 1/23/2011
===================
-Added Winposes
-Added Special Intros with the other Turtles

UPDATE - 1/10/2011
===================
-Made GRAPPLER HOOK HURRICANE force the opponent into standing state 
-limited juggling with EX KANGAROO KICKS
-Increased damage dealt
-Added sliding stop to all turtles for dash-in standing & crouching attacks
-Afterimages on dash and super jump
-Added velocities to air attacks following a launcher pursuit for fewer whiffed chances
-Fixed opponent positions on custom states
-Fixed Posset bug with Turtles appearing beneath the floor

UPDATE - 12/25/2010
===================
-Added custom land state
-Added longer cool down to all Normals and Specials
-Added limiter to Standing LK to prevent infinites
-Added Command Throws
-Added Aerial Launcher Attack
-Added GRAPPLE HOOK HURRICANE Hyper Move
-Combo Tweaking
-Fixed bug with NumHits on both EX KANGAROO KICKs
(each now does the proper 3 hits)

UPDATE - 1/30/2010
===================
-Added Super BG and Super Cancel BG
-Intros with other turtles

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
- 1 taunt
- 3 Specials
- 4 EX Special attacks
- 5 Supers 
- 3 Super Cancels

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

Alternate Launcher ("HEADS UP!")
-(From Standing states On the Ground)
============================
- HK, HK

Knock-Down


Guard Push/Advancing Guard
============================
Advancing Guard - Any 2 Punches while blocking


Throws (while next to the opponent)
======
Body Slam Throw   - F + HP 
Screen Splatter Throw - F + HK or B + HK


Crouching Attacks
=================
Down + LP - Crouching Light Punch (can chain after 2nd hit connects)
Down + MP - Crouching Medium Punch
Down + HP - Launcher (press up after movehits for the air pursuit)
Down + LK - Crouching Light Kick
Down + MK - Crouching Medium Kick
Down + HK - Crouching Slide Tackle


Pineapple Upside Down Kick (GROUND BOUNCER)
-(From Jumping states In the Air)
============================
- Hold UP + Press HK


--------SPECIAL MOVES----------
+++++++++++++++++++++++++++++++
===============================
-------------------------
COMMAND THROWS- (On the Ground or In The Air)
-------------------------
QCB + LP (Cross-Under OTG/ Knee-Gut Smasher In the Air)
QCB + MP (Flying Suplex)
QCB + HP (Spinning PileDriver)

------------------------------------------
RISING THUNDER -(On the Ground)
------------------------------------------
Hold Back, then Forward + LP (Launcher Type)
Hold Back, then Forward + MP (Side-Switch Type)
Hold Back, then Forward + HP (Classic Type)

------------------------------------------
KANGAROO KICK (Horizontal Type)-(On the Ground)
------------------------------------------
QCF + MK

------------------------------------------
KANGAROO KICK (Vertical   Type)-(On the Ground)
------------------------------------------
QCF + HK

------------------------------------------
EX KANGAROO KICK (Horizontal Type)-(On the Ground)
----------------------------------(-500 power cost)
QCF , LK + MK
QCF , LK + HK 

------------------------------------------
EX KANGAROO KICK (Vertical   Type)-(On the Ground)
----------------------------------(-500 power cost)
QCF, MK + HK


------------------------------------------
BREAKDANCE -(On the Ground)
----------------------------------
QCB + LK (short  range)
QCB + MK (middle range)

------------------------------------------
EX BREAKDANCE (Side-Switch Type)-(On the Ground)
----------------------------------(-500 power cost)
QCB, LK + MK (long   range)


------------------------------------------
DYNAMITE BOMBER -(On the Ground)
----------------------------------
QCB + HK
------------------------------------------
EX DYNAMITE BOMBER (Squish Type)-(On the Ground)
----------------------------------(-500 power cost)
QCB, MK + HK

-------------------------
NOSE DIVE- (In the Air)
-------------------------
QCF + LP (short  range)
QCF + MP (middle range)
QCF + HP (long   range)

-------------------------
EX NOSE DIVE- (In the Air)
----------------------------------(-500 power cost)
QCF ,any two punches


------------------------------------------
RIPPLE FIST- (In The Air, multi-Hit for BIG Combos)
------------------------------------------
Back, then Forward + LP
	or
Back, then Forward + MP
	or
      MP, MP


------------------------------------------
SHELLICOPTER- (In The Air, Once per Combo String)
------------------------------------------
QCF + LK
QCF + MK
QCF + HK



-------------------------
EX BUCK-BUCK- (On the Ground)
----------------------------------(-500 power cost)
Forward, HP + HK 
Back, HP + HK 

*note: 
-You can randomly perform a SEWER RETREAT following a BUCK-BUCK attack by Holding DOWN while Mikey hops off 
-This random chance is increased if Mikey has performed an Air Combo with the EX Air Launcher before 
he attempts a "BUCK-BUCK" to end the combo string. 
-------------------------
EX AIR LAUNCHER- (In the Air)

*note: 
-cannot perform during a chain where jumping HP connects  (StateDef 620)
-cannot perform during a chain where crouching HK connects(StateDef 450)
----------------------------------(-500 power cost)
HP + HK 

-------------------------
DIVE KICK - (In the Air)
-------------------------
Hold Down & press HK in the air

-------------------------
EX DIVE KICK - (In the Air)
----------------------------------(-500 power cost)
Hold Down & press any two kicks
QCF ,any two kicks

-------------------------
GNARLY PUNT - (In the Air, Has a Ground Bounce attribute)
-------------------------
Hold Up & press HK in the air


----------SUPER MOVES-------------
++++++++++++++++++++++++++++++++++
==================================
1.)CHECK OUT THESE CHUCKS (On The Ground)
----------------------------------(-1000 power cost)
QCF, QCF + any Punch Button

2.)THE MISSING LINK (On The Ground)
----------------------------------(-1000 power cost)
QCB, QCB + any Punch Button

3.)FOOT UPRISING (On The Ground)
----------------------------------(-1000 power cost)
QCF, QCF + any Kick Button 

4.)FOOT UPRISING (In the Air)
----------------------------------(-1000 power cost)
QCF, QCF + any Kick Button 

5.)AIR MIKEY (In the Air)
----------------------------------(-1000 power cost)
QCF, QCF + any Punch Button 

----------HYPER MOVE-------------
++++++++++++++++++++++++++++++++++
==================================
GRAPPLE HOOK HURRICANE
----------------------------------(-3000 power cost)
QCB, QCF + any Punch Button



-----SUPER CANCELS-----
+++++++++++++++++++++++
=======================

----------------------------------------------------------
1;) CHECK OUT THESE CHUCKS > FOOT UPRISING (On The Ground)
---------------------------------------------------------
Must input 'FOOT UPRISING (OTG)' command before the grab

---------------------------------------------------------
2;) CHECK OUT THESE CHUCKS > FOOT UPRISING (In the Air)
---------------------------------------------------------
Input 'FOOT UPRISING (ITA)' command after the final Kangaroo Kick hit connects

--------------------------------------------------------------
3;) FOOT UPRISING (On The Ground) > FOOT UPRISING (In the Air)
--------------------------------------------------------------


Basic Combos
++++++++++++
============
-LIGHT PUNCH COMBO  = LP > LP or Press Back + LP to just do the follow-Up Light Punch Move
-MEDIUM PUNCH COMBO = MP > MP or Press Back + MP to just do the follow-Up Medium Punch Move
-HEAVY PUNCH COMBO  = HP > HP can only perform the follow-up attack if normal standing HP connects

LP, MP, HP
LP, MP, HP, HP  
LP, LP, MP, MP, HP, HP  

Back + LP, MP, MP, Down + LK, Down + MK, MK, MK	

LK, MK, HK
LK, MK, MK, HK
MK, MK, HK

LP, MP, MK, HP, HP
LP, LP, MK, MK, MK, Down + HK

LP, MK, MK, Down + MK, QCF + MK
LP, MK, MK, Down + MK, QCF + HK

MP, HP, MK, MK, Down + MK, QCF + MK
MP, HP, MK, MK, Down + MK, QCF + HK

LP, MP, MK, Down + MK, QCF + MK
LP, MP, MK, Down + MK, QCF + HK

LP, MP, MK, MK, Down + MK, QCF + MK
LP, MP, MK, MK, Down + MK, QCF + HK


QCB + LP, MK, MK, HK, LK > Land > Down + MP, Down + HP > AIR COMBO




IN THE CORNER
++++++++++++
============
LP, Down + MP, Down + HP > AIR COMBO
Down + LP, Down + MP, Down + HP > AIR COMBO
Down + LK, Down + MK, Down + HK, HP, HP > AIR COMBO

LP, MP, Down + MK, LK, Down + MP, Down + HP > AIR COMBO
MP, HP, LK, Down + MP, Down + HP > AIR COMBO  


INSTANT KANGAROO KICK

conditions: (must be near opponent, not in the corner) 
-----------------------
LP, MP, HP, MK or HK 


conditions: (can be either In or Out of the corner) 
-----------------------
MP, HP, HK, HK
LP, HP, HK, HK




======================================================
                     ADVANCED COMBOS

1.)================================================== 

Dive Kick > Crouching MK > Kangaroo Kick > Nose Dive
          --------------------------
         (Opponent Must be standing)
=====================================================
Dive kick > Land > Down + MK, QCF + MK, QCF + LP
Dive kick > Land > Down + MK, QCF + MK, QCF + MP
Dive kick > Land > Down + MK, QCF + MK, QCF + HP

Dive kick > Land > Down + MK, QCF + HK, QCF + LP
Dive kick > Land > Down + MK, QCF + HK, QCF + MP
Dive kick > Land > Down + MK, QCF + HK, QCF + HP
=================================================
++++++++++++++++++++++++++++++++++++++++++++++++++


2.)=================================================
               Ninja Knee-Slapper
          --------------------------
                 (In the Corner)
====================================================
LP, MP, HP, MK > Land > MP, HP, MK, HK, HK 
=================================================
++++++++++++++++++++++++++++++++++++++++++++++++++


3.)=================================================
                 Fancy Footwork
               -----------------
         (Opponent Must be standing)
=====================================================

MK, MK, HK, LK > Land > QCB + Any Punch

MK, MK, HK, LK > Land > FOOT UPRISING (On The Ground)

CROSS UP > Land, LP, MP, MK, MK, LK > Land > Down + MK, Down + HK, Down + HP > AIR COMBO



4.)=================================================
                  Air Mikey 
          --------------------------
(Extended Air combo Once the Opponent has been hit by a ground launcher)

-500 Power Cost
-cannot perform during a chain where jumping HP connects  (StateDef 620)
-cannot perform during a chain where crouching HK connects(StateDef 450)
====================================================
*note: all commands are following the initial ground launcher pursuit
-------------------------------------------------------------


LP, LK, MK, MP > AIR LAUNCHER > LK, MK, LK, MP, HP > NOSE DIVE 

LK, MK, LK, MK, LP, MP > AIR LAUNCHER > LK, MK, LK, MK, MP, HP > FOOT UPRISING




----------------------
Jump-In (In the air jumping towards the opponent who's on the ground)
===============

LK, HK > Land     (CROSS UP)  

LK, MK, HK > Land (CROSS UP)

Dive Kick > Land  (CROSS UP)



---------------------
AIR COMBO / LAUNCHER SET-UPS
============================

LP, MP, HK, HK > AIR COMBO
LP, MP, Down + MP, Down + HP > AIR COMBO

LP, MP, HP, LK > Land > MK, MK, HK, HK > AIR COMBO
LP, MP, HP, LK > Land > Down + MK, MK, HK, Down + HP > AIR COMBO
LP, MP, MK, MK, LK > Land > Down + MK, Down + HK, Down + HP > AIR COMBO

MP, HK, HK > AIR COMBO
MK, MK, HK, HP > AIR COMBO
MK, MK, Down + MK, Down + MP, Down + HP > AIR COMBO

Down + LP (let both hits connect), Down + MP, Down + HP > AIR COMBO
Down + LP (let both hits connect), MP, HP, LK, Land > Down + MP, Down + HP > AIR COMBO










