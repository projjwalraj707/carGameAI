import math
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
START_X = 700
START_Y = 631

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
		self.acc = 0.1
		self.drag = 0.05 #deceleration due to drag
		self.rotation = 3
	
	def polygonify(self):
		x, y = self.center[0], self.center[1]
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
		headX = self.center[0]
		headY = self.center[1]-BIKE_HEIGHT*0.25
		pp = pygame.math.Vector2((self.center[0], self.center[1]))
		return (pygame.math.Vector2(headX, headY) - pp).rotate(self.tilt) + pp
	
	def accelerate(self):
		self.velocity += self.acc
		self.velocity = min(self.velocity, self.max_velocity)

	def decelerate(self):
		self.velocity -= self.acc
		self.velocity = max(self.velocity, -self.max_velocity)
	
	def goBack(self, isNeg):
		x = self.center[0]
		y = self.center[1]
		x += (1 if isNeg else -1)*2*(math.sin(math.pi*self.tilt/180))
		y -= (1 if isNeg else -1)*2*(math.cos(math.pi*self.tilt/180))
		x = min(x, DISPLAY_WIDTH-5)
		x = max(0, x)
		y = min(y, DISPLAY_HEIGHT-5)
		y = max(0, y)
		self.center = [x, y]

	def move(self):
		#Decrease velocity due to drag
		if self.velocity>0:
			self.velocity -= self.drag
			self.velocity = max(0, self.velocity) # make sure the velocity does not oscillate between -ve and +ve when it is standing still
		elif self.velocity<0:
			self.velocity += self.drag
			self.velocity = min(0, self.velocity)
			
		x = self.center[0]
		y = self.center[1]
		x += self.velocity*(math.sin(math.pi*self.tilt/180))
		y -= self.velocity*(math.cos(math.pi*self.tilt/180))
		x = min(x, DISPLAY_WIDTH-5)
		x = max(0, x)
		y = min(y, DISPLAY_HEIGHT-5)
		y = max(0, y)
		self.center = [x, y]
		if display_pixels[int(self.center[1])][int(self.center[0])] == (-1, -1):
			while display_pixels[int(self.center[1])][int(self.center[0])] == (-1, -1):
				isNeg = self.velocity<0
				self.goBack(isNeg)
			self.velocity = -self.velocity/2

	def rotate(self, right):
		if (right == True):
			self.tilt += self.rotation
		else:
			self.tilt -= self.rotation
		self.tilt = self.tilt % 360

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

	def getObsInfo(self, tilt): # returns the distance of the obstacle present at tilt degrees from the bike
		lastX, lastY = self.bike1.center[0], self.bike1.center[1]
		dist = 0
		for i in range(100):
			dist += 1
			newX = self.bike1.center[0] + i*(math.sin(math.pi*tilt/180))
			newY = self.bike1.center[1] - i*(math.cos(math.pi*tilt/180))
			if display_pixels[newY][newX] == (-1, -1) or newX<=0 or newY<=0 or newX>=DISPLAY_WIDTH or newY>=DISPLAY_HEIGHT:
				break
			lastX, lastY = newX, newY
		obsCenter = display_pixels[lastY][lastX]
		
		return (dist, ())
		

	def play_step(self):
		game.display.blit(TRACK_IMG, (0, 0))
		game.display.blit(FINISH_LINE, (START_X-23, START_Y-37))
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