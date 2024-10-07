from mlgame.view.view_model import create_image_view_data, create_text_view_data
from typing import List, Dict
import pygame
import math

from ..level import Level
from .map import Map

# Check If There's Collision Between Multiple Reacts
def check_collision(rect1: dict, rects: list):
    for rect2 in rects:
        rect1_right = rect1['x'] + rect1['width']
        rect1_bottom = rect1['y'] + rect1['height']
        rect2_right = rect2['x'] + rect2['width']
        rect2_bottom = rect2['y'] + rect2['height']

        if (rect1['x'] < rect2_right and rect2['x'] < rect1_right) and (rect1['y'] < rect2_bottom and rect2['y'] < rect1_bottom):
            return True

    return False

# Player
class Player:
    PLAYER_HITBOX_WIDTH: int = 50
    PLAYER_HITBOX_HEIGHT: int = 60

    # Initialize The Player
    def __init__(self, level: Level, map: Map, team: int) -> None:
        self.Level = level
        self.Map = map

        self.team = team
        self.score: int = 0

        self.bombs = level.Rules.player_bombs
        self.place_bomb_cooldown: int = 0

        self.x: float = 0
        self.y: float = 0

        self.rotate_speed = -level.Rules.player_speed / 33.3
        self.target_angle: float = 0
        self.angle: float = 0

        self.flash: float = 0

    # Move The Player
    def move(self, direction: str, speed: float, foreground_tiles: List[dict]) -> None:
        match direction:
            case 'left':
                self.x -= speed
            case 'right':
                self.x += speed 
            case 'up':
                self.y -= speed
            case 'down':
                self.y += speed

        # Check the collision with the foreground tiles.
        for tile in foreground_tiles:
            if check_collision({
                "x": self.x - (self.PLAYER_HITBOX_WIDTH / 2), "y": (self.y + 32) - self.PLAYER_HITBOX_HEIGHT,
                "width": self.PLAYER_HITBOX_WIDTH, "height": self.PLAYER_HITBOX_HEIGHT
            }, [{ "x": tile["x"], "y": tile["y"], "width": 64, "height": 64 }]):
                # Fix the player position.
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
            # Fix the player position.
            if direction == "left":
                self.x = self.PLAYER_HITBOX_WIDTH / 2
            elif direction == "right":
                self.x = (self.Map.width * 64) - (self.PLAYER_HITBOX_WIDTH / 2)
            elif direction == "up":
                self.y = self.PLAYER_HITBOX_HEIGHT - 32
            elif direction == "down":
                self.y = (self.Map.height * 64) - 32
    # Kill The Player
    def kill(self, enemies_position: List[dict]) -> None:
        spawns = []

        for index in range(len(self.Level.Map.spawns)):
            spawn = self.Level.Map.spawns[index]
            distance: float = 0

            for position in enemies_position:
                distance += math.dist([spawn["x"] * 64, spawn["y"] * 64], [position["x"], position["y"]])

            spawns.append({ "index": index, "distance": distance })

        spawns.sort(key = lambda spawn : spawn["distance"], reverse = True)

        self.x = (self.Level.Map.spawns[spawns[0]["index"]]["x"] * 64) + 32
        self.y = (self.Level.Map.spawns[spawns[0]["index"]]["y"] * 64) + 32

