# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

# AI Game
from enum import Enum
from player import PreferenceType
import numpy as np
import copy
from utilities import GameError


class Board:
    total_rows = 12
    total_columns = 8

    def __init__(self):
        self.matrix = np.zeros(shape=(self.total_rows, self.total_columns), dtype='object')
        self.card_list = {}
        self.move_list = {}

    def place_card(self, card, part1_row, part1_col, part2_row, part2_col):
        self.matrix[part1_row, part1_col] = card.part1['Color'] + ':' + card.part1['Dot']
        self.matrix[part2_row, part2_col] = card.part2['Color'] + ':' + card.part2['Dot']
        self.card_list[str(part1_row) + str(part1_col)] = card
        moves_count = len(self.move_list)
        self.move_list[moves_count + 1] = str(part1_row) + ':' + str(part1_col) + ':' + str(part2_row) + ':' + str(
            part2_col)

    def remove_card(self, part1_row, part1_col, part2_row, part2_col):
        self.matrix[part1_row, part1_col] = 0
        self.matrix[part2_row, part2_col] = 0
        card = self.card_list.pop(str(part1_row) + str(part1_col))
        moves_count = len(self.move_list)
        self.move_list.pop(moves_count)

        return card

    def _fetch_card(self, part1_row, part1_col, part2_row, part2_col):
        card = self.card_list.pop(str(part1_row) + str(part1_col))
        self.matrix[part1_row, part1_col] = 0
        self.matrix[part2_row, part2_col] = 0
        return card

    def print_board(self):
        for i in range(11, -1, -1):
            for j in range(0, 8):
                card_side = self.matrix[i, j]
                if card_side == 0:
                    print('0' + '   ', end="")
                else:
                    print(str(self.matrix[i, j]) + ' ', end="")
            print()

    def boundary_check(self, row, column):
        if (row < 0 or
                row > 11):
            return False, GameError.RVE

        if (column < 0 or
                column > 7):
            return False, GameError.CVE
        return True, None

    def is_new_move_valid(self, part1_row, part1_col, part2_row, part2_col):

        # Boundary Validation
        status, error_code = self.boundary_check(part1_row, part1_col)
        if status:
            status, error_code = self.boundary_check(part2_row, part2_col)
        else:
            return status, error_code

        # to check if there is card under the given position
        if status and part1_row > 0:
            if part1_row == part2_row:  # horizontal card
                if (self.matrix[part1_row - 1, part1_col] == 0 or
                        self.matrix[part2_row - 1, part2_col] == 0):
                    status = False
                    error_code = GameError.LPE
            elif part1_col == part2_col:  # vertical card
                if self.matrix[part1_row - 1, part1_col] == 0:
                    status = False
                    error_code = GameError.LPE

        # To check if the position is empty
        if status and (self.matrix[part1_row, part1_col] != 0 or
                       self.matrix[part2_row, part2_col] != 0):
            status = False
            error_code = GameError.NPNE

        return status, error_code

    def is_recycle_move_valid(self, new_part1_row, new_part1_col, new_part2_row, new_part2_col, prev_part1_row,
                              prev_part1_col, prev_part2_row, prev_part2_col):

        if len(self.card_list) != 24:
            return False, GameError.CSLCPRN

        last_move = str(self.move_list[len(self.move_list)]).split(':')

        if (prev_part1_row == int(last_move[0]) and
                prev_part1_col == int(last_move[1])):
            return False, GameError.CMLCPOP

        if prev_part1_col == prev_part2_col:  # card is vertical
            if ((prev_part2_row + 1 < self.total_rows) and
                    self.matrix[prev_part2_row + 1][prev_part1_col] != 0):
                return False, GameError.UPNE
        elif prev_part1_row == prev_part2_row:  # card is horizontal
            if ((prev_part1_row + 1 < self.total_rows) and
                    self.matrix[prev_part1_row + 1][prev_part1_col] != 0 or
                    self.matrix[prev_part2_row + 1][prev_part2_col] != 0):
                return False, GameError.UPNE

        if (prev_part1_row == new_part1_row and
                prev_part1_col == new_part1_col and
                prev_part2_row == new_part2_row and
                prev_part2_col == new_part2_col):
            return False, GameError.CCPSL
        elif (self.matrix[prev_part1_row][prev_part1_col] == 0 or
              self.matrix[prev_part2_row][prev_part2_col] == 0):
            return False, GameError.OPE

        status, error_code = self.is_new_move_valid(new_part1_row, new_part1_col, new_part2_row, new_part2_col)
        return status, error_code

    def vertical_set_count(self, row, col):
        color_count_bck = [0, 0]
        dot_count_bck = [0, 0]

        for i in range(0, 2):
            previous_dot_type_bck = 'N'
            previous_color_type_bck = 'N'
            row_tmp = row[i]
            col_tmp = col[i]

            for j in range(0, 4):
                status, error_code = self.boundary_check(row_tmp - j, col_tmp)

                if status:
                    card_bck = str(self.matrix[row_tmp - j, col_tmp])
                    if card_bck != '0':
                        if card_bck[0] == previous_color_type_bck:
                            color_count_bck[i] = color_count_bck[i] + 1
                        else:
                            previous_color_type_bck = card_bck[0]
                            color_count_bck[i] = 1

                        if card_bck[2] == previous_dot_type_bck:
                            dot_count_bck[i] = dot_count_bck[i] + 1
                        else:
                            previous_dot_type_bck = card_bck[2]
                            dot_count_bck[i] = 1

        return color_count_bck, dot_count_bck

    def vertical_set_check(self, row, col):
        color_set = False
        dot_set = False

        color_count_bck, dot_count_bck = self.vertical_set_count(row, col)
        if (color_count_bck[0] == 4 or
                color_count_bck[1] == 4):
            color_set = True

        if (dot_count_bck[0] == 4 or
                dot_count_bck[1] == 4):
            dot_set = True

        if color_count_bck == 4:
            color_set = True
        if dot_count_bck == 4:
            dot_set = True

        return color_set, dot_set

    def horizontal_set_count(self, row, col):
        color_count_fwd = [0, 0]
        dot_count_fwd = [0, 0]
        color_count_bck = [0, 0]
        dot_count_bck = [0, 0]

        for i in range(0, 2):
            previous_dot_type_fwd = 'N'
            previous_color_type_fwd = 'N'
            previous_dot_type_bck = 'N'
            previous_color_type_bck = 'N'

            row_tmp = row[i]
            col_tmp = col[i]
            for j in range(0, 4):
                status, error_code = self.boundary_check(row_tmp, col_tmp + j)
                if status:
                    card_fwd = str(self.matrix[row_tmp, col_tmp + j])
                    if card_fwd != '0':
                        if card_fwd[0] == previous_color_type_fwd:
                            color_count_fwd[i] = color_count_fwd[i] + 1
                        else:
                            previous_color_type_fwd = card_fwd[0]
                            color_count_fwd[i] = 1

                        if card_fwd[2] == previous_dot_type_fwd:
                            dot_count_fwd[i] = dot_count_fwd[i] + 1
                        else:
                            previous_dot_type_fwd = card_fwd[2]
                            dot_count_fwd[i] = 1

                status, error_code = self.boundary_check(row_tmp, col_tmp - j)
                if status:
                    card_bck = str(self.matrix[row_tmp, col_tmp - j])
                    if card_bck != '0':
                        if card_bck[0] == previous_color_type_bck:
                            color_count_bck[i] = color_count_bck[i] + 1
                        else:
                            previous_color_type_bck = card_bck[0]
                            color_count_bck[i] = 1

                        if card_bck[2] == previous_dot_type_bck:
                            dot_count_bck[i] = dot_count_bck[i] + 1
                        else:
                            previous_dot_type_bck = card_bck[2]
                            dot_count_bck[i] = 1

        return color_count_bck, dot_count_bck, color_count_fwd, dot_count_fwd

    def horizontal_set_check(self, row, col):

        dot_set = False
        color_set = False

        color_count_bck, dot_count_bck, color_count_fwd, dot_count_fwd = self.horizontal_set_count(row, col)
        if (color_count_bck[0] == 4 or
                color_count_bck[1] == 4 or
                color_count_fwd[0] == 4 or
                color_count_fwd[1] == 4):
            color_set = True

        if (dot_count_bck[0] == 4 or
                dot_count_bck[1] == 4 or
                dot_count_fwd[0] == 4 or
                dot_count_fwd[1] == 4):
            dot_set = True

        return color_set, dot_set

    def diagonal_set_count(self, row, col):

        color_count_all = {}
        dot_count_all = {}

        for i in range(0, 2):
            row_c = row[i]
            col_c = col[i]
            new_card_square_color = self.matrix[row_c, col_c][0]
            new_card_dot_color = self.matrix[row_c, col_c][2]

            color_count_ru = 1
            dot_count_ru = 1
            color_count_rd = 1
            dot_count_rd = 1
            color_count_lu = 1
            dot_count_lu = 1
            color_count_ld = 1
            dot_count_ld = 1

            for k in range(1, 4):
                status, error_code = self.boundary_check(row_c + k, col_c + k)
                if status:
                    card_ru = str(self.matrix[row_c + k, col_c + k])
                    if card_ru != '0':
                        if card_ru[0] == new_card_square_color:
                            color_count_ru = color_count_ru + 1
                        if card_ru[2] == new_card_dot_color:
                            dot_count_ru = dot_count_ru + 1

                status, error_code = self.boundary_check(row_c - k, col_c + k)
                if status:
                    card_rd = str(self.matrix[row_c - k, col_c + k])
                    if card_rd != '0':
                        if card_rd[0] == new_card_square_color:
                            color_count_rd = color_count_rd + 1
                        if card_rd[2] == new_card_dot_color:
                            dot_count_rd = dot_count_rd + 1

                status, error_code = self.boundary_check(row_c + k, col_c - k)
                if status:
                    card_lu = str(self.matrix[row_c + k, col_c - k])
                    if card_lu != '0':
                        if card_lu[0] == new_card_square_color:
                            color_count_lu = color_count_lu + 1
                        if card_lu[2] == new_card_dot_color:
                            dot_count_lu = dot_count_lu + 1

                status, error_code = self.boundary_check(row_c - k, col_c - k)
                if status:
                    card_ld = str(self.matrix[row_c - k, col_c - k])
                    if card_ld != '0':
                        if card_ld[0] == new_card_square_color:
                            color_count_ld = color_count_ld + 1
                        if card_ld[2] == new_card_dot_color:
                            dot_count_ld = dot_count_ld + 1

            color_count = (color_count_ru, color_count_rd, color_count_lu, color_count_ld)
            dot_count = (dot_count_ru, dot_count_rd, dot_count_lu, dot_count_ld)
            color_count_all[i] = color_count
            dot_count_all[i] = dot_count

        return color_count_all, dot_count_all

    def diagonal_set_check(self, row, col):
        color_set = False
        dot_set = False

        color_count_all, dot_count_all = self.diagonal_set_count(row, col)

        for i in range(0, 2):
            color_count = color_count_all.get(i)
            dot_count = dot_count_all.get(i)
            color_set_tmp = False
            dot_set_tmp = False

            if (color_count[0] == 4 or
                    color_count[1] == 4 or
                    color_count[2] == 4 or
                    color_count[3] == 4):
                color_set_tmp = True

            if (dot_count[0] == 4 or
                    dot_count[1] == 4 or
                    dot_count[2] == 4 or
                    dot_count[3] == 4):
                dot_set_tmp = True

            color_set = color_set or color_set_tmp
            dot_set = dot_set or dot_set_tmp

        return color_set, dot_set

    def check_winner(self):
        last_pos = len(self.move_list)
        position = self.move_list[last_pos].split(':')
        row = [int(position[0]), int(position[2])]
        col = [int(position[1]), int(position[3])]

        color_set_horizontal, dot_set_horizontal = self.horizontal_set_check(row, col)
        color_set_vertical, dot_set_vertical = self.vertical_set_check(row, col)
        color_set_diagonal, dot_set_diagonal = self.diagonal_set_check(row, col)

        color_set = color_set_horizontal or color_set_vertical or color_set_diagonal
        dot_set = dot_set_horizontal or dot_set_vertical or dot_set_diagonal

        return color_set, dot_set

    def find_possible_moves(self, card):
        if len(self.card_list) >= 24:
            possible_moves = self.find_possible_recycle_moves()
        else:
            possible_moves = self.find_possible_normal_moves(card)
        return possible_moves

    def find_possible_normal_moves(self, card):
        move_count = 1
        possible_moves = {}
        for part1_col in range(0, 8):
            part1_row = 0
            while (part1_row < 12 and
                   self.matrix[part1_row, part1_col] != 0):
                part1_row = part1_row + 1
            if part1_row == 12:
                continue

            for rotation in range(1, 9):
                card_tmp = copy.deepcopy(card)
                card_tmp.rotate_card(str(rotation))
                if rotation in (1, 3, 5, 7):
                    part2_col = part1_col + 1
                    part2_row = part1_row
                elif rotation in (2, 4, 6, 8):
                    part2_row = part1_row + 1
                    part2_col = part1_col

                # check if move is valid or not
                status, error_code = self.is_new_move_valid(part1_row, part1_col, part2_row, part2_col)
                if status:
                    #  print(part1_row, part1_col, part2_row, part2_col)
                    move = (0, card_tmp, part1_row, part1_col, part2_row, part2_col)
                    possible_moves[move_count] = move
                    move_count = move_count + 1
        return possible_moves

    def find_possible_recycle_moves(self):
        move_count = 1
        possible_moves = {}
        for prev_part1_col in range(0, 8):
            prev_part1_row = 0
            while (prev_part1_row < 12 and
                   self.matrix[prev_part1_row, prev_part1_col] != 0):
                prev_part1_row = prev_part1_row + 1
            if prev_part1_row == 12:
                continue
            else:
                prev_part1_row = prev_part1_row - 1

            card = self.card_list.get(str(prev_part1_row) + str(prev_part1_row), None)
            if card.rotation in ('1', '3', '5', '7'):
                prev_part2_row = prev_part1_row
                prev_part2_col = prev_part1_col + 1
            else:
                prev_part2_row = prev_part1_row + 1
                prev_part2_col = prev_part1_col

            if card is not None:
                for new_part1_col in range(0, 8):
                    new_part1_row = 0
                    while (new_part1_row < 12 and
                           self.matrix[new_part1_row, new_part1_col] != 0):
                        new_part1_row = new_part1_row + 1
                    if new_part1_row == 12:
                        continue

                    for rotation in range(1, 9):
                        card_tmp = copy.deepcopy(card)
                        card_tmp.rotate_card(str(rotation))
                        if rotation in (1, 3, 5, 7):
                            new_part2_col = new_part1_col + 1
                            new_part2_row = new_part1_row
                        elif rotation in (2, 4, 6, 8):
                            new_part2_row = new_part1_row + 1
                            new_part2_col = new_part1_col

                        # check if move is valid or not
                        status, error_code = self.is_recycle_move_valid(new_part1_row, new_part1_col, new_part2_row,
                                                                        new_part2_col, prev_part1_row,
                                                                        prev_part1_col, prev_part2_row, prev_part2_col)
                        if status:
                            #  print(row, column, part2_row, part2_col)
                            move = (
                                1, card_tmp, new_part1_row, new_part1_col, new_part2_row, new_part2_col, prev_part1_row,
                                prev_part1_col, prev_part2_row, prev_part2_col)
                            possible_moves[move_count] = move
                            move_count = move_count + 1

        return possible_moves

    def calculate_heuristic_value(self, max_player_preference):

        last_pos = len(self.move_list)
        position = self.move_list[last_pos].split(':')
        row = [int(position[0]), int(position[2])]
        col = [int(position[1]), int(position[3])]

        color_hz_bck, dot_hz_bck, color_hz_fwd, dot_hz_fwd = self.horizontal_set_count(row, col)
        color_count_vertical, dot_count_vertical = self.vertical_set_count(row, col)
        color_count_all, dot_count_all = self.diagonal_set_count(row, col)
        color = 0
        dot = 0
        for i in range(0, 2):
            color_count = color_count_all.get(i)
            dot_count = dot_count_all.get(i)

            color = color + color_count[0] + color_count[1] + color_count[2] + color_count[3]
            color = color + color_hz_bck[i] + color_hz_fwd[i] + color_count_vertical[i]
            dot = dot + dot_count[0] + dot_count[1] + dot_count[2] + dot_count[3]
            dot = dot + dot_hz_bck[i] + dot_hz_fwd[i] + dot_count_vertical[i]

        value = color - dot

        if max_player_preference == PreferenceType.C:
            return value
        else:
            return -value
