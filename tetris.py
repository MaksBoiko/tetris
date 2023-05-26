import os
import sys
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
        self.empty_pix = "·"
        # middle of container
        self.width_middle = int(self.width / 2)
        # score
        self.score = 0
        # deleted lines
        self.deleted_lines = 0
        # level
        self.level = 1
        # start time
        self.start_time = time.time()
        # game frame
        self.frame = 0
        # figure
        self.figure = []
        # next figure
        self.next_figure = []
        #
        self.hide_hints = False
        # instant for blocks
        wm = self.width_middle
        h = 0
        # [[x, y], ...[rotate center(index of block)]]
        self.I = [[wm, h], [wm, h + 1], [wm, h + 2], [wm, h + 3], 1]
        self.J = [[wm + 1, h], [wm + 1, h + 1], [wm + 1, h + 2], [wm, h + 2], 1]
        self.L = [[wm, h], [wm, h + 1], [wm, h + 2], [wm + 1, h + 2], 1]
        self.O = [[wm, h], [wm + 1, h], [wm, h + 1], [wm + 1, h + 1], 0]
        self.S = [[wm + 1, h], [wm + 2, h], [wm, h + 1], [wm + 1, h + 1], 3]
        self.T = [[wm - 1, h], [wm, h], [wm + 1, h], [wm, h + 1], 1]
        self.Z = [[wm - 1, h], [wm, h], [wm, h + 1], [wm + 1, h + 1], 2]
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
        figure_preview = self.generate_figure_preview()
        row_counter = 0
        print('+', '* '*(self.width-1), '+')
        preview_counter = 0
        for row in self.game_field:
            print('*', end='')
            for pix in row:
                # if game over and already method print half of board print game over in this row
                if row_counter == self.height // 2 and self.is_game_over():
                    message = 'GAME OVER!'
                    tabs_count = self.width - len(message) // 2
                    print(self.empty_pix * (tabs_count-1), message, self.empty_pix * (tabs_count-1), end='')
                    break
                # else game is not over and draw yard how it was before
                else:
                    if pix == 0:
                        print(self.empty_pix, end=' ')
                    elif pix == 1:
                        print("▄", end=' ')
                    elif pix == 2:
                        print("▄", end=' ')
                    elif pix == 3:
                        print("@", end=' ')
            print('*', end='')
            # count time in game based on start time
            time_in_game = self.count_time()
            # printing game data on screen
            if row_counter == 1:
                print("   Level: {}".format(self.level), end='')
            elif row_counter == 2:
                print("   Score: {}".format(self.score), end='')
            elif row_counter == 3:
                print("   Lines clear: {}".format(self.deleted_lines), end='')
            elif row_counter == 4:
                print("   Elapsed time: {}m".format(time_in_game), end='')
            elif row_counter == 5:
                print("   Frame: {}".format(self.frame), end='')
            # printing figure preview
            elif row_counter == 7:
                print("   Next figure:", end='')
            elif row_counter == 8:
                print('   ', end='')
                for pix in figure_preview[preview_counter]:
                    print(pix, end=' ')
                preview_counter += 1
            elif row_counter == 9:
                print('   ', end='')
                for pix in figure_preview[preview_counter]:
                    print(pix, end=' ')
                preview_counter += 1
            elif row_counter == 10:
                print('   ', end='')
                for pix in figure_preview[preview_counter]:
                    print(pix, end=' ')
                preview_counter += 1
            elif row_counter == 11:
                print('   ', end='')
                for pix in figure_preview[preview_counter]:
                    print(pix, end=' ')
                preview_counter += 1
            elif row_counter == 12:
                print('   ', end='')
                for pix in figure_preview[preview_counter]:
                    print(pix, end=' ')
                preview_counter += 1
            row_counter += 1
            print()
        print('+', '* '*(self.width-1), '+')
        if not self.hide_hints:
            print('Press "w" for figure rotation, \n"a" for move to left side or "d" to right side,\n'
                  ' "s" for boost, button "gap" for pause,\n click "q" in order to hide this text.')

    def generate_figure_preview(self):
        next_figure_preview = []
        row_counter = 0
        for block in range(len(self.next_figure)-1):
                next_figure_preview.append([])
                next_figure_preview[row_counter].append(self.next_figure[block][0]-(self.width_middle//2+1))
                next_figure_preview[row_counter].append(self.next_figure[block][1])
                row_counter += 1
        i = 0
        preview_field = []
        # generating preview field
        row_counter = 0
        for y in range(5):
            preview_field.append([])
            for x in range(5):
                preview_field[row_counter].append("_")
            row_counter += 1

        for block in next_figure_preview:
            preview_field[block[1]][block[0]] = "▄"
        return preview_field

    # spawning random figure and took this figure on the board
    def spawn_random_figure(self):
        spawn_new_figure = True
        # figure cans spawn only when previous figure is not on the field
        for y in range(self.height):
            for x in range(self.width):
                if self.game_field[y][x] == 1 or self.game_field[y][x] == 2:
                    spawn_new_figure = False
        # choose random figure and took this figure on the board
        if spawn_new_figure:
            self.figure = self.next_figure
            self.next_figure = random.choice([self.I, self.I, self.J, self.L, self.O, self.S, self.T, self.Z])
            for i in range(4):
                coord = self.figure[i]
                # if figure already spawns in 'frozen' block..
                if self.game_field[coord[1]][coord[0]] == 3:
                    # 'froze' this figure
                    tetris.figure_falling()
                if i == self.figure[4]:
                    self.game_field[coord[1]][coord[0]] = 2
                else:
                    self.game_field[coord[1]][coord[0]] = 1

    # rendering game with giving FPS
    def render_game_field(self, FPS):
        self.frame += 1
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
        # checking if created block don't go out from game field and don't stuck in "frozen" blocks
        counter = 0
        for block in full_block:
            if (0 <= block[0] < self.width) and (0 <= block[1] < self.height)\
                    and self.game_field[block[1]][block[0]] != 3:
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
            self.score += 1
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
        # add points to score and count deleted lines
        if len(self.lines_for_del) == 1:
            self.score += 100
            self.deleted_lines += 1
        elif len(self.lines_for_del) == 2:
            self.score += 300
            self.deleted_lines += 2
        elif len(self.lines_for_del) == 3:
            self.score += 500
            self.deleted_lines += 3
        elif len(self.lines_for_del) == 4:
            self.score += 800
            self.deleted_lines += 4
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

    # this method make a level based the score he calculate level and return FPS
    def make_lvl(self):
        if self.score < 1000:
            self.level = 1
        elif 1000 <= self.score < 5000:
            self.level = 2
        elif 5000 <= self.score < 20_000:
            self.level = 3
        elif 20_000 <= self.score < 50_000:
            self.level = 4
        elif 50_000 <= self.score < 100_000:
            self.level = 5
        elif 100_000 <= self.score < 200_000:
            self.level = 6
        elif 200_000 <= self.score < 400_000:
            self.level = 7
        elif 400_000 <= self.score < 700_000:
            self.level = 8
        elif 700_000 <= self.score < 1_000_000:
            self.level = 9
        elif 1_000_000 <= self.score < 10_000_000:
            self.level = 10
        else:
            self.level = 11
        FPS = self.level
        return FPS

    # checking game over method
    def is_game_over(self):
        for x in range(self.width):
            if self.game_field[0][x] == 3:
                return True
        return False

    def count_time(self):
        timer = round((time.time() - self.start_time) / 60, 2)
        return timer


# create tetris object
tetris = Tetris()
# is game in boost mode
is_boost = False
FPS = 1
tetris.next_figure = random.choice([tetris.I, tetris.I, tetris.J, tetris.L, tetris.O, tetris.S, tetris.T, tetris.Z])
# main game loop
while True:
    # if game lost
    if tetris.is_game_over():
        tetris.figure_falling()
        tetris.print_game_field()
        # TODO: main menu
        print("Press any button for exit..")
        os.system('pause')
        sys.exit(0)
    if not is_boost:
        FPS = tetris.make_lvl()
    # spawning of figure
    tetris.spawn_random_figure()
    # rendering of game
    tetris.render_game_field(FPS)
    # delete lines of field if it needs
    tetris.del_tetris_lines()
    for _ in range(len(tetris.lines_for_del)):
        tetris.falling_of_reminder()
    # if any button is pressed..
    if msvcrt.kbhit():
        user_input = msvcrt.getch().decode()
        # tab - pause
        if user_input == ' ':
            start_pause_time = time.time()
            tetris.print_game_field()
            os.system('pause')
            os.system('cls')
            last_pause_time = time.time()
            tetris.start_time += last_pause_time - start_pause_time
        # w - rotation of figure
        if user_input == 'w':
            tetris.rotate_figure()
        # a or d - figure moving to left or right side
        elif user_input == 'a' or user_input == 'd':
            tetris.move_figure(user_input)
        # s - increasing figure speed
        elif user_input == 's':
            if FPS != 11:
                is_boost = True
                FPS = 11
            elif FPS == 11:
                FPS = tetris.level
                is_boost = False
        elif user_input == 'q':
            tetris.hide_hints = True
    # if player doesn't do anything..
    else:
        # figure will be fall
        tetris.figure_falling()



