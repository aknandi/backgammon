import copy

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


class CompareAllMoves(Strategy):
    def move(self, board, colour, dice_roll):

        result = self.move_recursively(board, colour, dice_roll)
        if len(result['pieces_to_try_swapped']) > 0:
            new_dice_roll = dice_roll.copy()
            new_dice_roll.reverse()
            result_swapped = self.move_recursively(board, colour,
                                                   dice_rolls=new_dice_roll,
                                                   pieces_to_try=result['pieces_to_try_swapped'])
            if result_swapped['best_value'] < result['best_value']:
                result = result_swapped

        if result['best_moves'] is not None:
            for move in result['best_moves']:
                board.move_piece(board.get_piece_at(move['piece_at']), move['die_roll'])

    def move_recursively(self, board, colour, dice_rolls, pieces_to_try=None):
        best_board_value = float('inf')
        best_pieces_to_move = None
        pieces_to_try_swapped = []

        if pieces_to_try is None:
            pieces_to_try = [x.location for x in board.get_pieces(colour)]

        pieces_to_try = list(set(pieces_to_try))

        valid_pieces = []
        for piece_location in pieces_to_try:
            valid_pieces.append(board.get_piece_at(piece_location))
        valid_pieces.sort(key=Piece.spaces_to_home, reverse=True)

        dice_rolls_left = dice_rolls.copy()
        die_roll = dice_rolls_left.pop(0)

        for piece in valid_pieces:
            if board.is_move_possible(piece, die_roll):
                board_copy = copy.deepcopy(board)
                new_piece = board_copy.get_piece_at(piece.location)
                board_copy.move_piece(new_piece, die_roll)
                if len(dice_rolls_left) > 0:
                    result = self.move_recursively(board_copy, colour, dice_rolls_left)
                    if result['best_moves'] is None:
                        # we have done the best we can do
                        board_value = evaluate_board(board_copy, colour)
                        if board_value < best_board_value:
                            # Problem here: if it gives a better value to make less moves, this will be done.
                            best_board_value = board_value
                            best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]
                    if result['best_value'] < best_board_value:
                        best_board_value = result['best_value']
                        move = {'die_roll': die_roll, 'piece_at': piece.location}
                        best_pieces_to_move = [move] + result['best_moves']
                else:
                    board_value = evaluate_board(board_copy, colour)
                    if board_value < best_board_value:
                        best_board_value = board_value
                        best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]
            elif len(dice_rolls_left) != 0 and (die_roll != dice_rolls_left[0]):
                pieces_to_try_swapped.append(piece.location)

        return {'best_value': best_board_value,
                'best_moves': best_pieces_to_move,
                'pieces_to_try_swapped': pieces_to_try_swapped}

