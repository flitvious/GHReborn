import enums

#Eventually make it into a proper class assigned to app

# debug log switch
VERBOSITY_DEBUG = True

# debug log subtype suppression
SHOW_INPUT = False
SHOW_CHEATS = True
SHOW_MOVEMENT = False
SHOW_LEVEL_GEN = False
SHOW_RENDERING = False
SHOW_COMBAT = True
SHOW_AI = True


# error log switch
VERBOSITY_ERROR = True

# game log switch
VERBOSITY_GAME = True

# suppressor based on message class

types = enums.enum('cheats', 'movement', 'level_gen', 'rendering', 'input', 'ai', 'combat')

# rendering - rendering-related stuff (consoles, e.t.c.)
# input - various keypresses (actions)
# cheats - cheat codes
# level_gen - level generation
# ai - ai related stuff
# movement - movement and collisions
# combat - getting and receiving damage



def log(subtype, message):
	"""Output debug log message of given type"""
	if VERBOSITY_DEBUG:
		if subtype == types.cheats and not SHOW_CHEATS:
			return
		if subtype == types.movement and not SHOW_MOVEMENT:
			return
		if subtype == types.level_gen and not SHOW_LEVEL_GEN:
			return
		if subtype == types.input and not SHOW_INPUT:
			return
		if subtype == types.combat and not SHOW_COMBAT:
			return
		if subtype == types.ai and not SHOW_AI:
			return
		str(message)
		print "DEBUG (" + types.reverse_mapping[subtype] + "): " + message

def error(message):
	"""Output error log message of given type"""
	if VERBOSITY_ERROR:
		str(message)
		print "ERROR: " + message

def game(message):
	"""Output game information"""
	if VERBOSITY_GAME:
		print "GAME: " + message
