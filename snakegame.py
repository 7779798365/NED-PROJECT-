import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

font = pygame.font.SysFont("Arial", 25)

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(win, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def message(msg, color, x, y):
    text = font.render(msg, True, color)
    win.blit(text, [x, y])

def game_loop():
    game_over = False
    game_close = False

    x = WIDTH // 2
    y = HEIGHT // 2
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            win.fill(WHITE)
            message("Game Over! Press C to Play Again or Q to Quit", RED, 50, HEIGHT // 2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0

        x += x_change
        y += y_change

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        win.fill(WHITE)
        pygame.draw.rect(win, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        message(f"Score: {snake_length - 1}", BLACK, 10, 10)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()