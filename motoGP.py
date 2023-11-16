import pygame
import math
# import Enum
pygame.init()

CLOCK_SPEED = 60
BLOCK_SIZE = 10
BIKE_WIDTH = 15
BIKE_HEIGHT = 30
DISPLAY_WIDTH = 1350
DISPLAY_HEIGHT = 700
HEAD_RAD = 4
#Defining Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 250)
BLUE2 = (0, 0, 120)
TRACK_IMG = pygame.image.load("img/TRACK.png")

class Point:
	def __init__(self, x, y):
		self.x=0
		self.y=0

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
	
	def move(self):
		x = self.center[0]
		y = self.center[1]
		x += self.velocity*(math.sin(math.pi*self.tilt/180))
		y -= self.velocity*(math.cos(math.pi*self.tilt/180))
		x = min(x, DISPLAY_WIDTH-5)
		x = max(0, x)
		y = min(y, DISPLAY_HEIGHT-5)
		y = max(0, y)
		self.center = [x, y]

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
		self.bike1 = Bike(w/2, h/2)

	def play_step(self):
		#1. Collecting user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					self.bike1.rotate(0)
				elif event.key == pygame.K_d:
					self.bike1.rotate(1)
				elif event.key == pygame.K_w:
					self.bike1.accelerate()
				elif event.key == pygame.K_s:
					self.bike1.decelerate();
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			self.bike1.rotate(0)
		if keys[pygame.K_d]:
			self.bike1.rotate(1)
		if keys[pygame.K_w]:
			self.bike1.accelerate()
		elif keys[pygame.K_s]:
			self.bike1.decelerate()
		#update UI and Clock
		self.bike1.move()
		self.update_ui()
		self.clock.tick(CLOCK_SPEED)

	def update_ui(self):
		# self.display.fill(BLACK)
		pygame.draw.polygon(self.display, BLUE1, self.bike1.polygonify())
		pygame.draw.circle(self.display, RED, self.bike1.findHead(), HEAD_RAD)
		pygame.display.flip()


if __name__ == '__main__':
	game = MotoGPGame()
	while True:
		game.display.blit(TRACK_IMG, (0, 0))
		game.play_step()
	pygame.quit()