# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:01:33 2019

@author: binay
"""
from player import PlayerType as pt
from player import Player,PreferenceType 
from game import Game, GameStage

def play_game(new_game):
    while True :
        input_line = input()
        lines = input_line.split('\n')
        for move_index in range(0,len(lines)):
         input_move = lines[move_index].split(" ")
         input_first = input_move[0]
            
         print('\nmove '+str(len(new_game.board.move_list)+1)+': '+lines[move_index])         
         if (input_first=='0'):
             card_angle = input_move[1]
             row = input_move[3]
             column = input_move[2]
             new_game.play_regular_move(card_angle, row , column)
         else:
             prev_part1_row = input_move[1]
             prev_part1_col = input_first
             prev_part2_row = input_move[3]
             prev_part2_col = input_move[2]
             card_angle = input_move[4]
             row = input_move[6]
             column = input_move[5]
             new_game.play_recycle_move(prev_part1_row,prev_part1_col,prev_part2_row,
                                        prev_part2_col,card_angle, row , column)     
        
         status = new_game.get_stage()
         new_game.disply_board()
         if (status == GameStage.end):
             break
         elif (status == GameStage.REC):
            print('Only Recycle moves allowed now')
           
         new_game.change_turn()
         
        if (status == GameStage.end):
             break
            
    new_game.print_result()
    
def initialize_game():
  print('Lets Play the Game')
  game_mode = input('Enter 1 - Manual Mode 2 - Automatic Mode')

  player1_type = pt.H
  player1_choice = input('Enter Player1''s Preference choice:\n1 - dots or 2 - colors?\n')

  if(player1_choice == '1'):
     player1_choice = PreferenceType.D
     player2_choice = PreferenceType.C
  elif (player1_choice == '2'):
     player1_choice = PreferenceType.C
     player2_choice = PreferenceType.D
  else:   
     return 'N'   
   
  if(game_mode=='1'):
    player2_type = pt.H
  else:
    player2_type = pt.AI

  player1 = Player('Player 1', player1_type, player1_choice)
  player2 = Player('Player 2', player2_type, player2_choice)

  new_game = Game(game_mode)
  new_game.add_player(player1)
  new_game.add_player(player2)
  return new_game

new_game = initialize_game()
if (new_game != 'N'):
  play_game(new_game)
else:
  print('Invalid Input')  