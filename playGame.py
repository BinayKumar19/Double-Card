# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:01:33 2019

@author: binay
"""
from player import PlayerType as pt
from player import Player 
from game import Game, GameStage

def play_game(new_game):
    while True :
        input_line = input()
        lines = input_line.split('\n')
        for move_index in range(0,len(lines)):
         input_move = lines[move_index].split(" ")
         card_move = input_move[0]
         card_angle = input_move[1]
         row = input_move[3]
         column = input_move[2]
#         print('card_move:'+card_move)
#         print('card_angle:'+card_angle)
#         print('row:'+row)
#         print('column:'+column)
#         print('before calling move func')
         print('\nmove: '+lines[move_index])         
         if (card_move=='0'):
           new_game.play_regular_move(card_angle, row , column)
         else:
           new_game.play_recycle_move(card_angle, row , column)     
        
         status = new_game.get_stage()
         if (status == GameStage.end):
             break
         elif (status == GameStage.REC):
            print('No cards left, time to play the Regular moves')
         else:
            print('else')
           
         new_game.change_turn()
         new_game.disply_board()
         
        if (status == GameStage.end):
             break
            
    new_game.print_result()
    
def initialize_game():
  print('Lets Play the Game')
  game_mode = input('Enter 1 - Manual Mode 2 - Automatic Mode')

  player1_type = pt.H
  player1_choice = int(input('Enter Player1''s Preference choice:\n1 - dots or 2 - colors?\n'))

  if(game_mode==1):
    player2_type = pt.H
  else:
    player2_type = pt.AI

  player2_choice = 3 - player1_choice

  player1 = Player('Player 1', player1_type, player1_choice)
  player2 = Player('Player 2', player2_type, player2_choice)

  new_game = Game(game_mode)
  new_game.add_player(player1)
  new_game.add_player(player2)
  return new_game

new_game = initialize_game()
play_game(new_game)