# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

#AI Game
import numpy as np
from enum import Enum

class card_placement(Enum):
       ZERO = 0
       Ninety = 90
       ONE_EIGHTY = 180
       TWO_SEVENTY = 270

class card:
    side1 = ["RB","WW"]
    side2 = ["RW","WB"]
    placement = card_placement.ZERO

class board:
    row = np.array(['0','0','0','0','0','0','0','0']) 
    matrix = np.array([row,row,row,row,row,row,row,row,row,row,row,row])  
     
    def insert_card(self, row, column, card):
      self.matrix[row][column] = card
    
    def print_board(self):
      print(self.matrix)         
    