# The Players Component
class Players:
    TEAM_COLORS: List[str] = ["#3996E8", "#E93850", "#E9D738", "#38E849"]
    TEAM_BOMB_ICONS: List[str] = ["bomb_icon_blue", "bomb_icon_red", "bomb_icon_yellow", "bomb_icon_green"]

    # Initialize The Component
    def __init__(self, level: Level, map: Map, amount: int, team_mode: bool) -> None:
        if amount > len(level.Map.spawns):
            raise Exception(f"Error: Player amount out of bounds: {amount} (Max {len(level.Map.spawns)})")

        self.Level = level
        self.Map = map
        self.players: Dict[str, Player] = {}

        for index in range(amount):
            name = str(index + 1) + "P"
            spawn = self.Level.Map.spawns[index]

            self.players[name] = Player(level, map, index)
            self.players[name].x = (spawn["x"] * 64) + 32
            self.players[name].y = (spawn["y"] * 64) + 32

        if team_mode:
            if amount == 3:
                self.players["1P"].team = 0
                self.players["2P"].team = 0
                self.players["3P"].team = 1
            elif amount == 4:
                self.players["1P"].team = 0
                self.players["2P"].team = 0
                self.players["3P"].team = 1
                self.players["4P"].team = 1

        self.target_teams_score: Dict[int, int] = {}
        self.teams_score: Dict[int, float] = {}

        # Initialize the teams' score.
        for _, player in self.players.items():
            if player.team not in self.target_teams_score:
                self.target_teams_score[player.team] = 0
                self.teams_score[player.team] = 0

    # Get Enemies Position
    def get_enemies_position(self, team: int) -> List[dict]:
        positions: List[dict] = []

        for _, player in self.players.items():
            if player.team != team:
                positions.append({ "x": player.x, "y": player.y })

        return positions

    # Get A Matrix Of The Enemies
    def get_enemy_matrix(self, team: int) -> List[int]:
        matrix: List[int] = [0] * (self.Level.Map.width * self.Level.Map.height)

        for position in self.get_enemies_position(team):
            index = math.floor(position["x"] / 64) + (math.floor(position["y"] / 64) * self.Level.Map.width)

            matrix[index] = matrix[index] + 1

        return matrix

    # Update The Players
    def update(self, commands: dict) -> None:
        foreground_tiles = self.Map.get_foreground_tiles_with_position()

        # Move The Players
        for player_name, actions in commands.items():
            if actions != None:
                # Make the player move slower when moving diagonally.
                speed = self.Level.Rules.player_speed / 1.4 if (
                    ("move_left" in actions or "move_right" in actions)
                    and ("move_up" in actions or "move_down" in actions)
                ) else self.Level.Rules.player_speed

                player = self.players[player_name]

                if "move_left" in actions:
                    player.move("left", speed, foreground_tiles)
                elif "move_right" in actions:
                    player.move("right", speed, foreground_tiles)
                
                if "move_up" in actions:
                    player.move("up", speed, foreground_tiles)
                elif "move_down" in actions:
                    player.move("down", speed, foreground_tiles)

                # Player the walking animation if the player is moving.
                if "move_left" in actions or "move_right" in actions or "move_up" in actions or "move_down" in actions:
                    if player.rotate_speed == 0:
                        if "move_left" in actions or "move_down" in actions:
                            player.rotate_speed = self.Level.Rules.player_speed / 33.33333
                        else:
                            player.rotate_speed = -self.Level.Rules.player_speed / 33.33333
        
                    player.target_angle += player.rotate_speed
        
                    if player.target_angle > 0.5:
                        player.target_angle = 0.5
                        player.rotate_speed = -player.rotate_speed
                    elif player.target_angle < -0.5:
                        player.target_angle = -0.5
                        player.rotate_speed = -player.rotate_speed
                else:
                    # Reset the walking animation when the player stops moving.
                    player.target_angle = 0
                    player.rotate_speed = 0

        for _, player in self.players.items():
            # Update the cool down for placing bombs.
            if player.place_bomb_cooldown > 0:
                player.place_bomb_cooldown -= 1
            
            # Update the walking animation.
            player.angle += (player.target_angle - player.angle) / 1.5

        # Update the teams' score.
        for team, _ in self.target_teams_score.items():
            self.target_teams_score[team] = 0

        for _, player in self.players.items():
            self.target_teams_score[player.team] += player.score

        for team, _ in self.target_teams_score.items():
            self.teams_score[team] += (self.target_teams_score[team] - self.teams_score[team]) / 10

    # Get The Sprites To Render
    def get_sprites(self) -> List[dict]:
        sprites: List[dict] = []

        player_render_size = self.Map.tile_size * 0.9

        font = pygame.font.Font(None, round(self.Map.tile_size * 0.5))
        font.set_bold(True)

        for name, player in self.players.items():
            render_x = self.Map.render_offset_x + ((self.Map.tile_size / 64) * player.x)
            render_y = self.Map.render_offset_y + ((self.Map.tile_size / 64) * player.y)

            if abs(player.angle > 0.001):
                render_y -= abs(player.angle) * (player_render_size / 1.25)

            # Add the sprite for the player itself.
            sprites.append({
                "layer": 5,
                "data": create_image_view_data(
                    "player" if (round(player.flash) % 2) == 0 else "player_flash",

                    render_x - (player_render_size / 2),
                    render_y - (player_render_size / 2),

                    player_render_size,
                    player_render_size,

                    # This should be a float.
                    player.angle
                )
            })

            size = font.size(name)

            # Add the sprite for the player name.
            sprites.append({
                "layer": 7,
                "data": create_text_view_data(
                    name,

                    round(self.Map.render_offset_x + (((self.Map.tile_size / 64) * player.x) - (size[0] / 2))),
                    round((self.Map.render_offset_y + (((self.Map.tile_size / 64) * player.y) - (player_render_size * 0.9))) - (abs(player.angle) * (player_render_size / 5))),

                    self.TEAM_COLORS[player.team],
                    str(round(self.Map.tile_size * 0.5)) + 'px Bold'
                )
            })

        return sprites
