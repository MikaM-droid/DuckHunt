
'''
Author: Mikaela Monsma
Date: 15/03/2025
Description: My own game made with duckhunt as an inspiration.
'''

from game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

    