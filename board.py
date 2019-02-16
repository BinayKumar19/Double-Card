# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

#AI Game
import numpy as np

class Board:
    
    
    def __init__(self):
      self.matrix = np.zeros(shape=(12,8),dtype='object') 
      self.card_list = {}
      self.move_list = {}
    
           
    def _card_part2_position(self, card_angle, row, column):
      if(card_angle in ('1','3','5','7')):
        part2_col = column + 1
        part2_row = row   
      elif(card_angle in ('2','4','6','8')):
        part2_row = row + 1
        part2_col = column
      
      return part2_row, part2_col
     
    def regular_move(self, card, card_angle, row, column):  
            
      row, column = self._position_translation(row, column)          
      part2_row, part2_col = self._card_part2_position(card_angle, row, column)  
     
      print('row:'+str(row))
      print('column:'+str(column))
      print('part2_col:'+str(part2_col))
      print('part2_row:'+str(part2_row))
           
      if (self.is_new_move_valid(card_angle,row, column, part2_row, part2_col)):  
        card.rotate_card(card_angle)  
        print('part1:'+str(card.part1))
        print('part2:'+str(card.part2))
    
        self.matrix[row , column] = card.part1['square']+':'+card.part1['circle']
        self.matrix[part2_row , part2_col] = card.part2['square']+':'+card.part2['circle'] 
        self.card_list[str(row)+str(column)] = card
        moves_count = len(self.move_list)
        self.move_list[moves_count+1] = str(row)+':'+str(column)
        return True
      else:
        return False
  
    def _position_translation(self, row, column):
      column = ord(column.lower()) - 96      
      row = int(row) - 1
      column = int(column) -1
      
      return row, column
        
        
    def recycle_move(self, part1_row, part1_col, part2_row, part2_col,card_angle, row, column):  
      
      if (len(self.card_list)!=24):
          print('Cards still left, Can''t play recycling move now')
          return False
        
      row, column = self._position_translation(row, column)
        
      new_part2_row, new_part2_col = self._card_part2_position(card_angle, row, column)  
      
      if (self.is_new_move_valid(card_angle, row, column, new_part2_row, new_part2_col)):  
       
       part1_row, part1_col = self._position_translation(part1_row, part1_col)
       last_move = self.move_list[len(self.move_list)].split[':']          
       
       if(part1_row == last_move[0] and part1_col == last_move[1]):
          print('Can''t move the latest card played by the other player')    
          return False
     
       part2_row, part2_col = self._position_translation(part2_row, part2_col)
       card =  self._fetch_card(part1_row, part1_col, part2_row, part2_col)
       card.rotate_card(card_angle)          
      
       self.matrix[row , column] = card.part1['square']+':'+card.part1['circle']
       self.matrix[part2_row , part2_col] = card.part2['square']+':'+card.part2['circle'] 
       self.card_list[str(row) + str(column)] = card
       moves_count = len(self.move_list)
       self.move_list[moves_count+1] = str(row)+':'+str(column)          
       return True
      else:
       return False
      
     
    def _fetch_card(self, part1_row, part1_col, part2_row, part2_col):
        card = self.card_list.pop(str(part1_row) + str(part1_col))
        self.matrix[part1_row , part1_col] = 0
        self.matrix[part2_row , part2_col] = 0      
        return card
        
      
    def is_new_move_valid(self, card_angle, row, column, part2_row, part2_col):
        
        #Boundary Validation
        if(row < 0 or row > 11 or 
           part2_row<0 or part2_row > 11 or
           column <0 or column > 7 or 
           part2_col <0 or part2_col > 7):
            return False
        
        #to check if there is card under the given position        
         
        if (card_angle in ('1','3','5','7') and row >0):
            if (self.matrix[row-1, column] == 0 or
                self.matrix[part2_row - 1, part2_col] == 0 ):
                return False
        elif(card_angle in ('2','4','6','8') and row >0):
            if (str(self.matrix[row-1, column]) == '0'):
                return False
           
        #To check if the position is empty    
        if (str(self.matrix[row, column]) != '0' or
            str(self.matrix[part2_row, part2_col]) != '0' ):
                return False     
            
        return True
    
    
    def print_board(self):
       for i in range(11,-1,-1):
          for j in range(0,8):           
              card_side = self.matrix[i,j]
              if (card_side == 0):
                print('0' +'   ', end="")    
              else:
                print(str(self.matrix[i,j])+' ' , end="")
          print()
                      
    