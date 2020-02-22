from random import shuffle

from game import Strategy
from piece import Piece

class MoveFurthestBackStrategy(Strategy):
    def move(self, board, colour, dice_roll):
        for die_roll in dice_roll:
            valid_pieces = board.get_pieces(colour)
            valid_pieces.sort(key=Piece.spaces_to_home, reverse=True)
            for piece in valid_pieces:
                if board.is_move_possible(piece, die_roll):
                    board.move_piece(piece, die_roll)
                    break


class MoveFurthestBackOrderDiceStrategy(Strategy):
    def move(self, board, colour, dice_roll):
        dice_roll.sort(reverse=True)
        for die_roll in dice_roll:
            valid_pieces = board.get_pieces(colour)
            valid_pieces.sort(key=Piece.spaces_to_home, reverse=True)
            for piece in valid_pieces:
                if board.is_move_possible(piece, die_roll):
                    board.move_piece(piece, die_roll)
                    break


class HumanStrategy(Strategy):
    def move(self, board, colour, dice_roll):
        print("It is your turn, you are %s, your roll is %s" % (colour, dice_roll))
        while len(dice_roll) > 0:
            board.print_board()
            print("You have %s left" % dice_roll)
            location = self.get_location(board, colour)
            piece = board.get_piece_at(location)
            die_roll = None
            while die_roll is None:
                try:
                    value = int(input("How far (or 0 to move another piece)?\n"))
                    if value == 0:
                        break
                    if value not in dice_roll or not board.is_move_possible(piece, value):
                        print("You can't make that move!")
                    else:
                        dice_roll.remove(value)
                        die_roll = value
                        board.move_piece(piece, die_roll)
                        print("")
                        print("")
                except ValueError:
                    print("That's not a number! Try again")
        print("Done!")

    def get_location(self, board, colour):
        value = None
        while value is None:
            try:
                location = int(input("Enter the location of the piece you want to move?\n"))
                piece_at_location = board.get_piece_at(location)
                if piece_at_location is None or piece_at_location.colour != colour:
                    print("You don't have a piece at location %s" % value)
                else:
                    value = location
            except ValueError:
                print("That's not a number! Try again")
        return value


class MoveRandomPiece(Strategy):
    def move(self, board, colour, dice_roll):
        for die_roll in dice_roll:
            valid_pieces = board.get_pieces(colour)
            shuffle(valid_pieces)
            for piece in valid_pieces:
                if board.is_move_possible(piece, die_roll):
                    board.move_piece(piece, die_roll)
                    break
