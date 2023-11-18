import pygame
from collections import deque
pygame.init()
display = pygame.display.set_mode((400, 200))
RED = (200, 0, 0)
path = set()
centerX = 150
centerY = 40

def isInside(topLoc, x, y, rad):
	dist2 = (topLoc[0]-x)**2 + (topLoc[1]-y)**2
	if dist2<=rad**2:
		return True
	return False

def bfs():
	global path
	q = deque()
	q.append((centerX, centerY))
	while len(q):
		topLoc = q.popleft()
		if topLoc in path or not isInside(topLoc, centerX, centerY, 20):
			continue
		path.add(topLoc)
		q.append((topLoc[0] + 1, topLoc[1]))
		q.append((topLoc[0] - 1, topLoc[1]))
		q.append((topLoc[0], topLoc[1] + 1))
		q.append((topLoc[0], topLoc[1] - 1))

bfs()
while True:
	for ele in path:
		pygame.draw.circle(display, RED, ele, 1)
	pygame.display.flip()