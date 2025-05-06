import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
PLAYER_SIZE = 50
ITEM_SIZE = 30
FPS = 60

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Items")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH//2, HEIGHT-PLAYER_SIZE*2, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 5

items = []
item_spawn_rate = 25  
item_speed = 3

score = 0
font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed


    if random.randint(1, item_spawn_rate) == 1:
        item_x = random.randint(0, WIDTH - ITEM_SIZE)
        items.append(pygame.Rect(item_x, 0, ITEM_SIZE, ITEM_SIZE))

    for item in items[:]:
        item.y += item_speed
        if item.colliderect(player):
            items.remove(item)
            score += 10
        elif item.y > HEIGHT:
            items.remove(item)

    screen.fill(BLACK)
    
    pygame.draw.rect(screen, BLUE, player)
    
    for item in items:
        pygame.draw.rect(screen, RED, item)
    
    draw_text(f"Score: {score}", WHITE, 10, 10)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()