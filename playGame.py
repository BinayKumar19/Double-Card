# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:01:33 2019

@author: binay
"""
from player import PlayerType as pt
from player import Player, PreferenceType
from game import Game, GameStage
from utilities import FileWriter

def play_game(new_game):
    print('Initial Stage of the board')
    new_game.display_board()
    while True:
        print(new_game.players[new_game.current_turn].player_type)
        if new_game.players[new_game.current_turn].player_type == pt.AI:
            new_game.play_automatic_move()
            new_game.display_board()
            if new_game.get_stage() == GameStage.end:
                break
            elif new_game.get_stage() == GameStage.REC:
                print('Only Recycle moves allowed now')
            new_game.change_turn()
        else:
            print('Input the move:')
            input_line = input()
            lines = input_line.split('\n')
            for move_index in range(0, len(lines)):
                input_move = lines[move_index].split(" ")
                input_first = input_move[0]

                print('\nmove ' + str(len(new_game.board.move_list) + 1) + ': ' + lines[move_index])
                if input_first == '0':
                    card_angle = input_move[1]
                    row = input_move[3]
                    column = input_move[2]
                    status, error_code = new_game.play_regular_move(card_angle, row, column)
                else:
                    prev_part1_row = input_move[1]
                    prev_part1_col = input_first
                    prev_part2_row = input_move[3]
                    prev_part2_col = input_move[2]
                    card_angle = input_move[4]
                    row = input_move[6]
                    column = input_move[5]
                    status, error_code = new_game.play_recycle_move(prev_part1_row, prev_part1_col, prev_part2_row,
                                                                    prev_part2_col, card_angle, row, column)

                if status:
                    new_game.display_board()
                    if new_game.get_stage() == GameStage.end:
                        break
                    elif new_game.get_stage() == GameStage.REC:
                        print('Only Recycle moves allowed now')

                    new_game.change_turn()
                else:
                    print(error_code.value)

        if new_game.get_stage() == GameStage.end:
            break

    new_game.print_result()
    FileWriter.close_file_writer()

def initialize_game():
    print('Lets Play the Game')
    game_mode = input('Enter 1 - Manual Mode 2 - Automatic Mode')
    player1_choice = input('Enter Player1''s Preference choice:\n1 - dots or 2 - colors?\n')
    if (player1_choice == '1'):
        player1_choice = PreferenceType.D
        player2_choice = PreferenceType.C
    elif (player1_choice == '2'):
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
