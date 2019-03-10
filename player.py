# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:18:38 2019

@author: binay
"""
from enum import Enum
from utilities import FileWriter, GameError
import copy
from game import Game, GameStage


class Card:

    def __init__(self):
        self.part1 = {'Color': 'N', 'Dot': 'N'}
        self.part2 = {'Color': 'N', 'Dot': 'N'}
        self.rotation = None

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
        else:
            raise ValueError(GameError.IRV.value)

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

    def find_optimal_move(self, board):

        # initialise
        alpha = float("-inf")
        beta = float("inf")
        self.heuristic_eval_count = 0
        self.level2_heuristic_values = []
        new_board = copy.deepcopy(board)

        if Game.stage == GameStage.REC :
            card = None
        else:
            card = self.get_card()

        self.current_level_heuristic_value, optimal_move = self._minimax(new_board, card, self.minimax_level, alpha,
                                                                         beta, True)

        FileWriter.write_to_trace_file(self.heuristic_eval_count, self.current_level_heuristic_value,
                                       self.level2_heuristic_values)
        return optimal_move

    def _minimax(self, board_current, card, level, alpha, beta, max_player):

        if Game.stage == GameStage.REC:
            possible_moves = board_current.find_possible_recycle_moves()
        else:
            possible_moves = board_current.find_possible_normal_moves(card)

        optimal_move = 0
        if max_player:
            node_value_max = float("-inf")
            for key, value in possible_moves.items():
                move_type = value[0]
                card = value[1]
                part1_row = value[2]
                part1_col = value[3]
                part2_row = value[4]
                part2_col = value[5]
                if move_type == 0:
                    board_current.place_card(card, part1_row, part1_col, part2_row, part2_col)
                else:
                    prev_part1_row = value[6]
                    prev_part1_col = value[7]
                    prev_part2_row = value[8]
                    prev_part2_col = value[9]
                    card_temp = board_current.remove_card(prev_part1_row, prev_part1_col, prev_part2_row, prev_part2_col)

                    board_current.matrix[part1_row, part1_col] = card.part1['Color'] + ':' + card.part1['Dot']
                    board_current.matrix[part2_row, part2_col] = card.part2['Color'] + ':' + card.part2['Dot']
                    board_current.card_list[str(part1_row) + str(part1_col)] = card


                color_set, dot_set = board_current.check_winner()

                if level == 1 or color_set or dot_set:
                    self.heuristic_eval_count = self.heuristic_eval_count + 1
                    node_value_tmp = board_current.calculate_heuristic_value(self.preference_type)
                else:
                    node_value_tmp, optimal_move = self._minimax(board_current, card, level - 1, alpha,
                                                                 beta, not max_player)

                board_current.remove_card(part1_row, part1_col, part2_row, part2_col)
                if move_type == 1:
                     board_current.matrix[prev_part1_row, prev_part1_col] = card_temp.part1['Color'] + ':' + card_temp.part1['Dot']
                     board_current.matrix[prev_part2_row, prev_part2_col] = card_temp.part2['Color'] + ':' + card_temp.part2['Dot']
                     board_current.card_list[str(prev_part1_row) + str(prev_part1_col)] = card_temp

                if node_value_max < node_value_tmp:
                    optimal_move = value
                    node_value_max = node_value_tmp
                if self.alpha_beta_activated:
                    alpha = max(alpha, node_value_tmp)
                    if beta <= alpha:
                        break

            return node_value_max, optimal_move
        else:
            node_value_min = float("inf")
            for key, value in possible_moves.items():
                move_type = value[0]
                card = value[1]
                part1_row = value[2]
                part1_col = value[3]
                part2_row = value[4]
                part2_col = value[5]
                if move_type == 0:
                    board_current.place_card(card, part1_row, part1_col, part2_row, part2_col)
                else:
                    prev_part1_row = value[6]
                    prev_part1_col = value[7]
                    prev_part2_row = value[8]
                    prev_part2_col = value[9]
                    card_temp = board_current.remove_card(prev_part1_row, prev_part1_col, prev_part2_row, prev_part2_col)
                    board_current.matrix[part1_row, part1_col] = card.part1['Color'] + ':' + card.part1['Dot']
                    board_current.matrix[part2_row, part2_col] = card.part2['Color'] + ':' + card.part2['Dot']
                    board_current.card_list[str(part1_row) + str(part1_col)] = card

                if level == 1:
                    node_value_tmp = board_current.calculate_heuristic_value(self.preference_type)
                else:
                    node_value_tmp, optimal_move = self._minimax(board_current, card, level - 1, alpha,
                                                                 beta, not max_player)
                board_current.remove_card(part1_row, part1_col, part2_row, part2_col)

                if move_type == 1:
                    board_current.matrix[prev_part1_row, prev_part1_col] = card_temp.part1['Color'] + ':' + card_temp.part1['Dot']
                    board_current.matrix[prev_part2_row, prev_part2_col] = card_temp.part2['Color'] + ':' + card_temp.part2['Dot']
                    board_current.card_list[str(prev_part1_row) + str(prev_part1_col)] = card_temp

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
