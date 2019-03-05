# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

# AI Game
import numpy as np
from enum import Enum
import random

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

    def place_card(self, card, row, column, part2_row, part2_col):
        self.matrix[row, column] = card.part1['Color'] + ':' + card.part1['Dot']
        self.matrix[part2_row, part2_col] = card.part2['Color'] + ':' + card.part2['Dot']
        self.card_list[str(row) + str(column)] = card
        moves_count = len(self.move_list)
        self.move_list[moves_count + 1] = str(row) + ':' + str(column) + ':' + str(part2_row) + ':' + str(part2_col)

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

    def calculate_heuristic_value(self, board_state, max_player, max_player_preference):
    # # logic for calculation of heuristic value
    #     for i in range(0, 12):
    #         for j in range(0, 8):
    #             card_side = self.matrix[i, j].split(':')
      return random.randint(1, 10)

    # return heuristic value