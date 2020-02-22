import unittest

from board import Board
from colour import Colour


class TestBoardBase(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def add_piece(self, colour, location):
        self.add_many_pieces(1, colour, location)

    def add_many_pieces(self, number_of_pieces, colour, location):
        self.board.add_many_pieces(number_of_pieces, colour, location)


class TestBoardIsMovePossible(TestBoardBase):

    def test_can_move_to_unoccupied_space(self):
        self.add_many_pieces(1, Colour.BLACK, 12)

        self.assert_piece_at(12, Can.move(6))

    def test_cannot_move_to_occupied_space(self):
        self.add_many_pieces(1, Colour.BLACK, 17)
        self.add_many_pieces(2, Colour.WHITE, 11)

        self.assert_piece_at(17, Cannot.move(6))

    def test_can_move_to_occupied_space_if_same_colour(self):
        self.add_many_pieces(1, Colour.WHITE, 17)
        self.add_many_pieces(2, Colour.WHITE, 11)

        self.assert_piece_at(17, Can.move(6))

    def test_can_take_piece(self):
        self.add_many_pieces(1, Colour.BLACK, 17)
        self.add_many_pieces(1, Colour.WHITE, 11)

        self.assert_piece_at(17, Can.move(6))

    def test_cannot_move_off_before_end_game(self):
        self.add_many_pieces(1, Colour.BLACK, 1)
        self.add_many_pieces(1, Colour.BLACK, 17)

        self.assert_piece_at(1, Cannot.move(6))

    def test_can_move_several_pieces_off_in_end_game(self):
        self.add_many_pieces(1, Colour.BLACK, 1)
        self.add_many_pieces(2, Colour.BLACK, 2)

        self.assert_piece_at(2, Can.move(2))
        self.board.move_piece(self.board.get_piece_at(2), 2)
        self.assert_piece_at(2, Can.move(2))
        self.board.move_piece(self.board.get_piece_at(2), 2)
        self.assert_piece_at(1, Can.move(2))

    def test_cannot_move_off_low_value_piece_too_soon(self):
        self.add_many_pieces(1, Colour.BLACK, 1)
        self.add_many_pieces(1, Colour.BLACK, 6)

        self.assert_piece_at(1, Cannot.move(5))

    def test_cannot_move_other_piece_if_there_is_a_taken_piece(self):
        self.add_many_pieces(1, Colour.WHITE, 0)
        self.add_many_pieces(1, Colour.WHITE, 6)

        self.assert_piece_at(6, Cannot.move(1))

    def test_can_move_taken_piece(self):
        self.add_many_pieces(1, Colour.WHITE, 0)
        self.add_many_pieces(1, Colour.WHITE, 6)

        self.assert_piece_at(0, Can.move(1))

    def assert_piece_at(self, piece_location, move):
        piece = self.board.get_piece_at(piece_location)
        die_roll = move[0]
        expect_move_possible = move[1]
        self.assertEqual(self.board.is_move_possible(piece, die_roll), expect_move_possible)


class TestBoardMovePiece(TestBoardBase):

    def test_can_move_to_unoccupied_space(self):
        self.add_piece(Colour.WHITE, 12)

        self.move_piece_at(12, Die.roll_of(1))

        self.assert_location(12, Contains(0).pieces())
        self.assert_location(13, Contains(1).piece())

    def test_can_move_to_occupied_space_of_same_colour(self):
        self.add_piece(Colour.BLACK, 12)
        self.add_many_pieces(2, Colour.BLACK, 10)

        self.move_piece_at(12, Die.roll_of(2))

        self.assert_location(12, Contains(0).pieces())
        self.assert_location(10, Contains(3).pieces())

    def test_can_take_piece(self):
        self.add_piece(Colour.WHITE, 12)
        self.add_piece(Colour.BLACK, 15)

        self.move_piece_at(12, Die.roll_of(3))

        self.assert_location(12, Contains(0).pieces())
        self.assert_location(15, Contains(1).piece())
        self.assertEqual(self.board.get_piece_at(15).colour, Colour.WHITE)
        self.assert_location(25, Contains(1).piece())

    def test_can_move_piece_off(self):
        self.add_piece(Colour.WHITE, 22)

        self.move_piece_at(22, Die.roll_of(3))

        white_piece = self.board.get_pieces(Colour.WHITE)
        self.assertEqual(len(white_piece), 0)

    def test_can_move_piece_off_when_overshooting(self):
        self.add_piece(Colour.BLACK, 1)

        self.move_piece_at(1, Die.roll_of(6))

        black_pieces = self.board.get_pieces(Colour.BLACK)
        self.assertEqual(len(black_pieces), 0)

    def move_piece_at(self, location, roll):
        piece_to_move = self.board.get_piece_at(location)
        self.board.move_piece(piece_to_move, roll)

    def assert_location(self, location, pieces_count):
        self.assertEqual(len(self.board.pieces_at(location)), pieces_count)


class Can:
    @staticmethod
    def move(die_roll):
        return die_roll, True


class Cannot:
    @staticmethod
    def move(die_roll):
        return die_roll, False


class Die:
    @staticmethod
    def roll_of(roll):
        return roll


class Contains:
    def __init__(self, pieces_count):
        self.__pieces_count = pieces_count

    def pieces(self):
        return self.__pieces_count

    def piece(self):
        return self.__pieces_count


if __name__ == '__main__':
    unittest.main()
