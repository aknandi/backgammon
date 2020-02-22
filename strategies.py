import copy
from random import shuffle

from game import Strategy
from piece import Piece


def evaluate_board(myboard, colour):
    pieces = myboard.get_pieces(colour)
    sum_distances = 0
    number_of_singles = 0
    number_occupied_spaces = 0
    for piece in pieces:
        sum_distances = sum_distances + piece.spaces_to_home()
    for location in range(1, 25):
        pieces = myboard.pieces_at(location)
        if len(pieces) != 0 and pieces[0].colour == colour:
            if len(pieces) == 1:
                number_of_singles = number_of_singles + 1
            elif len(pieces) > 1:
                number_occupied_spaces = number_occupied_spaces + 1
    opponents_taken_pieces = len(myboard.get_taken_pieces(colour.other()))

    board_value = sum_distances + 2*number_of_singles - number_occupied_spaces - opponents_taken_pieces
    return board_value


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


class CompareAllMoves(Strategy):
    def move(self, board, colour, dice_roll):
        valid_pieces = board.get_pieces(colour)
        best_board_value = float('inf')
        best_pieces_to_move = None
        for piece1 in valid_pieces:
            if board.is_move_possible(piece1, dice_roll[0]):
                board1 = copy.deepcopy(board)
                new_piece = board1.get_piece_at(piece1.location)
                board1.move_piece(new_piece, dice_roll[0])
                valid_pieces2 = board1.get_pieces(colour)
                for piece2 in valid_pieces2:
                    if board1.is_move_possible(piece2, dice_roll[1]):
                        board2 = copy.deepcopy(board1)
                        new_piece = board2.get_piece_at(piece2.location)
                        board2.move_piece(new_piece, dice_roll[1])
                        board_value = evaluate_board(board2, colour)
                        if board_value < best_board_value:
                            best_board_value = board_value
                            best_pieces_to_move = [piece1.location, piece2.location]
        if best_pieces_to_move is not None:
            board.move_piece(board.get_piece_at(best_pieces_to_move[0]), dice_roll[0])
            board.move_piece(board.get_piece_at(best_pieces_to_move[1]), dice_roll[1])
