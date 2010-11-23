import Tkinter as tk

class Window(object):
	def __init__(self):
		self.root = tk.Tk()
		self.tkc = tk.Canvas(self.root, bg = "white", width = 400, height = 400)
		self.tkc.pack()
		self.tkc.create_oval(5, 5, 100, 100)
		self.root.mainloop()
	

Window()