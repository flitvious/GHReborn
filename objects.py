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
			self.x += dx
			self.y += dy
			logger.log("movement", self.name + " moved to " + str((self.x, self.y)))