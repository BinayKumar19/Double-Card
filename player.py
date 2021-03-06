# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:18:38 2019

@author: binay
"""
from utilities import FileWriter, GameError
import copy
from game import Game, GameStage

"""
==========
player
==========
This module contains a Card class and a Player class to implement the logic required at the player's end.

Contents
--------
* Card - A class representing the card.
* Player - A class representing the player playing the game, contains card assigned to the player.
* _set_card_side() - To set the card on a particular side.
* rotate_card() - To rotate the card.
* get_card() - returns card from the player.
* is_card_available() - Checks if the player has a card or not.
* find_AI_optimal_move() - Finds optimal move for the AI using Minimax/Alpha-Beta Algorithm.
* _minimax_algo() - Minimax Algorithm logic.

"""


class Card:
    """
    Instance represent a Card Object.
    ===========
    Description
    ===========
    Represent the card which will be placed by Players on the board.
    """
    def __init__(self):
        self.part1 = {'Color': 'N', 'Dot': 'N'}
        self.part2 = {'Color': 'N', 'Dot': 'N'}
        self.rotation = None

    def _set_card_side(self, side1_color, side1_dot, side2_color, side2_dot):
        """
        Returns:
        ===========
        Description
        ===========
        Sets the card sides.
        """

        self.part1['Color'] = side1_color
        self.part1['Dot'] = side1_dot
        self.part2['Color'] = side2_color
        self.part2['Dot'] = side2_dot

    def rotate_card(self, rotation_value):
        """
        Returns:
        ===========
        Description
        ===========
        Rotate the card according to the rotation_value
        """
        if rotation_value in ('1', '4'):
            self._set_card_side('R', 'B', 'W', 'W')
        elif rotation_value in ('2', '3'):
            self._set_card_side('W', 'W', 'R', 'B')
        elif rotation_value in ('5', '8'):
            self._set_card_side('R', 'W', 'W', 'B')
        elif rotation_value in ('6', '7'):
            self._set_card_side('W', 'B', 'R', 'W')
        else:
            raise ValueError(GameError.IRV.value)

        self.rotation = rotation_value


class Player:
    """
    Instance represent a Player Object.
    ===========
    Description
    ===========
    Represent the Players, can be Human or AI.
    """
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
        """
         Returns: Card object
         ===========
         Description
         ===========
         Return card from the card list
         """
        return self.cards.pop()

    def is_card_available(self):
        """
        Returns: True or False
        ===========
        Description
        ===========
        Return True if cards are available with the player, otherwise False.
        """
        if len(self.cards) > 0:
            return True
        else:
            return False

    def find_AI_optimal_move(self, board):
        """
        Returns: optimal move
        ===========
        Description
        ===========
        Finds optimal move for the AI player.
        """
        # initialise
        alpha = float("-inf")
        beta = float("inf")
        self.heuristic_eval_count = 0
        self.level2_heuristic_values = []
        new_board = copy.deepcopy(board)

        if Game.stage == GameStage.REC:
            card = None
        else:
            card = self.get_card()

        new_board.max_player_preference = self.preference_type
        new_board.set_heuristic_parameters()
        self.current_level_heuristic_value, optimal_move = self._minimax_algo(new_board, card, self.minimax_level, alpha,
                                                                              beta, True)

        FileWriter.write_to_trace_file(self.heuristic_eval_count, self.current_level_heuristic_value,
                                       self.level2_heuristic_values)
        return optimal_move

    def _minimax_algo(self, board_current, card, level, alpha, beta, max_player):
        """
        Returns: heuristic value, optimal move
        ===========
        Description
        ===========
        Using Minimax algorithm, finds the heuristic value and the optimal mode,
        If alpha_beta_activated is True, Alpha Beta pruning is activated.
        """
        color_set, dot_set = board_current.check_winner()

        if level == 1 or color_set or dot_set:
            self.heuristic_eval_count = self.heuristic_eval_count + 1
            node_value_tmp = board_current.calculate_heuristic_value()
            return node_value_tmp, None

        if Game.stage == GameStage.REC:
            possible_moves = board_current.find_possible_recycle_moves()
        else:
            possible_moves = board_current.find_possible_regular_moves(card)
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
                    board_current.place_card(card, part1_row, part1_col, part2_row, part2_col, True)
                else:
                    prev_part1_row = value[6]
                    prev_part1_col = value[7]
                    prev_part2_row = value[8]
                    prev_part2_col = value[9]
                    card_temp = board_current.remove_card(prev_part1_row, prev_part1_col, prev_part2_row,
                                                          prev_part2_col, False)
                    board_current.place_card(card, part1_row, part1_col, part2_row, part2_col, True)

                node_value_tmp, optimal_move_tmp = self._minimax_algo(board_current, card, level - 1, alpha,
                                                                      beta, not max_player)

                board_current.remove_card(part1_row, part1_col, part2_row, part2_col, True)
                if move_type == 1:  # revert the recycle move
                    board_current.place_card(card_temp, prev_part1_row, prev_part1_col, prev_part2_row, prev_part2_col,
                                             False)

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
                    board_current.place_card(card, part1_row, part1_col, part2_row, part2_col, True)
                else:
                    prev_part1_row = value[6]
                    prev_part1_col = value[7]
                    prev_part2_row = value[8]
                    prev_part2_col = value[9]
                    card_temp = board_current.remove_card(prev_part1_row, prev_part1_col, prev_part2_row,
                                                          prev_part2_col, False)
                    board_current.place_card(card, part1_row, part1_col, part2_row, part2_col, True)

                node_value_tmp, optimal_move_tmp = self._minimax_algo(board_current, card, level - 1, alpha, beta,
                                                                      not max_player)

                board_current.remove_card(part1_row, part1_col, part2_row, part2_col, True)

                if move_type == 1:  # revert the recycle move
                    board_current.place_card(card_temp, prev_part1_row, prev_part1_col, prev_part2_row, prev_part2_col,
                                             False)

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
