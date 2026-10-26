import pygame as pg
import numpy as np

def check_move(x, y):
    global current_turn

    for r_index, center in enumerate(circles):
        for c_index, col in enumerate(center):
            if board[r_index][c_index] == 0:
                dist_squared = (x - col[0]) ** 2 + (y - col[1]) ** 2

                if r_index == 5:
                    if dist_squared <= 40 ** 2:
                        board[r_index][c_index] = current_turn
                        current_turn = 1 if current_turn == 2 else 2
                        return r_index, c_index
                else:
                    position = board[r_index + 1][c_index]

                    if dist_squared <= 40 ** 2 and position != 0:
                        board[r_index][c_index] = current_turn
                        current_turn = 1 if current_turn == 2 else 2
                        return r_index, c_index
    return None

def get_winner(index_r, index_c):
    check = board[index_r][index_c]
    first, last = circles[index_r][index_c]
    same = 1
    colours = [check]

    for i in range(1,4):
        try:
            if board[index_r][index_c + i] == check:
                first = circles[index_r][index_c + i]
                colours.append(check)
                same += 1
        except IndexError:
            pass

        try:
            if board[index_r][index_c - i] == check and index_c - i >= 0:
                last = circles[index_r][index_c - i]
                colours.append(check)
                same += 1
        except IndexError:
            pass

    count = 0
    count = [count+1 for i in colours if i == check]
    print(count)

    if len(count) == 4:
        return first, last

    print(same)
    print(colours)

    return None



pg.init()
screen = pg.display.set_mode((1000, 720))
clock = pg.time.Clock()
running = True
won = False

board = np.zeros((6,7), dtype=int)
player = 1
ai = 2
current_turn = player

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

            if valid:
                print(get_winner(valid[0], valid[1]))
                if get_winner(valid[0], valid[1]):
                    won = True
                    print('ran')
                    #line_start, line_end = get_winner(valid[0], valid[1])
                    print(get_winner(valid[0], valid[1]))


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

    # if won:
    #     pg.draw.line(screen, (255, 255, 255), line_start, line_end, HEADER)

    pg.display.flip()
    clock.tick(60)

pg.quit()
