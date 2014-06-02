## Things to consider

* libtcode zip should be integraed properly (subfolders at least), cheap stuff for now

* Sort out fov_maps. Ae they per-object or single for player only?
* Refactor roomer code, it takes shitty things like player and fov.
* move screen width and height inside the renderer (and all other stuff)
* player component for object
* fixme: fighters kill fighters by bumping into them! player kills himself by standing in place. Shit, this is just too hilarious!

## Some sort of roadmap

These are the features I want first:

* Fightable mecha (one simple arena level)
	* Weapons, damage types, armor
	* Mecha design files + constructor(?)
	* Mecha components
	* Mecha salvage from other mecha

This stuff comes after the combat:
* Random Maps
* Wilderness
* Plots