import unittest

from colour import Colour
from compare_all_moves_strategy import CompareAllMoves
from test_board_base import TestBoardBase, Contains


class TestBoardIsMovePossible(TestBoardBase):

    def test_moves(self):

        self.add_many_pieces(1, Colour.WHITE, 1)
        self.add_many_pieces(1, Colour.WHITE, 3)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [6, 4])

        self.assert_location(7, Contains(2).pieces())

    def test_make_single_move_to_win(self):

        self.add_many_pieces(1, Colour.WHITE, 23)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [6, 4])

        self.assert_location(23, Contains(0).pieces())

    def test_can_use_second_roll_without_first(self):
        self.add_many_pieces(2, Colour.WHITE, 0)
        self.add_many_pieces(2, Colour.BLACK, 3)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [3, 4])

        self.assert_location(4, Contains(1).pieces())
        self.assert_location(0, Contains(1).pieces())

    def test_can_use_not_all_dice(self):
        self.add_many_pieces(3, Colour.WHITE, 18)
        self.add_many_pieces(1, Colour.WHITE, 12)
        self.add_many_pieces(2, Colour.BLACK, 17)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [5, 5, 5, 5])

        self.assert_location(23, Contains(3).pieces())
        self.assert_location(12, Contains(1).pieces())


if __name__ == '__main__':
    unittest.main()
