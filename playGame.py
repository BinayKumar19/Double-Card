# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:01:33 2019

@author: binay
"""
from player import PlayerType as pt
from player import Player, PreferenceType
from game import Game, GameStage
from utilities import FileWriter, position_translation


def play_game(new_game):
    print('Initial Stage of the board')
    new_game.display_board()
    while True:
        print(new_game.players[new_game.current_turn].player_type)
        status = True
        if new_game.players[new_game.current_turn].player_type == pt.AI:
            new_game.play_automatic_move()
        else:
            print('Input the move:')
            input_line = input()
            status, error_code = new_game.play_manual_move(input_line)

        if status:
            new_game.display_board()
            if new_game.get_stage() == GameStage.end:
                new_game.print_result()
                return
            elif new_game.get_stage() == GameStage.REC:
                print('Only Recycle moves allowed now')
            new_game.change_turn()
        else:
            print(error_code.value)


def initialize_game():
    print('Lets Play the Game')
    game_mode = input('Enter 1 - Manual Mode 2 - Automatic Mode')
    player1_choice = input('Enter Player1''s Preference choice:\n1 - dots or 2 - colors?\n')
    if player1_choice == '1':
        player1_choice = PreferenceType.D
        player2_choice = PreferenceType.C
    elif player1_choice == '2':
        player1_choice = PreferenceType.C
        player2_choice = PreferenceType.D
    else:
        return 'N'

    if game_mode == '1':
        player1_type = pt.H
        player2_type = pt.H
        alpha_beta_activated = False
    else:
        ai_choice = input('Which player shall AI play: 1 - 1st player \n 2 - 2nd player')
        if ai_choice == '1':
            player1_type = pt.AI
            player2_type = pt.H
        else:
            player2_type = pt.AI
            player1_type = pt.H

        alpha_beta_activated = input('alpha-beta should be activated or not?\n 1- Yes \n 2- No')
        if alpha_beta_activated == '1':
            alpha_beta_activated = True
        else:
            alpha_beta_activated = False

        generate_trace_file = input('generate a trace of the minimax/alpha-beta?\n 1- Yes \n 2- No')

        if generate_trace_file == '1':
            FileWriter.print_trace_file = True
            FileWriter.open_file_writer()

    player1 = Player('Player 1', player1_type, player1_choice, alpha_beta_activated)
    player2 = Player('Player 2', player2_type, player2_choice, alpha_beta_activated)

    game = Game(game_mode)
    game.add_player(player1)
    game.add_player(player2)
    return game


new_game = initialize_game()
if new_game != 'N':
    play_game(new_game)
else:
    print('Invalid Input')
