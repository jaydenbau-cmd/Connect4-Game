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

def is_board_full():
    if 0 in board:
        return False
    else:
        return True

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

def get_winner(index_r, index_c):
    check = board[index_r][index_c]
    rows, cols = len(board), len(board[0])

    for dr, dc in DIRECTIONS:
        count = 1
        start = end = (index_r, index_c)

        rr, cc = index_r + dr, index_c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == check:
            end = (rr, cc)
            count += 1
            rr += dr
            cc += dc

        rr, cc = index_r - dr, index_c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == check:
            start = (rr, cc)
            count += 1
            rr -= dr
            cc -= dc

        if count >= 4:
            return circles[start[0]][start[1]], circles[end[0]][end[1]]

    return None

pg.init()
screen = pg.display.set_mode((1000, 720))
clock = pg.time.Clock()

font = pg.font.SysFont('None', 56)
running = True
won = False

board = np.zeros((6,7), dtype=int)
player = 1
ai = 2
score = {
    '1': 0,
    '2': 0,
}
current_turn = player

HEADER = 50

y_increment = screen.get_height() / 7
current_pos = [0.0,0.0]
circles = np.zeros((6, 7), dtype=object)
full = False

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
                if get_winner(valid[0], valid[1]):
                    won = True
                    line_start, line_end = get_winner(valid[0], valid[1])
                    if current_turn == 1:
                        winner = 2
                        score['2'] += 1
                    else:
                        winner = 1
                        score['1'] += 1

    screen.fill((0,20,100))
    screen.fill((30,30,30), rect=(0, 0, 1280, 100))

    turn_text = font.render(f'Player {current_turn} move', True, (255,255,255))
    screen.blit(turn_text, (100, 30))

    score_text = font.render(f'Player 1 Score: {score['1']} \nPlayer 2 Score: {score['2']}', True, (255,255,255))
    screen.blit(score_text, (560, 10))

    for circle in circles:
        for col in circle:
            pg.draw.circle(screen, (0,0,0), col, 40)

    for r_index, turn in enumerate(board):
        for c_index, col in enumerate(turn):
            if col == 1:
                pg.draw.circle(screen, (234, 51, 35), circles[r_index, c_index], 40)
            elif col == 2:
                pg.draw.circle(screen, (255, 254, 84), circles[r_index, c_index], 40)

    if won:
        pg.draw.line(screen, (255, 255, 255), line_start, line_end, width=10)
        pg.display.update()
        pg.display.message_box('Winner', f'Player {winner} has won the game!', 'info')
        board = np.zeros((6,7), dtype=int)
        won = False

    if is_board_full():
        pg.display.update()
        pg.display.message_box('Tie', "There are no more available spaces. It's a tie!", 'info')
        board = np.zeros((6,7), dtype=int)

    pg.display.flip()
    clock.tick(60)

pg.quit()
