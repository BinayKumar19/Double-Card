# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:48:07 2019

@author: binay
"""
from board import Board
from enum import Enum
from utilities import position_translation, GameError, PreferenceType
import datetime

"""
==========
game
==========
This module contains a Game class that represent the game and contain board, players and methods to necessary to play 
the game.

Contents
--------
* Game     - Game class that represent the game which will be played.
* GameStage - An enumeration to represent the stage of the game i.e. Regular, Recycle or End.
* add_player() - Add player to the game.
* change_player_turn() - Change player's turn.
* play_regular_move() - Play regular move on the board.
* play_recycle_move() - Play recycle move on the board.
* _set_winner() - Set a winner for the game.
* print_result() - print result of the game.
* display_board() - display the board.
* play_manual_move() - play manual move for the human player.
* play_automatic_move() - play automatic move for the AI.

"""


class GameStage(Enum):
    REG = 'Regular'
    REC = 'Recycle'
    end = 'End'


class Game:
    """
    Instance represent a Game Object.
    ===========
    Description
    ===========
    Represent the game which will be played.
    """
    stage = None
    draw_move_count = 40

    def __init__(self, game_type):
        self.game_type = game_type
        self.board = Board()
        self.current_turn = 0
        self.players = []
        self.winner = 'N'
        Game.stage = GameStage.REG

    def add_player(self, player):
        """
        Returns:
        ===========
        Description
        ===========
        Receives a player as a parameter and add it to the game.
        """
        self.players.append(player)

    def change_player_turn(self):
        """
        Returns:
        ===========
        Description
        ===========
        Changes the player turn.
        """
        if self.current_turn == 0:
            self.current_turn = 1
        else:
            self.current_turn = 0

    def _card_part2_position(self, card_rotation, row, column):
        """
        Returns: row and column value for the second half part of the card
        ===========
        Description
        ===========
        Finds the position for the second half part of the card through rotation value.
        """
        if card_rotation in ('1', '3', '5', '7'):
            part2_col = column + 1
            part2_row = row
        elif card_rotation in ('2', '4', '6', '8'):
            part2_row = row + 1
            part2_col = column
        else:
            raise ValueError(GameError.IRV.value)
        return part2_row, part2_col

    def play_regular_move(self, card_rotation, card_part1_row, card_part1_col):
        """
        Returns: status and error code
        ===========
        Description
        ===========
        After validating the regular move, plays it by calling board.place_card(),
        If validation fails, returns False and the error code.
        """
        if self.players[self.current_turn].is_card_available():
            card_part2_row, card_part2_col = self._card_part2_position(card_rotation, card_part1_row,
                                                                       card_part1_col)
            status, error_code = self.board.is_regular_move_valid(card_part1_row, card_part1_col,
                                                                  card_part2_row, card_part2_col)
            if status:
                card = self.players[self.current_turn].get_card()
                card.rotate_card(card_rotation)
                self.board.place_card(card, card_part1_row, card_part1_col, card_part2_row, card_part2_col, True)
                print('card placed at ' + (chr(int(card_part1_col + 1) + 96)).upper() + ' ' + str(
                    int(card_part1_row) + 1) + ' : ' + (chr(int(card_part2_col + 1) + 96)).upper() + ' ' + str(
                    int(card_part2_row) + 1))

                self.is_winner_decided()
                if len(self.board.card_list) == 24:
                    Game.stage = GameStage.REC

        else:
            status = False
            Game.stage = GameStage.REC
            error_code = GameError.ORMAN
        return status, error_code

    def play_recycle_move(self, prev_part1_row, prev_part1_col, prev_part2_row,
                          prev_part2_col, card_angle, new_part1_row, new_part1_col):
        """
        Returns: status and error code
        ===========
        Description
        ===========
        After validating the recycle move, removes the card from the old position via board.remove_card() adn then
        plays it by calling board.place_card(),
        If validation fails, returns False and the error code.
        """

        new_part2_row, new_part2_col = self._card_part2_position(card_angle, new_part1_row, new_part1_col)

        status, error_code = self.board.is_recycle_move_valid(new_part1_row, new_part1_col, new_part2_row,
                                                              new_part2_col,
                                                              prev_part1_row, prev_part1_col,
                                                              prev_part2_row, prev_part2_col)
        if status:
            card = self.board.remove_card(prev_part1_row, prev_part1_col, prev_part2_row, prev_part2_col, False)
            card.rotate_card(card_angle)
            self.board.place_card(card, new_part1_row, new_part1_col, new_part2_row, new_part2_col, True)
            print('card placed at ' + (chr(int(new_part1_col + 1) + 96)).upper() + ' ' + str(
                int(new_part1_row) + 1) + ' : ' + (chr(int(new_part2_col + 1) + 96)).upper() + ' ' + str(
                int(new_part2_row) + 1))

            self.is_winner_decided()
            if len(self.board.move_list) == self.draw_move_count:
                Game.stage = GameStage.end
            return status, error_code
        else:
            return status, error_code

    def _set_winner(self, color_set, dot_set):
        """
        Returns: True and False
        ===========
        Description
        ===========
        Returns True if color or Dot set is preset, otherwise False
        """
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
        Game.stage = GameStage.end
        return True

    def is_winner_decided(self):
        """
        Returns: True and False
        ===========
        Description
        ===========
        Returns True if a winner is decided, otherwise False
        """
        status = False
        move_count = len(self.board.move_list)

        if move_count == self.draw_move_count:
            Game.stage = GameStage.end
            return status

        color_set, dot_set = self.board.check_winner()
        status = self._set_winner(color_set, dot_set)

        return status

    def print_result(self):
        """
        Returns:
        ===========
        Description
        ===========
        Prints the game result
        """
        if self.winner == 'N':
            print('Draw')
        else:
            print('Winner is ' + self.winner.player_name + '(' + str(self.winner.preference_type.value) + ')')

    def display_board(self):
        """
        Returns:
        ===========
        Description
        ===========
        Displays the current state of the board
        """
        self.board.print_board()

    def play_manual_move(self, move):
        """
        Returns: status, error code
        ===========
        Description
        ===========
        returns True if manual move is done successfully, otherwise False, error code
        """
        input_move = move.split(" ")
        input_first = input_move[0]
        try:
            print('\nmove ' + str(len(self.board.move_list) + 1) + ': ' + move)
            if input_first == '0':
                card_rotation = input_move[1]
                new_row = input_move[3]
                new_col = input_move[2]
                card_part1_row, card_part1_col = position_translation(new_row, new_col)

                status, error_code = self.play_regular_move(card_rotation, card_part1_row, card_part1_col)
            elif input_first.isalpha():
                prev_part1_row = input_move[1]
                prev_part1_col = input_first
                prev_part2_row = input_move[3]
                prev_part2_col = input_move[2]
                card_rotation = input_move[4]
                new_row = input_move[6]
                new_col = input_move[5]
                print(
                    'moving card from ' + prev_part1_col + ' ' + prev_part1_row + ' : ' + prev_part2_col + ' ' + prev_part2_row)

                prev_part1_row, prev_part1_col = position_translation(prev_part1_row, prev_part1_col)
                new_part1_row, new_part1_col = position_translation(new_row, new_col)
                prev_part2_row, prev_part2_col = position_translation(prev_part2_row, prev_part2_col)

                status, error_code = self.play_recycle_move(prev_part1_row, prev_part1_col, prev_part2_row,
                                                            prev_part2_col, card_rotation, new_part1_row,
                                                            new_part1_col)
            else:
                raise ValueError(GameError.FCE.value)
        except ValueError as ve:
            print(repr(ve))
            status = False
            error_code = GameError.IVE
        except IndexError:
            status = False
            error_code = GameError.IVE

        return status, error_code

    def play_automatic_move(self):
        """
        Returns: status, error code
        ===========
        Description
        ===========
        returns True if automatic move is done successfully.
        """

        # find an optimal move
        start_time = datetime.datetime.now()
        move = self.players[self.current_turn].find_AI_optimal_move(self.board)
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time

        print('Time taken(s) to generate move:' + str(time_taken.total_seconds()))

        move_type = move[0]
        card = move[1]
        part1_row = move[2]
        part1_col = move[3]
        part2_row = move[4]
        part2_col = move[5]
        if move_type == 0:
            print('Playing automatic regular move')
            self.board.place_card(card, part1_row, part1_col, part2_row, part2_col, True)
            if len(self.board.card_list) == 24:
                Game.stage = GameStage.REC

        else:
            print('Playing automatic recycle move')
            prev_part1_row = move[6]
            prev_part1_col = move[7]
            prev_part2_row = move[8]
            prev_part2_col = move[9]
            print('Removing card from ' + (chr(int(prev_part1_col + 1) + 96)).upper() + ' ' + str(
                int(prev_part1_row) + 1) + ' : ' + (chr(int(prev_part2_col + 1) + 96)).upper() + ' ' + str(
                int(prev_part2_row) + 1))

            self.board.remove_card(prev_part1_row, prev_part1_col, prev_part2_row, prev_part2_col, False)
            self.board.place_card(card, part1_row, part1_col, part2_row, part2_col, True)

            print('card placed at ' + (chr(int(part1_col + 1) + 96)).upper() + ' ' + str(
                int(part1_row) + 1) + ' : ' + (chr(int(part2_col + 1) + 96)).upper() + ' ' + str(
                int(part2_row) + 1))

        self.is_winner_decided()
        if len(self.board.move_list) == self.draw_move_count:
            Game.stage = GameStage.end
        return True, None
