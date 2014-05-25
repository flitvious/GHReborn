import libtcodpy as libtcod
import logger

class Tile:
	"""a tile of the map and its properties"""
	
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: 
			self.block_sight = blocked
		else:
			self.block_sight = block_sight

class Rect:
	"""A rectangle on the map. Used to characterize a room."""
	
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		"""returns center of the rectangle"""
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)

	def intersect(self, other):
		"""returns true if this rectangle intersects with another one"""
		if  (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1):
			return True
		else:
			return False

class Zone:
	"""A map, x by y of empty tiles"""
	
	def __init__(self, width=80, height=45):
		
		self.width = width
		self.height = height
		#map starts with all tiles "blocked"
		self.cells = [[Tile(blocked=True) for y in range(self.height)] for x in range(self.width)]

	def __getitem__(self, index):
		"""
		Returns a tile specified by index. 
		Proper way to call this is zone[x][y], with just zone[x] an array of tiles is returned
		"""
		# zone[x][y] means zone.__getitem__(x).__getitem__(y) which does the trick
		return self.cells[index]

	def random_valid_coords(self, max_tries=50):
		"""Tries to return a random non-blocked tile inside the zone. If it fails, it returns the first non-blocked tile it finds"""
		for r in range(max_tries):
			x = libtcod.random_get_int(0, 0, self.width - 1)
			y = libtcod.random_get_int(0, 0, self.height - 1)
			if self.cells[x][y].blocked is False:
				return (x, y)
		# Okay, nothing reached in max tries. Time to check for valid tiles one by one
		for y in range(self.height):
			for x in range(self.width):
				if self.cells[x][y].blocked is False:
					logger.error("Could not find random coords, checking for a first valid tile.")
					return(x, y)
		# Okay, there are no non-blocked tiles.... put player in the corner
		logger.error("Hey, the zone has no valid coords! Returning zeroes.")
		return (0, 0)

	def roomer(self, room_max_size=10, room_min_size=6, max_rooms=30):
		"""Fills zone with rooms and tunnels"""
		rooms = []
		prev_num = 0

		def has_intersections(candidate):
			"""run through the existing rooms and see if they intersect with the candidate"""
			for other_room in rooms:
				if candidate.intersect(other_room) is True:
					# this room intersects another room
					return True
			return False

		def tunnelize(coords_new, coords_prev):
			"""Draw a pair of tunnels vertically and horizontally between new and prev"""

			logger.log("Tunnelizing between " + str(coords_new) + " and " + str(coords_prev))

			new_x, new_y = coords_new
			prev_x, prev_y = coords_prev

			#draw a coin (random number that is either 0 or 1)
			if libtcod.random_get_int(0, 0, 1) == 1:
				#first move horizontally, then vertically
				self.carve_h_tunnel(prev_x, new_x, prev_y) # 0 3 3
				self.carve_v_tunnel(prev_y, new_y, new_x)  # 3 0 3
			else:
				#first move vertically, then horizontally
				self.carve_v_tunnel(prev_y, new_y, prev_x) # 3 0 0
				self.carve_h_tunnel(prev_x, new_x, new_y)  # 0 3 0

		for room_num in range(max_rooms):
			#random width and height
			w = libtcod.random_get_int(0, room_min_size, room_max_size)
			h = libtcod.random_get_int(0, room_min_size, room_max_size)
			#random position without going out of the boundaries of the map
			x = libtcod.random_get_int(0, 0, self.width - w - 1)
			y = libtcod.random_get_int(0, 0, self.height - h - 1)

			new_room = Rect(x, y, w, h)
			
			if has_intersections(new_room) is False:
				#this means there are no intersections, so this room is valid
				self.carve_room(new_room)
				rooms.append(new_room)
				current_room_idx = len(rooms) - 1
				if current_room_idx > 0:
					logger.log("Roomer: trying to tunnel #" + str(current_room_idx))
					tunnelize(rooms[current_room_idx].center(), rooms[current_room_idx - 1].center())

	def carve_room(self, rect):
		"""go through the tiles inside the rectangle borders and make them passable"""
		# range gives one *less* than specified, so outer "walls" will be left in place
		for x in range(rect.x1, rect.x2):
			for y in range(rect.y1, rect.y2):
				self.cells[x][y].blocked = False
				self.cells[x][y].block_sight = False
		#logger.log("Created a room")
	
	def carve_h_tunnel(self, x1, x2, y):
		"""create a horizontal line of passable tiles between x1 and x2 and a specified y"""
		# minmax is for the thing to work in both directions
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.cells[x][y].blocked = False
			self.cells[x][y].block_sight = False

	def carve_v_tunnel(self, y1, y2, x):
		"""create a vertical line of passable tiles between y1 and y2 and a specified x"""
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.cells[x][y].blocked = False
			self.cells[x][y].block_sight = False