init python:
    from bisect import bisect_right
    import random

    import pygame

    from board import BoardController
    from player import Player, Enemy

    settings = {
        "logical_width": 6,
        "logical_height": 6,
        "stone_size": 64,
    }

    def next_turn(player_one, player_two):
        player_one.turn = not player_one.turn
        player_two.turn = not player_two.turn

    class NewReversiGame(Action):
        def __init__(self, board):
            self.board = board

        def __call__(self):
            self.board.board_controller.board = self.board.board_controller.clear_board()
            player_one.score = 0
            player_two.score = 0
            renpy.redraw(self.board, 0)


    class Scoreboard(renpy.Displayable):
        def render(self, width, height, st, at):
            render = renpy.Render(640, 800)

            scoreboard = "{} has {} points. {} has {} points.".format(
                player_one.name, player_one.score, player_two.name, player_two.score
            )

            render.place(Text(scoreboard), 300, 500)

            renpy.redraw(self, 0)

            return render


    class DisplayableBoard(renpy.Displayable):
        def __init__(self, background, x_stone, x_hover_stone, o_stone, **kwargs):
            super(DisplayableBoard, self).__init__(**kwargs)

            self.board_controller = BoardController(
                settings["logical_width"],
                settings["logical_height"]
            )

            self.width = settings["logical_width"]
            self.height = settings["logical_height"]

            self.board_d = background

            self.x_stone = x_stone
            self.x_hover_stone = x_hover_stone
            self.o_stone = o_stone

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
                
        def render(self, width, height, st, at):
            render = renpy.Render(800, 600)

            # Draw board
            render.place(self.board_d, 0, 0)

            # Draw stones
            for y in range(self.height):
                for x in range(self.width):
                    if self.board_controller.board[x][y] != 0:
                        if self.board_controller.board[x][y] == 'X':
                            stone = self.x_stone
                        elif self.board_controller.board[x][y] == 'O':
                            stone = self.o_stone

                        render.place(stone, (self.one_tile_size * x), (self.one_tile_size * y))

            # Draw hovering stone
            if player_one.turn:
                #if self.mouse_x >= self.mapping[0] and self.mouse_y >= self.mapping[0]:
                if not self.mouse_x < 0 or self.mouse_y < 0:
                    c, d = self.find_nearest_tile(self.mouse_x, self.mouse_y)
                    if c <= 5 and d <= 5:
                        if self.board_controller.board[c][d] == 0:
                            render.place(
                                self.x_hover_stone,
                                self.one_tile_size * c, 
                                self.one_tile_size * d
                            )

            if player_two.turn:
                move = player_two.get_move(self.board_controller)

                result = self.board_controller.try_move((move.x, move.y), player_two.stone_type)
                if result:
                    player_two.score += result
                    renpy.redraw(self, 0)
                    next_turn(player_one, player_two)

            return render

        def find_nearest_tile(self, x, y):
            x1 = bisect_right(self.mapping, x)
            y1 = bisect_right(self.mapping, y)
            return x1, y1

        def event(self, ev, x, y, st):
            if player_one.turn:
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
                                player_one.stone_type
                            )
                            if result:
                                player_one.score += result
                                next_turn(player_one, player_two)

                renpy.redraw(self, 0)

init python:
    board_bg = Image("board.png")
    black_stone = Image("black_stone.png")
    white_stone = Image("white_stone.png")
    hover_stone = Transform(black_stone, alpha=0.5)
    
    board = DisplayableBoard(
        background=board_bg,
        x_stone=black_stone,
        x_hover_stone=hover_stone,
        o_stone=white_stone,
    )

    player_one = Player(name="Player", stone_type='X')
    player_two = Enemy(name="CPU", stone_type='O')

    player_one.turn = True

    scoreboard = Scoreboard()

screen reversi:
    add board:
        xalign 0.25
        xpos 400
    
    add scoreboard
    
    textbutton "New Game" xalign 0.98 yalign 0.98 action NewReversiGame(board)

label start:
    call screen reversi
    return