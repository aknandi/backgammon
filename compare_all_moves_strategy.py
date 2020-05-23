from strategies import Strategy
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

    @staticmethod
    def get_difficulty():
        return "Hard"

    def move(self, board, colour, dice_roll, make_move):

        result = self.move_recursively(board, colour, dice_roll)
        not_a_double = len(dice_roll) == 2
        if not_a_double:
            new_dice_roll = dice_roll.copy()
            new_dice_roll.reverse()
            result_swapped = self.move_recursively(board, colour,
                                                   dice_rolls=new_dice_roll)
            if result_swapped['best_value'] < result['best_value'] and \
                    len(result_swapped['best_moves']) >= len(result['best_moves']):
                result = result_swapped

        if len(result['best_moves']) != 0:
            for move in result['best_moves']:
                make_move(move['piece_at'], move['die_roll'])

    def move_recursively(self, board, colour, dice_rolls):
        best_board_value = float('inf')
        best_pieces_to_move = []

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
                board_copy = board.create_copy()
                new_piece = board_copy.get_piece_at(piece.location)
                board_copy.move_piece(new_piece, die_roll)
                if len(dice_rolls_left) > 0:
                    result = self.move_recursively(board_copy, colour, dice_rolls_left)
                    if len(result['best_moves']) == 0:
                        # we have done the best we can do
                        board_value = evaluate_board(board_copy, colour)
                        if board_value < best_board_value and len(best_pieces_to_move) < 2:
                            best_board_value = board_value
                            best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]
                    elif result['best_value'] < best_board_value:
                        new_best_moves_length = len(result['best_moves']) + 1
                        if new_best_moves_length >= len(best_pieces_to_move):
                            best_board_value = result['best_value']
                            move = {'die_roll': die_roll, 'piece_at': piece.location}
                            best_pieces_to_move = [move] + result['best_moves']
                else:
                    board_value = evaluate_board(board_copy, colour)
                    if board_value < best_board_value and len(best_pieces_to_move) < 2:
                        best_board_value = board_value
                        best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]

        return {'best_value': best_board_value,
                'best_moves': best_pieces_to_move}

