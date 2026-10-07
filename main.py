import pygame as pg
import numpy as np

def check_move(x, y):
    for r_index, center in enumerate(circles):
        for c_index, col in enumerate(center):
            dist_squared = (x - col[0]) ** 2 + (y - col[1]) ** 2

            if r_index == 5:
                if dist_squared <= 40 ** 2:
                    board[r_index][c_index] = player
                    return center
            else:
                position = board[r_index + 1][c_index]

                if dist_squared <= 40 ** 2 and position != 0:
                    board[r_index][c_index] = player
                    return center
    return None

def get_winner():
    pass

pg.init()
screen = pg.display.set_mode((1000, 720))
clock = pg.time.Clock()
running = True

board = np.zeros((6,7), dtype=int)
player = 1
ai = 2

HEADER = 50

y_increment = screen.get_height() / 7
current_pos = [0.0,0.0]
circles = np.zeros((6, 7), dtype=object)

for r_index, row in enumerate(board):
    if r_index == 0:
        current_pos[1] += y_increment + HEADER
    else:
        current_pos[1] += y_increment

    x_increment = screen.get_width() / 8
    current_pos[0] = x_increment

    for c_index, col in enumerate(row):
        circles[r_index][c_index] = [current_pos[0],current_pos[1]]
        current_pos[0] += x_increment

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            valid = check_move(mx, my)

    screen.fill((0,20,100))
    screen.fill((30,30,30), rect=(0, 0, 1280, 100))

    #Render here
    for circle in circles:
        for col in circle:
            pg.draw.circle(screen, (0,0,0), col, 40)

    for r_index, turn in enumerate(board):
        for c_index, col in enumerate(turn):
            if col == 1:
                pg.draw.circle(screen, (234, 51, 35), circles[r_index, c_index], 40)
            elif col == 2:
                pg.draw.circle(screen, (255, 254, 84), circles[r_index, c_index], 40)

    pg.display.flip()
    clock.tick(60)

pg.quit()
