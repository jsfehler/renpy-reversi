class Piece(object):
    BLACK = 'X'
    WHITE = 'O'

    def __init__(self, position, state):
        self.x = position[0]
        self.y = position[1]
        self.state = state

    @property
    def other_side(self):
        """The opposite side of this piece.

        Returns:
            str: Whatever the other side of piece current is.
        """

        if self.state == self.BLACK:
            return self.WHITE

        return self.BLACK
