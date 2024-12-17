from mlgame.view.view_model import create_image_view_data, create_polygon_view_data
from math import cos, sin, radians, dist, floor
from typing_extensions import Self
from random import random
from typing import List

from ..constants import TEAM_COLORS
from .map import Map

# The explosion cloud itself.
class ExplosionCloud:
    # Initialize the explosion cloud.
    def __init__(self, x: float, y: float, render_size: float) -> None:
        self.x = x
        self.y = y
        self.animation = 1

        self.render_size = render_size

    # Update the explosion cloud.
    def update(self) -> bool:
        self.animation += 0.6

        return round(self.animation) > 11

    # Render the explosion cloud.
    def render(self) -> dict:
        render_size = self.render_size + ((self.render_size * self.animation) * 0.02)

        return {
            "layer": 8,
            "data": create_image_view_data(
                f"explosion_cloud_{round(self.animation)}",

                self.x - (render_size / 2),
                self.y - (render_size / 2),

                render_size,
                render_size 
            )
        }

# The bomb itself.
class Bomb:
    # Initialize the bomb.
    def __init__(self, map: Map, team: int, x: float, y: float) -> None:
        self.Level = map.Level
        self.Map = map

        self.team = team

        self.x = x
        self.y = y
        self.countdown = self.Level.Rules.bomb_countdown

        self.explosion_clouds = []

        self.timer_render_size = map.tile_render_size * 0.3
        self.sparks_render_size = map.tile_render_size * 0.5

    # Destory the tiles around the bomb.
    def destory_tiles(self) -> None:
        self.Map.render_shake += self.Level.Rules.bomb_explosion_range * 0.0015

        for tile in self.Map.get_tiles_with_position():
            # We want to get the distance to the center of the tile.
            if self.Map.TILE_TYPES[tile["type"]]["destroyable"] and dist([self.x, self.y], [tile["x"] + 32, tile["y"] + 32]) < self.Level.Rules.bomb_explosion_range:

                self.Map.set_tile("empty", tile["map_x"], tile["map_y"])

    # Activate the bomb if any of the bombs around it exploded.
    def activate_bomb(self, bombs: List[Self]) -> None:
        

        return

    # Update the bomb.
    def update(self) -> str:
        if self.countdown > 0:
            self.countdown -= 1
        elif self.countdown > -1:
            self.countdown = -1

            # Initialize the explosion clouds.
            for _ in range(floor(self.Level.Rules.bomb_explosion_range / 40)):
                angle = radians(random() * 360)
                distance = random() * self.Level.Rules.bomb_explosion_range

                self.explosion_clouds.append(ExplosionCloud(
                    self.Map.render_offset_x + ((self.Map.tile_render_size / 64) * (self.x + (distance * cos(angle)))),
                    self.Map.render_offset_y + ((self.Map.tile_render_size / 64) * (self.y + (distance * cos(angle)))),
                    self.timer_render_size * 7.5
                ))
            
            return "explode"

        # Update the explosion clouds.
        for index in reversed(range(len(self.explosion_clouds))):
            if (self.explosion_clouds[index].update()):
                self.explosion_clouds.pop(index)

        if self.countdown == -1 and len(self.explosion_clouds) == 0:
            return "delete"

        return "none"

    # Render the bomb.
    def render(self) -> List[dict]:
        sprites = []

        if self.countdown > 0:
            bomb_render_x = self.Map.render_offset_x + ((self.Map.tile_render_size / 64) * self.x)
            bomb_render_y = self.Map.render_offset_y + ((self.Map.tile_render_size / 64) * self.y)
     
            countdown_render_x = bomb_render_x + (self.timer_render_size * 0.011)
            countdown_render_y = bomb_render_y + (self.timer_render_size * 0.074)
    
            background_points = []
            countdown_points = [[countdown_render_x, countdown_render_y]]
    
            # Generate the background polygon.
            for i in range(360):
                background_points.append([
                    countdown_render_x + ((self.timer_render_size * 0.3) * cos(radians(i - 90))),
                    countdown_render_y + ((self.timer_render_size * 0.3) * sin(radians(i - 90)))
                ])
    
            sprites.append({
                "layer": 5,
                "data": create_polygon_view_data(
                    "timer_background",
    
                    background_points,
    
                    '#ffffff'
                )
            })
    
            # Generate the countdown polygon.
            for i in range(round((360 / self.Level.Rules.bomb_countdown) * (self.Level.Rules.bomb_countdown - self.countdown))):
                countdown_points.append([
                    countdown_render_x + ((self.timer_render_size * 0.3) * cos(radians(i - 90))),
                    countdown_render_y + ((self.timer_render_size * 0.3) * sin(radians(i - 90)))
                ])
    
            # Make sure the points are enough to at least make a triangle.
            if (len(countdown_points) >= 3):
                sprites.append({
                    "layer": 5,
                    "data": create_polygon_view_data(
                        "timer_countdown",
        
                        countdown_points,
        
                        TEAM_COLORS[self.team - 1]
                    )
                })
    
            sprites.append({
                "layer": 5,
                "data": create_image_view_data(
                    "timer",
                    
                    bomb_render_x - (self.timer_render_size / 2),
                    bomb_render_y - (self.timer_render_size / 2),
    
                    self.timer_render_size,
                    self.timer_render_size
                )
            })
    
            # Render the sparks when the bomb is about to explode.
            if self.countdown < 2:
                sparks_render_x = bomb_render_x + (self.timer_render_size * 0.1)
                sparks_render_y = bomb_render_y - (self.timer_render_size * 0.1)
    
                sprites.append({
                    "layer": 5,
                    "data": create_image_view_data(
                        "timer_sparks",
    
                        sparks_render_x - (self.sparks_render_size / 2),
                        sparks_render_y - (self.sparks_render_size / 2),
    
                        self.sparks_render_size,
                        self.sparks_render_size
                    )
                })
    
            # Draw the explosion range.
            for y in range(self.Map.height):
                for x in range(self.Map.width):
                    if dist([self.x, self.y], [(x * 64) + 32, (y * 64) + 32]) < self.Level.Rules.bomb_explosion_range:
                        sprites.append(self.Map.create_tile_sprites(f"explosion_range_{self.team}", 4, x, y + 0.07))

        # Render the explosion clouds.
        for explosion_cloud in self.explosion_clouds:
            sprites.append(explosion_cloud.render())
        
        return sprites
