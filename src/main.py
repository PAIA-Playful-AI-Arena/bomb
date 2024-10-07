from mlgame.game.paia_game import PaiaGame, GameStatus, Scene
from typing import Union, List
from os import path

from .components.players import Players
from .components.overlay import Overlay
from .components.bombs import Bombs
from .components.map import Map
from .loader import get_assets
from .level import Level

# The Game Itself
class Game(PaiaGame):
    # Initialize The Game
    def __init__(self, level_name: str, level_path: Union[None, str], width: int = 750, height: int = 500, user_num: int = 1, team_mode: str = "off", game_duration: int = 10) -> None:
        super().__init__(user_num = user_num)

        # Find the level in the default level set if "level_path" is not set.
        if level_path == None:
            level_path = path.join(path.dirname(__file__), "levels/" + level_name + ".json")

        self.width = width
        self.height = height

        self.Level = Level(level_path)
        self.Map = Map(self.Level, width, height)
        self.Players = Players(self.Level, self.Map, user_num, team_mode == "on")
        self.Bombs = Bombs(self.Level, self.Map, self.Players)
        self.Overlay = Overlay(self.Players)

        self.scene = Scene(width, height, "#211711")
        self.game_duration = game_duration
        self.frame_count: int = 0

    # Initialize The Scene
    def get_scene_init_data(self) -> dict:
        return {
            "scene": self.scene.__dict__,

            "assets": get_assets(),
            "background": []
        }

    # Update The Game
    def update(self, commands) -> Union[None, str]:
        self.Map.update()
        self.Players.update(commands)
        self.Bombs.update()

        for player_name, actions in commands.items():
            if actions != None:
                if "place_bomb" in actions:
                    player = self.Players.players[player_name]

                    if player.bombs > 0 and player.place_bomb_cooldown == 0:
                        player.bombs -= 1
                        player.place_bomb_cooldown = 5

                        self.Bombs.spawn_bomb(player_name)

        self.frame_count += 1

        if self.frame_count >= self.game_duration:
            return "QUIT"

    # Get The Data For The Players
    def get_data_from_game_to_player(self) -> dict:
        data: dict = {}

        tile_matrix = self.Map.get_foreground_tile_matrix()

        for name, player in self.Players.players.items():
            data[name] = {
                "status": GameStatus.GAME_ALIVE,
                "frame": self.frame_count,

                "score": player.score,
                "bombs": player.bombs,
                "place_bomb_cooldown": player.place_bomb_cooldown,

                "width": self.Map.width,
                "height": self.Map.height,
                "x": player.x,
                "y": player.y,

                "tile_matrix": tile_matrix,
                "player_matrix": self.Players.get_enemy_matrix(player.team),
                "bomb_matrix": self.Bombs.get_enemy_bomb_matrix(player.team)
            }

        return data

    # Get The Scene Progress Data
    def get_scene_progress_data(self) -> dict:
        sprites: List[dict] = []

        sprites.extend(self.Map.get_sprites())
        sprites.extend(self.Players.get_sprites())
        sprites.extend(self.Bombs.get_sprites())
        sprites.extend(self.Overlay.get_sprites(self.width, self.height, self.game_duration, self.frame_count))

        # 0: Background Tile
        # 1: Foreground Tile
        # 2: Tile Explosion Range
        # 3: Bomb
        # 4: Bomb Countdown
        # 5: Player
        # 6: Player Explosion Range
        # 7: Player Name
        # 8: Explosion Cloud
        # 99: Overlay
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

    # Get The Result Of The Game
    def get_game_result(self) -> dict:
        return {
            "frame_used": self.frame_count,
            "status": GameStatus.GAME_ALIVE if self.frame_count < self.game_duration else GameStatus.GAME_OVER,
            "attachment": [
                {
                    "player_num": "1P"
                }
            ]
        }

    # Reset The Game
    def reset(self) -> None:
        return
