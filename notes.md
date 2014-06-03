## Misc stuff / Refactoring

* libtcode zip should be integraed properly (subfolders at least), cheap stuff for now
* Sort out fov_maps. Ae they per-object or single for player only?
* properly implement color constants inside the renderer

## Design

* look at mapobjects in tome

### Objects

Sort out objects, inheritance and components. There clearly should be:

* entity – any item, lever or creture in-game. 
	* Can be added-to map (x, y, coords, blocking). Use map_object thing for that?
	* Can return its kind (actor, item, e.t.c). 
	* Has character and name. Has color. 
	* Can each map hold a list of entities in it? And world later an overall list of entities?
* actor (entity) – entity that can act
	* must have ai addon
	* can have *stats* dict (hp, defense, etc.) these are loaded from premades, i think
	* can take turns (act) - engine goes over every entity in zone and calls its act method (if it is actor, ignore otherwise).
	* can move on itself around the level
	* can deal and receive damage
* item (entity) – thing that can be *used* and *carried around*, but doesn't act on its own.
	* this has to wait until inventory system
	* stacks
	* item that flies around the level? no such thing. Maybe create a projectile class eventually.
* ai component
	* must be called from actor's act

### Refactor

* player is a kind of ai that is handled by player input from main.
* Ai-handling routine. For each object in zone that has ai: if that is controlled by ai=player, take input and act. Something like that. player.take_turn should do that.
* aww, rename take_turn to act. Call act for each entity type based on its kind (for now if it is actor, but there may be sentient items!)
* snapons with entity's .extend method that is overriden in children accordingly.

### Attacking/damage

This works like messaging. Works between two actors.

`self.emit_damage(damage_type, value, destination)`, e.g. send 3 hp damage to orc. This calls receiving actor's `actor.receieve_damage(Damage)`. Which handles the damage accordingly.

Since we are creating mechas, they are living inventories. So `emit_damage` can be targeted or something and `receive_damage` distribute damage to components based on damage types.

Damage class:
types = enum
self.type
self.value
self.source

Emit creates damage entity, receive operates it. This way there can be multiple destinations for damage. Emit to: [orc, troll, everything-in-radius-5-of-tiles-around]

## Some sort of roadmap

These are the features I want first:

* scale 0 prototype — integral PC, monsters, basic items. Not too advanced. Will be used for city hub action later.

* scale 1 prototype — fightable mecha (one simple arena level)
	* Mecha components, mounts and design
	* Mecha operation — game mechanics like weight, speed, e.t.c.
	* Getting and dealing damage (actor-to-actor and mirrored to components)
	* Repairing, customizing mecha (mounts)
	* Custom mecha design
	* Mecha salvage from other mecha (loot)
	* Mecha design files + constructor app(?)

This stuff comes after the combat:
* Random Maps
* Wilderness
* Plots