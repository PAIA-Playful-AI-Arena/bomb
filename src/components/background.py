from mlgame.view.view_model import create_image_view_data
from math import sin, radians
from random import random
from typing import List

from .map import Map

# The background itself.
class Background:
    GRADIENT_WIDTH = 1024
    GRADIENT_HEIGHT = 725

    # Initialize the background.
    def __init__(self, map: Map) -> None:
        self.Map = map

        self.waves = []
        self.last_x = 0
        self.last_y = 0

        self.wave_size = map.tile_render_size * 2

        # Generate the waves.
        for _ in range(round((map.window_width + map.window_height) / self.wave_size)):
            x = map.window_width * random()
            y = map.window_height * random()
            tries = 0

            # Make sure each waves are far enough from each other.
            while abs(self.last_x - x) < self.wave_size * 2 and tries < 10:
                x = map.window_width * random()
                tries += 1

            tries = 0

            while abs(self.last_y - y) < self.wave_size * 2:
                y = map.window_height * random()
                tries += 1

            self.last_x = x
            self.last_y = y

            self.waves.append({
                "x": map.window_width * random(),
                "y": map.window_height * random(),
                "size": self.wave_size + ((self.wave_size * 1.5) * random()),
                "animation": 360 * random()
            })

    # Update the background.
    def update(self) -> None:
        for index in reversed(range(len(self.waves))):
            wave = self.waves[index]

            if wave["animation"] > 360:
                wave["animation"] = 0
            else:
                wave["animation"] += 2

            if wave["x"] > self.Map.window_width:
                # Reset the wave.

                size = self.wave_size + ((self.wave_size * 1.5) * random())

                wave["x"] = -size
                wave["y"] = self.Map.window_width * random()
                wave["size"] = size

                tries = 0

                # Make sure each waves are far enough from bomb placed by other players.
                while abs(self.last_y - wave["y"]) < self.wave_size * 2 and tries < 10:
                    wave["y"] = self.Map.window_height * random()
                    tries += 1

                self.last_y = wave["y"]
            else:
                wave["x"] += self.wave_size * 0.01

    # Render the background.
    def render(self) -> List[dict]:
        sprites = []

        gradient_ratio = max(self.Map.window_width / self.GRADIENT_WIDTH, self.Map.window_width / self.GRADIENT_HEIGHT)
        gradient_width = self.GRADIENT_WIDTH * gradient_ratio
        gradient_height = self.GRADIENT_HEIGHT * gradient_ratio

        # Render the background gradient.
        sprites.append({
            "layer": 0,
            "data": create_image_view_data(
                "background_gradient",
 
                (self.Map.window_width / 2) - (gradient_width / 2),
                (self.Map.window_height / 2) - (gradient_height / 2),
 
                gradient_width,
                gradient_height
            )
        })

        # Render the background waves.
        for wave in self.waves:
            wave_render_height = wave["size"] * (0.25 + abs(sin(radians(wave["animation"]))))

            sprites.append({
                "layer": 0,
                "data": create_image_view_data(
                    "background_wave",
    
                    wave["x"] + self.Map.shake_render_offset_x,
                    (wave["y"] - (wave_render_height / 2)) + self.Map.shake_render_offset_x,

                     wave["size"],
                     wave_render_height
                )
            })

        return sprites
