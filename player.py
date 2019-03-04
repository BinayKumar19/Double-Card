# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:18:38 2019

@author: binay
"""
from enum import Enum
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
        self.part1 = {'square': 'N', 'circle': 'N'}
        self.part2 = {'square': 'N', 'circle': 'N'}
        self.rotation = 0

    def _set_side(self, side1_square, side1_circle, side2_square, side2_circle):
        self.part1['square'] = side1_square
        self.part1['circle'] = side1_circle
        self.part2['square'] = side2_square
        self.part2['circle'] = side2_circle

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

    def __init__(self, player_name, player_type, preference_type):
        self.player_name = player_name
        self.player_type = player_type
        self.preference_type = preference_type
        self.cards = []

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

    def find_optimal_move(self, root, card):

        # find all possible card movement in the board find_possible_moves
        root.find_possible_moves()
        # initialise
        node_value_max = float("-inf")
        alpha = float("-inf")
        node_value_min = float("inf")
        beta = float("inf")
        level = 1

        # for each move
        for key, value in root.possible_moves.iteritems():
            # place each move on the board and change current_board_state
            #root.board.regular_move(regular_move(self, card, card_angle, row_old, column_old))
            #new_board_state =
            # call minimax(new_board_state, level,node_value_max, alpha, node_value_min, beta) to find node_value_tmp
            node_value_tmp = root.minimax(root.board, level, node_value_max, alpha, node_value_min, beta)
            # if greater than node_value_max than update node_value_max with node_value_tmp
            if node_value_max < node_value_tmp:
                node_value_max = node_value_tmp
                # assign optimal_move
                optimal_move = value
                # assign node_value_max to alpha
                alpha = node_value_max
        # return optimal_move
        return optimal_move

class TreeNode:
    possible_moves = {}
    heuristic_value = 0

    def __init__(self, board):
        self.board = board
        self.matrix = board.matrix

    def find_possible_moves(self, card):
        move_count = 1
        for column in range(0, 9):
            row = 0
            while (row < 12 and
                   self.matrix[row, column] != '0'):
                        row = row + 1
            if row == 12:
                continue
            else:
                row = row - 1

            for rotation in range(1, 9):
                card.rotate_card(rotation)

                if rotation in ('1', '3', '5', '7'):
                    part2_col = column + 1
                    part2_row = row
                elif rotation in ('2', '4', '6', '8'):
                    part2_row = row + 1
                    part2_col = column

                # check if move is valid or not

                move =(row,column,part2_row,part2_col)
                self.possible_moves[move_count] = move
                move_count = move_count + 1

    def minimax(self, board_current, level, node_value, alpha, beta):

        # if maximum level is reached, check whose turn is this(max or min)
        # call find_possible_moves for the current state to find all possible moves
        # find new_board_state for each possible moves by placing the card on the current_board_state
        # calculate_heuristic_value(new_board_state) and if greater than previous node_value than update node_value
        # if max's turn is there
        # if node_value greater than beta no need to go further(pruing)
        # assign node_value to alpha if greater than alpha
        # if min's turn is there
        #
        # Return node_value
        # else
        # use the new board to create a node
            board_new = copy.deepcopy(board_current)
            node_new = TreeNode(board_new)
        # create all possible moves for the node
        # for each move
        # place move on the board and find new_board_state
        # if max's turn is there
        # call minimax(new_board_state, level+1,node_value_max, alpha, node_value_min, beta) to find node_value_tmp
        # if greater than node_value_max than update node_value_max
        # if node_value_max greater than beta no need to go further(pruing)
        # assign node_value_max to alpha if greater than alpha
        # if min's turn is there
        # call minimax(new_board_state, level+1,node_value_max, alpha, node_value_min, beta) to find node_value_tmp
        # if less than previous node_value_min than update node_value_min with node_value_tmp
        # if node_value_min less than alpha no need to go further(pruing)
        # assign node_value_min to beta if smaller than beta

        # check if max or min turn
        # if min's turn then choose the minimum value out of all children's value
        # if max's turn then choose the maximum value out of all children's value
        # return the chosen value to the calling node

        def calculate_heuristic_value(self, board_state):
    # logic for calculation of heuristic value
    # return heuristic value