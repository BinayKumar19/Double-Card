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
    
class cardFrontPart1:
    square_color = 'R'
    circle_color = 'B'

class cardFrontPart2:
    square_color = 'W'
    circle_color = 'W'
    
class cardBackPart1:
    square_color = 'R'
    circle_color = 'W'

class cardBackPart2:
    square_color = 'W'
    circle_color = 'B'

class Player:
    cards = []

    def __init__(self, player_name, player_type, preference_type):
      self.player_name = player_name  
      self.player_type = player_type
      self.preference_type = preference_type
      for i in range(1,12):
          card = (i,cardFrontPart1(),cardFrontPart2(),cardBackPart1,cardBackPart2 )
          self.cards.append(card)
    
    def get_card(self):
      if (len(self.cards) > 0):
          card = self.cards.pop()
          return card