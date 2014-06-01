import libtcodpy as libtcod

#color constants


### these should be zone-specific!
COLOR_WALL_DARK = libtcod.Color(0, 0, 100)
COLOR_WALL_LIT = libtcod.Color(130, 110, 50)
COLOR_GROUND_DARK = libtcod.Color(50, 50, 150)
COLOR_GROUND_LIT = libtcod.Color(200, 180, 50)

class Renderer:
	"""Renders to console"""
	
	def __init__(self, con):
		# console to render into
		self.con = con
		pass

	def process_zone(self, zone, fov_map):
		"""Renders lit and unlit zone tiles and explores them"""	
		# renderer exploring = bad, fix this 
		for y in range(zone.height):
			for x in range(zone.width):
				
				lit = libtcod.map_is_in_fov(fov_map, x, y)
				wall = zone[x][y].block_sight
				
				if not lit:
					#it's out of the player's FOV
					#if it's not visible right now, the player can only see it if it's explored
					if zone[x][y].explored:
						if wall:
							libtcod.console_set_char_background(self.con, x, y, COLOR_WALL_DARK, libtcod.BKGND_SET)
						else:
							libtcod.console_set_char_background(self.con, x, y, COLOR_GROUND_DARK, libtcod.BKGND_SET)
				else:
					#it is inside the player's fov
					if wall:
						libtcod.console_set_char_background(self.con, x, y, COLOR_WALL_LIT, libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(self.con, x, y, COLOR_GROUND_LIT, libtcod.BKGND_SET)
					# explore the tile
					if not zone[x][y].explored:
						zone[x][y].explored = True

	def show_all(self, zone, objects):
		"""Show all the tiles in a zone."""
		# this repeats process_zone and render_objects, fix this somehow
		for y in range(zone.height):
			for x in range(zone.width):
				wall = zone[x][y].block_sight
				if wall:
					libtcod.console_set_char_background(self.con, x, y, COLOR_WALL_LIT, libtcod.BKGND_SET)
				else:
					libtcod.console_set_char_background(self.con, x, y, COLOR_GROUND_LIT, libtcod.BKGND_SET)
		for obj in objects:
			libtcod.console_set_default_foreground(self.con, obj.color)
			libtcod.console_put_char(self.con, obj.x, obj.y, obj.char, libtcod.BKGND_NONE)

	def render_objects(self, objects, fov_map):
		"""Renders all objects"""
		for obj in objects:
			if libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
				#render only visible objects
				libtcod.console_set_default_foreground(self.con, obj.color)
				libtcod.console_put_char(self.con, obj.x, obj.y, obj.char, libtcod.BKGND_NONE)

	def clear_objects(self, objects):
		"""Clears all objects"""
		for obj in objects:
			libtcod.console_put_char(self.con, obj.x, obj.y, ' ', libtcod.BKGND_NONE)

class Fov:
	"""Fov map wrapper"""	
	def __init__(self, algo, light_walls, light_radius):
		
		self.light_radius = light_radius
		self.light_walls = light_walls
		self.algo = algo
		
		# make an empty fov map for zone
		self.map = None

	def read_zone(self, zone):
		"""Read the zone and adjust map values accordingly"""
		self.map = libtcod.map_new(zone.width, zone.height)
		for y in range(zone.height):
			for x in range(zone.width):
				#libtcode requires the opposite values, so invert them!
				libtcod.map_set_properties(self.map, x, y, not zone[x][y].block_sight, not zone[x][y].blocked)

	def recompute(self, x, y):
		"""Compute fov for position"""
		libtcod.map_compute_fov(self.map, x, y, self.light_radius, self.light_walls, self.algo)