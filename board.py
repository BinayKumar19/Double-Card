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
     
    def regular_move(self, card, card_angle, row_old, column_old):  
            
      row, column = self._position_translation(row_old, column_old)          
      part2_row, part2_col = self._card_part2_position(card_angle, row, column)  
           
      if (self.is_new_move_valid(card_angle,row, column, part2_row, part2_col)):  
        card.rotate_card(card_angle)              
        print('card placed at '+ column_old +' ' +row_old +' : '+ (chr(int(part2_col+1) + 96)).upper() +' '+str(int(part2_row)+1))  

        self.matrix[row , column] = card.part1['square']+':'+card.part1['circle']
        self.matrix[part2_row , part2_col] = card.part2['square']+':'+card.part2['circle'] 
        self.card_list[str(row)+str(column)] = card
        moves_count = len(self.move_list)
        self.move_list[moves_count+1] = str(row)+':'+str(column)+':'+str(part2_row)+':'+str(part2_col)
        return True
      else:
        return False
  
    def _position_translation(self, row, column):
      column = ord(column.lower()) - 96      
      row = int(row) - 1
      column = int(column) -1     
      return row, column
        
        
    def recycle_move(self, part1_row, part1_col, part2_row, part2_col, card_angle, row_old, column_old):  
      
      if (len(self.card_list)!=24):
          print('Cards still left, Can''t play recycling move now')
          return False
    
      print('moving card from '+ part1_col +' ' +part1_row +' : '+ part2_col +' '+part2_row)        
        
      row, column = self._position_translation(row_old, column_old)
      new_part2_row, new_part2_col = self._card_part2_position(card_angle, row, column)  
      
      if (self.is_new_move_valid(card_angle, row, column, new_part2_row, new_part2_col)):  
       part1_row, part1_col = self._position_translation(part1_row, part1_col)
       last_move = str(self.move_list[len(self.move_list)]).split(':')          
       
       if(part1_row == int(last_move[0]) and part1_col == int(last_move[1])):
          print('Can''t move the last card played by the other player')    
          return False
     
       part2_row, part2_col = self._position_translation(part2_row, part2_col)
       
       status = self._recycle_move_validation(row, column, new_part2_row, new_part2_col,part1_row, part1_col, part2_row, part2_col)
       if (not status): 
          return status

       print('card placed at '+ column_old +' ' +row_old +' : '+ (chr(int(new_part2_col+1) + 96)).upper() +' '+str(int(new_part2_row)+1))  
 
       card =  self._fetch_card(part1_row, part1_col, part2_row, part2_col)
       card.rotate_card(card_angle)          
      
       self.matrix[row , column] = card.part1['square']+':'+card.part1['circle']
       self.matrix[new_part2_row , new_part2_col] = card.part2['square']+':'+card.part2['circle'] 
       self.card_list[str(row) + str(column)] = card
       moves_count = len(self.move_list)
       self.move_list[moves_count+1] = str(row)+':'+str(column)+':'+str(new_part2_row)+':'+str(new_part2_col)
       return True
      else:
       return False
      
    def _recycle_move_validation(self,row, column, new_part2_row, new_part2_col, part1_row, part1_col, part2_row, part2_col):
      if (self.boundary_check(part1_row+1,part1_col) and
           (self.matrix[part1_row+1][part1_col]!=0 and 
           part1_row != row and
           part1_col != column)):
           return False
      elif( self.boundary_check(part2_row+1,part2_col) and
             self.matrix[part2_row+1][part2_col]!=0 and
             part2_row != new_part2_row and
             part2_col != new_part2_col):
            return False
      elif(self.matrix[part1_row][part1_col]==0 or
            self.matrix[part2_row][part2_col]==0 ):
           return False
      return True 
        
    def _fetch_card(self, part1_row, part1_col, part2_row, part2_col):
        card = self.card_list.pop(str(part1_row) + str(part1_col))
        self.matrix[part1_row , part1_col] = 0
        self.matrix[part2_row , part2_col] = 0      
        return card
        
      
    def boundary_check(self,row, column):
        if(row < 0 or row > 11 or 
           column <0 or column > 7): 
            return False
        return True
        
    
    def is_new_move_valid(self, card_angle, row, column, part2_row, part2_col):
        
        #Boundary Validation
        status = self.boundary_check(row,column) 
        status = status and self.boundary_check(part2_row,part2_col)
        if(not status):
            return status

        #to check if there is card under the given position        
         
        if (card_angle in ('1','3','5','7') and row >0):
            if (self.matrix[row-1, column] == 0 or
                self.matrix[part2_row - 1, part2_col] == 0 ):
                return False
        elif(card_angle in ('2','4','6','8') and row >0):
            if (self.matrix[row-1, column] == 0):
                return False
           
        #To check if the position is empty    
        if (self.matrix[row, column] != 0 or
            self.matrix[part2_row, part2_col] != 0 ):
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
                      
    