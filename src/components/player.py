from mlgame.view.view_model import create_image_view_data, create_text_view_data
from math import cos, sin, radians, dist
from typing_extensions import Self
from typing import List, Dict
import pygame

from ..constants import TEAM_COLORS
from .bomb import Bomb
from .map import Map

# Check if there's collision between multiple rectangles.
def check_collision(rectangle: dict, rectangles: list):
    for rectangle2 in rectangles:
        rectangle_right = rectangle['x'] + rectangle['width']
        rectangle_bottom = rectangle['y'] + rectangle['height']
        rectangle2_right = rectangle2['x'] + rectangle2['width']
        rectangle2_bottom = rectangle2['y'] + rectangle2['height']

        if (rectangle['x'] < rectangle2_right and rectangle2['x'] < rectangle_right) and (rectangle['y'] < rectangle2_bottom and rectangle2['y'] < rectangle_bottom):
            return True

    return False

# Get the offset needed to after rotating the rectangle.
def get_rotation_offset(width: int, height: int, angle: float) -> Dict[str, float]:
    rotated_width = abs(width * cos(angle)) + abs(height * sin(angle))
    rotated_height = abs(width * sin(angle)) + abs(height * cos(angle))

    return {
        "x": -((rotated_width - width) / 2),
        "y": -((rotated_height - height) / 2)
    }

# The ghost itself.
class Ghost:
    # Initialize the ghost.
    def __init__(self, map: Map, team: int, x: float, y: float, facing: str, bomb: bool, bomb_x: int, bomb_y: int) -> None:
        self.Map = map

        self.team = team

        self.facing = facing

        self.x = x
        self.y = y
        self.dy = map.tile_render_size * -0.2

        self.bomb = bomb
        self.bomb_x = bomb_x
        self.bomb_y = bomb_y
        self.bomb_dy = map.tile_render_size * -0.2

        self.player_render_size = map.tile_render_size * 1.1
        self.bomb_render_size = map.tile_render_size * 0.35

    # Update the ghost.
    def update(self) -> bool:
        self.x += (-1 if self.facing == 'right' else 1) * (self.player_render_size * 0.05)
        self.y += self.dy
        self.dy += self.player_render_size * 0.02

        self.bomb_x += (-1 if self.facing == 'right' else 1) * (self.player_render_size * 0.075)
        self.bomb_y += self.bomb_dy
        self.bomb_dy += self.bomb_render_size * 0.04 

        return (self.Map.target_render_offset_y + ((self.Map.tile_render_size / 64) * self.y)) - (self.player_render_size / 2) > self.Map.window_height and self.bomb_y - (self.bomb_render_size / 2) > self.Map.window_height

    # Render the ghost.
    def render(self) -> List[dict]:
        player_render_x = self.Map.target_render_offset_x + ((self.Map.tile_render_size / 64) * self.x)
        player_render_y = self.Map.target_render_offset_y + ((self.Map.tile_render_size / 64) * self.y)

        # Render the ghost itself.
        sprites = [{
            "layer": 6,
            "data": create_image_view_data(
                f"ghost_{self.team}_{self.facing}",

                player_render_x - (self.player_render_size / 2),
                player_render_y - (self.player_render_size / 2),

                self.player_render_size,
                self.player_render_size,
            )
        }]

        # Render the bomb the player was holding if available.
        if self.bomb:
            sprites.append({
                "layer": 6,
                "data": create_image_view_data(
                    f"bomb_{self.team}",

                    self.bomb_x - (self.bomb_render_size / 2),
                    self.bomb_y - (self.bomb_render_size / 2),

                    self.bomb_render_size,
                    self.bomb_render_size
                )
            })

        return sprites

