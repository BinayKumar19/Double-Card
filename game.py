# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:48:07 2019

@author: binay
"""

class game:
    
    turn = 0   #not defined 
    
    def __init__(self, game_type):
        self.game_type = game_type
    
    def change_turn(self):
        if (self.turn == 1):
            self.turn = 2
        else:
            self.turn = 1
    
    def play_move(self):
        
    
    def insert_card(self, row, column, card):
      self.matrix[row][column] = card
    
    def print_board(self):
      print(self.matrix)         
   
    def is_winner_decided(self):
           return False  