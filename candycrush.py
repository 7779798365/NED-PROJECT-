import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
TILE_SIZE = 60
GRID_SIZE = 8
FPS = 60

COLORS = {
    'R': (255, 0, 0),
    'G': (0, 255, 0),
    'B': (0, 0, 255),
    'Y': (255, 255, 0),
    'P': (255, 0, 255),
    'O': (255, 165, 0),
    'W': (255, 255, 255)
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush")
clock = pygame.time.Clock()

grid = [[random.choice(list(COLORS.keys())[:-1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

selected = None
score = 0

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2)
            pygame.draw.rect(screen, COLORS[grid[y][x]], rect)
            pygame.draw.rect(screen, COLORS['W'], rect, 1)

def find_matches():
    matches = set()
    

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y][x+1] == grid[y][x+2]:
                matches.update([(x, y), (x+1, y), (x+2, y)])
    
    # Check vertical matches
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y+1][x] == grid[y+2][x]:
                matches.update([(x, y), (x, y+1), (x, y+2)])
    
    return matches

def remove_matches(matches):
    global score
    for x, y in matches:
        grid[y][x] = None
    score += len(matches) * 100

def drop_candies():
    for x in range(GRID_SIZE):
        column = [grid[y][x] for y in range(GRID_SIZE) if grid[y][x] is not None]
        column = column + [random.choice(list(COLORS.keys())[:-1]) for _ in range(GRID_SIZE - len(column))]
        for y in range(GRID_SIZE):
            grid[y][x] = column[y]

def swap_tiles(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]

def is_adjacent(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) == 1


running = True
while running:
    screen.fill(COLORS['W'])
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = x // TILE_SIZE
            grid_y = y // TILE_SIZE
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                if selected is None:
                    selected = (grid_x, grid_y)
                else:
                    if is_adjacent(selected, (grid_x, grid_y)):
                        swap_tiles(selected, (grid_x, grid_y))
                        matches = find_matches()
                        if not matches:

                            swap_tiles(selected, (grid_x, grid_y))
                        else:
                            while matches:
                                remove_matches(matches)
                                drop_candies()
                                matches = find_matches()
                        selected = None
                    else:
                        selected = (grid_x, grid_y)
    
    draw_grid()
    

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, COLORS['W'])
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()