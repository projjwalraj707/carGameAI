import math
import torch
import numpy as np
from road import display_pixels
import pygame
pygame.init()

#ENVIRONMENT
TRACK_IMG = pygame.image.load("img/TRACK.png")
FINISH_LINE = pygame.image.load("img/race_flag_start.png")
FINISH_LINE = pygame.transform.scale(FINISH_LINE, (80, 50))
FINISH_LINE = pygame.transform.rotate(FINISH_LINE, 90)
BIKE_WIDTH = 15
BIKE_HEIGHT = 30
HEAD_RAD = 4
START_Y = 700
START_X = 631

#PYGAME
CLOCK_SPEED = 60
BLOCK_SIZE = 10
DISPLAY_WIDTH = 1350
DISPLAY_HEIGHT = 700

#COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 250)
BLUE2 = (0, 0, 120)

class Bike:
	def __init__(self, x, y, tilt = 90):
		self.center = [x, y] # coordinates of the center of the bike
		self.width = BIKE_WIDTH
		self.height = BIKE_HEIGHT
		self.tilt = tilt #angle of tilt of the bike
		self.vertices = [(0, 0), (1, 1), (2, 2), (3, 3)]
		self.head = (0, 0)
		self.velocity = 0
		self.max_velocity = 7
		self.acc = 0.7
		self.drag = 0.05 #deceleration due to drag
		self.rotation = 3
		# self.visited = [[0] * DISPLAY_WIDTH for _ in range(DISPLAY_HEIGHT)]
		self.didCrashed = 0
		self.checkPoints = [0]*7
	
	def polygonify(self):
		x, y = self.center[1], self.center[0]
		pp = pygame.math.Vector2((x, y))
		points = (
			(x-BIKE_WIDTH/2, y+BIKE_HEIGHT/2),
			(x+BIKE_WIDTH/2, y+BIKE_HEIGHT/2),
			(x+BIKE_WIDTH/2, y-BIKE_HEIGHT/2),
			(x-BIKE_WIDTH/2, y-BIKE_HEIGHT/2),
		)
		return [
			(pygame.math.Vector2(a, b) - pp).rotate(self.tilt) + pp for a, b in points
		]

	def findHead(self):
		headX = self.center[1]
		headY = self.center[0]-BIKE_HEIGHT*0.25
		pp = pygame.math.Vector2((self.center[1], self.center[0]))
		return (pygame.math.Vector2(headX, headY) - pp).rotate(self.tilt) + pp
	
	def accelerate(self):
		self.velocity += self.acc
		self.velocity = min(self.velocity, self.max_velocity)

	def decelerate(self):
		self.velocity -= self.acc
		self.velocity = max(self.velocity, -self.max_velocity)
	
	def goBack(self, isNeg):
		x = self.center[1]
		y = self.center[0]
		x += (1 if isNeg else -1)*2*(math.sin(math.pi*self.tilt/180))
		y -= (1 if isNeg else -1)*2*(math.cos(math.pi*self.tilt/180))
		x = min(x, DISPLAY_WIDTH-5)
		x = max(0, x)
		y = min(y, DISPLAY_HEIGHT-5)
		y = max(0, y)
		self.center = [y, x]

	def move(self):
		#Decrease velocity due to drag
		self.didCrashed = 0
		if self.velocity>0:
			self.velocity -= self.drag
			self.velocity = max(0, self.velocity) # make sure the velocity does not oscillate between -ve and +ve when it is standing still
		elif self.velocity<0:
			self.velocity += self.drag
			self.velocity = min(0, self.velocity)
			
		x = self.center[1]
		y = self.center[0]
		x += self.velocity*(math.sin(math.pi*self.tilt/180))
		y -= self.velocity*(math.cos(math.pi*self.tilt/180))
		x = min(x, DISPLAY_WIDTH-5)
		x = max(0, x)
		y = min(y, DISPLAY_HEIGHT-5)
		y = max(0, y)
		self.center = [y, x]
		if display_pixels[int(self.center[0])][int(self.center[1])] == (-1, -1):
			self.didCrashed = 1
			while display_pixels[int(self.center[0])][int(self.center[1])] == (-1, -1):
				isNeg = self.velocity<0
				self.goBack(isNeg)
			self.velocity = -self.velocity/2
		else:
			if self.center[1]>800:
				self.checkPoints[0] = 1
			if self.center[1]>1000:
				self.checkPoints[1] = 1
			if self.center[1]>1200:
				self.checkPoints[2] = 1
			if self.center[0]<=590 and self.center[1]>800:
				self.checkPoints[3] = 1

	def rotate(self, right):
		if (right == True):
			self.tilt += self.rotation
		else:
			self.tilt -= self.rotation
		self.tilt = self.tilt % 360
	
	def getReward(self):
		ans = -1 #negative reward with each frame
		
		#negative reward for not moving or moving in the back direction else positive reward
		if self.velocity<=0:
			ans -= 100
		else:
			ans += (self.velocity/7)*50

		# if not self.visited[int(self.center[0])][int(self.center[1])]:
		# 	ans += 20
		# 	self.visited[int(self.center[0])][int(self.center[1])] = 1
		
		#check for crashing condition
		if self.didCrashed == 1:
			ans -= 100

		#check distance from the center
		cX, cY = display_pixels[int(self.center[0])][int(self.center[1])]
		distFromCenter = math.sqrt((self.center[0]-cX)**2 + (self.center[1]-cY)**2)
		ans += (30-distFromCenter)*10

		# checkpoint-based reward
		ans += (sum(self.checkPoints))*80
		return ans

