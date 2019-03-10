# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:01:33 2019

@author: binay
"""
from player import Player
from game import Game, GameStage
from utilities import FileWriter, GameError, PlayerType, PreferenceType


def play_game(new_game):
    print('Initial Stage of the board')
    new_game.display_board()
    while True:
        player = new_game.players[new_game.current_turn]
        print(player.player_name +'\'s turn (' + player.player_type.value+'), '+'cards available ' + str(len(player.cards)))
        status = True
        if new_game.players[new_game.current_turn].player_type == PlayerType.AI:
            new_game.play_automatic_move()
        else:
            print('Input the move:')
            input_line = input()
            status, error_code = new_game.play_manual_move(input_line)

        if status:
            new_game.display_board()
            if Game.stage == GameStage.end:
                new_game.print_result()
                return
            elif new_game.stage == GameStage.REC:
                print(GameError.ORMAN.value)
            new_game.change_turn()
        else:
            print(error_code.value)


def initialize_game():
    print('Lets Play the Game')
    game_mode = input('Enter Game Mode Preference:\n1 - Manual Mode \n2 - Automatic Mode\n')

    if game_mode == '1':
        player1_type = PlayerType.H
        player2_type = PlayerType.H
        alpha_beta_activated = False
    else:
        ai_choice = input('Which player shall AI play:\n1 - 1st player \n2 - 2nd player\n')
        if ai_choice == '1':
            player1_type = PlayerType.AI
            player2_type = PlayerType.H
        else:
            player2_type = PlayerType.AI
            player1_type = PlayerType.H

        alpha_beta_activated = input('Do you want to activate alpha-beta??\n1- Yes \n2- No\n')
        if alpha_beta_activated == '1':
            alpha_beta_activated = True
        else:
            alpha_beta_activated = False

        generate_trace_file = input('Do you want to generate a trace of the minimax/alpha-beta?\n1- Yes \n2- No\n')

        if generate_trace_file == '1':
            FileWriter.print_trace_file = True
            FileWriter.open_file_writer()

    player1_choice = input('Enter Player1\'s Preference choice:\n1 - dots \n2 - colors\n')
    if player1_choice == '1':
        player1_choice = PreferenceType.D
        player2_choice = PreferenceType.C
    elif player1_choice == '2':
        player1_choice = PreferenceType.C
        player2_choice = PreferenceType.D
    else:
        return 'N'

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
