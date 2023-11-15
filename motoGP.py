import pygame
# import Enum
pygame.init()

CLOCK_SPEED = 60
BLOCK_SIZE = 40
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

class MotoGPGame:
	def __init__(self, w=640, h=480):
		self.w = w
		self.h = h
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption("MotoGP")
		self.clock = pygame.time.Clock()
		self.head = Point(w/2, h/2)
		self.bike = [self.head,
					Point(self.head.x-BLOCK_SIZE, self.head.y), 
					Point(self.head.x-2*BLOCK_SIZE, self.head.y)]

	def play_step(self):
		#update UI and Clock
		self.update_ui()
		self.clock.tick(CLOCK_SPEED)

	def update_ui(self):
		self.display.fill(BLACK)
		for pt in self.bike:
			pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
			pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, BLOCK_SIZE/2, BLOCK_SIZE/2))
		pygame.display.flip()



if __name__ == '__main__':
	game = MotoGPGame()
	while True:
		game.play_step()
	pygame.quit()