# The player itself.
class Player:
    PLAYER_HITBOX_WIDTH: int = 50
    PLAYER_HITBOX_HEIGHT: int = 60

    # Initialize the player.
    def __init__(self, map: Map, name: str, team: int, x: int, y: int) -> None:
        self.Level = map.Level
        self.Map = map

        self.name = name
        self.team = team
        self.score = 0

        self.x = x
        self.y = y
        self.facing = 'right'
        self.ghosts = []

        self.bomb_amount = self.Level.Rules.player_bombs
        self.bomb_cooldown = 0
        self.bomb_size = 1
        self.bombs = []

        self.rotate_speed = -self.Level.Rules.player_speed / 33.3
        self.target_angle = 0
        self.angle = 0 

        self.flash = 0

        self.player_render_size = map.tile_render_size * 1.1
        self.bomb_render_size = map.tile_render_size * 0.35

    # Move the player.
    def move(self, direction: str, speed: int, tiles: List[dict]):
        match direction:
            case 'left':
                self.x -= speed
                self.facing = 'left'
            case 'right':
                self.x += speed
                self.facing = 'right'
            case 'up':
                self.y -= speed
            case 'down':
                self.y += speed

        # Check the collision with the tiles.
        for tile in tiles:
            if check_collision({
                "x": self.x - (self.PLAYER_HITBOX_WIDTH / 2), "y": (self.y + 32) - self.PLAYER_HITBOX_HEIGHT,
                "width": self.PLAYER_HITBOX_WIDTH, "height": self.PLAYER_HITBOX_HEIGHT
            }, [{ "x": tile["x"], "y": tile["y"], "width": 64, "height": 64 }]):
                # Fix the position of the player.
                match direction:
                    case 'left':
                        self.x = (tile["x"] + 64) + (self.PLAYER_HITBOX_WIDTH / 2)
                    case 'right':
                        self.x = tile["x"] - (self.PLAYER_HITBOX_WIDTH / 2)
                    case 'up':
                        self.y = (tile["y"] + 64) - (32 - self.PLAYER_HITBOX_HEIGHT)
                    case 'down':
                        self.y = tile["y"] - 32

                return

        # Check the collsion with the map edges.
        if check_collision({
            "x": self.x - (self.PLAYER_HITBOX_WIDTH / 2), "y": (self.y + 32) - self.PLAYER_HITBOX_HEIGHT,
            "width": self.PLAYER_HITBOX_WIDTH, "height": self.PLAYER_HITBOX_HEIGHT
        }, [
            # The edges is also represented as multiple reacts.
            { "x": -100, "y": 0, "width": 100, "height": self.Map.height * 64 },
            { "x": self.Map.width * 64, "y": 0, "width": 100, "height": self.Map.height * 64 },
            { "x": 0, "y": -100, "width": self.Map.width * 64, "height": 100 },
            { "x": 0, "y": self.Map.height * 64, "width": self.Map.width * 64, "height": 100 }
        ]):
            # Fix the position of the player.
            if direction == "left":
                self.x = self.PLAYER_HITBOX_WIDTH / 2
            elif direction == "right":
                self.x = (self.Map.width * 64) - (self.PLAYER_HITBOX_WIDTH / 2)
            elif direction == "up":
                self.y = self.PLAYER_HITBOX_HEIGHT - 32
            elif direction == "down":
                self.y = (self.Map.height * 64) - 32
 
    # Kill the player.
    def kill(self, bombs: List[Bomb]) -> None:
        bomb_render_position = self.get_bomb_render_position()

        # Initialize the player death animation.
        self.ghosts.append(Ghost(self.Map, self.team, self.x, self.y, self.facing, self.bomb_amount > 0, bomb_render_position["x"], bomb_render_position["y"]))

        spawns = []

        # Find a spawn that is the farthest in average from the enemy.
        for index in range(len(self.Level.Map.spawns)):
            spawn = self.Level.Map.spawns[index]
            total_distance: float = 0

            for bomb in bombs:
                if bomb.team != self.team and bomb.countdown >= 0:
                    total_distance += dist([spawn["x"] * 64, spawn["y"] * 64], [bomb.x, bomb.y])

            spawns.append({ "index": index, "total_distance": total_distance })

        spawns.sort(key = lambda spawn : spawn["total_distance"], reverse = True)

        self.x = (self.Level.Map.spawns[spawns[0]["index"]]["x"] * 64) + 32
        self.y = (self.Level.Map.spawns[spawns[0]["index"]]["y"] * 64) + 32

        # Play the player flashing animation.
        self.flash = 6

    # Update the player.
    def update(self, actions: List[str], players: Dict[str, Self], bombs: List[Bomb]) -> None:
        if "move_left" in actions or "move_right" in actions or "move_up" in actions or "move_down" in actions:
            # Play the walking animation when the player is moving.
            if self.rotate_speed == 0:
                if "move_left" in actions or "move_down" in actions:
                    self.rotate_speed = self.Level.Rules.player_speed * 1.4
                else:
                    self.rotate_speed = -self.Level.Rules.player_speed * 1.4
    
            self.target_angle += self.rotate_speed
    
            if self.target_angle > 10:
                self.target_angle = 10
                self.rotate_speed = -self.rotate_speed
            elif self.target_angle < -10:
                self.target_angle = -10
                self.rotate_speed = -self.rotate_speed
        else:
            # Reset the walking animation when the player stops moving.
            self.target_angle = 0
            self.rotate_speed = 0
 
        self.angle += (self.target_angle - self.angle) * 0.5
        self.bomb_size += (1 - self.bomb_size) * 0.35

        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1
        elif "place_bomb" in actions:
            if self.bomb_amount > 0:
                self.bomb_amount -= 1
                self.bomb_cooldown = 5
                self.bomb_size = 0.75
 
                self.bombs.append(Bomb(self.Map, self.team, self.x, self.y)) 

        # Update the bomb the player has placed.
        for index in reversed(range(len(self.bombs))):
            bomb = self.bombs[index]
            bomb_state = bomb.update()

            if (bomb_state == "explode"):
                self.bomb_amount += 1
                self.bomb_size = 1.25

                bomb.destory_tiles()

                for _, player in players.items():
                    if player.team != self.team and dist([player.x, player.y], [bomb.x, bomb.y]) <= self.Level.Rules.bomb_explosion_range:
                        player.score -= 1
                        player.kill(bombs)

                        self.score += 2

                    # Activate the bombs around the exploded bomb.
                    for other_bomb in player.bombs:
                        if other_bomb.countdown > 0 and bomb != other_bomb:
                            distance = dist([bomb.x, bomb.y], [other_bomb.x, other_bomb.y])

                            if (dist([bomb.x, bomb.y], [other_bomb.x, other_bomb.y]) < self.Level.Rules.bomb_explosion_range):
                                if other_bomb.countdown > self.Level.Rules.bomb_countdown / 10:
                                    other_bomb.countdown = self.Level.Rules.bomb_countdown / 10
                                else:
                                    other_bomb.countdown = 0

            elif bomb_state == "delete":
                self.bombs.pop(index) 

        # Update the dead players.
        for index in reversed(range(len(self.ghosts))):
            ghost = self.ghosts[index]

            if ghost.update():
                self.ghosts.pop(index)

        # Update the flash animation.
        if self.flash > 0:
            self.flash -= 0.1

    # Render the player.
    def render(self) -> List[dict]:
        player_render_x = self.Map.render_offset_x + ((self.Map.tile_render_size / 64) * self.x)
        player_render_y = self.Map.render_offset_y + ((self.Map.tile_render_size / 64) * self.y)

        rotation_offset = get_rotation_offset(self.player_render_size, self.player_render_size, radians(self.angle))

        player_render_rotated_x = player_render_x + rotation_offset["x"]
        player_render_rotated_y = player_render_y + rotation_offset["y"]

        # Render the player itself.
        sprites = [{
            "layer": 6,
            "data": create_image_view_data(
                f"player_{self.team}_{self.facing}",

                player_render_rotated_x - (self.player_render_size / 2),
                player_render_rotated_y - (self.player_render_size / 2),

                self.player_render_size,
                self.player_render_size,

                # This should be a float.
                radians(self.angle)
            )
        }]

        font = pygame.font.Font(None, round(self.player_render_size * 0.4))
        font.set_bold(True)

        player_name_text_size = font.size(self.name)

        # Render the name of the player.
        sprites.append({
            "layer": 6,
            "data": create_text_view_data(
                self.name,

                (player_render_x - (player_name_text_size[0] / 2)),
                (player_render_y - (self.player_render_size / 2)) - (player_name_text_size[1] * 1.2),

                TEAM_COLORS[self.team - 1], 
                f'{round(self.player_render_size * 0.4)}px bold Arial'
            )
        })

        # Render the player flash.
        if round(self.flash) > 0 and (round(self.flash) % 2) == 0:
            sprites.append({
                "layer": 6,
                "data": create_image_view_data(
                    f"player_flash_{self.facing}",

                    player_render_rotated_x - (self.player_render_size / 2),
                    player_render_rotated_y - (self.player_render_size / 2),

                    self.player_render_size,
                    self.player_render_size,

                    # This should be a float.
                    radians(self.angle)
            )
        })

        # Render the shadow of the player.
        sprites.append({
            "layer": 2,
            "data": create_image_view_data(
                "player_shadow",

                player_render_x - (self.player_render_size / 2),
                (player_render_y - (self.player_render_size / 2)) + (self.player_render_size * 0.4),

                self.player_render_size,
                self.player_render_size,
            )
        })

        # Render the bomb the player is holding if available.
        if self.bomb_amount > 0:
            bomb_render_position = self.get_bomb_render_position()

            sprites.append({
                "layer": 6,
                "data": create_image_view_data(
                    f"bomb_{self.team}",

                    bomb_render_position["x"] - (bomb_render_position["size"] / 2),
                    bomb_render_position["y"] - (bomb_render_position["size"] / 2),

                    bomb_render_position["size"],
                    bomb_render_position["size"],

                    radians(self.angle)
                )
            })

        # Render the bombs the player has placed.
        for bomb in self.bombs:
            sprites.extend(bomb.render())

        # Render the ghosts.
        for ghost in self.ghosts:
            sprites.extend(ghost.render())

        return sprites

    # Get the render position of the bomb the player is holding.
    def get_bomb_render_position(self):
        player_render_x = self.Map.render_offset_x + ((self.Map.tile_render_size / 64) * self.x)
        player_render_y = self.Map.render_offset_y + ((self.Map.tile_render_size / 64) * self.y)

        bomb_render_size = self.bomb_render_size * self.bomb_size
        bomb_render_angle = self.angle + 110 if self.facing == 'right' else self.angle - 110

        rotation_offset = get_rotation_offset(bomb_render_size, bomb_render_size, radians(self.angle))

        return {
            "x": (player_render_x + ((self.player_render_size * 0.61) * sin(radians(bomb_render_angle)))) + rotation_offset["x"],
            "y": (player_render_y + ((self.player_render_size * 0.61) * cos(radians(bomb_render_angle)))) + rotation_offset["y"],
            "size": bomb_render_size
        } 
