# Character.py
# Aaron Taylor
# Moose Abumeeiz
#
# This is the class for the main character it handles all controls and
# functions that they have

from pygame import *
from random import randint
from math import *
from const import GRATIO
from UIHeart import *
from Tear import *
from Fire import *
from Coin import *
from Key import *
from Pickup import *
from Heart import *
from Bomb import *
from Item import *
from Pill import *
from Trapdoor import *
from Banner import *

class Character:
	"""The main class for Isaac"""

	hurtDistance = .6

	def __init__(self, variant, xy, keys, textures, sounds, fonts):
		self.variant = variant
		self.x, self.y = xy
		self.textures = textures["character"][variant]

		# Record import sounds and textures
		self.tearTextures = textures["tears"]
		self.tearSounds = sounds["tear"]
		self.heartTextures = textures["hearts"]
		self.sounds = sounds["hurt"]

		# Setup starting info
		self.dead = False
		self.isFlying = False
		self.pill = None
		self.lastHurt = -1

		# Tears + hearts
		self.tears = []
		self.hearts = [UIHeart(0, 2, textures["hearts"]) for i in range(3)]

		# Head, shoulders knees and toes, knees and toes!
		self.heads = [self.textures.subsurface(Rect((i*64)*2, 0, 64, 64)) for i in range(3)]
		self.heads.append(transform.flip(self.heads[1], True, False))
		self.tearHeads = [self.textures.subsurface(Rect(64+(i*64)*2, 0, 64, 64)) for i in range(3)]
		self.tearHeads.append(transform.flip(self.tearHeads[1], True, False))
		self.feet = [
			[self.textures.subsurface(Rect((i*64), 64, 64, 64)) for i in range(8)],
			[self.textures.subsurface(Rect((i*64), 64*2, 64, 64)) for i in range(8)],
			[],
			[]
		]

		# The rect for the characters body
		self.bodyRect = Rect(self.x-16, self.y-16, 32, 32)

		# The things he can pickup
		self.pickups = [Pickup(i, textures["pickups"], fonts["pickups"]) for i in range(3)] # Keys, Bombs, Coins

		# Walkign forward and backwards have the same animation
		for frame in self.feet[0]:
			self.feet[2].append(frame)

		# Allow for reversed feet
		for frame in self.feet[1]:
			self.feet[3].append(transform.flip(frame, True, False))

		# Setup head and body
		self.head = self.heads[0]
		self.body = self.feet[0][0]

		# Used for holding arms in the air and gettting hurt
		self.specialFrames = [self.textures.subsurface(i*128, 272+128, 128, 128) for i in range(1, 3)]
		self.specialFrame = 0

		self.lastPickup = 0

		# Animation setup
		self.interval = .06
		self.lastAnimate = 0
		self.walking = False
		self.eyesOpen = True
		self.walkIndex = 0
		self.lastTear = 0
		
		# Velocity
		self.xVel = 0
		self.yVel = 0

		# Direction
		self.up = False
		self.down = False
		self.left = False
		self.right = False
		self.lastKey = 0
		self.lastTearKey = 0

		# Last pressed key
		self.lastKeys = []
		self.lastTearKeys = []

		# Keys
		self.moveKeys = keys[0]
		self.tearKeys = keys[1]

		# Stats
		self.speed = 2
		self.shotRate = 1
		self.damage = 2
		self.range = 2
		self.shotSpeed = 1
		self.luck = 1

		# The items isaac has picked up
		self.items = []

	def heal(self, ammount, variant):
		# Heal character

		if not self.dead:
			starting = -1
			heartCount = len(self.hearts)
			for i in range(heartCount):
				# Advance to the correct heart type
				if self.hearts[i].variant == variant:
					starting = i
					break

			# Catch heart overflow
			if starting == -1:
				return 2

			# Track the leftover ammount for heart
			leftover = self.hearts[starting].add(ammount)

			# Loop and add hearts
			for i in range(starting, heartCount):	
				if leftover <= 0:
					break
				else:
					heart = self.hearts[i]
					leftover = heart.add(leftover) # Heart overflow

					if leftover != 0 and variant != 0 and (i == heartCount-1 or self.hearts[i+1].variant != variant): 
							return leftover

			return True

	def clearTears(self):
		self.tears = []

	def hurt(self, ammount, enemyX, enemyY, time):

		if time-self.lastHurt < 1:
			return

		self.sounds[randint(0,1)].play() # Play random hurt sound

		leftover = self.hearts[-1].damage(1) # Hurt the last heart
		for i in range(len(self.hearts)-1, -1, -1):
			if type(leftover) == bool and leftover: # If the heart should be removed
				del self.hearts[i] 
				break
			else:
				if leftover <= 0:
					break # There is no longer a need to take health away
				else:
					if i == 0 and self.hearts[i].health == 1: # Check number of hearts
						self.dead = True
					leftover = self.hearts[i].damage(leftover) # damage

		# Character push back
		if enemyX != None and enemyY != None:
			# Push the character away from where they were hurt

			dx, dy = ((enemyX-self.x)*-1, (enemyY-self.y)*-1)
			angle = atan2(dy, dx) # Reverse it!

			pConst = 2

			# Add the direction to the X and Y velocity
			self.xVel += pConst*cos(angle)
			self.yVel += pConst*sin(angle)

		self.lastHurt = time

		# Set character to hurt look
		self.specialFrame = 2

		# Check if character should die
		if self.hearts[0].health == 0:
			self.die()

	def usePill(self):
		if self.pill != None: # Ensure the character has a pill

			self.pill.use(self) # Pass in the character to check for PHD
			st = self.pill.stats # The pills statss
			types = ["Speed", "Tears", "Damage", "Range", "Shot Speed", "Luck"] # The types of pills
			if sum(st) == -1:
				# Its a negative pill
				self.game.banners.append(Banner(types[st.index(-1)] + " Down", self.game.textures))
			else:
				# Its a positive pill
				self.game.banners.append(Banner(types[st.index(1)] + " Up", self.game.textures))

			# Add all the stats
			self.speed += st[0]
			self.shotRate += st[1]
			self.damage += st[2]
			self.range += st[3]
			self.shotSpeed += st[4]
			self.luck += st[5]
			
			# Destroy pill
			self.pill = None

	def die(self):
		self.dead = True

	def updateVel(self):
		# Update the X and Y velocity

		if self.up:
			self.yVel += -0.15

		if self.down:
			self.yVel += 0.15

		if self.left:
			self.xVel += -0.15

		if self.right:
			self.xVel += 0.15

		# Ensure you cant click 2 oppisite directions at the same time
		if (not self.left) and (not self.right) or (self.left and self.right):
			self.xVel *= 0.85

		if (not self.up) and (not self.down) or (self.up and self.down):
			self.yVel *= 0.85

		# Cap the maximum velocity
		if abs(self.xVel) > 1:
			self.xVel = 1 if self.xVel > 0 else -1

		if abs(self.yVel) > 1:
			self.yVel = 1 if self.yVel > 0 else -1


		# Reset head texture
		if self.xVel == 0 and self.yVel == 0:
			self.head = self.heads[0]

	def moving(self, key, value, joystick):
		# Find correct key
		try:
			index = self.moveKeys.index(key)
		except:
			try:
				index = self.tearKeys.index(key)
				if value:
					self.lastTearKey = index
					self.lastTearKeys.append(index)
				else:
					self.lastTearKeys.remove(index)
			except:
				pass
			return

		# Set direction
		if index == 0:
			self.down = value
		elif index == 1:
			self.right = value
		elif index == 2:
			self.up = value
		elif index == 3:
			self.left = value

		# Set the last key down and add to down keys
		if value:
			self.lastKey = index
			self.lastKeys.append(index)
		else:
			try:
				# Attempt to remove an up key
				self.lastKeys.remove(index)
			except:
				pass

		# Reset head
		if len(self.lastKeys) > 0:
			self.head = self.heads[self.lastKeys[-1]]
		else:
			self.head = self.heads[0]

		if len(self.lastTearKeys) > 0:
			self.head = self.heads[self.lastTearKeys[-1]]

	def step(self, time):
		xVel = round(abs(self.xVel), 1)
		yVel = round(abs(self.yVel), 1)

		if xVel > 0.1 or yVel > 0.1:
			# The character will be still (creating a sliding effect)

			if all([not self.down, not self.right, not self.up, not self.left]):
				# No keys are down

				self.head = self.heads[0]

			# Reset body
			if len(self.lastKeys) > 0:
				self.body = self.feet[self.lastKeys[-1]][int(self.walkIndex)]
			else:
				self.body = self.feet[self.lastKey][int(self.walkIndex)]

			self.walkIndex += 1

			if self.walkIndex >= len(self.feet[0]):
				# Reset foot frame
				self.walkIndex = 0
		else:
			self.walkIndex = 0
			self.head = self.heads[0]
			self.body = self.feet[0][0]

		# When you remove a key, set position to latest key down
		if len(self.lastKeys) > 0 and (xVel > 0.1 or yVel > 0.1):
			self.head = self.heads[self.lastKeys[-1]]
			self.body = self.feet[self.lastKeys[-1]][int(self.walkIndex)]
		else:
			self.head = self.heads[0]

		# Fix head
		if len(self.lastTearKeys) > 0:
			self.head = self.heads[self.lastTearKeys[-1]]


	def render(self, surface, time, bounds, obsticals, doors):
		move = [0,0] # Which direction on the map to move

		# Move feet when necesarry
		if time-self.lastAnimate >= self.interval:
			self.lastAnimate = time
			self.step(time)

		# Allow for Arm lift and Hurt animation
		if self.specialFrame == 2 and time-self.lastHurt >= 0.22:
			self.specialFrame = 0
		elif self.specialFrame == 1 and time-self.lastPickup >= 0.5:
			self.specialFrame = 0

		# Spawn a tear in the correct direction
		if self.lastTearKey in self.lastTearKeys and time-self.lastTear >= (8-self.shotRate)/18:
			self.tears.append(Tear([(0, 1), (1, 0), (0, -1), (-1, 0)][self.lastTearKey], (self.x, self.y-20), (self.xVel*1.5, self.yVel*1.5), self.shotSpeed, self.damage, self.range, True, self.tearTextures, self.tearSounds))
			self.lastTear = time
		elif time-self.lastTear <= 0.1:
			try:
				# Set the head to favor the tear
				self.head = self.tearHeads[self.heads.index(self.head)]
			except:
				pass
		else:
			try:
				self.head = self.heads[self.tearHeads.index(self.head)]
			except:
				pass

		sizeModifier = 2.5 # Tear speed to grid ratio

		if sum(map(int, [self.left, self.right, self.up, self.down])) > 1:
			sizeModifier /= 1.414213 # So there is no benefit to going diagonal (sqrt(2))

		# Delta x and y
		dx = self.xVel * sizeModifier * (self.speed//2+1)
		dy = self.yVel * sizeModifier * (self.speed//2+1) 

		# Ensure the tear is within the level bounds
		inBoundsX = bounds.collidepoint(self.x+dx, self.y)
		inBoundsY = bounds.collidepoint(self.x, self.y+dy)

		rockColX = False
		rockColY = False

		for ob in obsticals:
			# Collide with ob
			try:
				if ob.destroyed:
					continue
			except:
				pass

			# Check collission with anything in the level
			rcx = ob.bounds.collidepoint(self.x+dx, self.y)
			rcy = ob.bounds.collidepoint(self.x, self.y+dy)
			if rcx:
				rockColX = rcx
			if rcy:
				rockColY = rcy

			# Bash out every possible tear collide
			if rcx or rcy:
				if type(ob) == Fire:
					self.hurt(1, None, None, time)
				elif type(ob) == Coin:
					self.pickups[0].add(ob.worth)
					ob.pickup()
				elif type(ob) == Key:
					if self.pickups[0].use(ob.price):
						self.pickups[2].add(1)
						ob.pickup()
				elif type(ob) == Bomb and not ob.shouldExplode:
					if self.pickups[0].use(ob.price):
						self.pickups[1].add(1)
						ob.pickup()
				elif type(ob) == Heart:
					if self.pickups[0].use(ob.price):
						amm = self.heal(ob.health, ob.variant)
						if amm == 0:
							self.hearts.append(UIHeart(ob.variant, ob.health, self.heartTextures))
						elif type(amm) == int:
							self.hearts.append(UIHeart(ob.variant, amm, self.heartTextures))
						ob.pickup()

						if ob.variant == 1: # Sould heart
							self.specialFrame = 1
							self.lastPickup = time
				elif type(ob) == Pill:
					if self.pickups[0].use(ob.price):
						self.pill = ob
						ob.pickup()
				elif type(ob) == PHD:
					if self.pickups[0].use(ob.price):
						self.items.append(ob)
						ob.pickup()
				elif type(ob) == Trapdoor:
					self.game.floorIndex += 1
					self.game.currentRoom = (0,0)
					self.game.setup()
					self.game.updateFloor()
				if not ob.collideable and not rockColX and not rockColY:
					# Object not collideable
					rockColX = rockColY = False

		# Moves x and y
		mx = [0, 1, 0, -1]
		my = [-1, 0, 1, 0]

		# Render doors
		for i in range(len(doors)):
			door = doors[i]

			# Dont allow walking through closed doors
			if not door.isOpen:
				continue

			# Door collision
			dcx = door.rect.collidepoint(self.x+dx, self.y)
			dcy = door.rect.collidepoint(self.x, self.y+dy)

			# If youre in a locked room with 1 exit, unlock the doors
			if len(doors) == 1 and door.locked:
				door.locked = False

			# Unlocking doors
			if door.locked and self.pickups[2].score > 0 and (dcx or dcy):
				door.locked = False
				self.pickups[2].score -= 1
				continue

			# Stop you from walking through locked doors
			if door.locked:
				continue

			# Door collission x and y
			if dcx:
				self.x += dx

			if dcy:
				self.y += dy

			side = door.side

			# Try to walk throught the door
			if not dcx or not dcy:
				if sum(map(int, [
						mx[side] < 0 and door.rect.x-(self.x+dx) > 0,
						mx[side] > 0 and door.rect.x+door.rect.w-(self.x+dx) < 0,
						my[side] > 0 and door.rect.y-(self.y+dy) > 0,
						my[side] < 0 and door.rect.y+door.rect.h-(self.y+dy) < 0,
					])) == 1:
					move[0] = mx[side]
					move[1] = my[side]
					break

		# Move character 
		self.x += dx if	inBoundsX and (not rockColX or self.isFlying) else 0
		self.y += dy if inBoundsY and (not rockColY or self.isFlying) else 0

		# Update characters body rect
		self.bodyRect = Rect(self.x-16, self.y, 32, 16) # Move body rect

		# Update velocity
		self.updateVel()
		
		# Draw characters special frame
		if self.specialFrame == 0:
			surface.blit(self.body, (self.x-32, self.y-32))
			surface.blit(self.head, (self.x-32, self.y-32-20))
		else:
			surface.blit(self.specialFrames[self.specialFrame-1], (self.x-64, self.y-72))

		# Render tears
		for tear in self.tears[:]:
			if not tear.render(surface, time, bounds, obsticals):
				self.tears.remove(tear)

		for i in range(len(self.hearts)):
			self.hearts[i].render(surface, i)

		for p in self.pickups:
			p.render(surface)

		if self.pill != None:
			surface.blit(self.pill.texture, (WIDTH-80, HEIGHT-60))

		for item in self.items:
			item.renderCorner(surface)


		return move
