# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

# AI Game
from enum import Enum
from utilities import FileWriter
import random
import numpy as np
from player import PreferenceType


class GameError(Enum):
    UPNE = 'Upper Position Not Empty'
    LPE = 'Lower Position Empty'
    OPE = 'Old Position Empty'
    CCPSL = 'Card can''t be placed at the same location'
    ORMAN = 'Only Recycle moves allowed now'
    BCF = 'Boundary Check Failed'
    IIP = 'Invalid Input Position'
    NPNE = 'New Position not Empty'
    CSLCPRN = 'Cards still left, Can''t play recycling move now'
    CMLCPOP = 'Can''t move the last card played by the other player'


class Board:

    def __init__(self):
        self.matrix = np.zeros(shape=(12, 8), dtype='object')
        self.card_list = {}
        self.move_list = {}

    def _card_part2_position(self, card_angle, row, column):
        if card_angle in ('1', '3', '5', '7'):
            part2_col = column + 1
            part2_row = row
        elif card_angle in ('2', '4', '6', '8'):
            part2_row = row + 1
            part2_col = column

        return part2_row, part2_col

    def regular_move(self, card, card_angle, row_old, column_old):
        row, column = self._position_translation(row_old, column_old)
        part2_row, part2_col = self._card_part2_position(card_angle, row, column)

        status, error_code = self.is_new_move_valid(card_angle, row, column, part2_row, part2_col)

        if status:
            print('card placed at ' + column_old + ' ' + row_old + ' : ' + (
                chr(int(part2_col + 1) + 96)).upper() + ' ' + str(int(part2_row) + 1))
            card.rotate_card(card_angle)
            self.place_card(card, row, column, part2_row, part2_col)

        return status, error_code

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
        self.card_list.pop(str(part1_row) + str(part1_col))
        moves_count = len(self.move_list)
        self.move_list.pop(moves_count)

    def _position_translation(self, row, column):
        column = ord(column.lower()) - 96
        row = int(row) - 1
        column = int(column) - 1
        return row, column

    def recycle_move(self, part1_row, part1_col, part2_row, part2_col, card_angle, row_old, column_old):

        if len(self.card_list) != 24:
            return False, GameError.CSLCPRN

        print('moving card from ' + part1_col + ' ' + part1_row + ' : ' + part2_col + ' ' + part2_row)

        row, column = self._position_translation(row_old, column_old)
        new_part2_row, new_part2_col = self._card_part2_position(card_angle, row, column)

        status, error_code = self.is_new_move_valid(card_angle, row, column, new_part2_row, new_part2_col)
        if status:
            part1_row, part1_col = self._position_translation(part1_row, part1_col)
            last_move = str(self.move_list[len(self.move_list)]).split(':')

            if (part1_row == int(last_move[0]) and
                    part1_col == int(last_move[1])):
                return False, GameError.CMLCPOP

            part2_row, part2_col = self._position_translation(part2_row, part2_col)

            status, error_code = self._recycle_move_validation(row, column, new_part2_row, new_part2_col, part1_row,
                                                               part1_col,
                                                               part2_row, part2_col)
            if not status:
                return status, error_code

            print('card placed at ' + column_old + ' ' + row_old + ' : ' + (
                chr(int(new_part2_col + 1) + 96)).upper() + ' ' + str(int(new_part2_row) + 1))

            card = self._fetch_card(part1_row, part1_col, part2_row, part2_col)
            card.rotate_card(card_angle)
            self.place_card(card, row, column, new_part2_row, new_part2_col)

        return status, error_code

    def _recycle_move_validation(self, new_part1_row, new_part1_col, new_part2_row, new_part2_col, old_part1_row,
                                 old_part1_col, old_part2_row, old_part2_col):

        status, error_code = self.boundary_check(old_part1_row + 1, old_part1_col)

        if status:
            status, error_code = self.boundary_check(old_part2_row + 1, old_part2_row)

        if not status:
            return status, error_code

        if (old_part1_row == new_part1_row and
                old_part1_col == new_part1_col and
                old_part2_row == new_part2_row and
                old_part2_col == new_part2_col):
            status = False
            error_code = GameError.CCPSL
        elif (self.matrix[old_part1_row + 1][old_part1_col] != 0 or
              self.matrix[old_part2_row + 1][old_part2_col] != 0):
            status = False
            error_code = GameError.UPNE
        elif (self.matrix[old_part1_row][old_part1_col] == 0 or
              self.matrix[old_part2_row][old_part2_col] == 0):
            status = False
            error_code = GameError.OPE

        return status, error_code

    def _fetch_card(self, part1_row, part1_col, part2_row, part2_col):
        card = self.card_list.pop(str(part1_row) + str(part1_col))
        self.matrix[part1_row, part1_col] = 0
        self.matrix[part2_row, part2_col] = 0
        return card

    def boundary_check(self, row, column):
        if (row < 0 or
                row > 11 or
                column < 0 or
                column > 7):
            return False, GameError.BCF
        return True, None

    def is_new_move_valid(self, card_angle, row, column, part2_row, part2_col):

        # Boundary Validation
        status, error_code = self.boundary_check(row, column)
        if status:
            status, error_code = self.boundary_check(part2_row, part2_col)
        else:
            return status, error_code

        # to check if there is card under the given position
        if status and row > 0:
            if card_angle in ('1', '3', '5', '7'):
                if (self.matrix[row - 1, column] == 0 or
                        self.matrix[part2_row - 1, part2_col] == 0):
                    status = False
                    error_code = GameError.LPE
            elif card_angle in ('2', '4', '6', '8'):
                if self.matrix[row - 1, column] == 0:
                    status = False
                    error_code = GameError.LPE

        # To check if the position is empty
        if status and (self.matrix[row, column] != 0 or
                       self.matrix[part2_row, part2_col] != 0):
            status = False
            error_code = GameError.NPNE

        return status, error_code

    def print_board(self):
        for i in range(11, -1, -1):
            for j in range(0, 8):
                card_side = self.matrix[i, j]
                if card_side == 0:
                    print('0' + '   ', end="")
                else:
                    print(str(self.matrix[i, j]) + ' ', end="")
            print()

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
