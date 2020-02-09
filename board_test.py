import unittest

from board import Board
from colour import Colour


class TestBoard(unittest.TestCase):

    def test_cannot_move_to_unoccupied_space(self):
        board = Board()

        board.add_many_pieces(1, Colour.BLACK, 12)

        piece = board.pieces_at(12)[0]
        self.assertEqual(board.is_move_possible(piece, 6), True)

    def test_cannot_move_off_before_end_game(self):
        board = Board()

        board.add_many_pieces(1, Colour.BLACK, 1)
        board.add_many_pieces(1, Colour.BLACK, 17)

        piece = board.pieces_at(1)[0]
        self.assertEqual(board.is_move_possible(piece, 6), False)

    def test_cannot_move_to_occupied_space(self):
        board = Board()

        board.add_many_pieces(1, Colour.BLACK, 17)
        board.add_many_pieces(2, Colour.WHITE, 11)

        piece = board.pieces_at(17)[0]
        self.assertEqual(board.is_move_possible(piece, 6), False)

    def test_cannot_move_off_low_value_piece_too_soon(self):
        board = Board()

        board.add_many_pieces(1, Colour.BLACK, 1)
        board.add_many_pieces(1, Colour.BLACK, 6)

        piece = board.pieces_at(1)[0]
        self.assertEqual(board.is_move_possible(piece, 5), False)


if __name__ == '__main__':
    unittest.main()
