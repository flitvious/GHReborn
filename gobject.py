import libtcodpy as libtcod

class Object:
	"""    this is a generic object: the player, a monster, an item, the stairs... it's always represented by a character on screen. """
	def __init__(self, x, y, char, color, con, zone):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		# console this object will be rendered to
		self.con = con
		# zone this object belongs to (this should just be an app class reference!)
		self.zone = zone

	def move(self, dx, dy):
		"""move by the given amount"""
		
		# check if blocked
		if not self.zone[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy

	def draw(self):
		"""set the color and then draw the character that represents this object at its position"""
		libtcod.console_set_default_foreground(self.con, self.color)
		libtcod.console_put_char(self.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self):
		"""erase the character that represents this object"""
		libtcod.console_put_char(self.con, self.x, self.y, ' ', libtcod.BKGND_NONE)