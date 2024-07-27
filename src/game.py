from mlgame.game.paia_game import PaiaGame, GameStatus, Scene
from typing import Union
from os import path

from .objects.players import Players
from .objects.bombs import Bombs
from .objects.map import Map 
from .level import Level

# The Game Itself
class Game(PaiaGame):
    # Initialize The Game
    def __init__(self, level_name: str, level_file: Union[None, str], width: int = 750, height: int = 500, user_num: int = 1, game_duration: int = 1800, team_mode: str = "off", *args, **kwargs):
        super().__init__(user_num = user_num)

        if level_file == None:
            level_file = path.join(path.dirname(__file__), "levels/" + level_name + ".bomb")

        self.Level = Level(level_file)
 
        self.width = width
        self.height = height
        
        self.Map = Map(self.Level, width, height)
        self.Players = Players(self.Level, user_num, team_mode == "on")
        self.Bombs = Bombs(self.Level, self.Map, self.Players)

        self.scene = Scene(self.width, self.height, "#211711")
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

    @staticmethod
    def ai_clients():
        return [
            { "name": "1P" },
            { "name": "2P" }
        ]

    # Update The Game
    def update(self, commands):
        foreground_tiles = self.Map.get_foreground_tiles_with_position()

        self.Map.update()
        self.Players.update(commands, foreground_tiles)
        self.Bombs.update(commands)

        return

    # Get The Data For The Players
    def get_data_from_game_to_player(self):
        to_players_data = {}

        for name, data in self.Players.players_data.items():
            to_players_data[name] = {
                "status": GameStatus.GAME_ALIVE,
                "frame": self.frame_count,

                "team": data["team"],

                "score": data["score"],
                "bombs": data["bombs"],

                "x": data["x"],
                "y": data["y"]
            }

        return to_players_data

    # Get The Scene Progress Data (Render)
    def get_scene_progress_data(self):
        objects_info = []

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

    # Get The Game Status
    def get_game_status(self):
        # TODO return game status

        return GameStatus.GAME_ALIVE

    # Get The Game Result
    def get_game_result(self):
        return {
            "frame_used": self.frame_count,
            "status": self.game_result_state,
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
