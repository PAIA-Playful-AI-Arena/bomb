
import pygame

from mlgame.game.paia_game import GameStatus, GameResultState, PaiaGame
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import create_text_view_data, Scene, create_scene_progress_data, create_asset_init_data, \
    create_image_view_data
from .env import *

class Game(PaiaGame):
    def __init__(self, user_num=1,*args, **kwargs):
        super().__init__(user_num=user_num)
        self.frame_count = 0


    def update(self, commands):
        # update game by these commands
        ai_1p_cmd = commands[self.ai_clients()[0]["name"]]
        command = (PlatformAction(ai_1p_cmd)
                   if ai_1p_cmd in PlatformAction.__members__ else PlatformAction.NONE)

        if not self.is_running:
            return "RESET"


    def get_data_from_game_to_player(self):
        """
        return data to each ai 
        """
        to_players_data = {}
        data_to_1p = {
            "frame": self.frame_count,
            "status": self.get_game_status(),
            # TODO add other information

        }
        for ai_client in self.ai_clients():
            to_players_data[ai_client['name']] = data_to_1p

        return to_players_data


    def get_game_status(self):
        # TODO return game status 
        return GameStatus.GAME_ALIVE

    def reset(self):
        # TODO reset the game
        pass

    @property
    def is_running(self):
        return self.get_game_status() == GameStatus.GAME_ALIVE

    def get_scene_init_data(self):
        # TODO return scene_init data to load image in beginning
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

    @check_game_progress
    def get_scene_progress_data(self):
        # TODO generate scene progress data to draw on screen  
        scene_progress = []
        return scene_progress

    @check_game_result
    def get_game_result(self):
        if self._game_status == GameStatus.GAME_PASS:
            self.game_result_state = GameResultState.PASSED
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
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [
            {"name": "1P"}
        ]
