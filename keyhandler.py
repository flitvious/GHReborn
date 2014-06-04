import libtcodpy as libtcod
import enums
import logger

class KeyHandler:
	"""Handles Key through libtcode"""
	
	controls = enums.enum('none', 'other', 'exit', 'fullscreen')
	cheats = enums.enum('none', 'other', 'teleport', 'reveal_map')
	game = enums.enum('none', 'other', 
		'move_N', 'move_NE', 'move_E', 'move_SE', 'move_S', 'move_SW', 'move_W', 'move_NW', 'move_5')
	
	def __init__(self):
		pass

	def process_control_keys(self, key):
		"""
		Checks if passed key corresponds to control action. if so, return control action const.
		"""
		if key.vk == libtcod.KEY_NONE:
			logger.log(logger.types.input, "key none")
			return KeyHandler.controls.none

		elif key.vk == libtcod.KEY_ESCAPE:
			logger.log(logger.types.input, "key escape")
			return KeyHandler.controls.exit

		elif key.vk == libtcod.KEY_ENTER and key.lalt:
			logger.log(logger.types.input, "key alt+enter")
			return KeyHandler.controls.fullscreen		
		else:
			# some other key
			return KeyHandler.controls.other

	def process_cheat_keys(self, key):
		"""
		Checks if passed key corresponds to cheat action. if so, returns cheat action const.
		"""
		if key.vk == libtcod.KEY_NONE:
			return KeyHandler.cheats.none

		elif key.vk == libtcod.KEY_1 and key.lctrl:
			return KeyHandler.cheats.teleport
		
		elif key.vk == libtcod.KEY_2 and key.lctrl:
			return KeyHandler.cheats.reveal_map
		
		else:
			return KeyHandler.cheats.other

	def process_game_key(self, key):
		"""
		Checks if passed key corresponds to if passed key corresponds to any game action (that takes a turn). 
		If so, returns cheat action const.
		"""
		if libtcod.console_is_key_pressed(libtcod.KEY_UP) or libtcod.console_is_key_pressed(libtcod.KEY_KP8):
			return KeyHandler.game.move_N
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or libtcod.console_is_key_pressed(libtcod.KEY_KP2):
			return KeyHandler.game.move_S
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or libtcod.console_is_key_pressed(libtcod.KEY_KP4):
			return KeyHandler.game.move_W
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or libtcod.console_is_key_pressed(libtcod.KEY_KP6):
			return KeyHandler.game.move_E
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_KP7):
			return KeyHandler.game.move_NW
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_KP9):
			return KeyHandler.game.move_NE
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_KP1):
			return KeyHandler.game.move_SW
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_KP3):
			return KeyHandler.game.move_SE
		
		elif libtcod.console_is_key_pressed(libtcod.KEY_KP5) or libtcod.console_is_key_pressed(libtcod.KEY_5):
			return KeyHandler.game.move_5
		
		elif key.vk == libtcod.KEY_NONE:
			return KeyHandler.game.none

		else:
			return KeyHandler.game.other

	def wait_for_key(self):
		"""wait for a key and return it"""
		return libtcod.console_wait_for_keypress(True) 
