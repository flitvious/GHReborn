#Eventually make it into a proper class assigned to app

# debug log switch
VERBOSITY_DEBUG = True

# debug log subtype suppression
SHOW_CHEATS = True
SHOW_MOVEMENT = False
SHOW_LEVEL_GEN = False
SHOW_RENDERING = True

# error log switch
VERBOSITY_ERROR = True

# todo suppressor based on message class!
# cheats - cheat codes
# movement - player moves, monster moves
# level_gen - level generation
# rendering - rendering-related stuff (consoles, e.t.c.)

def log(subtype, message):
	"""Output debug log message of given type"""
	if VERBOSITY_DEBUG:
		if subtype == "cheats" and not SHOW_CHEATS:
			return
		if subtype == "movement" and not SHOW_MOVEMENT:
			return
		if subtype == "level_gen" and not SHOW_LEVEL_GEN:
			return
		str(message)
		print "DEBUG (" + subtype + "): " + message

def error(message):
	"""Output error log message of given type"""
	if VERBOSITY_ERROR:
		str(message)
		print "ERROR: " + message
