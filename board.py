import copy
from itertools import product

from piece import Piece


class BoardController(object):
    """Logic for a board.

    Whenever a Player puts a Stone on a Board, the Board determines if
    the move was legal.
    """
    NORTH = [0, -1]
    SOUTH = [0, 1]
    EAST = [1, 0]
    WEST = [-1, 0]

    NORTHEAST = [1, -1]
    NORTHWEST = [-1, -1]
    SOUTHEAST = [1, 1]
    SOUTHWEST = [-1, 1]

    directions = [
        SOUTH,
        # SOUTHEAST,
        # SOUTHWEST,
        EAST,
        WEST,
        NORTH,
        # NORTHEAST,
        # NORTHWEST,
    ]

    def __init__(self, map=None, board_width=0, board_height=0):
        self.map = map
        self.height = board_height
        self.width = board_width

        self.clean_board = self._build_board()
        self.board = self.clear_board()

    def _build_board(self):
        clean_board = []
        
        if self.map is not None:
            for x, y in product(range(self.height), range(self.width)):
                location = (self.width * y) + x
                if self.map[location] == "0":
                    clean_board.append(0)
                elif self.map[location] == "1":
                    clean_board.append(1)
        
            clean_board = [clean_board[i:i + self.width] for i in xrange(0, len(clean_board), self.width)]
        
        else:
            clean_row = [0 for _ in range(self.width)]

            for y in range(self.height):
                clean_board.append(copy.deepcopy(clean_row))

        return clean_board

    def clear_board(self):
        """Clear all stones from the board.
        """
        return copy.deepcopy(self.clean_board)

    @property
    def full(self):
        """Check if every tile on the board is full.

        Returns:
            bool: True if all tiles are occupied, else False.
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] not in ['X', 'O']:
                    return False

        return True

    def is_corner(self, x, y):
        """Check if the (x, y) coordinate is a corner tile or not.
        Returns:
            bool: True if the (x, y) coordinate is a corner of the board.
        """
        top_left = (x == 0 and y == 0)
        bottom_left = (x == 0 and y == self.height - 1)
        top_right = (x == self.width - 1 and y == 0)
        bottom_right = (x == self.width - 1 and y == self.height - 1)

        return top_left or bottom_left or top_right or bottom_right

    def try_move(self, move, tile):
        """Try to place a stone on the given coordinates.

        Returns:
            int: Number of stones that were flipped
        """
        new_piece = Piece(position=move, state=tile)

        if self.is_valid_move(new_piece):
            self.board[new_piece.x][new_piece.y] = tile

        else:
            return 0

        tiles_to_flip = self.flip_adjacent_tiles(new_piece)

        if len(tiles_to_flip):
            for x, y in tiles_to_flip:
                self.board[x][y] = tile

            # The number of flipped tiles, plus the new stone
            return len(tiles_to_flip) + 1

        # No tiles flipped, but a new stone was placed
        return 1

    def is_tile_on_board(self, x, y):
        """Checks if coordinates are valid or not.

        This is what handles the conversion from tile coordinates to
        array coordinates.

        Returns:
            bool: True if x, y are valid coordinates, else False
        """
        return (
            0 <= x <= self.width - 1 and
            0 <= y <= self.height - 1
        )

    def is_piece_on_tile(self, piece):
        """Checks if stone is already on coordinates

        Returns:
            bool: True if a piece is already on the tile, else False
        """
        if self.board[piece.x][piece.y] != 0:
            return True
        return False

    def is_valid_move(self, piece):
        """Checks if the piece's coordinates are valid.

        Returns:
            bool: True if move is valid, else False
        """
        on_board = self.is_tile_on_board(piece.x, piece.y)
        if not on_board:
            return False

        return not self.is_piece_on_tile(piece)

    def flip_adjacent_tiles(self, piece):
        """
        Returns:
             list
        """
        tiles_to_flip = []

        # Check every adjacent tile
        for adjacent_x, adjacent_y in self.directions:
            test_x = piece.x
            test_y = piece.y

            test_x += adjacent_x
            test_y += adjacent_y

            # If tile is not on the board, reject it
            on_board = self.is_tile_on_board(test_x, test_y)
            if not on_board:
                continue

            # Tile already belongs to you
            tile_to_check = self.board[test_x][test_y]
            if tile_to_check is piece.state:
                continue

            if tile_to_check == piece.other_side:
                tiles_to_flip.append([test_x, test_y])

        return tiles_to_flip
