import pygame
import random

dark_blue = pygame.Color(69, 98, 180)
light_blue = pygame.Color(69, 150, 180)

num_rows = 16
num_cols = 16
cell_size = 32
num_mines = 40


mine_grid = [[0] * num_cols for _ in range(num_rows)]
click_grid = [[False] * num_cols for _ in range(num_rows)]

window_width = num_cols * cell_size
window_height = num_rows * cell_size

pygame.init()

font_path = pygame.font.match_font("liberationmono")
font_size = cell_size - 2
font = pygame.font.Font(font_path, font_size)
numbers_text = font.render("12345678", True, "black", "gray") 
numbers_text_rect = numbers_text.get_rect()
number_width = numbers_text_rect.width / 8

screen = pygame.display.set_mode((window_width,window_height))
clock = pygame.time.Clock()
running = True

def place_mines():
    mines_placed = 0
    while mines_placed < num_mines:
        x = random.randrange(num_cols)
        y = random.randrange(num_rows)

        if mine_grid[y][x] >= 0:
            mines_placed += 1
            mine_grid[y][x] = -9
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i+x >= 0 and i+x < num_cols and j+y >= 0 and j+y < num_rows and (i != 0 or j != 0):
                        mine_grid[j+y][i+x] += 1



place_mines()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render game here
    screen.fill("black")

    for r in range(num_rows):
        for c in range(num_cols):
            tile = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
            if click_grid[r][c]:

                hint = mine_grid[r][c]
                if hint > 0:
                    offset = (hint - 1) * number_width
                    number_mask = pygame.Rect(offset, 0, number_width, numbers_text_rect.height)
                    left_padding = (cell_size - number_width) / 2
                    tile.left += left_padding
                    screen.blit(numbers_text, tile, number_mask)
                elif hint == 0:
                    pygame.draw.rect(screen, "gray", tile)
                    pygame.draw.rect(screen, "black", tile, 1)
                else:
                    # bomb
                    pygame.draw.rect(screen, "red", tile)
            else:
                color = light_blue if (r + c) % 2 == 0 else dark_blue
                pygame.draw.rect(screen, color, tile)
            

    pygame.display.flip()

    clock.tick(60) # locks the game to 60fps

pygame.quit()
