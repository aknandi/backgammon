from enum import Enum


class Colour(Enum):
    WHITE = 0
    BLACK = 1

    def other(self):
        if self == Colour.WHITE:
            return Colour.BLACK
        else:
            return Colour.WHITE

    def __str__(self):
        if self == Colour.WHITE:
            return 'white'
        else:
            return 'black'

    @staticmethod
    def load(str):
        if str == 'black':
            return Colour.BLACK
        elif str == 'white':
            return Colour.WHITE
        else:
            raise Exception("%s is not a valid colour" % str)
