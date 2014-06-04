## Misc stuff / Refactoring

* libtcode zip should be integraed properly (subfolders at least), cheap stuff for now
* Sort out fov_maps. Ae they per-object or single for player only?
* properly implement color constants inside the renderer
* todo - incapsulate all the damn properties and access through methods. Even `zone[x][y]` stuff. Incapsulate stats.
* fix cheats.. aaaaw, to hell with this :)
* step towards energy - per-entity rendering
* remove map-related stuff from renderer and create mapper
* move player-related bump functionality to player ai
* error handling - use raise everywhere
* distance calculation is shit, fix it with nice pathfinding algorithms.

## Design

### Extending

Extension modules may be passed as **kwargs as many as needed

### Objects

Sort out objects, inheritance and components. There clearly should be:

* entity – any item, lever or creture in-game. 
* actor (entity) – entity that can act
	* can have *stats* dict (hp, defense, etc.) these are loaded from premades, i think
* item (entity) – thing that can be *used* and *carried around*, but doesn't act on its own.
	* this has to wait until inventory system
	* stacks
	* item that flies around the level? no such thing. Maybe create a projectile class eventually.

* ai component
	* must be called from actor's act

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