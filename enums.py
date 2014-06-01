def enum(*sequential, **named):
	"""
	This simulates the enum functionality
	source: http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
	usage:
	Numbers = enum('ZERO', 'ONE', 'TWO')
	>>> Numbers.ZERO
	0
	>>> Numbers.ONE
	1

	extra support for reverse mapping (to display in logs)
	>>> Numbers.reverse_mapping[0]
	'ZERO'
	"""
	enums = dict(zip(sequential, range(len(sequential))), **named)
	reverse = dict((value, key) for key, value in enums.iteritems())
	enums['reverse_mapping'] = reverse
	return type('Enum', (), enums)