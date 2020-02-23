from random import randint

from colour import Colour
from game import Game
from strategies import MoveFurthestBackStrategy, HumanStrategy


if __name__ == '__main__':
    name = input('What is your name? ')

    game = Game(
        white_strategy=HumanStrategy(name),
        black_strategy=MoveFurthestBackStrategy(),
        first_player=Colour(randint(0, 1))
    )

    game.run_game(verbose=False)

    print("%s won!" % game.who_won())
    game.board.print_board()
