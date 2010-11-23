import Tkinter as tk
import export
import config
import subprocess


MOUSE_MOVE, MOUSE_LEFTCLICK, MOUSE_RIGHTCLICK = range(3)
TOOL_LINES, TOOL_CIRCLE = range(2)

class Element(object):
	def __init__(self, tkc):
		self.objects = []
		self.start   = (0, 0)
		self.end     = (0, 0)
		self.tkc     = tkc
		self.init()
		
	def init(self):
		pass
	
	def erase(self):
		for o in range(len(self.objects)):
			self.tkc.delete(self.objects.pop(0))
		
	def redraw(self):
		pass
	
	def start_drawing(self, point):
		pass
		
	def update_drawing(self, type, point):
		pass

	def get_start(self):
		return self.start
		
	def get_end(self):
		return self.end
		
class Circle(Element):
	def init(self):
		self.bbox = (0, 0, 0, 0)
		self.tempobj = None
		
	def start_drawing(self, point):
		self.start = point
		
	def update_drawing(self, type, point):
		if type == MOUSE_MOVE:
			if self.tempobj is not None:
				self.tkc.delete(self.tempobj)
			self.tempobj = self.tkc.circle(*self.start, *point)
		elif type == MOUSE_LEFTCLICK:
			self.tkc.delete(self.tempobj)
			self.objects.append(self.tkc.circle(*self.start, *point))
			self.end = point
			self.bbox = tuple(*self.start, *self.end)
			
	def redraw(self):
		self.erase()
		self.objects.append(self.tkc.circle(*self.bbox))
			
	

class LineArray(Element):
	def init(self):
		

class Canvas(object):
	def __init__(self, root):
		w, h = config.DRAWING_AREA_X, config.DRAWING_AREA_Y
		self.tkc = tk.Canvas(root, bg = "white", width = w, height = h)
		self.tkc.pack()
		self.tkc.bind("<Button-1>", self.on_leftclick)
		self.tkc.bind("<Button-2>", self.on_rightclick)
		self.tkc.bind("<Motion>", self.on_motion)
		self.elements = []
		self.tool = TOOL_LINES
		
		self.cur_elem = None
		
	def set_tool(self, t):
		self.tool = t
		
	def new_elem(self):
		if self.tool == TOOL_LINES:
			return LineArray(self.tkc)
		elif self.tool == TOOL_LINES:
			return Circle(self.tkc)
		return Element(self.tkc)
		
	def on_leftclick(self, event):
		if self.cur_elem is None:
			self.cur_elem = self.new_elem()
			

class Window(object):
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("MillDraw %s" % config.VERSION)
		self.canvas = Canvas(self.root)
		self.btn_clear = tk.Button(self.root, text="Clear", command = self.canvas.clear)
		self.btn_clear.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self.btn_undo  = tk.Button(self.root, text="Undo", command = self.canvas.undo)
		self.btn_undo.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self.btn_export = tk.Button(self.root, text="Export", command = self.export)
		self.btn_export.pack(side=tk.LEFT, fill=tk.X, expand=1)
		v = tk.IntVar()
		self.btn_path = tk.Checkbutton(self.root, text="Show Path", command = self.on_path, variable = v)
		self.btn_path.pack(side=tk.LEFT, fill=tk.X, expand=1)
		self.btn_path.var = v
		
		
	def start(self):
		self.root.mainloop()
		
	def export(self):
		lines = self.canvas.get_lines()
		text = export.gcode(lines)
		with open("tmp/gcode", "w") as o:
			o.write(text)
		subprocess.Popen("notepad.exe tmp/gcode")
		
	def on_path(self):
		if self.btn_path.var.get() == 0:
			self.canvas.clear_order()
		else:
			self.canvas.draw_order()

Window().start()