# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:48:07 2019

@author: binay
"""
from board import Board, GameError
from player import PreferenceType, TreeNode
from enum import Enum


class GameStage(Enum):
    REG = 'Regular'
    REC = 'Recycle'
    end = 'End'


class Game:
    def __init__(self, game_type):
        self.game_type = game_type
        self.board = Board()
        self.current_turn = 0  # not defined
        self.players = []
        self.winner = 'N'
        self.stage = GameStage.REG

    def add_player(self, player):
        self.players.append(player)

    def change_turn(self):
        if self.current_turn == 0:
            self.current_turn = 1
        else:
            self.current_turn = 0

    def play_regular_move(self, card_angle, row, column):
        status = False
        if self.players[self.current_turn].card_available():
            card = self.players[self.current_turn].get_card()
            status, error_code = self.board.regular_move(card, card_angle, row, column)

            if status:
                self.is_winner_decided()
                if len(self.board.card_list) == 24:
                    self.stage = GameStage.REC
        else:
            self.stage = GameStage.REC
            error_code = GameError.ORMAN
        return status, error_code

    def play_recycle_move(self, prev_part1_row, prev_part1_col, prev_part2_row,
                          prev_part2_col, card_angle, row, column):
        status, error_code = self.board.recycle_move(prev_part1_row, prev_part1_col, prev_part2_row,
                                                     prev_part2_col, card_angle, row, column)
        if status:
            self.is_winner_decided()
            if len(self.board.move_list) == 60:
                self.stage = GameStage.end
            return status, error_code

        return status, error_code

    def print_board(self):
        print(self.matrix)

    def _set_winner(self, color_set, dot_set):

        if (color_set and
                self.players[self.current_turn].preference_type == PreferenceType.C):
            self.winner = self.players[self.current_turn]
        elif (dot_set and
              self.players[self.current_turn].preference_type == PreferenceType.D):
            self.winner = self.players[self.current_turn]
        elif (color_set and
              self.players[self.current_turn].preference_type == PreferenceType.D):
            self.winner = self.players[1 - self.current_turn]
        elif (dot_set and
              self.players[self.current_turn].preference_type == PreferenceType.C):
            self.winner = self.players[1 - self.current_turn]
        else:
            return False
        self.stage = GameStage.end
        return True

    def is_winner_decided(self):
        status = False
        move_count = len(self.board.move_list)

        if move_count == 60:
            self.stage = GameStage.end
            return status

        color_set_horizontal, dot_set_horizontal = self._winner_check_horizontal()
        color_set_vertical, dot_set_vertical = self._winner_check_vertical()
        color_set_diagonal, dot_set_diagonal = self._winner_check_diagonal()

        color_set = color_set_horizontal or color_set_vertical or color_set_diagonal
        dot_set = dot_set_horizontal or dot_set_vertical or dot_set_diagonal

        status = self._set_winner(color_set, dot_set)
        return status

    def get_stage(self):
        return self.stage

    def print_result(self):
        if self.winner == 'N':
            print('Draw')
        else:
            print('Winner is ' + self.winner.player_name + '(' + str(self.winner.preference_type.value) + ')')

    def display_board(self):
        self.board.print_board()

    def _winner_check_vertical(self):
        last_pos = len(self.board.move_list)
        position = self.board.move_list[last_pos].split(':')
        row = [int(position[0]), int(position[2])]
        col = [int(position[1]), int(position[3])]
        color_set = False
        dot_set = False

        for i in range(0, 2):
            previous_dot_type_fwd = 'N'
            previous_color_type_fwd = 'N'
            color_count_fwd = 0
            dot_count_fwd = 0
            previous_dot_type_bck = 'N'
            previous_color_type_bck = 'N'
            color_count_bck = 0
            dot_count_bck = 0

            row_tmp = row[i]
            col_tmp = col[i]
            dot_set_tmp = False
            color_set_tmp = False
            for j in range(0, 4):
                status, error_code = self.board.boundary_check(row_tmp + j, col_tmp)
                if status:
                    card_fwd = str(self.board.matrix[row_tmp + j, col_tmp])
                    if card_fwd != '0':
                        if card_fwd[0] == previous_color_type_fwd:
                            color_count_fwd = color_count_fwd + 1
                        else:
                            previous_color_type_fwd = card_fwd[0]
                            color_count_fwd = 1

                        if card_fwd[2] == previous_dot_type_fwd:
                            dot_count_fwd = dot_count_fwd + 1
                        else:
                            previous_dot_type_fwd = card_fwd[2]
                            dot_count_fwd = 1

                status, error_code = self.board.boundary_check(row_tmp - j, col_tmp)

                if status:
                    card_bck = str(self.board.matrix[row_tmp - j, col_tmp])
                    if card_bck != '0':
                        if card_bck[0] == previous_color_type_bck:
                            color_count_bck = color_count_bck + 1
                        else:
                            previous_color_type_bck = card_bck[0]
                            color_count_bck = 1

                        if card_bck[2] == previous_dot_type_bck:
                            dot_count_bck = dot_count_bck + 1
                        else:
                            previous_dot_type_bck = card_bck[2]
                            dot_count_bck = 1

                if (dot_count_fwd == 4 or
                        dot_count_bck == 4):
                    dot_set_tmp = True
                if (color_count_fwd == 4 or
                        color_count_bck == 4):
                    color_set_tmp = True

        color_set = color_set or color_set_tmp
        dot_set = dot_set or dot_set_tmp

        return color_set, dot_set

    def _winner_check_horizontal(self):
        last_pos = len(self.board.move_list)
        position = self.board.move_list[last_pos].split(':')
        row = [int(position[0]), int(position[2])]
        col = [int(position[1]), int(position[3])]
        color_set = False
        dot_set = False

        for i in range(0, 2):
            previous_dot_type_fwd = 'N'
            previous_color_type_fwd = 'N'
            color_count_fwd = 0
            dot_count_fwd = 0
            previous_dot_type_bck = 'N'
            previous_color_type_bck = 'N'
            color_count_bck = 0
            dot_count_bck = 0

            row_tmp = row[i]
            col_tmp = col[i]
            dot_set_tmp = False
            color_set_tmp = False
            for j in range(0, 4):
                status, error_code = self.board.boundary_check(row_tmp, col_tmp + j)
                if status:
                    card_fwd = str(self.board.matrix[row_tmp, col_tmp + j])
                    if (card_fwd != '0'):
                        if (card_fwd[0] == previous_color_type_fwd):
                            color_count_fwd = color_count_fwd + 1
                        else:
                            previous_color_type_fwd = card_fwd[0]
                            color_count_fwd = 1

                        if (card_fwd[2] == previous_dot_type_fwd):
                            dot_count_fwd = dot_count_fwd + 1
                        else:
                            previous_dot_type_fwd = card_fwd[2]
                            dot_count_fwd = 1

                status, error_code = self.board.boundary_check(row_tmp, col_tmp - j)
                if status:
                    card_bck = str(self.board.matrix[row_tmp, col_tmp - j])
                    if card_bck != '0':
                        if card_bck[0] == previous_color_type_bck:
                            color_count_bck = color_count_bck + 1
                        else:
                            previous_color_type_bck = card_bck[0]
                            color_count_bck = 1

                        if card_bck[2] == previous_dot_type_bck:
                            dot_count_bck = dot_count_bck + 1
                        else:
                            previous_dot_type_bck = card_bck[2]
                            dot_count_bck = 1

            if (dot_count_fwd == 4 or
                    dot_count_bck == 4):
                dot_set_tmp = True
            if (color_count_fwd == 4 or
                    color_count_bck == 4):
                color_set_tmp = True

            color_set = color_set or color_set_tmp
            dot_set = dot_set or dot_set_tmp

        return color_set, dot_set

    def _winner_check_diagonal(self):
        last_pos = len(self.board.move_list)
        position = self.board.move_list[last_pos].split(':')
        row = [int(position[0]), int(position[2])]
        col = [int(position[1]), int(position[3])]

        color_set = False
        dot_set = False

        for i in range(0, 2):
            row_c = row[i]
            col_c = col[i]
            new_card_square_color = self.board.matrix[row_c, col_c][0]
            new_card_dot_color = self.board.matrix[row_c, col_c][2]

            color_count_ru = 1
            dot_count_ru = 1
            color_count_rd = 1
            dot_count_rd = 1
            color_count_lu = 1
            dot_count_lu = 1
            color_count_ld = 1
            dot_count_ld = 1

            for k in range(1, 4):
                status, error_code = self.board.boundary_check(row_c + k, col_c + k)
                if status:
                    card_ru = str(self.board.matrix[row_c + k, col_c + k])
                    if card_ru != '0':
                        if card_ru[0] == new_card_square_color:
                            color_count_ru = color_count_ru + 1
                        if card_ru[2] == new_card_dot_color:
                            dot_count_ru = dot_count_ru + 1

                status, error_code = self.board.boundary_check(row_c - k, col_c + k)
                if status:
                    card_rd = str(self.board.matrix[row_c - k, col_c + k])
                    if card_rd != '0':
                        if card_rd[0] == new_card_square_color:
                            color_count_rd = color_count_rd + 1
                        if card_rd[2] == new_card_dot_color:
                            dot_count_rd = dot_count_rd + 1

                status, error_code = self.board.boundary_check(row_c + k, col_c - k)
                if status:
                    card_lu = str(self.board.matrix[row_c + k, col_c - k])
                    if card_lu != '0':
                        if card_lu[0] == new_card_square_color:
                            color_count_lu = color_count_lu + 1
                        if card_lu[2] == new_card_dot_color:
                            dot_count_lu = dot_count_lu + 1

                status, error_code = self.board.boundary_check(row_c - k, col_c - k)
                if status:
                    card_ld = str(self.board.matrix[row_c - k, col_c - k])
                    if card_ld != '0':
                        if card_ld[0] == new_card_square_color:
                            color_count_ld = color_count_ld + 1
                        if card_ld[2] == new_card_dot_color:
                            dot_count_ld = dot_count_ld + 1

            color_set_tmp = False
            dot_set_tmp = False

            if (color_count_ru == 4 or
                    color_count_rd == 4 or
                    color_count_lu == 4 or
                    color_count_ld == 4):
                color_set_tmp = True

            if (dot_count_ru == 4 or
                    dot_count_rd == 4 or
                    dot_count_lu == 4 or
                    dot_count_ld == 4):
                dot_set_tmp = True

            color_set = color_set or color_set_tmp
            dot_set = dot_set or dot_set_tmp

        return color_set, dot_set

    def play_automatic_move(self):

        #find an optimal move
         board_copy = self.board.copy()
         root = TreeNode(board_copy)
         card = self.players[self.current_turn].get_card()
         self.players[self.current_turn].find_optimal_move(root, card)

         self.tree_traversal(board_copy)
        # call regular move or recycle move depending on the condition


    def tree_traversal(self, board_tmp):
        board_tmp.

