import heapq
DISPLAY_WIDTH = 1350
DISPLAY_HEIGHT = 700
ROAD_OFFSET = 40 # offset from the center of the road i.e offset = road_width/2

#track_line contains coordiantes of road's center
track_line = set()
with open('TrackLine.txt', 'r') as f:
	contents = f.read()
	track_line = set(eval(contents))


# this data structure contains data about whether a pixel lies on the raod or grass
display_pixels = [[(-1, -1)] * DISPLAY_WIDTH for _ in range(DISPLAY_HEIGHT)]
# if display_pixels[x][y] = 0, (x, y) pixel is grass
# else it is road

#create a priority queue for Dijkstra
pq = []

class CustomComparator:
	def __init__(self, val):
		self.val = val
	def __lt__(self, other):
		selfDist = (self.val[0]-self.val[2])**2 + (self.val[1]-self.val[3])**2
		otherDist = (other.val[0]-other.val[2])**2 + (other.val[1]-other.val[3])**2
		return selfDist<otherDist

for ele in track_line:
	display_pixels[ele[1]][ele[0]] = (ele[1], ele[0])
	heapq.heappush(pq, CustomComparator((ele[1], ele[0], ele[1], ele[0]))) # centerX, centerY, locX, locY

a = [0, 0, 1, -1]
b = [1, -1, 0, 0]

def dist(nxtX, nxtY, c):
	return (nxtX-c[0])**2 + (nxtY-c[1])**2

def Dijkstra():
	print("starting dijkstra")
	global display_pixels
	while len(pq):
		cX, cY, x, y = list(heapq.heappop(pq).val) # centerX, centerY, pixelX, pixelY
		if display_pixels[x][y] != (cX, cY):
			continue
		for i in range(4):
			nxtX, nxtY = x+a[i], y+b[i]
			if (display_pixels[nxtX][nxtY] == (-1, -1) or dist(nxtX, nxtY, display_pixels[nxtX][nxtY]) > dist(nxtX, nxtY, (cX, cY))) and dist(nxtX, nxtY, (cX, cY))<ROAD_OFFSET**2:
				display_pixels[nxtX][nxtY] = (cX, cY)
				heapq.heappush(pq, CustomComparator((cX, cY, nxtX, nxtY)))
	print("dijkstra ends here")


# Dijkstra()
# print(display_pixels)

if __name__ == '__main__':
	import pygame
	pygame.init()
	display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
	while True:
		for i in range(DISPLAY_HEIGHT):
			for j in range(DISPLAY_WIDTH):
				if display_pixels[i][j] != (-1, -1):
					pygame.draw.circle(display, (200, 0, 0), (j, i), 1)
			pygame.display.flip()