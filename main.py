# Play backgammon
from random import randint

from board import Board
from colour import Colour


def make_move(board, colour):
    die_roll = randint(1, 6)
    print("%s rolled %s" % (colour, die_roll))
    valid_pieces = board.get_pieces(colour)
    for piece in valid_pieces:
        if board.is_move_possible(piece, die_roll):
            board.move_piece(piece, die_roll)
            break


board = Board.create_starting_board()
board.print_board()

number_of_moves = 100
i = 0
while i < number_of_moves:
    if i % 2 == 0:
        make_move(board, Colour.WHITE)
    else:
        make_move(board, Colour.BLACK)
    board.print_board()
    i = i + 1

