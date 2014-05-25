import libtcodpy as libtcod

class Object:
	"""    this is a generic object: the player, a monster, an item, the stairs... it's always represented by a character on screen. """
	def __init__(self, x, y, char, color, zone):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		# zone this object belongs to (this should just be an app class reference!)
		self.zone = zone

	def move(self, dx, dy):
		"""move by the given amount"""
		
		# check if blocked
		if not self.zone[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy

	def draw(self, con, fov_map):
		"""set the color and then draw the character that represents this object at its position"""
		# ahhh, move this out.... this is a part of the rendering, not game logic.
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self, con):
		"""erase the character that represents this object"""
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)