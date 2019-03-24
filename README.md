# Double-Card
Introduction to Artificial Intelligence: Project

Double Card is a 2-player strategy game played with 24 identical cards and an 8×12 board. The board is numbered 1 to 12 from bottom to top, and A to H from left to right.

Each player will have 12 identical cards, initially. Each card has 2 sides, each side has 2 parts and each part has 2 parts i.e. Color and Dot. Colour can be white or Red and Dot can be filled or empty. Each card can be placed on the board on either side and can be rotated by 0, 90, 180 or 270 degrees, for a total of 8 possible placements. Cards can be rotated and placed on either side, but can only be placed at row 1 of the board or on top of a card already on the board. 

Each player will select a particular pattern of the cards(Color or Dot) at the start of the game and will try to make the pattern by placing cards on the board. The player who plays dots will try to get 4 consecutive Filled dot’s or 4 consecutive empty dots (in a row, a column or a diagonal) regardless of the colours of the cards. The player who plays colours will try to get 4 consecutive red1 segments or 4 consecutive white segments (in a row, a column or a diagonal) regardless of the dots on the cards. 

Each player takes turns placing his/her cards on the board. 
A player can play 2 types of moves:
1) Normal Move
The input 0 5 A 2 will indicate that we have a regular move and the card with rotation 5 will be placed at positions A2 and B2 on the board. 

2) Recycle Move
If all 24 cards have been played and neither player has won the game, then players proceed to use recycling moves rather than the regular moves. A recycling move consists of taking one card oﬀ the board and placing it somewhere else on the board. A player cannot move the card that the other player just moved/placed and must ensure that the resulting board will be legal. Players keep recycling one card at a time until either one player wins the game or a total of 60 moves have been played. If after 60 moves (regular + recycling), no player has won, then the game ends in a draw.
The input F 2 F 3 3 A 2 will indicate that we have a recycling move and the card at position F2 F3 will be rotated by factor 3(180 degrees), will be placed at positions A2 and B2 on the board. 

Play Modes
The game can be run in two modes:
1. Manual Mode: Manual entry for both players (i.e. 2 humans playing against each other)
2. Automatic Mode: Manual entry for one player, and automatic moves for the other (i.e. one human playing against your AI)

Winning
As soon as a player gets four consecutive identical dots or identical colours vertically, horizontally, or diagonally they win the game. If both players are in a winning position because the card that was just played puts both players in a winning position, then only the player who played the last card wins the game. 


How to Run
1) Run playGame.py
2) Select Mode(Manual or Automatic)
3) For Manual Mode, Skip 4 and 5 
4) Chose which player shall act as AI (Player 1 or Player 2)
5) Choose if Alpha-Beta should be activated(Minimax will be activated always)
6) Enter Player 1's preference - dots or Colors (Player 2 will have the other preference)
