# I use the terms Tile and Cells interchangeably in the comments. Both mean the same thing
# A tile or cell refers to the square or rectangle shape which can be clicked by the user

import pygame
import random

pygame.init()

# Color Values (The 3 values in the tuple are for RGB - Red, Green, Blue)
# The Max value for RGB is 255 and minimum is 0. Therefore, Black is 000, Grey is 128,128,128 and Yellow is 255,255,0
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Choosing the size of screen, the grid rows & columns, the tiles, and the speed at which the game runs
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH//TILE_SIZE
GRID_HEIGHT = HEIGHT//TILE_SIZE
FPS = 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def gen(num): # Generates random number of tiles to be used when user presses "G" on keyboard
	return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(positions): # Draws grids and creates rectangular tiles on the screen
	for position in positions:
		col, row = position
		top_left = (col * TILE_SIZE, row * TILE_SIZE)
		pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE)) # creates tiles in the grids

	for row in range(GRID_HEIGHT): #Draws horizontal lines
		pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

	for col in range(GRID_WIDTH): #Draws vertical lines
		pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjust_grid(positions): # Decides if a tile should remain alive or dead based on the rules
	all_neighbours = set()
	new_positions = set()

	for position in positions: # Fetches and updates neighbours
		neighbours = get_neighbours(position)
		all_neighbours.update(neighbours)

		# Gets list of neighbours which are alive
		neighbours = list(filter(lambda x: x in positions, neighbours))

		# If a tile has 2 or 3 alive neighours, it is kept alive in next round
		if len(neighbours) in [2, 3]:
			new_positions.add(position)

	# Checks neighbours of dead cells
	for position in all_neighbours:
		neighbours = get_neighbours(position)
		neighbours = list(filter(lambda x: x in positions, neighbours))

		# If dead cells have exactly 3 alive neighours, they become alive in next round
		if len(neighbours) == 3:
			new_positions.add(position)

	return new_positions

def get_neighbours(pos): # returns all neighbours of a tile
	x, y = pos # Current position
	neighbours = []
	for dx in [-1, 0, 1]: # Displacement in x
		if x + dx < 0 or x + dx > GRID_WIDTH: # ignores neighbours of corner cells which lie outside the display screen
			continue
		for dy in [-1, 0, 1]: # Displacement in y
			if y + dy < 0 or y + dy > GRID_HEIGHT: # ignores neighbours of corner cells which lie outside the display screen
				continue
			if dx == 0 and dy == 0: # Centre Position does not count
				continue

			neighbours.append((x + dx, y + dy))

	return neighbours

def main(): # This loop will be running constantly and checking for button presses
	running = True
	playing = False
	count = 0
	update_freq = 150 # How frequently the screen is updated

	positions = set()
	while running:
		clock.tick(FPS) # Regulates speed of while loop

		if playing:
			count += 1

		if count >= update_freq:
			count = 0
			positions = adjust_grid(positions)

		pygame.display.set_caption("Playing" if playing else "Paused") # Text displayed if game is paused or playing

		for event in pygame.event.get(): # Is user exits the game window
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN: # Detecting Mouse click on tiles
				x, y = pygame.mouse.get_pos()
				col = x//TILE_SIZE
				row = y//TILE_SIZE
				pos = (col, row)

				if pos in positions: # Deselecting the tile
					positions.remove(pos)
				else:
					positions.add(pos) # Selecting the tile

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					playing = not playing

				if event.key == pygame.K_c: # clears the entire screen
					positions = set()
					playing = False
					count = 0

				if event.key == pygame.K_g: # Randomly generates populated tiles in the grid
					positions = gen(random.randrange(4, 10) * GRID_WIDTH)

		screen.fill(GREY) # Setting the background color of screen as Grey
		draw_grid(positions) # Drawing Grids on top of Grey Background
		pygame.display.update()

	pygame.quit() # Closing game window

if __name__ == "__main__": # Only running main function if script is executed directly
	main()
