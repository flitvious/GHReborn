import libtcodpy as libtcod

class Object:
	"""    this is a generic object: the player, a monster, an item, the stairs... it's always represented by a character on screen. """
	def __init__(self, char, color, x, y):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.zone = None

	def set_zone(self, zone):
		self.zone = zone

	def move(self, dx, dy):
		"""move by the given amount"""
		
		# check if blocked
		if not self.zone[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy