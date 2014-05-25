## for now this will be my libtcod tutorial

import libtcodpy as libtcod
import logger
from gobject import Object
from zone import Zone

def handle_keys():
	"""handle input from the main loop"""
	#key = libtcod.console_check_for_keypress()
	key = libtcod.console_wait_for_keypress(True)
	
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt+Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return True  #exit game

	elif key.vk == libtcod.KEY_1 and key.lctrl:
	# cheats/debug
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

def render_all():
	"""render all objects and a map"""
	for gobject in objects:
		gobject.draw()

	for y in range(zone.height):
		
		for x in range(zone.width):
			
			wall = zone[x][y].block_sight
			
			if wall:
				libtcod.console_set_char_background(con, x, y, COLOR_WALL_DARK, libtcod.BKGND_SET)
			else:
				libtcod.console_set_char_background(con, x, y, COLOR_GROUND_DARK, libtcod.BKGND_SET)

	# blit out drawing buffer
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

# init and run the stuff

# constants
LIMIT_FPS = 20

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

#color constants

COLOR_WALL_DARK = libtcod.Color(0, 0, 100)
COLOR_GROUND_DARK = libtcod.Color(50, 50, 150)
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

# init the map
# these should be color constants, then
zone = Zone()
# will be just one room for now
zone.roomer(max_rooms=30)
# init objects in the zone

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', COLOR_PLAYER, con, zone)
# player to any non-blocked tile
player.x, player.y = zone.random_valid_coords()

npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', COLOR_NPC , con, zone)

objects = [npc, player]

# the main loop
while not libtcod.console_is_window_closed():

	render_all()
	libtcod.console_flush()

	# clear all objects
	for gobject in objects:
		gobject.clear()
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break