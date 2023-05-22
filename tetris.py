import os
import time
import msvcrt
import random

# pyinstaller --noconsole --onefile main.py
class Tetris:
    def __init__(self):
        # width and height of field
        self.width = 10
        self.height = 20
        # instant of game field:
        # 0 - empty block, 1 - part of figure, 2 - part of figure(rotation center), 3 - "frozen" block
        self.game_field = []
        # instant of empty block
        self.empty_pix = " "
        # middle of container
        self.width_middle = int(self.width / 2)
        # instant for blocks
        wm = self.width_middle
        h = 0
        # [[x, y], ...[rotate center(index of block)]]
        self.I = [[wm, h], [wm, h + 1], [wm, h + 2], [wm, h + 3], 0]
        self.J = [[wm, h], [wm, h + 1], [wm, h + 2], [wm - 1, h + 2], 0]
        self.L = [[wm, h], [wm, h + 1], [wm, h + 2], [wm + 1, h + 2], 0]
        self.O = [[wm, h], [wm + 1, h], [wm, h + 1], [wm + 1, h + 1], 0]
        self.S = [[wm + 1, h], [wm + 2, h], [wm, h + 1], [wm + 1, h + 1], 2]
        self.T = [[wm - 1, h], [wm, h], [wm + 1, h], [wm, h + 1], 0]
        self.Z = [[wm - 1, h], [wm, h], [wm, h + 1], [wm + 1, h + 1], 0]
        # filling of game field
        row_counter = 0
        for y in range(self.height):
            self.game_field.append([])
            for x in range(self.width):
                self.game_field[row_counter].append(0)
            row_counter += 1
        # filling available_lines variable for this game field
        self.available_lines = []
        counter = 0
        for y in range(self.height):
            self.available_lines.append([])
            for x in range(self.width):
                self.available_lines[counter].append([x, y])
            counter += 1

    # print game field on screen
    def print_game_field(self):
        print('* '*self.width)
        for row in self.game_field:
            print('*', end='')
            for pix in row:
                if pix == 0:
                    print(self.empty_pix, end=' ')
                elif pix == 1:
                    print("▄", end=' ')
                elif pix == 2:
                    print("▄", end=' ')
                elif pix == 3:
                    print("@", end=' ')
            print('*', end='')
            print()
        print('', '* '*self.width)

    # spawning random figure and took this figure on the board
    def spawn_random_figure(self):
        spawn_new_figure = True
        # figure can spawns only when previous figure is not on the field
        for y in range(self.height):
            for x in range(self.width):
                if self.game_field[y][x] == 1 or self.game_field[y][x] == 2:
                    spawn_new_figure = False
        # choose random figure and took this figure on the board
        if spawn_new_figure:
            figure = random.choice([self.I, self.J, self.L, self.O, self.S, self.T, self.Z])
            for i in range(4):
                coord = figure[i]
                if i == figure[4]:
                    self.game_field[coord[1]][coord[0]] = 2
                else:
                    self.game_field[coord[1]][coord[0]] = 1

    # rendering game with giving FPS
    def render_game_field(self, FPS):
        self.print_game_field()
        time.sleep(1/FPS)
        os.system('cls')

    # move figure in two directions left or right
    def move_figure(self, direct):
        # getting whole block for continious processing
        full_block = []
        for y in range(self.height):
            for x in range(self.width):
                if self.game_field[y][x] == 1 or self.game_field[y][x] == 2:
                    full_block.append([x, y])
        # right direction
        if direct == 'd':
            # if all part of whole block don't go out from field or took collision with "frozen" blocks..
            counter = 0
            for block in full_block:
                if block[0] < self.width - 1 and self.game_field[block[1]][block[0]+1] != 3:
                    counter += 1
            # ..whole block can moving in right side
            if counter == 4:
                full_block.reverse()
                for block in full_block:
                    y = block[1]
                    x = block[0]
                    if self.game_field[y][x] == 1:
                        self.game_field[y][x + 1] = 1
                    elif self.game_field[y][x] == 2:
                        self.game_field[y][x + 1] = 2
                    self.game_field[y][x] = 0
        # left direction
        elif direct == 'a':
            # if all part of whole block don't go out from field..
            counter = 0
            for block in full_block:
                if block[0] > 0 and self.game_field[block[1]][block[0]-1] != 3:
                    counter += 1
            # ..whole block can moving in left side
            if counter == 4:
                for block in full_block:
                    y = block[1]
                    x = block[0]
                    if self.game_field[y][x] == 1:
                        self.game_field[y][x - 1] = 1
                    elif self.game_field[y][x] == 2:
                        self.game_field[y][x - 1] = 2
                    self.game_field[y][x] = 0

    # method for rotating figure
    def rotate_figure(self):
        # geting whole block for continious processing
        full_block = []
        for y in range(self.height):
            for x in range(self.width):
                if self.game_field[y][x] == 1 or self.game_field[y][x] == 2:
                    full_block.append([x, y, self.game_field[y][x]])
        rotate_center = 0
        # finding rotating center for the whole block
        for block in full_block:
            if block[2] == 2:
                break
            elif block[2] == 1:
                rotate_center += 1
        # rotate whole block
        for block in full_block:
            y = block[1]
            x = block[0]
            px = full_block[rotate_center][0]
            py = full_block[rotate_center][1]
            block[0] = px + py - y
            block[1] = x + py - px
        # checking if created block don't go out from game field
        counter = 0
        for block in full_block:
            if (0 <= block[0] < self.width) and (0 <= block[1] < self.height):
                counter += 1
        # if each part of block don't go out from game field, clear whole block and create new block
        if counter == 4:
            for y in range(self.height):
                for x in range(self.width):
                    if self.game_field[y][x] == 1 or self.game_field[y][x] == 2:
                        self.game_field[y][x] = 0
            for block in full_block:
                x = block[0]
                y = block[1]
                if block[2] == 2:
                    self.game_field[y][x] = 2
                elif block[2] == 1:
                    self.game_field[y][x] = 1

    # this method can move figure down
    def figure_falling(self):
        # geting whole block for continious processing
        full_block = []
        for y in range(self.height):
            for x in range(self.width):
                if self.game_field[y][x] == 1 or self.game_field[y][x] == 2:
                    full_block.append([x, y])
        # checking each part of whole block for touch with last line
        counter = 0
        # reverse array for right processing
        full_block.reverse()
        for block in full_block:
            x = block[0]
            y = block[1]
            if y != self.height - 1 and self.game_field[y + 1][x] != 3:
                counter += 1
        full_block.reverse()
        # if each part of whole block doesn't in last line blocks from game field and doesn't touch "frozen",
        # figure will be "in falling"
        if counter == 4:
            full_block.reverse()
            for block in full_block:
                y = block[1]
                x = block[0]
                if self.game_field[y][x] == 2:
                    self.game_field[y + 1][x] = 2
                elif self.game_field[y][x] == 1:
                    self.game_field[y + 1][x] = 1
                self.game_field[y][x] = 0
        # else this figure transform in "frozen" figure
        else:
            for block in full_block:
                y = block[1]
                x = block[0]
                self.game_field[y][x] = 3

    # this method delete "frozen" on some line, if blocks in this line are "full"
    def del_tetris_lines(self):
        blocks = []
        # here are lines for deleting
        self.lines_for_del = []
        for y in range(self.height):
            for x in range(self.width):
                if self.game_field[y][x] == 3:
                    # append blocks while don't meeting new line
                    if x == 0:
                        blocks.clear()
                    blocks.append([x, y])
                    # if line is full, this line this line will be add to delete lines array
                    for line in self.available_lines:
                        if blocks == line:
                            self.lines_for_del.append(y)
        # delete lines blocks from deleted lines
        for line in self.lines_for_del:
            for block_x in range(self.width):
                self.game_field[line][block_x] = 0

    # this method can throw reminder of "frozen" blocks down
    def falling_of_reminder(self):
        # count of "frozen" block coordinates
        remainder = list()
        for y in range(self.height):
            for x in range(self.width):
                if self.game_field[y][x] == 3:
                    remainder.append([x, y])
        # throw down every "frozen" block
        # reverse array for right processing
        remainder.reverse()
        # do so many times, as how many lines are
        for block in remainder:
            x = block[0]
            y = block[1]
            if y < self.height - 1 and self.game_field[y+1][x] != 3:
                self.game_field[y][x] = 0
                self.game_field[y + 1][x] = 3


tetris = Tetris()
FPS = 1
# main game loop
while True:
    tetris.spawn_random_figure()
    tetris.render_game_field(FPS)
    # delete lines of field if it needs
    tetris.del_tetris_lines()
    for _ in range(len(tetris.lines_for_del)):
        tetris.falling_of_reminder()
    if msvcrt.kbhit():
        input = msvcrt.getch().decode()
        if input == 'w':
            tetris.rotate_figure()
        elif input == 'a' or input == 'd':
            tetris.move_figure(input)
        elif input == 's':
            if FPS == 1:
                FPS = 5
            elif FPS == 5:
                FPS = 1
    else:
        tetris.figure_falling()



