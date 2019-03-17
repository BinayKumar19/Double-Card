# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

# AI Game
from enum import Enum
import numpy as np
import copy
from utilities import GameError, PreferenceType


class Board:
    total_rows = 12
    total_columns = 8
    # Heuristic parameters
    best_case_value = 1
    second_best_case_value = 0.75
    neutral_case_value = 0
    worst_case_value = -1
    missing_case_value = 0.25

    def __init__(self):
        self.matrix = np.zeros(shape=(self.total_rows, self.total_columns), dtype='object')
        self.card_list = {}
        self.move_list = {}

    def place_card(self, card, part1_row, part1_col, part2_row, part2_col, count_as_move):

        self.matrix[part1_row, part1_col] = card.part1['Color'] + ':' + card.part1['Dot']
        self.matrix[part2_row, part2_col] = card.part2['Color'] + ':' + card.part2['Dot']
        self.card_list[str(part1_row) + str(part1_col)] = card
        if count_as_move:
            moves_count = len(self.move_list)
            self.move_list[moves_count + 1] = str(part1_row) + ':' + str(part1_col) + ':' + str(part2_row) + ':' + str(
                part2_col)

    def remove_card(self, part1_row, part1_col, part2_row, part2_col, count_as_move):
        self.matrix[part1_row, part1_col] = 0
        self.matrix[part2_row, part2_col] = 0
        card = self.card_list.pop(str(part1_row) + str(part1_col), None)
        if card is None:
            raise ValueError(GameError.ICP)
        if count_as_move:
            moves_count = len(self.move_list)
            self.move_list.pop(moves_count)
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

    @staticmethod
    def boundary_check(row, column):
        if (row < 0 or
                row > 11):
            return False, GameError.RVE

        if (column < 0 or
                column > 7):
            return False, GameError.CVE
        return True, None

    def is_new_move_valid(self, part1_row, part1_col, part2_row, part2_col):

        # Boundary Validation
        status, error_code = Board.boundary_check(part1_row, part1_col)
        if status:
            status, error_code = Board.boundary_check(part2_row, part2_col)
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

        if len(self.card_list) < 24:
            return False, GameError.CSLCPRN

        last_move = str(self.move_list[len(self.move_list)]).split(':')

        if (prev_part1_row == int(last_move[0]) and
                prev_part1_col == int(last_move[1])):
            return False, GameError.CMLCPOP

        if new_part1_row == prev_part2_row + 1:
            if prev_part1_col == prev_part2_col:  # previous position card is vertical
                if (prev_part1_col == new_part1_col or
                        prev_part1_col == new_part2_col):
                    return False, GameError.RMOPE
            if prev_part1_row == prev_part2_row:  # previous position card is horizontal
                if ((prev_part1_col == new_part1_col or
                     prev_part1_col == new_part2_col or
                     prev_part2_col == new_part1_col or
                     prev_part2_col == new_part2_col)):
                    return False, GameError.RMOPE

        if prev_part1_col == prev_part2_col:  # card is vertical
            if ((prev_part2_row + 1 < self.total_rows) and
                    self.matrix[prev_part2_row + 1][prev_part1_col] != 0):
                return False, GameError.UPNE
        elif prev_part1_row == prev_part2_row:  # card is horizontal
            if (prev_part1_row + 1 < self.total_rows and
                    (self.matrix[prev_part1_row + 1][prev_part1_col] != 0 or
                     self.matrix[prev_part2_row + 1][prev_part2_col] != 0)):
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
                status, error_code = Board.boundary_check(row_tmp - j, col_tmp)

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
                status, error_code = Board.boundary_check(row_tmp, col_tmp + j)
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

                status, error_code = Board.boundary_check(row_tmp, col_tmp - j)
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
                status, error_code = Board.boundary_check(row_c + k, col_c + k)
                if status:
                    card_ru = str(self.matrix[row_c + k, col_c + k])
                    if card_ru != '0':
                        if card_ru[0] == new_card_square_color:
                            color_count_ru = color_count_ru + 1
                        if card_ru[2] == new_card_dot_color:
                            dot_count_ru = dot_count_ru + 1

                status, error_code = Board.boundary_check(row_c - k, col_c + k)
                if status:
                    card_rd = str(self.matrix[row_c - k, col_c + k])
                    if card_rd != '0':
                        if card_rd[0] == new_card_square_color:
                            color_count_rd = color_count_rd + 1
                        if card_rd[2] == new_card_dot_color:
                            dot_count_rd = dot_count_rd + 1

                status, error_code = Board.boundary_check(row_c + k, col_c - k)
                if status:
                    card_lu = str(self.matrix[row_c + k, col_c - k])
                    if card_lu != '0':
                        if card_lu[0] == new_card_square_color:
                            color_count_lu = color_count_lu + 1
                        if card_lu[2] == new_card_dot_color:
                            dot_count_lu = dot_count_lu + 1

                status, error_code = Board.boundary_check(row_c - k, col_c - k)
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
        if last_pos == 0:
            return False, False

        position = self.move_list[last_pos].split(':')
        row = [int(position[0]), int(position[2])]
        col = [int(position[1]), int(position[3])]

        color_set_horizontal, dot_set_horizontal = self.horizontal_set_check(row, col)
        color_set_vertical, dot_set_vertical = self.vertical_set_check(row, col)
        color_set_diagonal, dot_set_diagonal = self.diagonal_set_check(row, col)

        color_set = color_set_horizontal or color_set_vertical or color_set_diagonal
        dot_set = dot_set_horizontal or dot_set_vertical or dot_set_diagonal

        return color_set, dot_set

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

        for move in self.move_list.values():
            move_positions = move.split(':')
            prev_part1_row = int(move_positions[0])
            prev_part1_col = int(move_positions[1])
            prev_part2_row = int(move_positions[2])
            prev_part2_col = int(move_positions[3])

            if prev_part1_col == prev_part2_col:  # card is vertical
                if ((prev_part2_row + 1 < self.total_rows) and
                        self.matrix[prev_part2_row + 1][prev_part1_col] != 0):
                    continue
            elif prev_part1_row == prev_part2_row:  # card is horizontal
                if (prev_part1_row + 1 < self.total_rows and
                        (self.matrix[prev_part1_row + 1][prev_part1_col] != 0 or
                         self.matrix[prev_part2_row + 1][prev_part2_col] != 0)):
                    continue

            card = self.card_list.get(str(prev_part1_row) + str(prev_part1_col), None)
            if card is not None:
                for new_part1_col in range(0, 8):
                    new_part1_row = 0
                    while (new_part1_row < 12 and
                           self.matrix[new_part1_row, new_part1_col] != 0):
                        new_part1_row = new_part1_row + 1
                    if new_part1_row == 12:
                        continue
                    key = str(new_part1_row) + str(new_part1_col)
                    if key in self.card_list:
                        continue

                    error_code = None
                    for rotation in range(1, 9):
                        card_tmp = copy.deepcopy(card)
                        card_tmp.rotate_card(str(rotation))
                        if rotation in (1, 3, 5, 7):
                            new_part2_col = new_part1_col + 1
                            new_part2_row = new_part1_row
                        elif rotation in (2, 4, 6, 8):
                            new_part2_row = new_part1_row + 1
                            new_part2_col = new_part1_col

                        key = str(new_part2_row) + str(new_part2_col)
                        if key in self.card_list:
                            continue

                        # check if move is valid or not
                        status, error_code = self.is_recycle_move_valid(new_part1_row, new_part1_col, new_part2_row,
                                                                        new_part2_col, prev_part1_row,
                                                                        prev_part1_col, prev_part2_row, prev_part2_col)
                        if status:
                            move = (
                                1, card_tmp, new_part1_row, new_part1_col, new_part2_row, new_part2_col, prev_part1_row,
                                prev_part1_col, prev_part2_row, prev_part2_col)
                            possible_moves[move_count] = move
                            move_count = move_count + 1
                        elif error_code == GameError.UPNE:
                            break
                    if error_code == GameError.UPNE:
                        break

        return possible_moves

    def diagonal_heuristic_inf(self, row, col):

        # row 0,2 for part1 and row 1,3 for part2 of the placed card
        diagonal = np.zeros(shape=(4, 8), dtype='object')

        for i in range(0, 2):
            row_tmp = row[i]
            col_tmp = col[i]
            diagonal[i][4] = str(self.matrix[row_tmp, col_tmp])
            diagonal[i + 2][4] = str(self.matrix[row_tmp, col_tmp])

            for k in range(1, 4):
                status, error_code = Board.boundary_check(row_tmp + k, col_tmp + k)
                if status:
                    card_tmp = str(self.matrix[row_tmp + k, col_tmp + k])
                    diagonal[i][4 + k] = card_tmp
                status, error_code = Board.boundary_check(row_tmp - k, col_tmp - k)
                if status:
                    card_tmp = str(self.matrix[row_tmp - k, col_tmp - k])
                    diagonal[i][4 - k] = card_tmp
                status, error_code = Board.boundary_check(row_tmp - k, col_tmp + k)
                if status:
                    card_tmp = str(self.matrix[row_tmp - k, col_tmp + k])
                    diagonal[i + 2][4 + k] = card_tmp
                status, error_code = Board.boundary_check(row_tmp + k, col_tmp - k)
                if status:
                    card_tmp = str(self.matrix[row_tmp + k, col_tmp - k])
                    diagonal[i + 2][4 - k] = card_tmp
        return diagonal

    def diagonal_heuristic_calculation(self, row, col):
        heuristic_value = 0

        diagonals = self.diagonal_heuristic_inf(row, col)

        for diagonal in diagonals:
            # print(diagonal)
            main_part = str(diagonal[4])
            for j in range(1, 4):
                current_cell = str(diagonal[4 + j])
                if current_cell != '0':
                    # print(current_cell +':'+ main_part)
                    if current_cell[0] == main_part[0]:
                        if current_cell[2] == main_part[2]:
                            heuristic_value = heuristic_value + self.second_best_case_value
                        else:
                            heuristic_value = heuristic_value + self.best_case_value
                    else:
                        if current_cell[2] == main_part[2]:
                            heuristic_value = heuristic_value + self.worst_case_value
                            # break?
                        else:
                            heuristic_value = heuristic_value + self.neutral_case_value
                            # break?
                else:
                    heuristic_value = heuristic_value + self.missing_case_value

                current_cell = str(diagonal[4 - j])
                if current_cell != '0':
                    if current_cell[0] == main_part[0]:
                        if current_cell[2] == main_part[2]:
                            heuristic_value = heuristic_value + self.second_best_case_value
                        else:
                            heuristic_value = heuristic_value + self.best_case_value
                    else:
                        if current_cell[2] == main_part[2]:
                            heuristic_value = heuristic_value + self.worst_case_value
                            # break?
                        else:
                            heuristic_value = heuristic_value + self.neutral_case_value
                            # break?
                else:
                    heuristic_value = heuristic_value + self.missing_case_value

        return heuristic_value

    def vertical_heuristic_inf(self, row, col):

        if col[0] == col[1]:  # vertical card
            print('remove this if not required')
        else:  # horizontal card
            verticals = np.zeros(shape=(2, 4), dtype='object')  # row 0 for part1, 1 for the part2 of the placed card
            for i in range(0, 2):
                row_tmp = row[i]
                col_tmp = col[i]
                verticals[i][0] = str(self.matrix[row_tmp, col_tmp])
                for j in range(1, 4):
                    status, error_code = Board.boundary_check(row_tmp - j, col_tmp)
                    if status:
                        card_fwd = str(self.matrix[row_tmp - j, col_tmp])
                        verticals[i][j] = card_fwd

        return verticals

    def vertical_heuristic_calculation(self, row, col):

        heuritic_value = 0

        if row[0] == row[1]:  # for a horizontal card
            verticals = self.vertical_heuristic_inf(row, col)
            for vertical in verticals:
                main_part = str(vertical[0])
                for j in range(1, 4):  # for a pattern below the card
                    current_cell = str(vertical[j])
                    if current_cell != '0':
                        if current_cell[0] == main_part[0]:
                            if current_cell[2] == main_part[2]:
                                heuritic_value = heuritic_value + self.second_best_case_value
                            else:
                                heuritic_value = heuritic_value + self.best_case_value
                        else:
                            if current_cell[2] == main_part[2]:
                                heuritic_value = heuritic_value + self.worst_case_value
                            else:
                                heuritic_value = heuritic_value + self.neutral_case_value
                            break
                    else:
                        heuritic_value = heuritic_value + self.missing_case_value

                # for a pattern above the card
                heuritic_value = heuritic_value + 3 * self.missing_case_value

        else:  # for a vertical card  (Ignore part 1)
            heuritic_value = heuritic_value + 3 * self.missing_case_value  # for part2

        return heuritic_value

    def horizontal_heuristic_inf(self, row, col):

        if row[0] == row[1]:  # horizontal card
            # horizontal = np.zeros(shape=(1, 8), dtype='object')
            horizontal = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
            row_tmp = row[0]
            col_tmp = col[0]
            # print('col_tmp+1:'+str(col_tmp+1))
            horizontal[4] = str(self.matrix[row_tmp, col_tmp])
            horizontal[5] = str(self.matrix[row_tmp, col_tmp + 1])
            for i in range(1, 4):
                status, error_code = Board.boundary_check(row_tmp, col_tmp - i)
                if status:
                    horizontal[4 - i] = str(self.matrix[row_tmp, col_tmp - i])
                status, error_code = Board.boundary_check(row_tmp, col_tmp + 1 + i)
                if status:
                    horizontal[5 + i] = str(self.matrix[row_tmp, col_tmp + 1 + i])
        else:  # vertical card
            # row 0 for part1 and row 1 for the part2 of the placed card
            horizontal = np.zeros(shape=(2, 9), dtype='object')
            for i in range(0, 2):
                row_tmp = row[i]
                col_tmp = col[i]
                horizontal[i][4] = str(self.matrix[row_tmp, col_tmp])
                for j in range(1, 4):
                    status, error_code = Board.boundary_check(row_tmp, col_tmp + j)
                    if status:
                        card_fwd = str(self.matrix[row_tmp, col_tmp + j])
                        horizontal[i][4 + j] = card_fwd
                    status, error_code = Board.boundary_check(row_tmp, col_tmp - j)
                    if status:
                        card_fwd = str(self.matrix[row_tmp, col_tmp - j])
                        horizontal[i][4 - j] = card_fwd

        return horizontal

    def horizontal_heuristic_calculation(self, row, col):

        heuritic_value = 0
        horizontals = self.horizontal_heuristic_inf(row, col)

        if row[0] == row[1]:  # horizontal card
            main_part = str(horizontals[4])
            for j in range(3, 1, -1):
                current_cell = str(horizontals[j])
                if current_cell != '0':
                    if current_cell[0] == main_part[0]:
                        if current_cell[2] == main_part[2]:
                            heuritic_value = heuritic_value + self.second_best_case_value
                        else:
                            heuritic_value = heuritic_value + self.best_case_value
                    else:
                        if current_cell[2] == main_part[2]:
                            heuritic_value = heuritic_value + self.worst_case_value
                        else:
                            heuritic_value = heuritic_value + self.neutral_case_value
                        break
                else:
                    heuritic_value = heuritic_value + self.missing_case_value

            main_part = str(horizontals[5])
            for j in range(1, 3):
                current_cell = str(horizontals[5 + j])
                if current_cell != '0':
                    if current_cell[0] == main_part[0]:
                        if current_cell[2] == main_part[2]:
                            heuritic_value = heuritic_value + self.second_best_case_value
                        else:
                            heuritic_value = heuritic_value + self.best_case_value
                    else:
                        if current_cell[2] == main_part[2]:
                            heuritic_value = heuritic_value + self.worst_case_value
                        else:
                            heuritic_value = heuritic_value + self.neutral_case_value
                        break
                else:
                    heuritic_value = heuritic_value + self.missing_case_value

        else:  # for a vertical card
            for horizontal in horizontals:
                main_part = str(horizontal[4])
                for i in range(1, 8):
                    for j in (i, i + 4):
                        if j >= 8:
                            break
                        current_cell = str(horizontal[j])
                        if current_cell != '0':
                            if current_cell[0] == main_part[0]:
                                if current_cell[2] == main_part[2]:
                                    heuritic_value = heuritic_value + self.second_best_case_value
                                else:
                                    heuritic_value = heuritic_value + self.best_case_value
                            else:
                                if current_cell[2] == main_part[2]:
                                    heuritic_value = heuritic_value + self.worst_case_value
                                    # break?
                                else:
                                    heuritic_value = heuritic_value + self.neutral_case_value
                                    # break?
                        else:
                            heuritic_value = heuritic_value + self.missing_case_value

        return heuritic_value

    def calculate_heuristic_value(self, max_player_preference):

        # color_set = {'RB', 'RW', 'WW', 'WB'}

        last_pos = len(self.move_list)
        position = self.move_list[last_pos].split(':')
        row = [int(position[0]), int(position[2])]
        col = [int(position[1]), int(position[3])]
        #print(self.move_list)

        diagonal_heuristic = self.diagonal_heuristic_calculation(row, col)
        horizontal_heuristic = self.horizontal_heuristic_calculation(row, col)
        vertical_heuristic = self.vertical_heuristic_calculation(row, col)

        heuristic_value = diagonal_heuristic + horizontal_heuristic + vertical_heuristic
        if max_player_preference == PreferenceType.C:
            return round(heuristic_value, 1)
        else:
            return -round(heuristic_value, 1)
