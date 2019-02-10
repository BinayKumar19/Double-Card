# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:01:33 2019

@author: binay
"""
from player import PlayerType as pt
from player import Player 
from game import Game

def play_game(new_game):
    while not new_game.is_winner_decided():
        #card_side = input('Enter side of the card')
        #card_angle = input('Enter Degree of Rotation of the card')
        #card_position = input('Enter Dposition of the card')
        input_line = input()
        input_move = input_line.split(" ")
        card_move = input_move[0]
        card_angle = input_move[1]
        row = input_move[3]
        column = input_move[2]
        
        if (card_move=='0'):
          new_game.play_regular_move(card_angle, row , column)
        else:
          new_game.play_recycle_move(card_angle, row , column)     
        
        new_game.change_turn()
        new_game.disply_board()
    
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