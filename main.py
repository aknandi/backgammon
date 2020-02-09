# Play backgammon

from game import Game

game = Game()
game.run_game(verbose=False)
winner = game.who_won()
print(winner)