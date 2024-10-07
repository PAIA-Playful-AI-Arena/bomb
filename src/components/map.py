from mlgame.view.view_model import create_image_view_data
from typing import List, Union
import random
import math

from ..level import Level

# Create A Tile Type
def create_tile_type(image: Union[None, str], destroyable: bool):
    return {
        "image": image,
        "destroyable": destroyable
    }

# Map
class Map:
    TILE_TYPES: dict = {
        "empty": create_tile_type(None, False),

        "ground_light": create_tile_type("tile_ground_light", False),
        "ground_dark": create_tile_type("tile_ground_dark", False),

        "barrel": create_tile_type("tile_barrel", True),
        "rock": create_tile_type("tile_rock", False),
        "rock2": create_tile_type("tile_rock2", False)
    }

    # Initialize The Component
    def __init__(self, level: Level, width: int, height: int) -> None:
        self.Level = level

        self.width = level.Map.width
        self.height = level.Map.height
        self.shake: float = 0

        self.background_tiles: List[str] = []
        self.foreground_tiles: List[str] = []

        # Generate the background tiles.
        for _ in range(level.Map.width * level.Map.height):
            if random.randint(0, 2) > 0:
                self.background_tiles.append("ground_dark")
            else:
                self.background_tiles.append("ground_light")

            self.foreground_tiles.append("empty")

        # Set the foreground tiles
        for tile in level.Map.tiles:
            self.set_foreground_tile(tile["type"], tile["x"], tile["y"])

        # Set the size of the tiles according to the size of the window.
        if width > height:
            self.tile_size = width / (self.width + 1)
        else:
            self.tile_size = height / (self.height + 1)

        # Fix tiles overflowing.
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
    def get_background_tile(self, x: int, y: int) -> str:
        if x + (y * self.width) < 0 or x + (y * self.width) >= len(self.background_tiles):
            raise Exception(f"Error: Tile position {x}, {y} out of bounds ({self.width}, {self.height})")

        return self.background_tiles[x + (y * self.width)]

    # Get A Foreground Tile
    def get_foreground_tile(self, x: int, y: int) -> str:
        if x + (y * self.width) < 0 or x + (y * self.width) >= len(self.foreground_tiles):
            raise Exception(f"Error: Tile position {x}, {y} out of bounds ({self.width}, {self.height})")

        return self.foreground_tiles[x + (y * self.width)]
    
    # Get Foreground Tiles With Position
    def get_foreground_tiles_with_position(self) -> List[dict]:
        tiles: List[dict] = []
        index: int = 0
 
        for y in range(self.height):
            for x in range(self.width):
                if self.foreground_tiles[index] != "empty":
                    tiles.append({ "type": self.foreground_tiles[index], "x": x * 64, "y": y * 64, "index": index })

                index += 1

        return tiles

    # Get A Matrix Of Foreground Tiles
    def get_foreground_tile_matrix(self) -> List[int]:
        matrix: List[int] = []

        for tile_type in self.foreground_tiles:
            if self.TILE_TYPES[tile_type]["image"] == None:
                matrix.append(0)
            else:
                if self.TILE_TYPES[tile_type]["destroyable"]:
                    matrix.append(2)
                else:
                    matrix.append(1)

        return matrix

    # Set A Foreground Tile
    def set_foreground_tile(self, tile_type: str, x: int, y: int) -> None:
        if tile_type not in self.TILE_TYPES:
            raise Exception(f"Error: Tile type \"{tile_type}\" not found ({x}, ${y})")

        self.foreground_tiles[x + (y * self.width)] = tile_type

    # Update The Map
    def update(self):
        self.shake = self.shake * 0.8
        self.render_offset_x = self.target_render_offset_x + random.randint(round(-self.shake * self.tile_size), round(self.shake * self.tile_size))
        self.render_offset_y = self.target_render_offset_y + random.randint(round(-self.shake * self.tile_size), round(self.shake * self.tile_size))

    # Get The Sprites To Render
    def get_sprites(self) -> List[dict]:
        sprites: List[dict] = []
        index: int = 0

        for y in range(self.height):
            for x in range(self.width):
                background_tile = Map.TILE_TYPES[self.background_tiles[index]]
                foreground_tile = Map.TILE_TYPES[self.foreground_tiles[index]]

                if (background_tile["image"] != None):
                    sprites.append(self.create_tile_sprite(background_tile["image"], 0, x, y))
                if (foreground_tile["image"] != None):
                    sprites.append(self.create_tile_sprite(foreground_tile["image"], 1, x, y))                

                index += 1

        return sprites

    # Create A Tile Sprite 
    def create_tile_sprite(self, image: str, layer: int, x: int, y: int) -> dict:
        return {
            "layer": layer,
            "data": create_image_view_data(
                image,
            
                self.render_offset_x + (x * self.tile_size),
                self.render_offset_y + (y * self.tile_size),
            
                self.tile_size,
                self.tile_size
            )
        }
