from mlgame.view.view_model import create_image_view_data
from typing import Union, List
from random import randint
from math import floor

from .overlay import Overlay
from ..level import Level

# Create a tile type.
def create_tile_type(image: Union[None, str], destroyable: bool):
    return {
        "image": image,
        "destroyable": destroyable
    }

# The map itself.
class Map:
    TILE_TYPES = {
        "empty": create_tile_type(None, False),

        "barrel": create_tile_type("tile_barrel", True),
        "rock": create_tile_type("tile_rock", False),
    }

    # Initialize the map.
    def __init__(self, level: Level, overlay: Overlay) -> None:
        self.Level = level

        self.width = level.Map.width
        self.height = level.Map.height
        self.window_width = overlay.window_width
        self.window_height = overlay.window_height

        self.tiles = []

        # Generate an 2D matrix representing the tiles.
        for _ in range(self.width * self.height):
            self.tiles.append("empty")

        # Load the tiles.
        for tile in level.Map.tiles:
            self.set_tile(tile["type"], tile["x"], tile["y"])

        # Set the render size of the tiles according to the size of the window.
        if self.window_width > self.window_height:
            self.tile_render_size = self.window_width / (self.width + 1)
        else:
            self.tile_render_size = self.window_height / (self.height + 1)

        available_width = self.window_width - ((overlay.overlay_render_width * 2) + (overlay.overlay_render_size * 1.6))
        available_height = self.window_height - overlay.overlay_render_size

        # Fix the tiles from overflowing.
        if self.tile_render_size * self.width > available_width:
            self.tile_render_size = available_width / self.width
        elif self.tile_render_size * self.height > available_height:
            self.tile_render_size = available_height / self.height

        self.tile_render_size = floor(self.tile_render_size * 0.99999)

        self.target_render_offset_x = round((self.window_width / 2) - ((self.width / 2) * self.tile_render_size), 0)
        self.target_render_offset_y = round((self.window_height / 2) - ((self.height / 2) * self.tile_render_size), 0)
        self.render_offset_x = self.target_render_offset_x
        self.render_offset_y = self.target_render_offset_y

        self.render_shake = 0
        self.shake_render_offset_x = 0
        self.shake_render_offset_y = 0

    # Get a tile.
    def get_tile(self, x: int, y: int) -> str:
        index = x + (y * self.width)

        if index < 0 or index >= len(self.tiles):
            raise Exception(f"[Error] Tile position {x}, {y} is out of bounds! ({self.width}, {self.height})")

        return self.tiles[index]

    # Get the tiles with position.
    def get_tiles_with_position(self) -> List[dict]:
        tiles: List[dict] = []
        index: int = 0
 
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[index] != "empty":
                    tiles.append({ "type": self.tiles[index], "x": (x * 64), "y": (y * 64), "map_x": x, "map_y": y })

                index += 1

        return tiles

    # Get a matrix of tiles.
    def get_tile_matrix(self) -> List[int]:
        matrix = []

        for tile_type in self.tiles:
            if self.TILE_TYPES[tile_type]["image"] == None:
                matrix.append(0)
            else:
                if self.TILE_TYPES[tile_type]["destroyable"]:
                    matrix.append(2)
                else:
                    matrix.append(1)

        return matrix

    # Set a tile.
    def set_tile(self, tile_type: str, x: int, y: int) -> None:
        index = x + (y * self.width)

        if tile_type not in self.TILE_TYPES:
            raise Exception(f"[Error] Tile type \"{tile_type}\" not found! ({x}, ${y})")
        if index < 0 or index >= len(self.tiles):
            raise Exception(f"[Error] Tile position {x}, {y} is out of bounds! ({self.width}, {self.height})")

        self.tiles[index] = tile_type

    # Update the map.
    def update(self) -> None:
        # Update the shaking animation.
        if (round(self.render_shake > 0)):
            self.shake_render_offset_x = randint(round(-self.render_shake * self.tile_render_size), round(self.render_shake * self.tile_render_size))
            self.shake_render_offset_y = randint(round(-self.render_shake * self.tile_render_size), round(self.render_shake * self.tile_render_size))
            self.render_shake = self.render_shake * 0.75

            self.render_offset_x = self.target_render_offset_x + self.shake_render_offset_x
            self.render_offset_y = self.target_render_offset_y + self.shake_render_offset_y
        else:
            self.shake_render_offset_x = 0
            self.shake_render_offset_y = 0

            self.render_offset_x = self.target_render_offset_x
            self.render_offset_y = self.target_render_offset_y

    # Render the map.
    def render(self) -> List[dict]:
        sprites = []
        index = 0

        for y in range(self.height):
            for x in range(self.width):
                sprites.append(self.create_tile_sprites('tile_ground', 1, x, y + 0.15))

                tile_image = self.TILE_TYPES[self.tiles[index]]["image"]

                # Make sure the tile is not empty.
                if (tile_image != None):
                    sprites.append(self.create_tile_sprites(tile_image, 3, x, y))

                index += 1

        return sprites

    # Create a tile sprite.
    def create_tile_sprites(self, image: str, layer: int, x: Union[int, float], y: Union[int, float]) -> dict:
        return {
                "layer": layer,
                "data": create_image_view_data(
                    image,
                
                    self.render_offset_x + (x * self.tile_render_size),
                    self.render_offset_y + (y * self.tile_render_size),
                
                    self.tile_render_size,
                    self.tile_render_size
                )
        }
