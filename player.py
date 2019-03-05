# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:18:38 2019

@author: binay
"""
from enum import Enum
from utilities import FileWriter
import copy

class PlayerType(Enum):
    H = 'HUMAN'
    AI = 'AI'


class PreferenceType(Enum):
    D = 'DOT'
    C = 'COLOR'


class Card:

    def __init__(self):
        self.side1 = True
        self.part1 = {'Color': 'N', 'Dot': 'N'}
        self.part2 = {'Color': 'N', 'Dot': 'N'}
        self.rotation = 0

    def _set_side(self, side1_color, side1_dot, side2_color, side2_dot):
        self.part1['Color'] = side1_color
        self.part1['Dot'] = side1_dot
        self.part2['Color'] = side2_color
        self.part2['Dot'] = side2_dot

    def rotate_card(self, rotation_value):
        if rotation_value in ('1', '4'):
            self._set_side('R', 'B', 'W', 'W')
        elif rotation_value in ('2', '3'):
            self._set_side('W', 'W', 'R', 'B')
        elif rotation_value in ('5', '8'):
            self._set_side('R', 'W', 'W', 'B')
        elif rotation_value in ('6', '7'):
            self._set_side('W', 'B', 'R', 'W')

        self.rotation = rotation_value


class Player:

    def __init__(self, player_name, player_type, preference_type, alpha_beta_activated):
        self.player_name = player_name
        self.player_type = player_type
        self.preference_type = preference_type
        self.cards = []
        self.alpha_beta_activated = alpha_beta_activated

        for i in range(0, 12):
            card = Card()
            self.cards.append(card)

    def get_card(self):
        return self.cards.pop()

    def card_available(self):
        if len(self.cards) > 0:
            return True
        else:
            return False

    def find_optimal_move(self, board, card, level):

        # initialise
        node_value_max = float("-inf")
        alpha = float("-inf")
        node_value_min = float("inf")
        beta = float("inf")
        node_value_max, optimal_move = self._minimax(board, card, level, node_value_max, alpha, node_value_min, beta,
                                                    True, self.preference_type)

        return optimal_move

    def _minimax(self, board_current, card, level, node_value_max, alpha, node_value_min, beta, max_player, max_player_pref_type):

        node = TreeNode(board_current)
        node.find_possible_moves(card)
        new_board = copy.deepcopy(node.board)
        optimal_move = 0
        FileWriter.write_to_trace_file('level:' + str(level) + '  moves' + str(len(node.possible_moves)))
        for key, value in node.possible_moves.items():
            #print(key, value[0].part1,value[0].part2,value[1],value[2],value[3],value[4])
            card = value[0]
            part1_row = value[1]
            part1_col = value[2]
            part2_row = value[3]
            part2_col = value[4]

            new_board.place_card(card, part1_row, part1_col, part2_row, part2_col)
            if level == 1:  # leaf nodes
                node_value_tmp = new_board.calculate_heuristic_value(new_board, max_player, max_player_pref_type)
            else:
                node_value_tmp, optimal_move = self._minimax(new_board, card, level - 1, node_value_max, alpha,
                                                             node_value_min, beta, not max_player, max_player_pref_type)
            if max_player:
                if node_value_max < node_value_tmp:
                    node_value_max = node_value_tmp
                    optimal_move = value
                    if (node_value_max > beta and
                            self.alpha_beta_activated):  # if node_value_max greater than beta no need to go further(pruing)
                        break
                    if alpha < node_value_max:
                        alpha = node_value_max
            else:
                if node_value_min > node_value_tmp:
                    node_value_min = node_value_tmp
                    optimal_move = value
                    if (node_value_min < alpha and
                            self.alpha_beta_activated):  # if node_value_min less than alpha no need to go further(pruing)
                        break
                    if beta > node_value_min:
                        beta = node_value_min

            new_board.matrix[part1_row, part1_col] = 0
            new_board.matrix[part2_row, part2_col] = 0

        if max_player:
            return node_value_max, optimal_move
        else:
            return node_value_min, optimal_move


class TreeNode:
    possible_moves = {}
    heuristic_value = 0

    def __init__(self, board):
        self.board = board
        self.matrix = board.matrix

    def find_possible_moves(self, card):
        move_count = 1
        for column in range(0, 8):
            row = 0
            while (row < 12 and
                   self.matrix[row, column] != 0):
                row = row + 1
            if row == 12:
                continue
            #else:
             #   row = row - 1

            for rotation in range(1, 9):
                card_tmp = copy.deepcopy(card)
                card_tmp.rotate_card(str(rotation))
                if rotation in (1, 3, 5, 7):
                    part2_col = column + 1
                    part2_row = row
                elif rotation in (2, 4, 6, 8):
                    part2_row = row + 1
                    part2_col = column

                # check if move is valid or not
                status, error_code = self.board.is_new_move_valid(str(rotation), row, column, part2_row, part2_col)
                if status:
                  #  print(row, column, part2_row, part2_col)
                    move = (card_tmp, row, column, part2_row, part2_col)
                    self.possible_moves[move_count] = move
                    move_count = move_count + 1
                # else:
                #     print(error_code)
                #     print(row, column, part2_row, part2_col)
