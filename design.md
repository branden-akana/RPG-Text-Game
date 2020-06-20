A text-based RPG.

Gameplay
--------

The game will be designed to be turn-based and take place in a system made up of
rooms.

- On the player's turn, they can perform an action. There will be two different
  types of actions: "quick actions" triggered by pressing the key assigned to
  that action, and "command actions" triggered by pressing a command entry
  button (:) and typing a command.

- On an NPC's (or enemy's) turn, they can think() in order to decide what action
  to do, and afterwards will trigger that action.

Turn Order
----------

When around other NPCs, a turn order will be decided. On an NPC's turn, they
will decide what action to do, and on the player's turn, a list of avaliable
actions will be displayed before prompting the player for input.

Logic Loop
-----------

On enter new room: init turn order

For NPC turn => run think() to decide action then do action (takes 1 game tick)
For player turn => change gamestate to "input", process player input while in
this state, do decided action, then change gamestate to "running"

Body Part System
----------------

All creatures have a body made up of a set of body parts.  Internally this
is defined as a list of part names, each with references to what other body
parts they are connected to.

A body part has different flags that define how it can be used and how it
behaves.

`status: str`: the state of the part,
	- `'healthy'`: the body part is functioning normally.
	- `'missing'`: the body part is no longer attached to the rest of the body.
The body part cannot be targeted if it is missing.
	- `'burnt'`
	- `'poisoned'`
	- `'mangled'`: the body part is attached but no longer functions.
`weight`: the weight to use in probability checks (not actual weight).
These weights are used to determine a targeted body part when an enemy attacks
blindly.
`is_vital`: if true, damaging/removing this part will kill the entity
instantly.
`can_hold_item`: if true, is able to hold items i.e. hands
`can_attack_unarmed`: if true, is able to attack unarmed i.e. hands and feet
`can_attack_armed`: if true, is able to attack armed i.e. hands

Creature Stats
--------------

All creatures have a set of stats which can be used when processing certain
actions. In general, `0` indicates no skill in that stat, `10` indicates average
skill, and `20` indicates professional skill.

NOTE: right now there is no upper limit for a stat.

For now the list of stats are similar to DnD.

- `STR`: strength - used to determine power when attacking
- `DEX`: dexterity - used to determine profeciency with weapons and the result
  of certain actions such as dodging or jumping
- `CON`: constituition - used to determine effect of getting hit
- `INT`: intelligence - used to determine result of reading or examining
  objects, and also effeciency when talking to NPCs
- `WIS`: wisdom - used to determine general awareness of the sitation, to
  determine results of looking around (or whether to try to look around)
- `CHR`: charisma - used to determine effect when talking to NPCs, possibly to
  persuade, barter, etc.

Stat Checks
-----------

Some actions may require checks against one or more stats. These actions will
provide a "difficulty" for each checked stat to determine the stats needed to
successfully perform the action.

#### Check Algorithm ####

When a check is needed for an action (`difficulty` is set by the action):

(?) The base value of the stat is added to two D6 rolls.

`(base stat) + (2D6) = (total stat)`

For example, if the action is to jump a small gap with the difficulty being
`{DEX: 5}`, and the player's base DEX stat is `2`, and the result of two D6
rolls are a `4` and `3`, then the `total stat` is:

`2 + 4 + 3 = 9`

and since `9 >= 5`, the player passes the check.

(?) Catastrophic Failure: if a player rolls snake eyes
(double 1s => a 1/36 chance of 2.778%), then the `total stat` will be half the
base stat.

#### Check Results ####

The result are a set of _success rates_ (percentages) which can be used to
determine how successful the check was.

If a result is needed to check if an action passes/fails, then check if
`(success rate) >= 1.0`.

If a result is needed to check the effectiveness of an action, then use the
success rate on its own. (`1.0 => 100% effectiveness, 2.0 => 200%
effectiveness`)


Items
-----

Items are a type of entity and represent any object that can be picked up, held,
wielded, worn, etc.

All items carry this metadata:

`name`: the actual name of the item i.e `Gold Coin`
`description`: the description of this item (what does this item look like?)
i.e. `A flat, round object made of gold`
`explanation`: an explanation of this item (what is the purpose of this item?)
i.e. `Used as currency`
`value`: the price value per item i.e. `1 Gold (or whichever
currency system is being used)`

examine stats:

`describe_req`: the INT required to describe this object
`explain_req`: the INT required to explain this object

damage-related stats:

`phys_damage`: the damage that this item can deal if wielded
`proj_damage`: the damage that this item can deal if thrown/shot

`is_blunt`: if true, this item can deal `blunt force` damage
`is_sharp`: if true, this item can `cut` or `slice`
`is_pointed`: if true, this item can `stab`

Action: Examining
-----------------

[`examine`, `ex`, `x`]

Requirements: `INT`

Attempt to examine something.

Examining an entity will show the description and explanation of it if `INT >=
item.explain_req`.
Examining an entity will show only the description if `INT >= item.describe_req`.
Examining an entity will show `"You fail to identify what this object is"` if
`INT < item.describe_req`.

- `examine <object>`: try to examine this object

Action: Looking
---------------

[`look`, `l`]

Requirements: `INT`

Attempt to look around the room. Can be affected by lighting conditions and/or
visibility of entities.

Action: Attacking
-----------------

[`attack`, `k`]

Requirements: `STR`, `DEX`, `CON`

Attack an entity physically i.e. swinging a sword or punching

`STR` and `DEX` are checked (when attacking) to determine the damage output and
accuracy.
`DEX` is checked (when being attacked) to determine if the attack can be dodged.
`CON` is checked (when getting hit) to determine the damage taken.

- `attack blindly... <ent?>`: will attack an enemy at a random part (easy roll)
- `attack precisely... <ent?>... <part?>`: will attack an enemy at a specific
  part (harder roll, but easier to hit a specific part)

Inanimate objects (like items) can be attacked with mixed results.

Action: Throw
-------------

[`throw`, `shoot`]

Requirements: `DEX`

Throw or shoot something. Counts as a ranged attack.

`STR` and `DEX` are checked (when attacking) to determine the damage output and
accuracy.
`DEX` is checked (when being attacked) to determine if the attack can be dodged.
`CON` is checked (when getting hit) to determine the damage taken.

- `throw... <item?>... <ent?>`: will throw or shoot an object at an entity.

NOTE: `shooting` an object that is a tool to shoot ammo will instead shoot the
ammo.

Action: Open
------------

[`open`]

Requirements: `STR`, `INT`, `WIS`

Open something, like a door, chest, etc.

`INT` is checked to identify that the object can be opened.
(on fail, assume it can)
`WIS` is checked to identify if the object should be opened. (if rigged etc.)
(on fail, open it anyway)
If locked, `INT` is checked to see if it can be picked.
(otherwise, try `attacking` the object instead)
`STR` is checked to open the object. (might be high for heavy objects like stone
doors etc.)

(?) Creatures can be "opened" with mixed results.

Action: Jump
------------

[`jump`, `leap`, `cross`]

Requirements: `INT`, `DEX`

Jump a gap or similar obstacle. Also extends to navigating traps, etc.

`DEX` is checked to determine success of navigating the obstacle.

Action: Scream
--------------

[`scream`, `yell`, `scare`]

Requirements: `CHR`

Scream.

Screaming will make anything living notice you.
`CHR` is checked to determine if it will also scare them.



