maj = 0
min = 1
with open("../py/version.py", "r") as f:
	p = f.read()
	maj = int(p[8:p.find("\n", 8)])
	min = int(p[18:p.find("\n", 18)])
	min += 1
with open("../py/version.py", "w") as f:
	f.write("MAJOR = %d\nMINOR = %d\n" % (maj, min))
	