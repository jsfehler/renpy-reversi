import copy
import random

from piece import Piece


class Player(object):
    def __init__(self, name, stone_type):
        self.name = name
        self.stone_type = stone_type

        self.turn = False
        self.score = 0


class Enemy(Player):
    """Player with an AI.
    """

    def get_possible_moves(self, board):
        """Returns a list of [x,y] lists of valid moves on the given board.
        """
        # Check every tile on the board, get list of possible valid places
        valids = []
        for x in range(1, board.width + 1):
            for y in range(1, board.height + 1):
                new_piece = Piece(
                    position=(x - 1, y - 1),
                    state=self.stone_type
                )
                if board.is_valid_move(new_piece):
                    valids.append(new_piece)

        return valids

    def get_move(self, board):
        """
        Args:
            board: The Board to look for moves on.

        Returns:
            False if no moves, else the Piece selected
        """
        possible_moves = self.get_possible_moves(board)
        if len(possible_moves) == 0:
            return False

        # Randomize starting point
        random.shuffle(possible_moves)

        # Corner takes priority
        for p in possible_moves:
            if board.is_corner(p.x, p.y):
                return p

        # Can't go to corner, so find best possible move
        best_score = -1
        best_move = possible_moves[0]

        for p in possible_moves:
            b = copy.deepcopy(board)
            result = b.try_move((p.x, p.y), self.stone_type)
            if result > best_score:
                best_move = p
                best_score = result

        return best_move
