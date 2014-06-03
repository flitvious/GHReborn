import libtcodpy as libtcod
import logger
import math

class Object:
	"""
	This is a generic object: the player, a monster, an item, the stairs... 
	it's always represented by a character on screen.
	
	Note: Right now objects belong to zone's list of objects. 
	Eventually there can be special objects, like artifacts or the player 
	that can belong to the "world" or move between the zones.
	"""
	
	# use static properties to init what u need
	#profession = enums.enum('Fighter', 'Mage')

	def __init__(self, char, name, color, blocks=False, fighter=None, ai=None):
		"""
		Initializes a basic object plus snaps on additional optonal components (fighter, ai, etc) if any
		"""
		# use from zone to set these!
		#self.x = x
		#self.y = y

		self.char = char
		self.color = color
		self.zone = None
		self.blocks = blocks
		self.name = name

		# components
		
		# todo - there should be a better constructor that snaps on these components without
		# the need to create them beforehand in code
		# just use enums and rename fighter to class, idk. 

		self.fighter = fighter
		if self.fighter:
			self.fighter.owner = self

		self.ai = ai
		if self.ai:
			logger.log(logger.types.ai, "AI assigned to " + self.name)
			self.ai.owner = self

	def set_zone(self, zone, x, y):
		"""
		Sets object's zone and positions the object at coords.
		DON'T use this directly (unless you want some special object!), call zone's method for adding objects to zone.
		"""
		self.zone = zone
		self.x = x
		self.y = y

	def move(self, dx, dy):
		"""move by the given amount"""
		# check if blocked by wall or object
		if not self.zone.is_blocked(self.x + dx, self.y + dy):
			# not blocked, move there
			self.x += dx
			self.y += dy
			logger.log(logger.types.movement, self.name + " moved to " + str((self.x, self.y)))
		else:
			# zone is blocked, let's try to bump into object!
			obj = self.zone.object_at(self.x + dx, self.y + dy)
			if not obj is None:
				#it is an object
				self.bump(obj)
			else:
				#it is a wall
				logger.log(logger.types.combat, 'The ' + self.name + ' bumps into a wall. Ugh.')
				pass

	def bump(self, obj):
		"""bumps into an object (this is called for objects only)"""
		# this handles collision. 
		# This shound check what type of object we are and handle collision properly (spell-to-actor comes to mind)
		# for now it is a dirty hack for player (who is not-sentient and without ai!) to attact anything sentient and fighter-like!
		if (not self.fighter is None) and (not obj.fighter is None) and (obj.ai is None) and (not obj is self):
			self.fighter.attack(obj)

	def step_towards(self, target_x, target_y):
		"""
		Moves one tile towards target coords
		"""
		#vector from this object to the target, and distance
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		#normalize it to length 1 (preserving direction), then round it and
		#convert to integer so the movement is restricted to the map grid
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
		self.move(dx, dy)

	def distance_to(self, other):
		"""
		Returns distance to another object
		"""
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

### Those below are components that can be snapped on the basic object. Each has its owner object.

class Fighter:
	"""
	Component class for object that can fight.
	Holds combat-related properties and methods (monster, player, npc).
	"""
	def __init__(self, hp, defense, power):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power

	def take_damage(self, damage):
		"""apply damage if possible"""
		if damage > 0:
			self.hp -= damage

	def attack(self, target):
		"""attack another object (must have fighter component)"""
		#a simple formula for attack damage
		damage = self.power - target.fighter.defense
 
		if damage > 0:
			#make the target take some damage
			logger.game(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
			target.fighter.take_damage(damage)
		else:
			logger.game(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

class BasicMonster:
	"""
	Component AI for a basic monster
	"""
	def take_turn(self, player, fov_map):
		"""
		Chase and try to attack. Needs to know where the player is and if she can see the monster.
		"""
		#a basic monster takes its turn. If you can see it, it can see you
		monster = self.owner
		#logger.log(logger.types.ai, monster.name + " takes turn")

		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			#move towards player if far away
			if monster.distance_to(player) >= 2:
				monster.step_towards(player.x, player.y)
			elif player.fighter.hp > 0:
				#close enough, attack! (if the player is still alive.)
				monster.fighter.attack(player)