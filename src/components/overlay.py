from mlgame.view.view_model import create_image_view_data, create_text_view_data
from math import cos, sin, radians
from typing import List
import pygame

from ..constants import TEAM_COLORS

# Render the info of the player.
def render_player_info(overlay_render_size: float, name: str, team: int, bomb_amount: int, x: float, y: float) -> List[dict]:
    frame_render_size = overlay_render_size * 3

    font = pygame.font.Font(None, round(overlay_render_size * 0.6))
    font.set_bold(True)

    bomb_amount_text_size = font.size(f"x{bomb_amount}")

    return [
        {
            "layer": 9,
            "data": create_image_view_data(
                "overlay_frame",

                x - (frame_render_size / 2),
                y - (frame_render_size / 2),

                frame_render_size,
                frame_render_size
            )
        },
        {
            "layer": 9,
            "data": create_image_view_data(
                f"icon_player_{team}",

                x - (overlay_render_size * 1.3),
                y - (overlay_render_size * 0.95),

                overlay_render_size * 0.85,
                overlay_render_size * 0.85
            )
        },
        {
            "layer": 9,
            "data": create_text_view_data(
                name,

                x - (overlay_render_size * 0.225),
                y - (overlay_render_size * 0.725),

                TEAM_COLORS[team - 1],
                f'{round(overlay_render_size * 0.65)}px bold Arial'
            )
        },
        {
            "layer": 9,
            "data": create_image_view_data(
                f"icon_bomb_{team}",

                (x + (overlay_render_size * 0.15)) - (bomb_amount_text_size[0] / 2),
                y + (overlay_render_size * 0.075),

                overlay_render_size * 0.55,
                overlay_render_size * 0.55
            )
        },
        {
            "layer": 9,
            "data": create_text_view_data(
                f"x{bomb_amount}",

                (x + (overlay_render_size * 0.75)) - (bomb_amount_text_size[0] / 2),
                y + (overlay_render_size * 0.175),

                TEAM_COLORS[team - 1],
                f'{round(overlay_render_size * 0.6)}px bold Arial'
            )
        },
    ]

# The overlay itself.
class Overlay:
    # Initialize the overlay.
    def __init__(self, window_width: int, window_height: int) -> None:
        self.window_width = window_width
        self.window_height = window_height

        self.overlay_render_height = window_height * 0.6
        self.overlay_render_width = 512 * (self.overlay_render_height / 1124)

        self.overlay_render_size = (self.overlay_render_width + self.overlay_render_height) * 0.075

        return

    # Render the overlay.
    def render(self, players: dict) -> List[dict]:
        left_background_render_x = self.overlay_render_size * 0.5
        left_background_render_y = (self.window_height / 2) - (self.overlay_render_height / 2)
        right_background_render_x = self.window_width - (self.overlay_render_width + (self.overlay_render_size * 0.5))
        right_background_render_y = (self.window_height / 2) - (self.overlay_render_height / 2)

        sprites = [
            {
                "layer": 9,
                "data": create_image_view_data(
                    "overlay_background",

                    left_background_render_x,
                    left_background_render_y,
                
                    self.overlay_render_width,
                    self.overlay_render_height
                )
            },
            {
                "layer": 9,
                "data": create_image_view_data(
                    "overlay_background",

                    right_background_render_x,
                    right_background_render_y,
                    
                    self.overlay_render_width,
                    self.overlay_render_height
                )
            }
        ]

        player_icon_background_width = self.overlay_render_size * 2
        player_icon_background_height = self.overlay_render_size * 0.8

        # Render players' on the left layout.
        if "1P" in players:
            sprites.extend(render_player_info(
                self.overlay_render_size,

                players["1P"].name,
                players["1P"].team,
                players["1P"].bomb_amount,

                left_background_render_x + (self.overlay_render_width / 2),
                left_background_render_y + ((self.overlay_render_height / 2) - (self.overlay_render_height / 5))
            ))
        if "2P" in players:
            sprites.extend(render_player_info(
                self.overlay_render_size,

                players["2P"].name,
                players["2P"].team,
                players["2P"].bomb_amount,

                left_background_render_x + (self.overlay_render_width / 2),
                left_background_render_y + ((self.overlay_render_height / 2) + (self.overlay_render_height / 5))
            ))

        # Render players' on the right layout.
        if "3P" in players:
            sprites.extend(render_player_info(
                self.overlay_render_size,

                players["3P"].name,
                players["3P"].team,
                players["3P"].bomb_amount,

                right_background_render_x + (self.overlay_render_width / 2),
                right_background_render_y + ((self.overlay_render_height / 2) - (self.overlay_render_height / 5))
            ))
        if "4P" in players:
            sprites.extend(render_player_info(
                self.overlay_render_size,

                players["4P"].name,
                players["4P"].team,
                players["4P"].bomb_amount,

                right_background_render_x + (self.overlay_render_width / 2),
                right_background_render_y + ((self.overlay_render_height / 2) + (self.overlay_render_height / 5))
            ))

        return sprites
