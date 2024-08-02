from mlgame.game.paia_game import PaiaGame, GameStatus, Scene
from typing import Union
from os import path

from .objects.players import Players
from .objects.bombs import Bombs
from .objects.time import Time
from .objects.map import Map 
from .level import Level

# The Game Itself
class Game(PaiaGame):
    # Initialize The Game
    def __init__(self, level_name: str, level_file: Union[None, str], width: int = 750, height: int = 500, user_num: int = 1, game_duration: int = 10, team_mode: str = "off", *args, **kwargs):
        super().__init__(user_num = user_num)

        if level_file == None:
            level_file = path.join(path.dirname(__file__), "levels/" + level_name + ".bomb")

        self.Level = Level(level_file)
 
        self.width = width
        self.height = height

        self.Time = Time()
        self.Map = Map(self.Level, width, height)
        self.Players = Players(self.Level, user_num, team_mode == "on")
        self.Bombs = Bombs(self.Level, self.Map, self.Players)

        self.scene = Scene(self.width, self.height, "#211711")
        self.game_duration = game_duration
        self.frame_count = 0

    # Initialize The Scene
    def get_scene_init_data(self):
        assets = []

        self.Map.add_assets(assets)
        self.Players.add_assets(assets)
        self.Bombs.add_assets(assets)

        scene_init_data = {
            "scene": self.scene.__dict__,

            "assets": assets,
            "background": []
        }

        return scene_init_data

    # Update The Game
    def update(self, commands):
        foreground_tiles = self.Map.get_foreground_tiles_with_position()

        if self.frame_count < self.game_duration:
            self.Map.update()
            self.Players.update(commands, foreground_tiles)
            self.Bombs.update(commands)

            self.frame_count += 1

    # Get The Data For The Players
    def get_data_from_game_to_player(self):
        to_players_data = {}

        winning_team = self.Players.get_winning_team()

        tiles_matrix = self.Map.get_matrix()

        for player_name, player_data in self.Players.players_data.items():
            status = GameStatus.GAME_ALIVE

            if self.frame_count >= self.game_duration:
                if player_data["team"] == winning_team:
                    status = GameStatus.GAME_PASS
                else:
                    status = GameStatus.GAME_OVER

            to_players_data[player_name] = {
                "status": status,
                "frame": self.frame_count,

                "team": player_data["team"],
                "score": player_data["score"],
                "bombs": player_data["bombs"],

                "x": player_data["x"],
                "y": player_data["y"],

                "tiles_matrix": tiles_matrix,
                "players_matrix": self.Players.get_matrix(player_data["team"]),
                "bombs_matrix": self.Bombs.get_matrix(player_data["team"])
            }

        return to_players_data


    # Get The Scene Progress Data (Render)
    def get_scene_progress_data(self):
        objects_info = []

        self.Time.render(self.width, self.height, objects_info, self.game_duration, self.frame_count)
        self.Map.render(objects_info)
        self.Players.render(self.width, self.height, objects_info, self.Map.render_offset_x, self.Map.render_offset_y, self.Map.tile_size)
        self.Bombs.render(objects_info, self.Map.render_offset_x, self.Map.render_offset_y, self.Map.tile_size)

        objects_info.sort(key = sort_objects)

        sorted_objects = []

        for object_info in objects_info:
            sorted_objects.append(object_info["object"])

        return {
            "frame": self.frame_count,

            "background": [],
            "foreground": [],

            "object_list": sorted_objects,
            "toggle_with_bias": [],
            "toggle": [],

            "user_info": [],
            "game_sys_info": {}
        }

    # Get The Game Result
    def get_game_result(self):
        print(True)

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
    def reset(self):
        return

# Sort Objects
def sort_objects (item: dict):
    return item["layer"]
