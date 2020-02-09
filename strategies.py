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


class MoveRandomPiece(Strategy):
    def move(self, board, colour, dice_roll):
        for die_roll in dice_roll:
            valid_pieces = board.get_pieces(colour)
            shuffle(valid_pieces)
            for piece in valid_pieces:
                if board.is_move_possible(piece, die_roll):
                    board.move_piece(piece, die_roll)
                    break
