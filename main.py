## for now this will be my libtcod tutorial

import libtcodpy as libtcod
import logger
from objects import Object
from zone import Zone
from renderer import Renderer

class Fov:
	"""Fov map wrapper"""	
	def __init__(self, algo, light_walls, light_radius):
		
		self.light_radius = light_radius
		self.light_walls = light_walls
		self.algo = algo
		
		# make an empty fov map for zone
		self.map = None

	#def __getitem__(self):
	#	if self.map is None
	#		logger.error("Fov: map is empty!")
	#	return self.map

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

def handle_keys():
	"""handle input from the main loop"""
	#key = libtcod.console_check_for_keypress()
	key = libtcod.console_wait_for_keypress(True)
	
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt+Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return True  #exit game

	# cheats/debug
	
	elif key.vk == libtcod.KEY_1 and key.lctrl:
		logger.log("teleporting randomly")
		player.x, player.y = zone.random_valid_coords() 

	#player movement
	if libtcod.console_is_key_pressed(libtcod.KEY_UP) or libtcod.console_is_key_pressed(libtcod.KEY_KP8):
		player.move(0, -1)
		logger.log("player moved to " + str((player.x, player.y)))

	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or libtcod.console_is_key_pressed(libtcod.KEY_KP2):
		player.move(0, 1)
		logger.log("player moved to " + str((player.x, player.y)))

	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or libtcod.console_is_key_pressed(libtcod.KEY_KP4):
		player.move(-1, 0)
		logger.log("player moved to " + str((player.x, player.y)))

	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or libtcod.console_is_key_pressed(libtcod.KEY_KP6):
		player.move(1, 0)
		logger.log("player moved to " + str((player.x, player.y)))

	elif libtcod.console_is_key_pressed(libtcod.KEY_KP7):
		player.move(-1, -1)
		logger.log("player moved to " + str((player.x, player.y)))

	elif libtcod.console_is_key_pressed(libtcod.KEY_KP9):
		player.move(1, -1)
		logger.log("player moved to " + str((player.x, player.y)))

	elif libtcod.console_is_key_pressed(libtcod.KEY_KP1):
		player.move(-1, 1)
		logger.log("player moved to " + str((player.x, player.y)))

	elif libtcod.console_is_key_pressed(libtcod.KEY_KP3):
		player.move(1, 1)
		logger.log("player moved to " + str((player.x, player.y)))	

# init and run the stuff

# constants
LIMIT_FPS = 20

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

COLOR_PLAYER = libtcod.white
COLOR_NPC = libtcod.yellow

# turn on fps limit
libtcod.sys_set_fps(LIMIT_FPS)
# import font
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
# root console / main window / 0
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Ghreborn', False)
# primary console
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
# init renderer
renderer = Renderer(con)


# init the map
# these should be color constants, then
zone = Zone()
# will be just one room for now
zone.roomer(max_rooms=30)

# init fov
fov = Fov(algo=0, light_walls=True, light_radius=10)
# load zone information
fov.read_zone(zone)

# init objects in the zone

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', COLOR_PLAYER, zone)
# player to any non-blocked tile
player.x, player.y = zone.random_valid_coords()

npc = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', COLOR_NPC, zone)
# put npc somewhere
npc.x, npc.y = zone.random_valid_coords()

objects = [npc, player]

# the main loop
while not libtcod.console_is_window_closed():
	# recompute fov for player position
	fov.recompute(player.x, player.y)
	# render and explore the zone
	renderer.process_zone(zone, fov.map)
	# render all objects in the zone
	renderer.render_objects(objects, fov.map)
	# blit out drawing buffer
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	# flush the console
	libtcod.console_flush()

	renderer.clear_objects(objects)
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break