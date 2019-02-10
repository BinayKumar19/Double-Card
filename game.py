# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:48:07 2019

@author: binay
"""

from board import Board
from player import PreferenceType

class Game:
    
    current_turn = 0   #not defined 
    players = [] 
    winner = 'None'
    
    def __init__(self, game_type):
        self.game_type = game_type
        self.board = Board()
        
    def add_player(self, player):
        self.players.append(player)
        print('Player added')
    
    def change_turn(self):
        if (self.current_turn == 0):
            self.current_turn = 1
        else:
            self.current_turn = 0
    
    def play_regular_move(self, card_angle, row , column):
        
        card = self.players[self.current_turn].get_card()
        result = self.board.regular_move(card, card_angle, row, column) 
        
        if (result):
            return result
        else:
            print('Illegal Move')
     
    def play_recycle_move(self, card_angle, row , column):
         print('Game-'+'recycle move')
         result = self.board.recycle_move(card_angle, row, column) 
         return result
          
    def print_board(self):
      print(self.matrix)         
   
    def _winner_check_horizontal(self):
        for i in range(0,12):
          dot_count = 0
          previous_dot_type = 'N'
          previous_color_type = 'N'        
          color_count = 0     
          for j in range(0,8):           
              card_side = self.board.matrix[i,j]
              if(card_side != 0):
                 if (card_side.square_color == previous_color_type):
                     color_count = color_count + 1
                 else:
                     previous_color_type = card_side.square_color
                     color_count = 0
                 
                 if (card_side.circle_color == previous_dot_type):
                     dot_count = dot_count + 1
                 else:
                     previous_dot_type = card_side.circle_color
                     dot_count = 0
                 
                 if (color_count == 4 or dot_count == 4):
                     return dot_count,color_count
        
              else:
                 dot_count = 0
                 previous_dot_type = 'N'
                 previous_color_type = 'N'        
                 color_count = 0
        return dot_count,color_count
    
    def _set_winner(self, preference_type , other_preference_type_count):
           if (self.players[self.current_turn].player_type == preference_type):
              self.winner = self.players[self.current_turn].player_name 
           elif(other_preference_type_count ==4):
              self.winner = self.players[3 - self.current_turn].player_name 
           else:
              return False
           return True
    
    def is_winner_decided(self):
       status = False 
       
       dot_count,color_count = self._winner_check_horizontal()
       if (color_count == 4):
           status = self._set_winner(PreferenceType.C,dot_count)
       elif (dot_count == 4):
           status = self._set_winner(PreferenceType.D, color_count)
                  
       dot_count,color_count = self._winner_check_vertical()
       if (color_count == 4):
           status = self._set_winner(PreferenceType.C,dot_count)
       elif (dot_count == 4):
           status = self._set_winner(PreferenceType.D, color_count)
       
       if (status):
         print('Winner is '+self.winner)     
         
       return status  

    def _winner_check_vertical(self):
        for i in range(0,8):
          dot_count = 0
          previous_dot_type = 'N'
          previous_color_type = 'N'        
          color_count = 0
            
          for j in range(0,12):           
              card_side = self.board.matrix[j,i]
              if(card_side != 0):
                 if (card_side.square_color == previous_color_type):
                     color_count = color_count + 1
                 else:
                     previous_color_type = card_side.square_color
                     color_count = 0
                 
                 if (card_side.circle_color == previous_dot_type):
                     dot_count = dot_count + 1
                 else:
                     previous_dot_type = card_side.circle_color
                     dot_count = 0
                 
                 if (color_count == 4 or dot_count == 4):
                     return dot_count,color_count
        
              else:
                 dot_count = 0
                 previous_dot_type = 'N'
                 previous_color_type = 'N'        
                 color_count = 0
        return dot_count,color_count

    def _winner_check_diagonal(self):
        for i in range(0,8):
          dot_count = 0
          previous_dot_type = 'N'
          previous_color_type = 'N'        
          color_count = 0
            
          for j in range(0,12):           
              card_side = self.board.matrix[j,i]
        return dot_count,color_count

    
    def disply_board(self):
        self.board.print_board()