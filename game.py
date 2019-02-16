# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:48:07 2019

@author: binay
"""

from board import Board
from player import PreferenceType
from enum import Enum

class GameStage(Enum):
       REG = 'Regular'
       REC = 'Recycle'
       end = 'End'

class Game:
    
    
    def __init__(self, game_type):
        self.game_type = game_type
        self.board = Board()
        self.current_turn = 0   #not defined 
        self.players = [] 
        self.winner = 'N'
        self.stage = GameStage.REG    
        
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
            if (len(self.board.card_list)==24):
               self.stage = GameStage.REC
            return result
        else:
            print('Illegal Move')
     
    def play_recycle_move(self, card_angle, row , column):
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
              card = str(self.board.matrix[i,j])
              if(card != '0'):
                 if (card[0] == previous_color_type):
                     color_count = color_count + 1
                 else:
                     previous_color_type = card[0] 
                     color_count = 0
                 
                 if (card[1] == previous_dot_type):
                     dot_count = dot_count + 1
                 else:
                     previous_dot_type = card[1]
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
           elif(other_preference_type_count == 4):
              self.winner = self.players[3 - self.current_turn].player_name 
           else:
              return False
           self.stage = GameStage.end       
           return True
    
    def is_winner_decided(self):
       status = False 
       move_count = len(self.board.move_list)
       
       if (move_count == 60):
           self.stage = GameStage.end       
           return status             
       
       dot_count,color_count = self._winner_check_horizontal()
       if (color_count == 4):
           status = self._set_winner(PreferenceType.C, dot_count)
       elif (dot_count == 4):
           status = self._set_winner(PreferenceType.D, color_count)
                  
       dot_count,color_count = self._winner_check_vertical()
       if (color_count == 4):
           status = self._set_winner(PreferenceType.C, dot_count)
       elif (dot_count == 4):
           status = self._set_winner(PreferenceType.D, color_count)
      
       dot_count,color_count = self._winner_check_diagonal()
            
       return status  
   
    def get_stage(self):
        return self.stage
            
    def print_result(self):
        if (self.winner =='N'):
            print('Draw')
        else:
            print('Winner is '+self.winner)     
        

    def _winner_check_vertical(self):
        for i in range(0,8):
          dot_count = 0
          previous_dot_type = 'N'
          previous_color_type = 'N'        
          color_count = 0
            
          for j in range(0,12):           
              card = str(self.board.matrix[j,i])
              if(card != '0'):
                 if (card[0] == previous_color_type):
                     color_count = color_count + 1
                 else:
                     previous_color_type = card[0]
                     color_count = 0
                 
                 if (card[1] == previous_dot_type):
                     dot_count = dot_count + 1
                 else:
                     previous_dot_type = card[1]
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
        
        last_pos = len(self.board.move_list)
        position = self.board.move_list[last_pos].split(':')
        print('is_winner_decided dict size:'+str(last_pos))
        if(last_pos>0):
           print('is_winner_decided last_pos:'+self.board.move_list[last_pos])

        
        row =  int(position[0]) 
        col =  int(position[1])
        
        new_card_square_color = self.board.matrix[row,col][0]
        new_card_dot_color = self.board.matrix[row,col][1]
        
        color_count_ru = 1
        dot_count_ru = 1
        color_count_rd = 1
        dot_count_rd = 1
        color_count_lu = 1
        dot_count_lu = 1
        color_count_ld = 1
        dot_count_ld = 1
        
        for k in range(1,4):
              card_ru = str(self.board.matrix[row + k, col + k])
              card_rd = str(self.board.matrix[row - k, col + k])
              card_lu = str(self.board.matrix[row + k, col - k])
              card_ld = str(self.board.matrix[row - k, col - k])
              
              if(card_ru != '0'):
                 if (card_ru[0] == new_card_square_color):
                     color_count_ru = color_count_ru + 1   
                 if (card_ru[1] == new_card_dot_color):
                     dot_count_ru = dot_count_ru + 1
              
              if(card_rd != '0'):
                 if (card_rd[0] == new_card_square_color):
                     color_count_rd = color_count_rd + 1   
                 if (card_rd[1] == new_card_dot_color):
                     dot_count_rd = dot_count_rd + 1
                
              if(card_lu != '0'):
                 if (card_lu[0] == new_card_square_color):
                     color_count_lu = color_count_lu + 1   
                 if (card_lu[1] == new_card_dot_color):
                     dot_count_lu = dot_count_lu + 1
                
              if(card_ld != '0'):
                 if (card_ld[0] == new_card_square_color):
                     color_count_ld = color_count_ld + 1   
                 if (card_ld[1] == new_card_dot_color):
                     dot_count_ld = dot_count_ld + 1
            
            
        dot_count = 0
        color_count = 0   
        if ( color_count_ru == 4 or
           color_count_rd == 4 or
           color_count_lu == 4 or
           color_count_ld == 4 ):
           color_count = 4
        
        if( dot_count_ru == 4 or
              dot_count_rd == 4 or
              dot_count_lu == 4 or
              dot_count_ld == 4 ):
                  dot_count = 4
        
        return dot_count,color_count

    
    def disply_board(self):
        self.board.print_board()