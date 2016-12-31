init -1500 python:
    from bisect import bisect_right
    from itertools import product

    import pygame

    from board import BoardController

    settings = {
        "stone_size": 64,
    }

    def next_turn(p1, p2):
        p1.turn = not p1.turn
        p2.turn = not p2.turn


    class NewReversiGame(Action):
        def __init__(self, board):
            self.board = board

        def __call__(self):
            self.board.board_controller.board = self.board.board_controller.clear_board()
            self.board.p1.score = 0
            self.board.p2.score = 0
            renpy.redraw(self.board, 0)


    class DisplayableBoard(renpy.Displayable):
        def __init__(self, map, x_stone, x_hover_stone, o_stone, player_one,
                     player_two, **kwargs):
            super(DisplayableBoard, self).__init__(**kwargs)

            self.map = map

            self.board_controller = BoardController(
                map[0],
                map[1],
                map[2]
            )

            self.width = map[1]
            self.height = map[2]

            self.x_stone = x_stone
            self.x_hover_stone = x_hover_stone
            self.o_stone = o_stone
    
            self.p1 = player_one
            self.p2 = player_two

            self.one_tile_size = settings["stone_size"]

            # List of each physical tile location
            self.mapping = []
            s = 0
            for _ in range(self.width):
                s += self.one_tile_size
                self.mapping.append(s)

            self.mouse_x = 0
            self.mouse_y = 0
            self.c = 0
            self.d = 0

        def get_pointer_position(self):
            if not self.mouse_x < 0 or self.mouse_y < 0:
                tile_x, tile_y = self.find_nearest_tile(self.mouse_x, self.mouse_y)
                if tile_x <= 5 and tile_y <= 5:
                    if self.board_controller.board[tile_x][tile_y] == 0:
                        return self.one_tile_size * tile_x, self.one_tile_size * tile_y

        def render(self, width, height, st, at):
            render = renpy.Render(800, 600)

            # Draw stones
            for y, x in product(range(self.height), range(self.width)):
                if self.board_controller.board[x][y] == 'X':
                    stone = self.x_stone
                elif self.board_controller.board[x][y] == 'O':
                    stone = self.o_stone
                else:
                    continue

                render.place(stone, (self.one_tile_size * x), (self.one_tile_size * y))

            # Draw hovering stone
            if self.p1.turn:
                p = self.get_pointer_position()
                if p is not None:
                    render.place(self.x_hover_stone, p[0], p[1])

            renpy.redraw(self, 0)
            return render

        def find_nearest_tile(self, x, y):
            x1 = bisect_right(self.mapping, x)
            y1 = bisect_right(self.mapping, y)
            return x1, y1

        def event(self, ev, x, y, st):
            if self.p1.turn:
                self.mouse_x = x
                self.mouse_y = y

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # Record the tile that was clicked on.
                    if not x < 0 or y < 0:
                        self.c, self.d = self.find_nearest_tile(x, y)

                elif ev.type == pygame.MOUSEBUTTONUP:
                    # If the currently hovered tile is the same as the one that was clicked, place the stone.
                    new_c, new_d = self.find_nearest_tile(x, y)
                    if new_c == self.c and new_d == self.d:
                        result = self.board_controller.try_move(
                            (self.c, self.d),
                            self.p1.stone_type
                        )
                        if result:
                            self.p1.score += result
                            renpy.restart_interaction()
                            next_turn(self.p1, self.p2)
                            renpy.call("cpu_turn")
