# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:01:33 2019

@author: binay
"""
from player import player_type as pt
from player import player 
from board import board
from game import game

 
def play_game():
    b = board()
    game = game()
    while not game.is_winner_decided():
        game.play_move()
        game.change_turn()
    
def initialize_game():
  print('Lets Play the Game')
  game_mode = input(Enter 1 - Manual Mode 2 - Automatic Mode)

  player1_type = pt.H
  player1_choice = int(input('Enter Player1''s Preference choice:\n1 - dots or 2 - colors?\n'))

  if(game_mode==1):
    player2_type = pt.H
  else:
    player2_type = pt.AI

  player2_choice = 3-player1_choice

  player1 = player(player1_type, player1_choice)
  player1 = player(player2_type, player2_choice)


initialize_game()
play_game()