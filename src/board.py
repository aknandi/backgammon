from random import shuffle
import copy
import json

from src.colour import Colour
from src.piece import Piece


class Board:
    def __init__(self):
        self.__pieces = []

    @classmethod
    def create_starting_board(cls):
        board = Board()
        board.add_many_pieces(2, Colour.WHITE, 1)
        board.add_many_pieces(5, Colour.BLACK, 6)
        board.add_many_pieces(3, Colour.BLACK, 8)
        board.add_many_pieces(5, Colour.WHITE, 12)
        board.add_many_pieces(5, Colour.BLACK, 13)
        board.add_many_pieces(3, Colour.WHITE, 17)
        board.add_many_pieces(5, Colour.WHITE, 19)
        board.add_many_pieces(2, Colour.BLACK, 24)
        return board

    def add_many_pieces(self, number_of_pieces, colour, location):
        for _ in range(number_of_pieces):
            self.__pieces.append(Piece(colour, location))

    def is_move_possible(self, piece, die_roll):
        if len(self.pieces_at(self.__taken_location(piece.colour))) > 0:
            if piece.location != self.__taken_location(piece.colour):
                return False
        if piece.colour == Colour.BLACK:
            die_roll = -die_roll
        new_location = piece.location + die_roll
        if new_location <= 0 or new_location >= 25:
            if not self.can_move_off(piece.colour):
                return False
            if new_location != 0 and new_location != 25:
                # this piece will overshoot the end
                return not any(x.spaces_to_home() >= abs(die_roll) for x in self.get_pieces(piece.colour))
            return True
        pieces_at_new_location = self.pieces_at(new_location)
        if len(pieces_at_new_location) == 0 or len(pieces_at_new_location) == 1:
            return True
        return self.pieces_at(new_location)[0].colour == piece.colour

    def no_moves_possible(self, colour, dice_roll):
        piece_locations = [x.location for x in self.get_pieces(colour)]
        piece_locations = list(set(piece_locations))

        dice_roll = list(set(dice_roll))

        pieces = []
        for piece_location in piece_locations:
            pieces.append(self.get_piece_at(piece_location))
        for die in dice_roll:
            for piece in pieces:
                if self.is_move_possible(piece, die):
                    return False

        return True

    def can_move_off(self, colour):
        return all(x.spaces_to_home() <= 6 for x in self.get_pieces(colour))

    def move_piece(self, piece, die_roll):
        if not self.__pieces.__contains__(piece):
            raise Exception('This piece does not belong to this board')
        if not self.is_move_possible(piece, die_roll):
            raise Exception('You cannot make this move')
        if piece.colour == Colour.BLACK:
            die_roll = -die_roll

        new_location = piece.location + die_roll
        if new_location <= 0 or new_location >= 25:
            self.__remove_piece(piece)

        pieces_at_new_location = self.pieces_at(new_location)

        if len(pieces_at_new_location) == 1 and pieces_at_new_location[0].colour != piece.colour:
            piece_to_take = pieces_at_new_location[0]
            piece_to_take.location = self.__taken_location(piece_to_take.colour)

        piece.location = new_location

    def pieces_at(self, location):
        return [x for x in self.__pieces if x.location == location]

    def get_piece_at(self, location):
        pieces = self.pieces_at(location)
        if len(pieces) == 0:
            return None
        return pieces[0]

    def get_pieces(self, colour):
        pieces = [x for x in self.__pieces if x.colour == colour]
        shuffle(pieces)
        return pieces

    def get_taken_pieces(self, colour):
        return self.pieces_at(self.__taken_location(colour))

    def has_game_ended(self):
        return len(self.get_pieces(Colour.WHITE)) == 0 or len(self.get_pieces(Colour.BLACK)) == 0

    def who_won(self):
        if not self.has_game_ended():
            raise Exception('The game has not finished yet!')
        return Colour.WHITE if len(self.get_pieces(Colour.WHITE)) == 0 else Colour.BLACK

    def create_copy(self):
        return copy.deepcopy(self)

    def get_move_lambda(self):
        return lambda l, r: self.move_piece(self.get_piece_at(l), r)

    def print_board(self):
        print("  13                  18   19                  24   25")
        print("---------------------------------------------------")
        line = "|"
        for i in range(13, 18 + 1):
            line = line + self.__pieces_at_text(i)
        line = line + "|"
        for i in range(19, 24 + 1):
            line = line + self.__pieces_at_text(i)
        line = line + "|"
        line = line + self.__pieces_at_text(self.__taken_location(Colour.BLACK))
        print(line)
        for _ in range(3):
            print("|                        |                        |")
        line = "|"
        for i in reversed(range(7, 12+1)):
            line = line + self.__pieces_at_text(i)
        line = line + "|"
        for i in reversed(range(1, 6+1)):
            line = line + self.__pieces_at_text(i)
        line = line + "|"
        line = line + self.__pieces_at_text(self.__taken_location(Colour.WHITE))
        print(line)
        print("---------------------------------------------------")
        print("  12                  7    6                   1    0")

    def to_json(self):
        data = {}
        for location in range(26):
            pieces = self.pieces_at(location)
            if len(pieces) > 0:
                data[location] = {'colour': pieces[0].colour.__str__(), 'count': len(pieces)}
        return json.dumps(data)

    def __taken_location(self, colour):
        if colour == Colour.WHITE:
            return 0
        else:
            return 25

    def __pieces_at_text(self, location):
        pieces = self.pieces_at(location)
        if len(pieces) == 0:
            return " .  "
        if pieces[0].colour == Colour.WHITE:
            return " %sW " % (len(pieces))
        else:
            return " %sB " % (len(pieces))

    def __remove_piece(self, piece):
        self.__pieces.remove(piece)
