from mlgame.view.view_model import create_image_view_data
import random
import math

from ..loader import create_image_asset
from ..level import Level

# The Map Object
class Map:
    TILE_TYPES = {
        "empty": { "image": None, "destroyable": False },

        "ground_light": { "image": "ground_light", "destroyable": False },
        "ground_dark": { "image": "ground_dark", "destroyable": False },

        "barrel": { "image": "barrel", "destroyable": True },
        "rock": { "image": "rock", "destroyable": False }
    }

    # Initialize The Object
    def __init__(self, level: Level, width: int, height: int):
        self.Level = level

        self.width = level.Map["width"]
        self.height = level.Map["height"]
        self.shake = 0

        self.background_tiles = []
        self.foreground_tiles = []

        for _ in range(level.Map["width"] * level.Map["height"]):
            if random.randint(0, 2) > 0:
                self.background_tiles.append("ground_dark")
            else:
                self.background_tiles.append("ground_light")

            self.foreground_tiles.append("empty")

        for _, tile in enumerate(level.Map["tiles"]):
            self.set_foreground_tile(tile["type"], tile["x"], tile["y"])

        self.resize(width, height)

    # Add The All Assets Needed By The Map
    def add_assets(self, assets: list):
        assets.append(create_image_asset("images/ground_light.png", 64, 64))
        assets.append(create_image_asset("images/ground_dark.png", 64, 64))
        assets.append(create_image_asset("images/barrel.png", 64, 64))
        assets.append(create_image_asset("images/rock.png", 64, 64))
    
    # Resize The Map
    def resize(self, width: int, height: int):
        self.tile_size = 0

        if width > height:
            self.tile_size = width / (self.width + 1)
        else:
            self.tile_size = height / (self.height + 1)

        if self.tile_size * self.width > width:
            self.tile_size = width / (self.width + 1)
        elif self.tile_size * self.height > height:
            self.tile_size = height / (self.height + 1)

        self.tile_size = math.floor(self.tile_size * 0.99999)

        self.target_render_offset_x = round((width / 2) - ((self.width / 2) * self.tile_size), 0)
        self.target_render_offset_y = round((height / 2) - ((self.height / 2) * self.tile_size), 0)

        self.render_offset_x = self.target_render_offset_x
        self.render_offset_y = self.target_render_offset_y

    # Get A Background Tile
    def get_background_tile(self, x: int, y: int):
        if x + (y * self.width) >= len(self.background_tiles):
            raise Exception(f"Position Out Of Bounds: {x}, {y} ({self.width}, {self.height})")

        return self.background_tiles[x + (y * self.width)]

    # Get A Foreground Tile
    def get_foreground_tile(self, x: int, y: int):
        if x + (y * self.width) >= len(self.foreground_tiles):
            raise Exception(f"Position Out Of Bounds: {x}, {y} ({self.width}, {self.height})")

        return self.foreground_tiles[x + (y * self.width)]

    # Get Matrix
    def get_matrix(self):
        matrix = []

        for index in range(len(self.background_tiles)):
            if self.foreground_tiles[index] == None:
                matrix.append(0)
            else:
                if self.TILE_TYPES[self.foreground_tiles[index]]["destroyable"]:
                    matrix.append(1)
                else:
                    matrix.append(2)

        return matrix


    # Set A Foreground Tile
    def set_foreground_tile(self, tile_type: str, x: int, y: int):
        if tile_type not in self.TILE_TYPES:
            raise Exception(f"Tile Type Not Found: \"{tile_type}\" ({x}, ${y})")

        self.foreground_tiles[x + (y * self.width)] = tile_type

    # Get All The Foreground Tiles With Position
    def get_foreground_tiles_with_position(self):
        tiles = []

        i = 0
 
        for y in range(self.height):
            for x in range(self.width):
                if self.foreground_tiles[i] != "empty":
                    # The size of the tile is 64 x 64
                    tiles.append({ "type": self.foreground_tiles[i], "x": x * 64, "y": y * 64, "index": i })

                i += 1

        return tiles

    # Bomb Exploaded
    def bomb_exploded(self, x: int, y: int):
        i = 0
 
        for tile_y in range(self.height):
            for tile_x in range(self.width):
                if self.TILE_TYPES[self.foreground_tiles[i]]["destroyable"] and math.dist([x, y], [tile_x * 64, tile_y * 64]) < self.Level.Rules["bomb_explode_range"]:
                    self.foreground_tiles[i] = "empty"
                        

                i += 1 

    # Update The Map
    def update(self):
        self.shake = self.shake * 0.8

        self.render_offset_x = self.target_render_offset_x + random.randint(round(-self.shake * self.tile_size), round(self.shake * self.tile_size))
        self.render_offset_y = self.target_render_offset_y + random.randint(round(-self.shake * self.tile_size), round(self.shake * self.tile_size))

    # Render The Map
    def render(self, object_info: list):
        for y in range(self.height):
            for x in range(self.width):
                background_tile = Map.TILE_TYPES[self.get_background_tile(x, y)]
                foreground_tile = Map.TILE_TYPES[self.get_foreground_tile(x, y)]
    
                if (background_tile["image"] != None):
                    object_info.append({
                        "layer": 0,
                        "object": create_image_view_data(
                            background_tile["image"],

                            self.render_offset_x + (x * self.tile_size),
                            self.render_offset_y + (y * self.tile_size),

                            self.tile_size,
                            self.tile_size
                        )
                    })

                if (foreground_tile["image"] != None):
                    object_info.append({
                        "layer": 1,
                        "object": create_image_view_data(
                            foreground_tile["image"],

                            self.render_offset_x + (x * self.tile_size),
                            self.render_offset_y + (y * self.tile_size),

                            self.tile_size,
                            self.tile_size
                        )
                    })