class MotoGPGame:
	def __init__(self, w=DISPLAY_WIDTH, h=DISPLAY_HEIGHT):
		self.w = w
		self.h = h
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption("MotoGP")
		self.clock = pygame.time.Clock()
		self.bike1 = Bike(START_X, START_Y)
		self.n_actions = 9 # total 9 actions can be taken for each step
		self.n_obs = 41 # size of state
	
	def reset(self):
		self.bike1 = Bike(START_X, START_Y)
		return self.getState()
	
	def getObsInfo(self, tilt): # returns the distance of the obstacle present at tilt degrees from the bike
		lastX, lastY = self.bike1.center[0], self.bike1.center[1]
		dist = 0
		foundObs = 0
		for i in range(1, 100, 3):
			dist += 3
			newX = self.bike1.center[0] + i*(math.sin(math.pi*tilt/180))
			newY = self.bike1.center[1] - i*(math.cos(math.pi*tilt/180))
			if newX<=0 or newY<=0 or newX>=DISPLAY_HEIGHT or newY>=DISPLAY_WIDTH or display_pixels[int(newX)][int(newY)] == (-1, -1):
				foundObs = 1
				break
			lastX, lastY = newX, newY
		
		if not foundObs:
			dist = 1000
		obsCenter = display_pixels[int(lastX)][int(lastY)]
		return (dist, math.atan2((lastY-obsCenter[1]), (lastX-obsCenter[0])))

	def getState(self):
		state = []
		for i in range(0, 360, 18):
			val = self.getObsInfo(self.bike1.tilt+i)
			state.append(val[0])
			state.append(val[1])
		state.append(self.bike1.velocity)
		return torch.tensor(state)



	def play_stepAI(self, action):
		self.display.blit(TRACK_IMG, (0, 0))
		self.display.blit(FINISH_LINE, (START_Y-23, START_X-37))
		#1. Collecting user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		if action == 0:
			#press w
			self.bike1.accelerate()
		elif action == 1:
			#press s
			self.bike1.decelerate()
		elif action == 2:
			#press a
			self.bike1.rotate(0)
		elif action == 3:
			#press d
			self.bike1.rotate(1)
		elif action == 4:
			#press w and a
			self.bike1.accelerate()
			self.bike1.rotate(0)
		elif action == 5:
			# press w and d
			self.bike1.accelerate()
			self.bike1.rotate(1)
		elif action == 6:
			#press s and a
			self.bike1.decelerate()
			self.bike1.rotate(0)
		elif action == 7:
			#press s and d
			self.bike1.decelerate()
			self.bike1.rotate(1)
		#else if nothing is pressed do nothing

		#update UI and Clock
		self.bike1.move()
		self.update_ui()
		self.clock.tick(CLOCK_SPEED)
		# return state, reward, done
		return self.getState(), self.bike1.getReward(), (1 if self.bike1.didCrashed else 0)

	def play_step(self):
		self.display.blit(TRACK_IMG, (0, 0))
		self.display.blit(FINISH_LINE, (START_Y-23, START_X-37))
		#1. Collecting user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]: # Only one of 'a' and 'd' will be registered
			self.bike1.rotate(0)
		elif keys[pygame.K_d]:
			self.bike1.rotate(1)
		if keys[pygame.K_w]: # Only one of 'w' and 's' will be registered
			print('hihiihhihihi')
			print(self.getObsInfo(self.bike1.tilt + 0))
			print(self.getObsInfo(self.bike1.tilt + 90))
			print(self.getObsInfo(self.bike1.tilt + 180))
			print(self.getObsInfo(self.bike1.tilt + 270))
			self.bike1.accelerate()
		elif keys[pygame.K_s]:
			self.bike1.decelerate()
		#update UI and Clock
		self.bike1.move()
		self.update_ui()
		self.clock.tick(CLOCK_SPEED)

	def update_ui(self):
		pygame.draw.polygon(self.display, BLUE1, self.bike1.polygonify())
		pygame.draw.circle(self.display, RED, self.bike1.findHead(), HEAD_RAD)
		pygame.display.flip()

if __name__ == '__main__':
	game = MotoGPGame()
	while True:
		game.play_step()
	pygame.quit()