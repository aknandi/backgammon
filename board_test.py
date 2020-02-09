import unittest

from board import Board
from colour import Colour


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_can_move_to_unoccupied_space(self):
        self.board.add_many_pieces(1, Colour.BLACK, 12)

        self.assert_piece_at(12, Can.move(6))

    def test_cannot_move_to_occupied_space(self):
        self.board.add_many_pieces(1, Colour.BLACK, 17)
        self.board.add_many_pieces(2, Colour.WHITE, 11)

        self.assert_piece_at(17, Cannot.move(6))

    def test_can_move_to_occupied_space_if_same_colour(self):
        self.board.add_many_pieces(1, Colour.WHITE, 17)
        self.board.add_many_pieces(2, Colour.WHITE, 11)

        self.assert_piece_at(17, Can.move(6))

    def test_can_take_piece(self):
        self.board.add_many_pieces(1, Colour.BLACK, 17)
        self.board.add_many_pieces(1, Colour.WHITE, 11)

        self.assert_piece_at(17, Can.move(6))

    def test_cannot_move_off_before_end_game(self):
        self.board.add_many_pieces(1, Colour.BLACK, 1)
        self.board.add_many_pieces(1, Colour.BLACK, 17)

        self.assert_piece_at(1, Cannot.move(6))

    def test_can_move_several_pieces_off_in_end_game(self):
        self.board.add_many_pieces(1, Colour.BLACK, 1)
        self.board.add_many_pieces(2, Colour.BLACK, 2)

        self.assert_piece_at(2, Can.move(2))
        self.board.move_piece(self.board.get_piece_at(2), 2)
        self.assert_piece_at(2, Can.move(2))
        self.board.move_piece(self.board.get_piece_at(2), 2)
        self.assert_piece_at(1, Can.move(2))

    def test_cannot_move_off_low_value_piece_too_soon(self):
        self.board.add_many_pieces(1, Colour.BLACK, 1)
        self.board.add_many_pieces(1, Colour.BLACK, 6)

        self.assert_piece_at(1, Cannot.move(5))

    def test_cannot_move_other_piece_if_there_is_a_taken_piece(self):
        self.board.add_many_pieces(1, Colour.WHITE, 0)
        self.board.add_many_pieces(1, Colour.WHITE, 6)

        self.assert_piece_at(6, Cannot.move(1))

    def test_can_move_taken_piece(self):
        self.board.add_many_pieces(1, Colour.WHITE, 0)
        self.board.add_many_pieces(1, Colour.WHITE, 6)

        self.assert_piece_at(0, Can.move(1))

    def assert_piece_at(self, piece_location, move):
        piece = self.board.get_piece_at(piece_location)
        die_roll = move[0]
        expect_move_possible = move[1]
        self.assertEqual(self.board.is_move_possible(piece, die_roll), expect_move_possible)


class Can:
    @staticmethod
    def move(die_roll):
        return die_roll, True


class Cannot:
    @staticmethod
    def move(die_roll):
        return die_roll, False

if __name__ == '__main__':
    unittest.main()
