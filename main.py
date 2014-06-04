## for now this will be my libtcod tutorial

import libtcodpy as libtcod
import logger
import enums
import entities
import zone
import renderer
from keyhandler import KeyHandler as k

class Engine:
	"""GHreborn Engine"""	

	def __init__(self):

		# init the renderer
		self.renderer = renderer.Renderer(screen_width=80, screen_height=50, fps_limit=20)

		# init the input
		self.keyhandler = k() #keyhandler.KeyHandler()

		# init the map
		self.zone = zone.Zone()
		# populate zone with roomer algorithm
		self.zone.roomer(max_rooms=30)
		
		# init fov
		self.fov = renderer.Fov(algo=0, light_walls=True, light_radius=10)
		
		# load zone information to fov
		self.fov.read_zone(self.zone)
		
		# create a player object in the zone and make him a fighter
		self.player = entities.Actor('@', 'player', libtcod.white, blocks=True, 
			design=entities.Actor.designs.player, ai=entities.AI.ais.player_control)
		
		# put player to random coords inside the zone
		self.zone.add_entity(self.player)

	def loop(self):
		"""Endless loop"""
		while not self.renderer.is_closed():
			
			# make renderer redraw the screen
			self.redraw()
			
			#build dict for act() method
			act_data = dict(player=self.player, fov_map=self.fov.map)

			# iterate over all entities in the zone
			for ent in self.zone.entities:
				
				if ent is self.player:
					# player is a special case!

					# player_made_turn is determined in ai (failed, cancelled skills and free retries, etc)
					player_made_turn = False
					
					while not player_made_turn:

						# wait for some input
						key = self.keyhandler.wait_for_key()

						# process controls
						# these will overlay any game action bound for the same key
						self.process_control_actions(action=self.keyhandler.process_control_keys(key))
						# process cheats
						# these will overlay any game action bound for the same key
						self.process_cheat_actions(action=self.keyhandler.process_cheat_keys(key))

						# get player's action
						act_data['player_action'] = self.keyhandler.process_game_key(key)
						
						# feed action to Actor.
						# if player didn't do any game action, repeat.
						player_made_turn = ent.act(act_data)
				else:
					# not player, regular mook
					result = ent.act(act_data)
					if result is False:
						logger.log(logger.types.ai, 'Actor ' + ent.name + 'could not act')
				

	def redraw():
		"""Redraw for main loop"""
		# recompute fov for player position
		self.fov.recompute(self.player.x, self.player.y)
		# render and explore the zone
		self.renderer.explore_and_render_zone(self.zone, self.fov.map)
		# render all objects in the zone
		self.renderer.render_entities(self.zone.entities, self.fov.map)
		# blit out drawing buffer
		self.renderer.blit_con()
		# flush the console
		self.renderer.flush()
		# clear the objects
		self.renderer.clear_entities(self.zone.entities)
		
	def process_control_actions(self, action):
		"""Run logic for control actions"""
		if action == k.controls.none or action == k.controls.other:
			pass
		elif action == k.controls.exit:
			quit(0)
		elif action == k.controls.fullscreen:
			self.renderer.toggle_fullscreen()

	def process_cheat_actions(self, action):
		"""Run logic for cheat actions"""
		if action == k.cheats.teleport:
			logger.log(logger.types.cheats, "teleporting")
			self.player.x, self.player.y = self.zone.random_valid_coords()
			self.redraw()
		elif action == k.cheats.reveal_map:
			logger.log(logger.types.cheats, "exploring all the map")
			self.renderer.show_all(self.zone, self.zone.entities)
			self.redraw()

def main():
	"""Engine init and main loop"""
	# init the new app!
	engine = Engine()
	# enter endless loop
	engine.loop()

if __name__ == '__main__':
	main()

