from pygame import *
from const import *
from math import *
from AStar import *

class Enemy:
	"""Enemy parent class"""

	isFlying = False
	dead = False
	path = []
	cx, cx = 0, 0

	def move(self):
		if not self.isFlying:
			# MOVE TO NEXT PATH

			if len(self.path) == 0:
				return
			
			dx, dy = self.x-self.path[0][0], self.y-self.path[0][1]

			if sqrt(dx**2+dy**2) < 0.15:
				self.path = self.path[1:]

		if len(self.path) != 0:
			dx, dy = self.path[0][0]-self.x, self.path[0][1]-self.y
		else:
			dx, dy = self.cx-self.x, self.cy-self.y

		something = sqrt(dx**2+dy**2)

		rx = dx/something
		ry = dy/something

		self.x += self.speed*rx
		self.y += self.speed*ry

	def pathFind(self, xy, nodes, paths):
		self.cx, self.cy = x, y = xy

		if self.isFlying:
			return

		start, end = nodes[int(self.x)][int(self.y)], nodes[int(x)][int(y)]

		path = paths.search(start, end)
		if path is None:
			# STOP THE ENEMY

			print("HELP NO PATH!")
		else:
			for i in range(len(path)):
				p = path[i]
				path[i] = (p.x, p.y)
			self.path = path
	