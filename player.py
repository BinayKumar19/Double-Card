# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:18:38 2019

@author: binay
"""
from enum import Enum

class PlayerType(Enum):
       H = 'HUMAN'
       AI = 'AI'

class PreferenceType(Enum):
       D = 'DOT'
       C = 'CIRCLE'
    
class Card:
    
    def __init__(self):
     self.side1 = True
     self.part1 = {'square':'N','circle':'N'}
     self.part2 = {'square':'N','circle':'N'}
     self.rotation = 0
        
    def _set_side(self, side1_square, side1_circle, side2_square, side2_circle):
        self.part1['square'] = side1_square
        self.part1['circle'] = side1_circle
        self.part2['square'] = side2_square
        self.part2['circle'] = side2_circle      
      
    def rotate_card(self, rotation_value):
       if(rotation_value in ('1','4')):
        self._set_side('R','B','W','W')
       elif(rotation_value in('2','3')):
        self._set_side('W','W','R','B')
       elif(rotation_value in ('5','8')):
        self._set_side('R','W','W','B')
       elif(rotation_value in('6','7')):
        self._set_side('W','B','R','W')

       self.rotation =  rotation_value
          
class Player:
   
    def __init__(self, player_name, player_type, preference_type):
      self.player_name = player_name  
      self.player_type = player_type
      self.preference_type = preference_type
      self.cards = []

      for i in range(1,12):
          card = Card()
          self.cards.append(card)
    
    def get_card(self):
      if (len(self.cards) > 0):
          card = self.cards.pop()
          return card