# Enenmy.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is parent enemy class, it contains the default moves
# for all enemies in the game.
# 

from pygame import *
from const import *
from math import *
from AStar import *
from random import randint

class Enemy:
	"""Enemy parent class"""

	# Setup
	isFlying = False
	dead = False
	path = []
	cx, cx = 0, 0
	health = 1
	weight = 1
	canHurt = True

	tears = []

	hurtDistance = 0.8

	def hurt(self, ammount):
		if not self.dead:
			self.health -= ammount
			if self.health <= 0:
				self.die()

	def checkHurt(self, character, time):
		# Check for any hurt

		self.cx, self.cy = ix, iy = (character.x-GRIDX)/GRATIO, (character.y-GRIDY)/GRATIO
		dx, dy = (self.cx-self.x), (self.cy-self.y)

		if not self.dead:
			# Check tear hurt
			for t in character.tears:
				tx = (t.x-GRIDX)/GRATIO
				ty = (t.y-GRIDY)/GRATIO
				dist = sqrt((tx-self.x)**2+(ty-self.y)**2)
				if dist < self.hurtDistance and not t.poped:
					t.pop(True)
					if self.canHurt:
						self.hurt(t.damage)

			# Check if character is too close
			if abs(dx) < 0.8 and abs(dy) < 0.8:
				fx, fy = (GRIDX+GRATIO*self.x, GRIDY+GRATIO*self.y)

				character.hurt(1, fx, fy, time)

		# Check if character should be hit
		for tear in self.tears:
			dist = sqrt((tear.x-character.x)**2+(tear.y-character.y)**2)
			if dist/GRATIO <= character.hurtDistance and not tear.poped:
				character.hurt(tear.damage, tear.x, tear.y, time)
				tear.pop(True)

	def die(self):
		if not self.dead:
			self.dead = True

	def move(self):
		if not self.isFlying and len(self.path) != 0:
			# MOVE TO NEXT PATH

			dx, dy = self.x-self.path[0][0], self.y-self.path[0][1]

			if sqrt(dx**2+dy**2) < 0.15:
				self.path = self.path[1:]

		if len(self.path) > 0:
			# Head towards next point
			dx, dy = self.path[0][0]-self.x, self.path[0][1]-self.y
		else:
			# Head towards character
			dx, dy = self.cx-self.x, self.cy-self.y

		# Move ratios
		dist = sqrt(dx**2+dy**2)

		rx = dx/dist
		ry = dy/dist

		# Move character
		self.x += self.speed*rx
		self.y += self.speed*ry

	def pathFind(self, xy, nodes, paths):
		# Do pathfinding
		
		self.cx, self.cy = x, y = list(map(round,xy))

		if self.isFlying:
			return

		start, end = nodes[round(self.x)][round(self.y)], nodes[x][y]

		path = paths.search(start, end)
		if path is None:
			# There is no path found to the character

			self.path = []
		else:
			for i in range(len(path)):
				p = path[i]
				path[i] = (p.x, p.y)
			self.path = path[1:]

	def render(self, surface, time, character, nodes, paths, bounds, obsticals):
		pass