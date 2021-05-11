from src.strategies import Strategy
from src.piece import Piece


class CompareAllMoves(Strategy):

    @staticmethod
    def get_difficulty():
        return "Hard"

    def assess_board(self, colour, myboard):
        pieces = myboard.get_pieces(colour)
        opponent_pieces = myboard.get_pieces(colour.other())
        pieces_on_board = len(pieces)
        sum_distances = 0
        number_of_singles = 0
        number_occupied_spaces = 0
        number_threatened_occupied_spaces = 0
        sum_single_distance_away_from_home = 0
        sum_threatened_single_distance_away_from_home = 0
        sum_distances_to_endzone = 0
        for piece in pieces:
            sum_distances = sum_distances + piece.spaces_to_home()
            if piece.spaces_to_home() > 6:
                sum_distances_to_endzone += piece.spaces_to_home() - 6
        last_opponents_piece_location = max([piece.location for piece in opponent_pieces])
        for location in range(1, 25):
            pieces = myboard.pieces_at(location)
            if len(pieces) != 0 and pieces[0].colour == colour:
                if len(pieces) == 1:
                    number_of_singles = number_of_singles + 1
                    sum_single_distance_away_from_home += 25 - pieces[0].spaces_to_home()
                    if location < last_opponents_piece_location:
                        sum_threatened_single_distance_away_from_home += 25 - pieces[0].spaces_to_home()
                elif len(pieces) > 1:
                    number_occupied_spaces += 1
                    if location < last_opponents_piece_location:
                        number_threatened_occupied_spaces += 1
        opponents_taken_pieces = len(myboard.get_taken_pieces(colour.other()))
        sum_distances_opponent = 0
        for piece in opponent_pieces:
            sum_distances_opponent = sum_distances_opponent + piece.spaces_to_home()
        return {
            'number_occupied_spaces': number_occupied_spaces,
            'opponents_taken_pieces': opponents_taken_pieces,
            'sum_distances': sum_distances,
            'sum_distances_opponent': sum_distances_opponent,
            'number_of_singles': number_of_singles,
            'sum_single_distance_away_from_home': sum_single_distance_away_from_home,
            'pieces_on_board': pieces_on_board,
            'sum_distances_to_endzone': sum_distances_to_endzone,
            'sum_threatened_single_distance_away_from_home': sum_threatened_single_distance_away_from_home,
            'number_threatened_occupied_spaces': number_threatened_occupied_spaces
        }

    def move(self, board, colour, dice_roll, make_move, opponents_activity):

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
                        board_value = self.evaluate_board(board_copy, colour)
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
                    board_value = self.evaluate_board(board_copy, colour)
                    if board_value < best_board_value and len(best_pieces_to_move) < 2:
                        best_board_value = board_value
                        best_pieces_to_move = [{'die_roll': die_roll, 'piece_at': piece.location}]

        return {'best_value': best_board_value,
                'best_moves': best_pieces_to_move}


class CompareAllMoves1(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] + 2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


# Weight opponents pieces based on their distance to home
class CompareAllMoves2(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent'])/3 + \
                      2 * board_stats['number_of_singles'] - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


# Weight singles based on their distance to home
class CompareAllMoves3(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent'])/3 + \
                      float(board_stats['sum_single_distance_away_from_home'])/6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces']
        return board_value


# Encourage moving pieces off the board if possible
class CompareAllMoves4(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board']

        return board_value


# Encourage getting pieces into the end zone as soon as possible
class CompareAllMoves5(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board'] + float(board_stats['sum_distances_to_endzone']) / 6

        return board_value


# Don't worry about leaving singles when all opponents pieces are past
class CompareAllMoves6(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_threatened_single_distance_away_from_home']) / 6 - \
                      board_stats['number_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board'] + float(board_stats['sum_distances_to_endzone']) / 6

        return board_value


#
class CompareAllMoves7(CompareAllMoves):

    def evaluate_board(self, myboard, colour):
        board_stats = self.assess_board(colour, myboard)

        board_value = board_stats['sum_distances'] - float(board_stats['sum_distances_opponent']) / 3 + \
                      float(board_stats['sum_threatened_single_distance_away_from_home']) / 6 - \
                      board_stats['number_threatened_occupied_spaces'] - board_stats['opponents_taken_pieces'] + \
                      3 * board_stats['pieces_on_board'] + float(board_stats['sum_distances_to_endzone']) / 6

        return board_value