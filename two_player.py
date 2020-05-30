from random import randint

from src.colour import Colour
from src.game import Game
from src.strategies import HumanStrategy


if __name__ == '__main__':
    players = {
        Colour.WHITE: input('Name of player 1: '),
        Colour.BLACK: input('Name of player 2: '),
    }

    game = Game(
        white_strategy=HumanStrategy(players[Colour.WHITE]),
        black_strategy=HumanStrategy(players[Colour.BLACK]),
        first_player=Colour(randint(0, 1))
    )

    game.run_game(verbose=False)

    print("%s won!" % players[game.who_won()])
    game.board.print_board()
