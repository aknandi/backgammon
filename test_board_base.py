import unittest

from board import Board


class TestBoardBase(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def add_piece(self, colour, location):
        self.add_many_pieces(1, colour, location)

    def add_many_pieces(self, number_of_pieces, colour, location):
        self.board.add_many_pieces(number_of_pieces, colour, location)

    def assert_piece_at(self, piece_location, move):
        piece = self.board.get_piece_at(piece_location)
        die_roll = move[0]
        expect_move_possible = move[1]
        self.assertEqual(self.board.is_move_possible(piece, die_roll), expect_move_possible)

    def assert_location(self, location, pieces_count):
        self.assertEqual(len(self.board.pieces_at(location)), pieces_count)

    def move_piece_at(self, location, roll):
        piece_to_move = self.board.get_piece_at(location)
        self.board.move_piece(piece_to_move, roll)


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
