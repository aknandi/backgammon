from colour import Colour


class Piece:
    def __init__(self, colour, location):
        self.colour = colour
        self.location = location

    def spaces_to_home(self):
        if self.colour == Colour.WHITE:
            return 25 - self.location
        else:
            return self.location