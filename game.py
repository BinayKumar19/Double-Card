# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:48:07 2019

@author: binay
"""
from board import Board, GameError
from player import PreferenceType, TreeNode
from enum import Enum
import datetime

class GameStage(Enum):
    REG = 'Regular'
    REC = 'Recycle'
    end = 'End'


class Game:

    def __init__(self, game_type):
        self.game_type = game_type
        self.board = Board()
        self.current_turn = 0
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

        color_set, dot_set = self.board.check_winner()
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

    def play_automatic_move(self):

        #find an optimal move
        card = self.players[self.current_turn].get_card()
        move = self.players[self.current_turn].find_optimal_move(self.board, card)
        card = move[0]
        part1_row = move[1]
        part1_col = move[2]
        part2_row = move[3]
        part2_col = move[4]
        self.board.place_card(card, part1_row, part1_col, part2_row, part2_col)
        print('automatic move:')
        print(move)
