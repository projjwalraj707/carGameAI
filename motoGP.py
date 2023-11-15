import pygame

class MotoGPGame:

	def __init__(self):
		pass

if __name__ == '__main__':
	game = MotoGPGame()
	while True:
		game.play_step()
	pygame.quit()