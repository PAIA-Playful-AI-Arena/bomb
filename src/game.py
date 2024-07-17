from os import path
import pygame

from mlgame.game.paia_game import GameStatus, PaiaGame
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_asset_init_data

from .render import render
from .objects import *

from .env import *

# The Game Itself
class Bomb(PaiaGame):
    # Initialize The Game
    def __init__(self, width: int = 750, height: int = 500, players: int = 1, *args, **kwargs): # 750 x 500
        super().__init__(user_num=players)

        self.frame_count = 0

        self.width = width
        self.height = height

        # Initialize game objects.

        self.Map = Map()
        self.Bombs = Bombs()

        self.Map.calculate_tile_size(width, height)

        self.Map.set_foreground_tile(1, 1, 'barrel')
        self.Map.set_foreground_tile(1, 2, 'barrel')
        self.Map.set_foreground_tile(2, 1, 'barrel')
        self.Map.set_foreground_tile(2, 2, 'barrel')

        self.Map.set_foreground_tile(4, 1, 'rock')
        self.Map.set_foreground_tile(4, 2, 'rock')

        self.Map.set_foreground_tile(6, 1, 'barrel')
        self.Map.set_foreground_tile(6, 2, 'rock')
        self.Map.set_foreground_tile(7, 1, 'rock')
        self.Map.set_foreground_tile(7, 2, 'barrel')
        self.Map.set_foreground_tile(8, 1, 'barrel')
        self.Map.set_foreground_tile(8, 2, 'rock')

        self.Map.set_foreground_tile(0, 4, 'barrel')
        self.Map.set_foreground_tile(1, 4, 'rock')
        self.Map.set_foreground_tile(2, 4, 'barrel')
        self.Map.set_foreground_tile(3, 4, 'rock')
        self.Map.set_foreground_tile(4, 4, 'barrel')
        self.Map.set_foreground_tile(5, 4, 'rock')
        self.Map.set_foreground_tile(6, 4, 'barrel')
        self.Map.set_foreground_tile(7, 4, 'rock')
        self.Map.set_foreground_tile(8, 4, 'barrel')
        self.Map.set_foreground_tile(9, 4, 'rock')


        # Initialize players data.

        self.players = {}

        for i in range(players):
            id = str(i + 1) + 'P'

            self.players[id] = Player(self.Map, self.Bombs, id)

        self.scene = Scene(width, height, '#211711') 

    # Get Scene Init Data
    def get_scene_init_data(self):
        scene_init_data = {
            "scene": self.scene.__dict__,
            "assets": [
                create_asset_init_data('ground_light', 64, 64, IMAGE_GROUND_LIGHT_PATH, IMAGE_GROUND_LIGHT_URL),
                create_asset_init_data('ground_dark', 64, 64, IMAGE_GROUND_DARK_PATH, IMAGE_GROUND_DARK_URL),

                create_asset_init_data('barrel', 64, 64, IMAGE_BARREL_PATH, IMAGE_BARREL_URL),
                create_asset_init_data('rock', 64, 64, IMAGE_ROCK_PATH, IMAGE_ROCK_URL),

                create_asset_init_data('player', 64, 64, IMAGE_PLAYER_PATH, IMAGE_PLAYER_URL),
                create_asset_init_data('bomb', 64, 64, IMAGE_BOMB_PATH, IMAGE_BOMB_URL),
                create_asset_init_data('bomb_flash', 64, 64, IMAGE_BOMB_FLASH_PATH, IMAGE_BOMB_FLASH_URL),
                create_asset_init_data('explosion_range', 128, 128, IMAGE_EXPLOSION_RANGE_PATH, IMAGE_EXPLOSION_RANGE_URL),
                create_asset_init_data('explosion_1', 64, 64, IMAGE_EXPLOSION_1_PATH, IMAGE_EXPLOSION_1_URL),
                create_asset_init_data('explosion_2', 64, 64, IMAGE_EXPLOSION_2_PATH, IMAGE_EXPLOSION_2_URL),
                create_asset_init_data('explosion_3', 64, 64, IMAGE_EXPLOSION_3_PATH, IMAGE_EXPLOSION_3_URL),
                create_asset_init_data('explosion_4', 64, 64, IMAGE_EXPLOSION_4_PATH, IMAGE_EXPLOSION_4_URL),
                create_asset_init_data('explosion_5', 64, 64, IMAGE_EXPLOSION_5_PATH, IMAGE_EXPLOSION_5_URL),
                create_asset_init_data('explosion_6', 64, 64, IMAGE_EXPLOSION_6_PATH, IMAGE_EXPLOSION_6_URL),
                create_asset_init_data('explosion_7', 64, 64, IMAGE_EXPLOSION_7_PATH, IMAGE_EXPLOSION_7_URL)
            ],
            "background": [
                # create_image_view_data("bg", 0, 0, 1000, 500),
            ]
        }

        return scene_init_data

    # Update The Game
    def update(self, players):
        self.frame_count += 1

        # update game by these commands
        #ai_1p_cmd = commands[self.ai_clients()[0]["name"]]
        #command = (PlatformAction(ai_1p_cmd)
        #           if ai_1p_cmd in PlatformAction.__members__ else PlatformAction.NONE)

        explodedBombs = self.Bombs.update()

        for explodedBomb in explodedBombs:
            self.players[explodedBomb["owner"]].bombs += 1

            self.Map.bomb_exploded(explodedBomb["x"], explodedBomb["y"])

        for id, commands in players.items():
            if (commands != None):
                for id in self.players:
                    self.players[id].calculate_player_size()

                self.players[id].update()

                x = 0
                y = 0

                if 'move_left' in commands:
                    x = -PLAYER_SPEED
                elif 'move_right' in commands:
                    x = PLAYER_SPEED
    
                if 'move_up' in commands:
                    y = -PLAYER_SPEED
                elif 'move_down' in commands:
                    y = PLAYER_SPEED

                self.players[id].move(x, y)

                if 'place_bomb' in commands:
                    self.players[id].place_bomb()

        if not self.is_running:
            return "RESET"

    # Get The Data For The Players
    def get_data_from_game_to_player(self):
        to_players_data = {}

        for ai_client in self.ai_clients():
            player = self.players[ai_client["name"]]

            to_players_data[ai_client["name"]] = {
                "status": GameStatus.GAME_ALIVE,
                "frame": self.frame_count,

                "score": player.score,

                "x": player.x,
                "y": player.y
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
        players = []

        for _, player in self.players.items():
            players.append(player)

        return {
            "frame": self.frame_count,

            "background": [],
            "foreground": [],

            "object_list": render(self.width, self.height, self.Map, self.Bombs, players),
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
