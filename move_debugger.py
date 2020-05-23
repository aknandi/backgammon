import json

from board import Board
from colour import Colour
from game import Strategy


if __name__ == '__main__':
    s = input('Paste move info:\n')
    data = json.loads(s)

    strategy = Strategy.create_by_name(data['strategy'])

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
