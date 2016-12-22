init python:
    from player import Player, Enemy

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

    tilemap_00 = (
        "AAAAAA"
        "AAAAAA"
        "AAAAAA"
        "AAAAAA"
        "AAAAAA"
        "AAAAAA"
    )

    tilemap_01 = (
        "A0AA0A"
        "AA00AA"
        "AAAAAA"
        "AA00AA"
        "A0AA0A"
        "AAAAAA"
    )


    board_tiles = [Image("board.png")]
    board_background = TileMap(map=tilemap_01, width=6, height=6, tiles=board_tiles)

    board = DisplayableBoard(
        map=(map_01, 6, 6),
        x_stone=black_stone,
        x_hover_stone=hover_stone,
        o_stone=white_stone,
        player_one=player_one,
        player_two=player_two
    )

    player_one.turn = True


screen reversi:

    frame:
        background None
        xalign 0.25
        xpos 400

        add board_background
        add board
    
    use scoreboard
    
    textbutton "New Game" xalign 0.98 yalign 0.98 action NewReversiGame(board)


screen scoreboard:
    frame:
        background None
        ypos 400

        text "{} has {} points. {} has {} points.".format(
            player_one.name, player_one.score, player_two.name, player_two.score
        )

label start:
    call screen reversi
    return