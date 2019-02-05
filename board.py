# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:06:03 2019

@author: binay
"""

#AI Game
import numpy as np
from enum import Enum

class card_placement(Enum):
       side1_0degree = ["LRB","RWW"]
       side1_90degree = ["URB","DWW"]
       side1_180degree = ["LRB","RWW"]
       side1_270degree = ["DRB","UWW"]
       side2_0degree = ["LRW","RWB"]
       side2_90degree = ["URW","DWB"]
       side2_180degree = ["LRW","RWB"]
       side2_270degree = ["DRW","UWB"]       

class card:
    side1 = ["RB","WW"]
    side2 = ["RW","WB"]
    placement = card_placement.side1_0degree

class board:
    row = np.array(['0','0','0','0','0','0','0','0']) 
    matrix = np.array([row,row,row,row,row,row,row,row,row,row,row,row])  
     
    def insert_card(self,row,column):
        self.matrix[row][column] = 1
    
    def print_board(self):
      print(self.matrix)         

b = board()
b.print_board() 
b.insert_card(3,4)  
b.print_board()   