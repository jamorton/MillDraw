import Tkinter as tk
import export
import config
import subprocess

class Line(object):
	def __init__(self, lineid, start, end):
		self.id = lineid
		self.start = start
		self.end = end

class Canvas(object):
	def __init__(self, root):
		w, h = config.DRAWING_AREA_X, config.DRAWING_AREA_Y
		self.tkc = tk.Canvas(root, bg = "white", width = w, height = h)
		self.tkc.pack()
		self.tkc.bind("<Button-1>", self.on_click)
		self.tkc.bind("<Motion>", self.on_motion)
		
		self.lines = []
		self.curr_line = None
		self.start_point = (0, 0)
		
		self.texts = []
		self.update_texts = False
		
	def undo(self):
		if len(self.lines):
			line = self.lines.pop()
			self.tkc.delete("all")
			newl = []
			for l in self.lines:
				sx, sy = l.start
				ex, ey = l.end
				newl.append(Line(self.tkc.create_line(sx, sy, ex, ey), (sx, sy), (ex, ey)))
			self.lines = newl
			if self.update_texts:
				self.clear_order()
				self.draw_order()
		
	def get_lines(self):
		return self.lines

	def clear(self):
		self.tkc.delete("all")
		self.lines = []
		
	def on_click(self, event):
		if self.curr_line is not None:
			self.curr_line = None
			sx, sy = self.start_point
			ex, ey = event.x, event.y
			ll = self.tkc.create_line(sx, sy, ex, ey)
			self.lines.append(Line(ll, (sx, sy), (ex, ey)))
			if self.update_texts:
				self.clear_order()
				self.draw_order()
		else:
			x, y = event.x, event.y
			self.curr_line = self.tkc.create_line(x, y, x, y)
			self.start_point = (x, y)
			
	def on_motion(self, event):
		if self.curr_line is not None:
			self.tkc.delete(self.curr_line)
			sx, sy, ex, ey = self.start_point[0], self.start_point[1], event.x, event.y
			self.curr_line = self.tkc.create_line(sx, sy, ex, ey)
			
	def draw_order(self):
		self.update_texts = True
		lines = export.find_best_order(self.lines)
		for i in range(len(lines)):
			x = lines[i]
			self.texts.append(self.tkc.create_text(x.start[0] + 5, x.start[1] + 5, text = str(i)))
			
	def clear_order(self):
		self.update_texts = False
		while len(self.texts):
			self.tkc.delete(self.texts.pop())

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