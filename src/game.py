from mlgame.game.paia_game import PaiaGame, GameStatus, Scene
from typing import Union
from math import floor
from os import path
import pygame

from .components.background import Background
from .components.overlay import Overlay
from .components.player import Player
from .components.map import Map
from .loader import load_assets
from .level import Level

if not pygame.font.get_init():
    pygame.font.init();

# The game itself.
class Game(PaiaGame):
    # Initialize the game.
    def __init__(self, level_name: str, level_path: Union[None, str], window_width: int = 1480, window_height: int = 740, user_num: int = 1, team_mode: str = "off", game_duration: int = 10):
        super().__init__(user_num = user_num)

        # Find the level in the default level set if "level_path" is not set.
        if level_path == None: 
            # There might be a better way to resolve the path.
            level_path = f"{path.dirname(path.dirname(__file__))}/assets/levels/{level_name}.json"

        self.Level = Level(level_path)

        if user_num > len(self.Level.Map.spawns):
            raise Exception(f"[Level Error] The level only supports up to {len(self.Level.Map.spawns)} players!")

        self.Overlay = Overlay(window_width, window_height);
        self.Map = Map(self.Level, self.Overlay);
        self.Background = Background(self.Map)
        self.Overlay = Overlay(window_width, window_height)

        self.players = {}

        # Initialize the players.
        for index in range(user_num):
            name = f"{str(index + 1)}P"
            spawn = self.Level.Map.spawns[index]

            self.players[name] = Player(self.Map, name, index + 1, (spawn["x"] * 64) + 32, (spawn["y"] * 64) + 32)

        if team_mode == "on":
            if len(self.players) == 3:
                self.players["1P"].team = 1
                self.players["2P"].team = 1
                self.players["3P"].team = 2
            elif len(self.players) == 4:
                self.players["1P"].team = 1
                self.players["2P"].team = 1
                self.players["3P"].team = 2
                self.players["4P"].team = 2

        self.scene = Scene(window_width, window_height)
        self.scene_width = window_width
        self.scene_height = window_height

        self.game_duration = game_duration
        self.frame_count = 0

    # Initialize the scene.
    def get_scene_init_data(self) -> dict:
        return {
            "scene": self.scene.__dict__,

            "assets": load_assets(),
            "background": []
        }

    # Update the game.
    def update(self, commands) -> Union[None, str]:
        self.Background.update()
        self.Map.update()

        tiles = self.Map.get_tiles_with_position()
        bombs = []

        for _, player in self.players.items():
            bombs.extend(player.bombs)

        for player_name, actions in commands.items():
            player = self.players[player_name]

            if actions != None:
                # Make the player move slower when moving diagonally.
                speed = self.Level.Rules.player_speed / 1.4 if (
                    ("move_left" in actions or "move_right" in actions)
                    and ("move_up" in actions or "move_down" in actions)
                ) else self.Level.Rules.player_speed 

                if "move_left" in actions:
                    player.move("left", speed, tiles)
                elif "move_right" in actions:
                    player.move("right", speed, tiles)
                
                if "move_up" in actions:
                    player.move("up", speed, tiles)
                elif "move_down" in actions:
                    player.move("down", speed, tiles)

            player.update([] if actions == None else actions, self.players, bombs)

        self.frame_count += 1

        if self.frame_count >= self.game_duration:
            return "QUITE"


    # Get the scene progress data.
    def get_scene_progress_data(self) -> dict:
        sprites = []

        sprites.extend(self.Map.render())
        sprites.extend(self.Background.render())
        sprites.extend(self.Overlay.render(self.players)) 

        for _, player in self.players.items():
            sprites.extend(player.render())

        # 0: Background
        # 1: Background Tiles
        # 2: Players' Shadow
        # 3: Foreground Tiles
        # 4: Explosion Range
        # 5: Bombs
        # 6: Players
        # 7: Players' Name
        # 8: Explosion Clouds
        # 9: Overlay
 
        sprites.sort(key = lambda sprite : sprite["layer"])

        for i in range(len(sprites)):
            sprites[i] = sprites[i]["data"]

        return {
            "frame": self.frame_count,

            "background": [],
            "foreground": [],

            "object_list": sprites,
            "toggle_with_bias": [],
            "toggle": [],

            "user_info": [],
            "game_sys_info": {}
        }

    # Get the data for the players from the game.
    def get_data_from_game_to_player(self) -> dict:
        data = {}

        tile_matrix = self.Map.get_tile_matrix()

        for name, player in self.players.items():
            enemy_matrix = [0] * (self.Level.Map.width * self.Level.Map.height)
            bomb_matrix = [0] * (self.Level.Map.width * self.Level.Map.height)

            # Generate the enemy matrix.
            for _, enemy in self.players.items():
                if enemy.team != player.team:
                    index = floor(enemy.x / 64) + (floor(enemy.y / 64) * self.Level.Map.width)
    
                    enemy_matrix[index] = enemy_matrix[index] + 1

                    # Generate the bomb matrix.
                    for bomb in enemy.bombs:
                        index = floor(bomb.x / 64) + (floor(bomb.y / 64) * self.Level.Map.width)

                        bomb_matrix[index] = bomb_matrix[index] + 1

            data[name] = {
                "status": GameStatus.GAME_ALIVE,
                "frame": self.frame_count,

                "score": player.score,
                "bomb_amount": player.bomb_amount,
                "bomb_cooldown": player.bomb_cooldown,

                "width": self.Map.width,
                "height": self.Map.height,
                "x": player.x,
                "y": player.y,

                "tile_matrix": tile_matrix,
                "enemy_matrix": enemy_matrix,
                "bomb_matrix": bomb_matrix
            }

        return data
 
    # Get the result of the game.
    def get_game_result(self) -> dict:
        return {}

    # Reset the game.
    def reset(self) -> None:
        return
