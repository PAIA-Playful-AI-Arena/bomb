from mlgame.view.view_model import create_image_view_data, create_polygon_view_data
from typing import List, Union
import random
import math

from pygame import sprite

from .players import Players
from ..level import Level
from .map import Map

# Bomb
class Bomb:
    # Initialize The Bomb
    def __init__(self, owner: str, x: float, y: float, countdown: int) -> None:
        self.owner: str = owner

        self.x = x
        self.y = y

        self.countdown = countdown

# Explosion Cloud
class ExplosionCloud:
    # Initialize The Explosion Cloud
    def __init__(self, x: float, y: float) -> None:
        self.animation_frame: int = 0

        self.x = x
        self.y = y

# The Bombs Component
class Bombs:
    # Initialize The Component
    def __init__(self, level: Level, map: Map, players: Players) -> None:
        self.Level = level
        self.Map = map
        self.Players = players

        self.bombs: List[Bomb] = []
        self.explosion_clouds = []

    # Spawn A Bomb
    def spawn_bomb(self, owner: str):
        if owner not in self.Players.players:
            raise Exception(f"Error: Player \"{owner}\" not found")

        player = self.Players.players[owner]

        if player.bombs > 0 and player.place_bomb_cooldown == 0:
            player.bombs -= 1
            player.place_bomb_cooldown = 5

        self.bombs.append(Bomb(owner, player.x, player.y, self.Level.Rules.bomb_countdown))

        return

    # Get The Amount Of The Explosion At A Position
    def get_explosion_amount(self, team: Union[None, int], x: float, y: float) -> int:
        amount: int = 0

        for bomb in self.bombs:
            if team != self.Players.players[bomb.owner].team and math.dist([x, y], [bomb.x, bomb.y]) <= self.Level.Rules.bomb_explosion_range:
                amount += 1

        return amount

    # Get A Matrix Of The Enemy Bombs
    def get_enemy_bomb_matrix(self, team: int) -> List[int]:
        matrix: List[int] = [0] * (self.Level.Map.width * self.Level.Map.height)

        for bomb in self.bombs:
            if self.Players.players[bomb.owner].team != team:
                index = math.floor(bomb.x / 64) + (math.floor(bomb.y / 64) * self.Level.Map.width)

                matrix[index] = matrix[index] + 1

        return matrix

    # Update The Bombs
    def update(self) -> None:
        for index in reversed(range(len(self.bombs))):
            bomb = self.bombs[index]

            if bomb.countdown > 0:
                bomb.countdown -= 1
            else:
                self.Players.players[bomb.owner].bombs += 1
                self.Map.shake += self.Level.Rules.bomb_explosion_range / 350

                # Destory the destroyable tiles in the explosion range.
                for tile in self.Map.get_foreground_tiles_with_position():
                    if self.Map.TILE_TYPES[tile["type"]]["destroyable"] and self.get_explosion_amount(None, tile["x"] - 32, tile["y"] - 32) > 0:
                        self.Map.set_foreground_tile("empty", math.floor(tile["x"] / 64), math.floor(tile["y"] / 64))

                # Kill the players that are in the explosion range.
                for _, player in self.Players.players.items():
                    if self.get_explosion_amount(player.team, player.x, player.y) > 0:
                        self.Players.players[bomb.owner].score += 2
                        player.score -= 1

                        player.kill(self.Players.get_enemies_position(player.team))

                self.bombs.pop(index)

                # Speed up the countdown of other bombs that are in the explosion range.
                for other_bomb in self.bombs:
                    if math.dist([other_bomb.x, other_bomb.y], [bomb.x, bomb.y]) < self.Level.Rules.bomb_explosion_range:
                        if other_bomb.countdown > math.floor(self.Level.Rules.bomb_countdown / 10):
                            other_bomb.countdown = math.floor(self.Level.Rules.bomb_countdown / 10)
                        else:
                            other_bomb.countdown = -1

                # Spawn the explosion clouds.
                for _ in range(math.floor(self.Level.Rules.bomb_explosion_range / 15)):
                    angle = random.uniform(0, 1) * (2 * math.pi)
                    distance = random.uniform(0, 1) * (self.Level.Rules.bomb_explosion_range / 2)

                    self.explosion_clouds.append(ExplosionCloud(
                        bomb.x + (math.cos(angle) * distance),
                        bomb.y + (math.sin(angle) * distance)
                    ))

        # Update the animation of the explosion clouds.
        for index in reversed(range(len(self.explosion_clouds))):
            explosion_cloud = self.explosion_clouds[index]

            explosion_cloud.animation_frame += 1

            if explosion_cloud.animation_frame > 18:
                self.explosion_clouds.pop(index)
                        

    # Get The Sprites To Render
    def get_sprites(self) -> List[dict]:
        sprites: List[dict] = []

        bomb_size = self.Map.tile_size * 0.75
        explosion_range = ((self.Map.tile_size / 64) * self.Level.Rules.bomb_explosion_range) * 2

        # Draw the tile explosion range.
        for y in range(self.Map.height):
            for x in range(self.Map.width):
                amount = self.get_explosion_amount(None, (x * 64 + 32), (y * 64) + 32)

                for _ in range(amount):
                    sprites.append(self.Map.create_tile_sprite("tile_explosion_range", 2, x, y))

        player_render_size = self.Map.tile_size * 0.9

        # Draw the player explosion range.
        for _, player in self.Players.players.items():
            amount = self.get_explosion_amount(player.team, player.x, player.y)

            for _ in range(amount):
                render_x = self.Map.render_offset_x + ((self.Map.tile_size / 64) * player.x)
                render_y = self.Map.render_offset_y + ((self.Map.tile_size / 64) * player.y)

                if abs(player.angle > 0.001):
                    render_y -= abs(player.angle) * (player_render_size / 1.25)

                sprites.append({
                    "layer": 6,
                    "data": create_image_view_data(
                        "player_explosion_range",
    
                        render_x - (player_render_size / 2),
                        render_y - (player_render_size / 2),
    
                        player_render_size,
                        player_render_size,
    
                        # This should be a float.
                        player.angle
                    )
                })

        # Draw the bombs.
        for bomb in self.bombs:
            render_x = self.Map.render_offset_x + ((self.Map.tile_size / 64) * bomb.x)
            render_y = self.Map.render_offset_y + ((self.Map.tile_size / 64) * bomb.y)

            # Add the sprite for the bomb itself.
            sprites.append({
                "layer": 3,
                "data": create_image_view_data(
                    "bomb" if (round(bomb.countdown / 15) % 2) == 0 else "bomb_flash",
                    
                    render_x - (bomb_size / 2),
                    render_y - (bomb_size / 2),

                    bomb_size,
                    bomb_size
                )
            })

            # Add the sprite for the bomb countdown.
            countdown_render_x = render_x + (bomb_size * 0.02)
            countdown_render_y = render_y + (bomb_size * 0.125)

            points: List[list] = [[countdown_render_x, countdown_render_y]]

            for i in range(int((360 / self.Level.Rules.bomb_countdown) * (self.Level.Rules.bomb_countdown - bomb.countdown))):
                 points.append([
                     countdown_render_x + ((bomb_size * 0.2) * math.cos(math.radians(i - 90))),
                     countdown_render_y + ((bomb_size * 0.2) * math.sin(math.radians(i - 90)))
                 ])

            if (len(points) >= 3):
                sprites.append({
                    "layer": 4,
                    "data": create_polygon_view_data(
                        "bomb_countdown",

                        points,

                        self.Players.TEAM_COLORS[self.Players.players[bomb.owner].team]
                    )
                })

        explosion_cloud_size = self.Map.tile_size * 2

        # Draw the explosion clouds.
        for explosion_cloud in self.explosion_clouds:
            sprites.append({
                "layer": 8,
                "data": create_image_view_data(
                    f"explosion_{math.floor(explosion_cloud.animation_frame / 3) + 1}",

                    self.Map.render_offset_x + (((self.Map.tile_size / 64) * explosion_cloud.x) - (explosion_cloud_size / 2)),
                    self.Map.render_offset_y + (((self.Map.tile_size / 64) * explosion_cloud.y) - (explosion_cloud_size / 2)),

                    explosion_cloud_size,
                    explosion_cloud_size            
                )
            })

        return sprites
