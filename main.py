import pygame
import random
import math

num_rows = 14
num_cols = 16
cell_size = 32
num_mines = 35

window_width = num_cols * cell_size
window_height = num_rows * cell_size

mine_grid = [[0] * num_cols for _ in range(num_rows)]
click_grid = [[False] * num_cols for _ in range(num_rows)]
waiting_for_first_click = True

dark_blue = pygame.Color(69, 98, 180)
dark_blue_border = pygame.Color(41, 58, 108)
light_blue = pygame.Color(69, 150, 180)
light_blue_border = pygame.Color(41, 90, 108)

pygame.init()

font_path = pygame.font.match_font("liberationmono")
font_size = cell_size - 2
font = pygame.font.Font(font_path, font_size)
numbers_text = font.render("12345678", True, "black", "gray") 
numbers_text_rect = numbers_text.get_rect()
number_width = numbers_text_rect.width / 8

flag_image = pygame.image.load("flag.png")

screen = pygame.display.set_mode((window_width,window_height))
clock = pygame.time.Clock()
running = True

def reset_game():
    global waiting_for_first_click
    waiting_for_first_click = True
    for r in range(num_rows):
        for c in range(num_cols):
            mine_grid[r][c] = 0
            click_grid[r][c] = False

def place_mines(safe_x, safe_y):
    mines_placed = 0
    while mines_placed < num_mines:
        x = random.randrange(num_cols)
        y = random.randrange(num_rows)

        if (abs(safe_x - x) > 2 or abs(safe_y - y) > 2) and mine_grid[y][x] >= 0:
            mines_placed += 1
            mine_grid[y][x] = -10
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i+x >= 0 and i+x < num_cols and j+y >= 0 and j+y < num_rows and (i != 0 or j != 0):
                        mine_grid[j+y][i+x] += 1


def dig_mine(x, y):
    global waiting_for_first_click
    if waiting_for_first_click:
        waiting_for_first_click = False
        place_mines(mx, my)
    click_grid[y][x] = True
    if mine_grid[y][x] < 0:
        reset_game()
    elif mine_grid[y][x] == 0:
        for i in range(-1, 2):
            for j in range(-1,2):
                if x+i>=0 and x+i<num_cols and \
                    y+j>=0 and y+j<num_rows and \
                    (i != 0 or j != 0) and click_grid[y+j][x+i] == False:
                    dig_mine(x+i, y+j)


def dig_pressed(event):
    return (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_f)

def flag_pressed(event):
    return (event.type == pygame.MOUSEBUTTONUP and event.button == 2) or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_d)

reset_game()



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif dig_pressed(event):
            mx, my = [math.floor(coord / cell_size) for coord in pygame.mouse.get_pos()]
            if click_grid[my][mx] != "flagged":
                dig_mine(mx, my)
        elif flag_pressed(event):
            mx, my = [math.floor(coord / cell_size) for coord in pygame.mouse.get_pos()]
            if click_grid[my][mx] != True:
                click_grid[my][mx] = "flagged" if click_grid[my][mx] == False else False

    

    # render game here
    screen.fill("black")

    mx, my = [math.floor(coord / cell_size) for coord in pygame.mouse.get_pos()]

    for r in range(num_rows):
        for c in range(num_cols):
            tile = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
            if click_grid[r][c] == True:
                hint = mine_grid[r][c]
                if hint > 0:
                    pygame.draw.rect(screen, "gray", tile)
                    offset = (hint - 1) * number_width
                    number_mask = pygame.Rect(offset, 0, number_width, numbers_text_rect.height)
                    left_padding = (cell_size - number_width) / 2
                    tile.left += left_padding
                    screen.blit(numbers_text, tile, number_mask)
                    tile.left -= left_padding
                    pygame.draw.rect(screen, "black", tile, 1)
                elif hint == 0:
                    pygame.draw.rect(screen, "gray", tile)
                    pygame.draw.rect(screen, "black", tile, 1)
                else:
                    # bomb
                    pygame.draw.rect(screen, "red", tile)
            else:
                if (r + c) % 2 == 0:
                    color = light_blue
                    border_color = light_blue_border
                else:
                    color = dark_blue
                    border_color = dark_blue_border
                pygame.draw.rect(screen, color, tile)
                pygame.draw.rect(screen, border_color, tile, 3)

                if click_grid[r][c] == "flagged":
                    screen.blit(flag_image, (c*cell_size, r*cell_size))

    mouse_rect = pygame.Rect(mx*cell_size, my*cell_size, cell_size, cell_size)
    mouse_box_surface = pygame.Surface((cell_size, cell_size))
    mouse_box_surface.set_alpha(40)
    mouse_box_surface.fill((0, 0, 0))
    screen.blit(mouse_box_surface, (mx*cell_size, my*cell_size))

    pygame.display.flip()

    clock.tick(60) # locks the game to 60fps

pygame.quit()
