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


if __name__ == '__main__':
    unittest.main()
