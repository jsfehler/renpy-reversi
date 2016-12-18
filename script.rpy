init python:
    from player import Player, Enemy

    board_bg = Image("board.png")
    black_stone = Image("black_stone.png")
    white_stone = Image("white_stone.png")
    hover_stone = Transform(black_stone, alpha=0.5)
    
    map_00 = (
        "000000"
        "000000"
        "000000"
        "000000"
        "000000"
        "000000"
    )
    
    map_01 = (
        "010010"
        "001100"
        "000000"
        "001100"
        "010010"
        "000000"
    )

    player_one = Player(name="Player", stone_type='X')
    player_two = Enemy(name="CPU", stone_type='O')

    board_background = TileBoard(map=(map_01, 6, 6), background=board_bg)

    board = DisplayableBoard(
        map=(map_01, 6, 6),
        x_stone=black_stone,
        x_hover_stone=hover_stone,
        o_stone=white_stone,
        player_one=player_one,
        player_two=player_two
    )

    player_one.turn = True

    scoreboard = Scoreboard(player_one, player_two)


screen reversi:
    add board_background:
        xalign 0.25
        xpos 400

    add board:
        xalign 0.25
        xpos 400
    
    add scoreboard
    
    textbutton "New Game" xalign 0.98 yalign 0.98 action NewReversiGame(board)

label start:
    call screen reversi
    return