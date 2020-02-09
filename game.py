from random import randint

from board import Board
from colour import Colour


class Game:
    def __init__(self):
        self.board = Board.create_starting_board()
        self.first_player = Colour(randint(0, 1))

    def run_game(self, verbose=True):
        if verbose:
            print('%s goes first' % self.first_player)
            self.board.print_board()
        i = self.first_player.value
        while True:
            dice_roll = [randint(1, 6), randint(1, 6)]
            if dice_roll[0] == dice_roll[1]:
                dice_roll = [dice_roll[0]] * 4
            colour = Colour(i % 2)
            if verbose:
                print("%s rolled %s" % (colour, dice_roll))
            self.make_move(dice_roll, colour)
            if verbose:
                self.board.print_board()
            i = i + 1
            if self.board.has_game_ended():
                if verbose:
                    print('%s has won!' % self.board.who_won())
                break

    def make_move(self, dice_roll, colour):
        for die_roll in dice_roll:
            valid_pieces = self.board.get_pieces(colour)
            for piece in valid_pieces:
                if self.board.is_move_possible(piece, die_roll):
                    self.board.move_piece(piece, die_roll)
                    break

    def who_started(self):
        return self.first_player

    def who_won(self):
        return self.board.who_won()
