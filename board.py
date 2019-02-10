# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

#AI Game
import numpy as np

class Board:
    
    def __init__(self):
      self.matrix = np.zeros(shape=(12,8), dtype=object)  
      
    def regular_move(self, card, card_angle, row, column):  
      column = ord(column.lower()) - 96
      
      row = int(row) - 1
      column = int(column) -1
      part2_col = column
      part2_row= row
      
      print('row:'+str(row))
      print('column:'+str(column))
      print('part2_col:'+str(part2_col))
      print('part2_row:'+str(part2_row))
      
      if(card_angle in ('1','4','5','8')):
        card_part1 = card[1]
        card_part2 = card[2] 
      elif(card_angle in ('2','3','6','7')):
        card_part1 = card[2]
        card_part2 = card[1]        
        
      if(card_angle in ('1','3','5','7')):
        part2_col = part2_col + 1
      elif(card_angle in ('2','4','6','8')):
        part2_row = part2_row + 1
           
      if (self.is_move_valid(card_angle,row, column, part2_row, part2_col)):  
        self.matrix[row , column] = card_part1
        self.matrix[part2_row , part2_col] = card_part2      
        return True
      else:
        return False
  
    def is_move_valid(self, card_angle, row, column, part2_row, part2_col):
        if(row < 0 or row > 11 or 
           part2_row<0 or part2_row > 11 or
           column <0 or column > 7 or 
           part2_col <0 or part2_col > 7):
            return False
        
        if (card_angle in ('1','3','5','7') and row >0):
            if (self.matrix[row-1, column] == 0 or
                self.matrix[part2_row - 1, part2_col] == 0 ):
                return False
        elif(card_angle in ('2','4','6','8') and row >0):
            if (self.matrix[row-1, column] == 0):
                return False
           
        return True
    
    def recycle_move(self, card_angle, row, column):  
       column = ord(column) - 9
    
    def print_board(self):
       for i in range(11,-1,-1):
          for j in range(0,8):           
              card_side = self.matrix[i,j]
              if (card_side == 0):
                print('0' +'   ', end="")    
              else:
                print(card_side.square_color+':'+card_side.circle_color+' ' , end="")
          print()
                      
    