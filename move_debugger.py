import json

from board import Board
from colour import Colour
from compare_all_moves_strategy import CompareAllMoves
from strategies import MoveFurthestBackStrategy, HumanStrategy, MoveFurthestBackOrderDiceStrategy


def get_strategy(strategy_name):
    strategies = [
        MoveFurthestBackStrategy,
        HumanStrategy,
        MoveFurthestBackOrderDiceStrategy,
        HumanStrategy,
        CompareAllMoves,
    ]

    for strategy in strategies:
        if strategy.__name__ == strategy_name:
            return strategy()

    raise Exception("Cannot find strategy %s" % strategy_name)


if __name__ == '__main__':
    s = input('Paste move info:\n')
    data = json.loads(s)

    strategy = get_strategy(data['strategy'])

    board = Board()
    for location, value in data['board'].items():
        board.add_many_pieces(value['count'], Colour.load(value['colour']), int(location))

    strategy.move(
        board=board,
        colour=Colour.load(data['colour_to_move']),
        dice_roll=data['dice_roll'],
        make_move=lambda l, r: board.move_piece(board.get_piece_at(l), r)
    )

    board.print_board()
