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
    heuristic_eval_count = None
    current_level_heuristic_value = None
    level2_heuristic_values = None
    minimax_level = 3

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

    def find_optimal_move(self, board, card):

        # initialise
        alpha = float("-inf")
        beta = float("inf")
        self.heuristic_eval_count = 0
        self.level2_heuristic_values = []
        new_board = copy.deepcopy(board)

        self.current_level_heuristic_value, optimal_move = self._minimax(new_board, card, self.minimax_level, alpha,
                                                                         beta, True)

        FileWriter.write_to_trace_file(self.heuristic_eval_count, self.current_level_heuristic_value,
                                       self.level2_heuristic_values)
        return optimal_move

    def _minimax(self, board_current, card, level, alpha, beta, max_player):

        node = TreeNode(board_current)
        possible_moves = node.find_possible_moves(card)
        optimal_move = 0
        if max_player:
            node_value_max = float("-inf")
            for key, value in possible_moves.items():
                card = value[0]
                part1_row = value[1]
                part1_col = value[2]
                part2_row = value[3]
                part2_col = value[4]
                board_current.place_card(card, part1_row, part1_col, part2_row, part2_col)

                if level == 1:
                    self.heuristic_eval_count = self.heuristic_eval_count + 1
                    node_value_tmp = board_current.calculate_heuristic_value(self.preference_type)
                else:
                    node_value_tmp, optimal_move = self._minimax(board_current, card, level - 1, alpha,
                                                                 beta, not max_player)
                board_current.remove_card(part1_row, part1_col, part2_row, part2_col)
                if node_value_max < node_value_tmp:
                    optimal_move = value
                    node_value_max = node_value_tmp
                if self.alpha_beta_activated:
                    alpha = max(alpha, node_value_tmp)
                    if beta <= alpha:
                        break

            if level == (self.minimax_level - 1):
                self.level2_heuristic_values.append(node_value_max)

            return node_value_max, optimal_move
        else:
            node_value_min = float("inf")
            for key, value in possible_moves.items():
                card = value[0]
                part1_row = value[1]
                part1_col = value[2]
                part2_row = value[3]
                part2_col = value[4]
                board_current.place_card(card, part1_row, part1_col, part2_row, part2_col)

                if level == 1:
                    node_value_tmp = board_current.calculate_heuristic_value(self.preference_type)
                else:
                    node_value_tmp, optimal_move = self._minimax(board_current, card, level - 1, alpha,
                                                                 beta, not max_player)
                board_current.remove_card(part1_row, part1_col, part2_row, part2_col)
                if node_value_min > node_value_tmp:
                    optimal_move = value
                    node_value_min = node_value_tmp
                if self.alpha_beta_activated:
                    beta = min(beta, node_value_tmp)
                    if beta <= alpha:
                        break
            if level == 2:
                self.level2_heuristic_values.append(node_value_min)
        return node_value_min, optimal_move


class TreeNode:

    def __init__(self, board):
        self.board = board
        self.matrix = board.matrix

    def find_possible_moves(self, card):
        move_count = 1
        possible_moves = {}
        for column in range(0, 8):
            row = 0
            while (row < 12 and
                   self.matrix[row, column] != 0):
                row = row + 1
            if row == 12:
                continue
            # else:
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
                    possible_moves[move_count] = move
                    move_count = move_count + 1
        return possible_moves
