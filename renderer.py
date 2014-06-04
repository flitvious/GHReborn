import libtcodpy as libtcod
import logger

#color constants
### these should be zone-specific! And also inside the class :)
COLOR_WALL_DARK = libtcod.Color(0, 0, 100)
COLOR_WALL_LIT = libtcod.Color(130, 110, 50)
COLOR_GROUND_DARK = libtcod.Color(50, 50, 150)
COLOR_GROUND_LIT = libtcod.Color(200, 180, 50)

class Renderer:
	"""Renders graphics"""
	
	def __init__(self, screen_width, screen_height, fps_limit):
		# store values
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.fps_limit = fps_limit

		# turn on fps limit if > 0
		if self.fps_limit > 0:
			logger.log(logger.types.rendering, "FPS limiter set to " + str(self.fps_limit))
			libtcod.sys_set_fps(self.fps_limit)

		# import font
		libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
		# root console / main window / 0
		self.rootcon = libtcod.console_init_root(self.screen_width, self.screen_height, 'Ghreborn', False)	
		# init primary console
		self.con = libtcod.console_new(self.screen_width, self.screen_height)

	def toggle_fullscreen(self):
		"""Toggle fullscreen mode"""
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	def is_closed(self):
		"""Wrapper around libtcod"""
		return libtcod.console_is_window_closed()

	def blit_con(self):
		"""blit out the drawing buffer"""
		libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)

	def flush(self):
		"""Flush everything to screen"""
		libtcod.console_flush()
	
	# Below things are strongly map-related. Should be separated into a Mapper class that calls renderer per-tile or something

	def explore_and_render_zone(self, zone, fov_map):
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

	def show_all(self, zone, entities):
		"""Cheat function: show all the tiles and entities in a zone."""
		# this repeats process_zone and render_objects, fix this somehow
		for y in range(zone.height):
			for x in range(zone.width):
				wall = zone[x][y].block_sight
				if wall:
					libtcod.console_set_char_background(self.con, x, y, COLOR_WALL_DARK, libtcod.BKGND_SET)
				else:
					libtcod.console_set_char_background(self.con, x, y, COLOR_GROUND_DARK, libtcod.BKGND_SET)
		for ent in entities:
			libtcod.console_set_default_foreground(self.con, ent.color)
			libtcod.console_put_char(self.con, ent.x, ent.y, ent.char, libtcod.BKGND_NONE)

	def render_entities(self, entities, fov_map):
		"""Renders all passed entities"""
		for ent in entities:
			if libtcod.map_is_in_fov(fov_map, ent.x, ent.y):
				#render only visible objects
				libtcod.console_set_default_foreground(self.con, ent.color)
				libtcod.console_put_char(self.con, ent.x, ent.y, ent.char, libtcod.BKGND_NONE)

	def clear_entities(self, entities):
		"""Clears all entities"""
		for ent in entities:
			libtcod.console_put_char(self.con, ent.x, ent.y, ' ', libtcod.BKGND_NONE)

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