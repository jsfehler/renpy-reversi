init -1500 python:
    import string

    """Draws a map displayable based on the map data and tile displayables provided.
    """
    class TileMap(renpy.Displayable):
        def __init__(self, map, width, height, tiles, **kwargs):
            super(TileMap, self).__init__(**kwargs)

            self.map = map
            self.width = width
            self.height = height
            self.tiles = tiles

            self.one_tile_size = settings["stone_size"]
            self.render_width = self.one_tile_size * width
            self.render_height = self.one_tile_size * height

            # Create letter-tile references
            self.tile_reference = {
                string.ascii_uppercase[i]: tiles[i] for i in range(len(tiles))
            }

        def render(self, width, height, st, at):
            render = renpy.Render(self.render_width, self.render_height)

            # Draw board
            for y, x in product(range(self.height), range(self.width)):
                location = (self.width * y) + x
                tile_value = self.map[location]
                if tile_value != "0":
                    current_tile = self.tile_reference[tile_value]
                    render.place(
                        current_tile,
                        self.one_tile_size * x,
                        self.one_tile_size * y
                    )

            return render