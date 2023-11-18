from collections import deque
import heapq
import pygame
DISPLAY_WIDTH = 1350
DISPLAY_HEIGHT = 700
ROAD_OFFSET = 40 # offset from the center of the road i.e offset = road_width/2

display_pixels = DISPLAY_HEIGHT*[DISPLAY_WIDTH*[10000]]
# this data structure contains data about whether a pixel lies on raod or grass
# if display_pixels[x][y] = 0, (x, y) pixel is grass
# else it is a road

# track_line contains the midPoint of the track
track_line = set()
with open('TrackLine.txt', 'r') as file:
	contents = file.read()
	track_line = set(eval(contents))
# Now add these points to priority_queue
pq = []
for x in track_line:
	pq.append((0, x[0], x[1]))
	display_pixels[x[1]][x[0]] = 0
heapq.heapify(pq)


# def dijkstra():
# 	global display_pixels

pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
while True:
	for i in range(len(display_pixels)):
		for j in range(len(display_pixels[i])):
			if display_pixels[i][j] == 0:
				print((j, i))
				pygame.draw.circle(display, (200, 0, 0), (j, i), 1)
	pygame.display.flip()


# def isInside(topLoc, mid_pixel):
# 	distSq = (topLoc[0]-mid_pixel[0])**2 + (topLoc[1]-mid_pixel[1])**2
# 	if distSq <= ROAD_OFFSET**2:
# 		return True
# 	return False

# def bfs(mid_pixel):
# 	global display_pixels
# 	path = set()
# 	q = deque()
# 	q.append(mid_pixel)
# 	while len(q):
# 		topLoc = q.popleft()
# 		if topLoc in path or not isInside(topLoc, mid_pixel):
# 			continue
# 		path.add(topLoc)
# 		q.append((topLoc[0] + 1, topLoc[1]))
# 		q.append((topLoc[0] - 1, topLoc[1]))
# 		q.append((topLoc[0], topLoc[1] + 1))
# 		q.append((topLoc[0], topLoc[1] - 1))
# 	# print(path)
# 	for ele in path:
# 		display_pixels[ele[1]][ele[0]] = 1

# for mid_pixel in track_line:
# 	bfs(mid_pixel)