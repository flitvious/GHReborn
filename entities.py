import libtcodpy as libtcod
import logger
import math
import enums
from keyhandler import KeyHandler as k

class Entity:
	"""
	This is a generic game entity that can be assigned to map.
	It can't act on its own.
	Actors inherit from it (and items, projectiles will)
	"""
	
	types = enums.enum('Entity', 'Actor')

	def __init__(self, char, name, color, blocks):
		
		self.char = char
		self.color = color
		self.name = name

		# map-specific stuff
		# these are none, added when zone sets them
		self.x = None
		self.y = None
		self.zone = None
		# whether it blocks passage or not
		self.blocks = blocks
		
	def get_type(self):
		"""
		Returns own type of entity in Entity.types.*
		Each child redefines this.
		"""
		#raise NotImplementedError("Subclass must implement abstract method")
		return Entity.types.Entity

	def set_zone(self, zone, x, y):
		"""
		Sets entity's zone and positions the object at given coords.
		"""
		self.zone = zone
		self.x = x
		self.y = y

class Actor(Entity):
	"""
	An entity that can act, take turns and have stats dict.
	act() is called by engine each turn
	ai component must be passed as a constant: entities.AI.ais.basic_monster

	* ai - ai to use
	* design - design to use (hardcoded for now, later can be loaded)
	* stats['hp'] - stats are a dict
	"""
	
	designs = enums.enum('orc', 'troll', 'player')
	
	def __init__(self, char, name, color, blocks, 
		ai, design):

		# call Entity's constructor class to setup the child
		Entity.__init__(self, char, name, color, blocks)

		# setup ai (it is a component, so will need an owner)
		if ai == AI.ais.player_control:
			# this ai just asks player for input
			self.ai = PlayerControl(owner=self)
			logger.log(logger.types.ai, "player_control ai assigned to " + self.name)
		
		elif ai == AI.ais.basic_monster:
			self.ai = BasicMonster(owner=self)
			logger.log(logger.types.ai, "basic_monster ai assigned to " + self.name)
		
		else:
			logger.error("Can't pick an ai for an actor")
		
		# setup stats based on design, hardcoded (later take from data files)
		if design == Actor.designs.player:
			self.stats = dict(max_hp=30, hp=30, defense=2, power=5)
		elif design == Actor.designs.orc:
			self.stats = dict(max_hp=10, hp=10, defense=2, power=5)
		elif design == Actor.designs.troll:
			self.stats = dict(max_hp=16, hp=16, defense=1, power=4)
		else:
			logger.error("Can't pick design for an actor")

	def get_type(self):
		"""	
		Returns own type of entity in Entity.types.*. 
		For now is used by main to call actor's act().
		"""
		return Entity.types.Actor

	def act(self, act_data):
		"""
		This method is called each turn for all actors in the map.
		For now it only gets ai to work based on its type.
		
		act_data - dict containing all the stuff
		"""
		
		# for now we only need to call an ai properly
		ai_type = self.ai.get_type()

		if ai_type == AI.ais.player_control:
			# no inbound params for player
			result = self.ai.work(player_action=act_data['player_action'])
		
		elif ai_type == AI.ais.basic_monster:
			# we need to feed player and fov_map to it
			result = self.ai.work(player=act_data['player'], fov_map=act_data['fov_map'])
		
		else:
			logger.error('Unknown ai type')
			# skip its turn just in case
			result = True

		# true if turn was made, false if not
		return result

	def move(self, dx, dy):
		"""move by the given amount"""
		# check if blocked by wall or entity
		if not self.zone.is_blocked(self.x + dx, self.y + dy):
			# not blocked, move there
			self.x += dx
			self.y += dy
			logger.log(logger.types.movement, self.name + " moved to " + str((self.x, self.y)))
		else:
			# tile is blocked, let's try to bump into object!
			entity = self.zone.entity_at(self.x + dx, self.y + dy)
			if not entity is None:
				#it is an entity
				self.bump(entity)
			else:
				#it is a wall
				logger.log(logger.types.movement, 'The ' + self.name + ' bumps into a wall. Ugh.')
				pass

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
		"""	Returns distance to another object """
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

	def bump(self, ent):
		"""bumps into an entity (this gets called for entities only, not for walls)"""
		# this should check for factions )
		# FIXME: attacking should be handled inside player! here only spontaneous collisions!
		# works only for actors.
		if (ent.get_type == Entity.types.Actor):
			# if player, attack any monster
			if (self.ai.get_type() == AI.ais.player_control) and (ent.ai.get_type == AI.ais.basic_monster):
				self.attack(ent)

	def take_damage(self, damage):
		"""apply damage if possible"""
		if damage > 0:
			self.stats['hp'] -= damage
			logger.log(logger.types.combat, self.name + ' now has ' + str(self.stats['hp']) + ' hp of ' + str(self.stats['max_hp']))

	def attack(self, target):
		"""
		attack another actor
		convert to send_damage eventually
		"""
		#a simple formula for attack damage
		damage = self.stats['power'] - target.stats['defense']
 
		if damage > 0:
			#make the target take some damage
			logger.game(self.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
			target.take_damage(damage)
		else:
			logger.game(self.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

#### AIs #####

class AI:
	"""
	Base class for all AIs.
	AI is a component and so must have owner.
	"""
	
	ais = enums.enum('base', 'player_control', 'basic_monster')

	def __init__(self, owner):
		self.owner = owner

	def get_type(self):
		""" 
		Returns the type of ai
		Used by Actor's act() to supply proper arguments
		children should redefine this
		"""
		return AI.ais.base

	def work(self):
		"""
		Returns True if this Actor's turn is made.
		children should redefine this
		"""
		raise NotImplementedError("Subclass must implement abstract method")

class BasicMonster(AI):
	"""
	Component AI for a basic monster
	"""
	def get_type(self):
		"""returns type of ai"""
		return AI.ais.basic_monster

	def work(self, player, fov_map):
		"""
		Chase and try to attack. Needs to know where the player is and if she can see the monster.
		"""
		#If you can see it, it can see you
		monster = self.owner

		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			#move towards player if far away
			if monster.distance_to(player) >= 2:
				monster.step_towards(player.x, player.y)
			elif player.stats['hp'] > 0:
				#close enough, attack! (if the player is still alive.)
				monster.attack(player)
		# did make a turn, okay!
		return True

class PlayerControl(AI):
	"""
	Controlled by a human player
	"""
	def get_type(self):
		"""returns type of ai"""
		return AI.ais.player_control

	def work(self, player_action):
		"""
		Make a turn based on player's action. Make no turn (return false) if passed action is not a game one. 
		(or cancelled a skill) (or instant skill)
		"""
		
		if player_action == k.controls.none:
			# this can't happen, because we use wait_key. But just in case!
			logger.error('Got no action as player!')
			return True

		elif player_action == k.controls.other:
			# just pressed some stupid key
			return False

		elif player_action == k.game.move_N:
			self.owner.move(0, -1)
			return True

		elif player_action == k.game.move_NE:
			self.owner.move(1, -1)
			return True

		elif player_action == k.game.move_E:
			self.owner.move(1, 0)
			return True

		elif player_action == k.game.move_SE:
			self.owner.move(1, 1)
			return True

		elif player_action == k.game.move_S:
			self.owner.move(0, 1)
			return True

		elif player_action == k.game.move_SW:
			self.owner.move(-1, 1)
			return True

		elif player_action == k.game.move_W:
			self.owner.move(-1, 0)
			return True

		elif player_action == k.game.move_NW:
			self.owner.move(-1, -1)
			return True

		elif player_action == k.game.move_5:
			self.owner.move(0, 0)
			return True

		else:
			# this can't happen, but just in case!
			logger.error('Got no action as player!')
			return True