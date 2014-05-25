#Eventually make it into a proper class assigned to app

# this should be just verbosity
VERBOSITY_DEBUG = True
VERBOSITY_ERROR = True

def log(message):
	"""Debug log"""
	if VERBOSITY_DEBUG:
		str(message)
		print "DEBUG: " + message

def error(message):
	"""Error log"""
	if VERBOSITY_ERROR:
		str(message)
		print "DEBUG: " + message
