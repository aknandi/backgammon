from enum import Enum


class Colour(Enum):
    WHITE = 0
    BLACK = 1

    def other(self):
        if self == Colour.WHITE:
            return Colour.BLACK
        else:
            return Colour.WHITE