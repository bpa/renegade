class map_location(object):
	"One square on the overview map"
	def __init__(self, map, loc):
		self.loc = loc
		self.map = map

	def loc(self):
		return self.loc
	
	def neighbor_north(self):
		return self.map.get( (self.loc[0], self.loc[1] - 1) )
		
class map_base:
	def __init__(self, width, height):
		self.rows = [ [map_location(self, (x,y)) for y in range(height)] \
				for x in range(width) ]

	def get(self, loc):
		return self.rows[loc[0]][loc[1]]
