import pygame
import math
# import Enum
pygame.init()

CLOCK_SPEED = 60
BLOCK_SIZE = 10
BIKE_WIDTH = 15
BIKE_HEIGHT = 30
HEAD_RAD = 4
#Defining Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 250)
BLUE2 = (0, 0, 120)

class Point:
	def __init__(self, x, y):
		self.x=0
		self.y=0

class Bike:
	def __init__(self, x, y, tilt = 25):
		self.center = [x, y] # coordinates of the center of the bike
		self.width = BIKE_WIDTH
		self.height = BIKE_HEIGHT
		self.tilt = tilt #angle of tilt of the bike
	
	def polygonify2(self):
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
	def head(self):
		headX = self.center[0]
		headY = self.center[1]+BIKE_HEIGHT*0.35
		pp = pygame.math.Vector2((self.center[0], self.center[1]))
		return (pygame.math.Vector2(headX, headY) - pp).rotate(self.tilt) + pp


class MotoGPGame:
	def __init__(self, w=1350, h=700):
		self.w = w
		self.h = h
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption("MotoGP")
		self.clock = pygame.time.Clock()
		self.bike1 = Bike(w/2, h/2)
		# self.head = Point(w/2, h/2)
		# self.bike = [self.head,
		# 			Point(self.head.x-BLOCK_SIZE, self.head.y), 
		# 			Point(self.head.x-2*BLOCK_SIZE, self.head.y)]

	def play_step(self):
		#1. Collecting user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.bike1.tilt = self.bike1.tilt - 1
				elif event.key == pygame.K_RIGHT:
					self.bike1.tilt = self.bike1.tilt + 1
		#update UI and Clock
		self.update_ui()
		self.clock.tick(CLOCK_SPEED)

	def update_ui(self):
		self.display.fill(BLACK)
		pygame.draw.polygon(self.display, BLUE1, self.bike1.polygonify2())
		pygame.draw.circle(self.display, RED, self.bike1.head(), HEAD_RAD)
		pygame.display.flip()


if __name__ == '__main__':
	game = MotoGPGame()
	while True:
		game.play_step()
	pygame.quit()