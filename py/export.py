
import config
import math

def scale(x, imin, imax, omin, omax):
	"""
	scales value x in range imin - imax to range omin - omax
	"""
	return (x - imin) * (omax - omin) / float(imax - imin) + omin

def ptc(p):
	"""
	converts a pixel drawing coordinate to a coordinate for gcodes
	"""
	fx = -scale(p[0], 0, config.DRAWING_AREA_X, -(config.MILL_AREA_X / 2), (config.MILL_AREA_X / 2))
	fy = -scale(p[1], 0, config.DRAWING_AREA_Y, -(config.MILL_AREA_Y / 2), (config.MILL_AREA_Y / 2))
	return (fx, fy)

# gcode coordinate to pixel
def ctp(p):
	"""
	converts a gcode coordinate to a canvas pixel coordinate
	"""
	fx = -scale(p[0], -(config.MILL_AREA_X / 2), (config.MILL_AREA_X / 2), 0, config.DRAWING_AREA_X)
	fy = -scale(p[0], -(config.MILL_AREA_Y / 2), (config.MILL_AREA_Y / 2), 0, config.DRAWING_AREA_Y)
	return (fx, fy)
	
def add_code(cmd, *args):
	for a in args:
		cmd = cmd.replace("?", str(a), 1)
	return cmd + "\n"

def dist(x1, y1, x2, y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)
	
def find_best_order_aux(input, start):
	"""
	nearest neighbor algorithm to find a good path
	"""
	lines = input[:]
	out = []
	cur = lines.pop(start)
	total = 0
	while len(lines):
		smallest = 1e1000
		best = 0
		for i in range(len(lines)):
			line = lines[i]
			d = dist(cur.end[0], cur.end[1], line.start[0], line.start[1])
			if d < smallest:
				smallest = d
				best = i
				total += d
		out.append(cur)
		cur = lines[best]
		lines.pop(best)
	out.append(cur)
	return total, out

def find_best_order(input):
	if len(input) == 0:
		return []
	tries = []
	for i in range(len(input)):
		tries.append(find_best_order_aux(input, i))
	
	best_n = 1e1000
	best = tries[0]
	for a in tries:
		if a[0] < best_n:
			best_n = a[0]
			best = a[1]
	return best
	
def gcode(lines):
	lines = find_best_order(lines)
	up  = config.MILL_RELEASE_AMOUNT
	out = add_code("G0 Z?", up)
	for line in lines:
		start = ptc(line.start)
		end   = ptc(line.end)
		out += add_code("G0 X? Y?", *start)
		out += add_code("G0 Z?", -up)
		out += add_code("G1 X? Y?", *end)
		out += add_code("G0 Z?", up)
	return out