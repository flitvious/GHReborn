import libtcodpy as libtcod
import logger

class Object:
	"""
	This is a generic object: the player, a monster, an item, the stairs... 
	it's always represented by a character on screen.
	
	Note: Right now objects belong to zone's list of objects. 
	Eventually there can be special objects, like artifacts or the player 
	that can belong to the "world" or move between the zones.
	"""
	def __init__(self, char, name, color, x, y, blocks=False):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.zone = None
		self.blocks = blocks
		self.name = name

	def set_zone(self, zone):
		"""DON'T use this directly (unless you want some special object!), call zone's method for adding objects to zone."""
		self.zone = zone

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
		"""bumps into an object"""
		#since we have only monsters, try to attack it"
		logger.log(logger.types.combat, 'The ' + obj.name + ' laughs at your puny efforts to attack him!')

