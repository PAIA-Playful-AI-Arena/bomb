import pygame

from mlgame.game.paia_game import GameStatus, GameResultState, PaiaGame
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene

from .objects import *

from .env import *

# The Game Itself
class Bomb(PaiaGame):
    # Initialize The Game
    def __init__(self, width:int = 750, height:int = 500, players: int = 1, *args, **kwargs):
        super().__init__(user_num=players)

        self.frame_count = 0
        self.width = width
        self.height = height

        # Initialize game objects.

        self.Map = Map()

        # Initialize players data.

        self.players_data = {}

        for i in range(players):
            self.players_data[str(i + 1) + 'P'] = { "score": 0, "x": 0, "y": 0 }

        self.scene = Scene(width, height, '#000000')

    # Get Scene Init Data
    def get_scene_init_data(self):
        scene_init_data = {
            "scene": self.scene.__dict__,
            "assets": [
                # create_asset_init_data("brick", 25, 10, BRICK_PATH, BRICK_URL),
            ],
            "background": [
                # create_image_view_data("bg", 0, 0, 1000, 500),
            ]
        }

        return scene_init_data

    # Update The Game
    def update(self, commands):
        # update game by these commands
        #ai_1p_cmd = commands[self.ai_clients()[0]["name"]z]
        #command = (PlatformAction(ai_1p_cmd)
        #           if ai_1p_cmd in PlatformAction.__members__ else PlatformAction.NONE)

        if not self.is_running:
            return "RESET"

    # Get The Data For The Players
    def get_data_from_game_to_player(self):
        to_players_data = {}

        #data_to_1p = {
        #    "frame": self.frame_count,
        #    "status": self.get_game_status()
        #}

        for ai_client in self.ai_clients():
            player_data = self.players_data[ai_client["name"]]

            print(player_data)

            to_players_data[ai_client["name"]] = {
                "status": None,
                "frame": self.frame_count,

                "score": player_data["score"],

                "x": player_data["x"],
                "y": player_data["y"]
            }

        return to_players_data

    # Get The Game Status
    def get_game_status(self):
        # TODO return game status

        return GameStatus.GAME_ALIVE

    # Reset The Game
    def reset(self):
        # TODO reset the game

        pass

    @property
    def is_running(self):
        return self.get_game_status() == GameStatus.GAME_ALIVE

    @check_game_progress
    def get_scene_progress_data(self) -> dict:
        object_list = []

        self.Map.render(self.width, self.height, object_list)

        return {
            "frame": self.frame_count,

            "background": [],
            "foreground": [],

            "object_list": object_list,
            "toggle_with_bias": [],
            "toggle": [],

            "user_info": [],
            "game_sys_info": {}
        }

    @check_game_result
    def get_game_result(self):
        #if self._game_status == GameStatus.GAME_PASS:
        #    self.game_result_state = GameResultState.PASSED

        return {
            "frame_used": self.frame_count,
            "status": self.game_result_state,
            "attachment": [
                {
                    "player_num": self.ai_clients()[0]['name'],
                    "rank": 1,
                    # TODO add other information

                }
            ]

        }

    def get_keyboard_command(self):
        cmd_1p = "NONE"
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_a]:
            cmd_1p = "SERVE_TO_LEFT"
        elif key_pressed_list[pygame.K_d]:
            cmd_1p = "SERVE_TO_RIGHT"
        elif key_pressed_list[pygame.K_LEFT]:
            cmd_1p = "MOVE_LEFT"
        elif key_pressed_list[pygame.K_RIGHT]:
            cmd_1p = "MOVE_RIGHT"
        else:
            cmd_1p = "NONE"

        ai_1p = self.ai_clients()[0]["name"]

        return {ai_1p: cmd_1p}

    @staticmethod
    def ai_clients():
        return [
            { "name": "1P" }
        ]
