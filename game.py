import json
from random import randint

from board import Board
from colour import Colour
from strategies import Strategy


class ReadOnlyBoard:
    board: Board

    def __init__(self, board):
        self.board = board

    # Delegate all readonly method calls to the board
    def __getattr__(self, name):
        if hasattr(self.board, name) and callable(getattr(self.board, name)):
            return getattr(self.board, name)

        return super(ReadOnlyBoard, self).__getattr__(name)

    def add_many_pieces(self, number_of_pieces, colour, location):
        self.__raise_exception__()

    def move_piece(self, piece, die_roll):
        self.__raise_exception__()

    def __raise_exception__(self):
        raise Exception("Do not try and change the board directly, use the make_move parameter instead")


class Game:
    def __init__(self, white_strategy: Strategy, black_strategy: Strategy, first_player: Colour):
        self.board = Board.create_starting_board()
        self.first_player = first_player
        self.strategies = {
            Colour.WHITE: white_strategy,
            Colour.BLACK: black_strategy
        }

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

            def handle_move(location, die_roll):
                if not dice_roll.__contains__(die_roll):
                    raise Exception("%d is not a roll that's allowed" % die_roll)
                piece = self.board.get_piece_at(location)
                self.board.move_piece(piece, die_roll)
                dice_roll.remove(die_roll)

            board_snapshot = self.board.to_json()
            dice_roll_snapshot = dice_roll.copy()

            self.strategies[colour].move(
                ReadOnlyBoard(self.board),
                colour,
                dice_roll.copy(),
                lambda location, die_roll: handle_move(location, die_roll)
            )

            if verbose and len(dice_roll) > 0:
                print('FYI not all moves were made. %s playing %s did not move %s' % (
                    colour,
                    self.strategies[colour].__class__.__name__,
                    dice_roll))
                self.board.print_board()
                state = {
                    'board': json.loads(board_snapshot),
                    'dice_roll': dice_roll_snapshot,
                    'colour_to_move': colour.__str__(),
                    'strategy': self.strategies[colour].__class__.__name__,
                }
                print(json.dumps(state))

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
