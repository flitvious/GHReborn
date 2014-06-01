## for now this will be my libtcod tutorial

import libtcodpy as libtcod
import logger
from objects import Object
from zone import Zone
from renderer import Renderer, Fov

class Application:
	"""GHreborn main application"""	

	def __init__(self, fps_limit=20, screen_width=80, screen_height=50):
		# constants
		self.LIMIT_FPS = fps_limit
		self.SCREEN_WIDTH = screen_width
		self.SCREEN_HEIGHT = screen_height

		# turn on fps limit if > 0
		if self.LIMIT_FPS > 0:
			libtcod.sys_set_fps(self.LIMIT_FPS)
		
		# import font
		libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
		# root console / main window / 0
		libtcod.console_init_root(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 'Ghreborn', False)
		
		# init primary console
		self.con = libtcod.console_new(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
		# init renderer
		self.renderer = Renderer(self.con)
		# init the map
		self.zone = Zone()
		# populate zone with roomer algorithm
		self.zone.roomer(max_rooms=30)
		# init fov
		self.fov = Fov(algo=0, light_walls=True, light_radius=10)
		# load zone information t ofov
		self.fov.read_zone(self.zone)
		# put player to random coords inside the zone
		self.player = self.zone.add_object('@', libtcod.white)

	def handle_keys(self):
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
			self.player.x, self.player.y = self.zone.random_valid_coords() 

		#player movement
		if libtcod.console_is_key_pressed(libtcod.KEY_UP) or libtcod.console_is_key_pressed(libtcod.KEY_KP8):
			player.move(0, -1)
			logger.log("player moved to " + str((self.player.x, self.player.y)))

		elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or libtcod.console_is_key_pressed(libtcod.KEY_KP2):
			self.player.move(0, 1)
			logger.log("player moved to " + str((self.player.x, self.player.y)))

		elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or libtcod.console_is_key_pressed(libtcod.KEY_KP4):
			self.player.move(-1, 0)
			logger.log("player moved to " + str((self.player.x, self.player.y)))

		elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or libtcod.console_is_key_pressed(libtcod.KEY_KP6):
			self.player.move(1, 0)
			logger.log("player moved to " + str((self.player.x, self.player.y)))

		elif libtcod.console_is_key_pressed(libtcod.KEY_KP7):
			self.player.move(-1, -1)
			logger.log("player moved to " + str((self.player.x, self.player.y)))

		elif libtcod.console_is_key_pressed(libtcod.KEY_KP9):
			self.player.move(1, -1)
			logger.log("player moved to " + str((self.player.x, self.player.y)))

		elif libtcod.console_is_key_pressed(libtcod.KEY_KP1):
			self.player.move(-1, 1)
			logger.log("player moved to " + str((self.player.x, self.player.y)))

		elif libtcod.console_is_key_pressed(libtcod.KEY_KP3):
			self.player.move(1, 1)
			logger.log("player moved to " + str((self.player.x, self.player.y)))	


def main():
	"""App init and main loop"""
	# init the new app!
	app = Application()

	# the main loop
	while not libtcod.console_is_window_closed():
		# recompute fov for player position
		app.fov.recompute(app.player.x, app.player.y)
		# render and explore the zone
		app.renderer.process_zone(app.zone, app.fov.map)
		# render all objects in the zone
		app.renderer.render_objects(app.zone.objects, app.fov.map)
		# blit out drawing buffer
		libtcod.console_blit(app.con, 0, 0, app.SCREEN_WIDTH, app.SCREEN_HEIGHT, 0, 0, 0)
		# flush the console
		libtcod.console_flush()

		# clear the objects
		app.renderer.clear_objects(app.zone.objects)
		
		#handle keys and exit game if needed
		exit = app.handle_keys()
		if exit:
			break

if __name__ == '__main__':
   main()




