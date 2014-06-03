## for now this will be my libtcod tutorial

import libtcodpy as libtcod
import logger
import enums
import objects
import zone
import renderer

class Application:
	"""GHreborn main application"""	

	def __init__(self):
		
		# these should be static, but I don't care since application has one instance.		
		# states
		self.states = enums.enum('playing', 'pause')
		self.state = self.states.playing

		# possible human player actions
		self.actions = enums.enum('exit', 'no_turn', 'move')

		# init the renderer
		self.renderer = renderer.Renderer(screen_width=80, screen_height=50, fps_limit=20)

		# init the map
		self.zone = zone.Zone()
		# populate zone with roomer algorithm
		self.zone.roomer(max_rooms=30)
		# init fov
		self.fov = renderer.Fov(algo=0, light_walls=True, light_radius=10)
		
		# load zone information to fov
		self.fov.read_zone(self.zone)
		
		# create a player object and make him a fighter
		self.player = objects.Object('@', 'player', libtcod.white, 
			blocks=True, 
			fighter=objects.Fighter(hp=30, defense=2, power=5)
			)
		
		# put player to random coords inside the zone
		self.zone.add_object(self.player)


	def handle_keys(self, key):
		"""
		Handle input from the main loop.
		"""

		def handle_movement():
			moved = False

			if libtcod.console_is_key_pressed(libtcod.KEY_UP) or libtcod.console_is_key_pressed(libtcod.KEY_KP8):
				moved = True
				dx = 0
				dy = -1

			elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or libtcod.console_is_key_pressed(libtcod.KEY_KP2):
				moved = True
				dx = 0
				dy = 1

			elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or libtcod.console_is_key_pressed(libtcod.KEY_KP4):
				moved = True
				dx = -1
				dy = 0

			elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or libtcod.console_is_key_pressed(libtcod.KEY_KP6):
				moved = True
				dx = 1
				dy = 0

			elif libtcod.console_is_key_pressed(libtcod.KEY_KP7):
				moved = True
				dx = -1
				dy = -1

			elif libtcod.console_is_key_pressed(libtcod.KEY_KP9):
				moved = True
				dx = 1
				dy = -1

			elif libtcod.console_is_key_pressed(libtcod.KEY_KP1):
				moved = True
				dx = -1
				dy = 1

			elif libtcod.console_is_key_pressed(libtcod.KEY_KP3):
				moved = True
				dx = 1
				dy = 1

			elif libtcod.console_is_key_pressed(libtcod.KEY_KP5) or libtcod.console_is_key_pressed(libtcod.KEY_5):
				moved = True
				dx = 0
				dy = 0
			
			if moved:
				# move the PC
				self.player.move(dx, dy)
				# return 'moved'
				return self.actions.move
			else:
				# return 'no turn taken'
				return self.actions.no_turn


		if key.vk == libtcod.KEY_ENTER and key.lalt:
			#Alt+Enter: toggle fullscreen
			self.renderer.toggle_fullscreen()

		elif key.vk == libtcod.KEY_ESCAPE:
			#exit game
			return self.actions.exit

		# cheats/debug
		elif key.vk == libtcod.KEY_1 and key.lctrl:
			logger.log(logger.types.cheats, "teleporting randomly")
			self.player.x, self.player.y = self.zone.random_valid_coords()

		elif key.vk == libtcod.KEY_2 and key.lctrl:
			logger.log(logger.types.cheats, "exploring all map")
			self.renderer.show_all(self.zone, self.zone.objects)
		
		#player movement, works only if playing
		if self.state == self.states.playing:
			action = handle_movement()
			
			#if player did something, let monsters take their turn
			if action != self.actions.no_turn:
				for obj in self.zone.objects:
					# if not player, act
					if not obj is self.player:
						#if has some ai, take turn
						if not obj.ai is None:
							#logger.log(logger.types.ai, "calling ai.take_turn for " + obj.name)
							obj.ai.take_turn(fov_map=self.fov.map, player=self.player)
			# return the action (check that player didin't choose to exit)
			return action

def main():
	"""App init and main loop"""
	# init the new app!
	app = Application()

	# the main loop
	while not app.renderer.is_closed():
		# recompute fov for player position
		app.fov.recompute(app.player.x, app.player.y)
		# render and explore the zone
		app.renderer.process_zone(app.zone, app.fov.map)
		# render all objects in the zone
		app.renderer.render_objects(app.zone.objects, app.fov.map)
		# show stats
		logger.game("Player's health is " + str(app.player.fighter.hp) + " of " + str(app.player.fighter.max_hp))
		# blit out drawing buffer
		app.renderer.blit_con()
		# flush the console
		app.renderer.flush()
		# clear the objects
		app.renderer.clear_objects(app.zone.objects)
		
		#handle keys and exit game if needed
		# libtcod 1.5.1 has this bugged and working twice, use 1.5.2!
		#key = libtcod.console_check_for_keypress()
		key = libtcod.console_wait_for_keypress(True)
		
		action = app.handle_keys(key)
		# logger stuff
		logger.log(logger.types.input, "Handle keys returned " + app.actions.reverse_mapping[action])
		if action == app.actions.exit:
			break

if __name__ == '__main__':
	main()




