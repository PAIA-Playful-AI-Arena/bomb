from mlgame.view.view_model import create_rect_view_data, create_text_view_data, create_image_view_data

from typing import List
import math

from .players import Players

# Overlay
class Overlay:
    # Initialize The Component
    def __init__(self, players: Players) -> None:
        self.Players = players

    # Get The Sprites To Render
    def get_sprites(self, width: int, height: int, game_duration: int, frame_count: int) -> List[dict]:
        sprites: List[dict] = []

        overlay_size = (width + height) / 100
        
        total_score: float = 0
        score_bar_x: int = 0

        # Sum up the score of all the teams.
        for _, score in self.Players.teams_score.items(): 
            total_score += score + 1

        # Draw the score bar.
        for team, score in self.Players.teams_score.items():
            score_bar_width = math.ceil((width / total_score) * (score + 1))

            sprites.append({
                "layer": 99,
                "data": create_rect_view_data(
                    "score_bar",

                    score_bar_x,
                    0,

                    score_bar_width,
                    int(overlay_size * 0.5),

                    self.Players.TEAM_COLORS[team]
                )
            })

            score_bar_x += score_bar_width

        text_x = overlay_size

        # Draw the statistics of the players.
        for name, player in self.Players.players.items():
            # Draw the player name and score.
            sprites.append({
                "layer": 99,
                "data": create_text_view_data(
                    name + ': ' + str(player.score),

                    int(text_x),
                    int(overlay_size * 1.25),

                    self.Players.TEAM_COLORS[player.team],

                    str(round(overlay_size * 2.5)) + 'px Bold'
                )
            })

            props: List[str] = []
            prop_x = text_x
            prop_y = overlay_size * 3

            for _ in range(player.bombs):
                props.append(self.Players.TEAM_BOMB_ICONS[player.team])

            # Draw the player props.
            for prop in props:
                sprites.append({
                    "layer": 99,
                    "data": create_image_view_data(
                        prop,

                        prop_x,
                        prop_y,

                        overlay_size * 1.5,
                        overlay_size * 1.5
                    )
                })

                prop_x += overlay_size * 1.25

                if (prop_x + (overlay_size * 1.25) >= text_x + ((width - (overlay_size * 2)) / len(self.Players.players)) or prop_x + (overlay_size * 1.25) >= width):
                    prop_x = text_x
                    prop_y += overlay_size * 1.5

            text_x += (width - (overlay_size * 2)) / len(self.Players.players)

        # Draw the time bar background.
        sprites.append({
            "layer": 99,
            "data": create_rect_view_data(
                'time_bar_background',
        
                0,
                int(height - (overlay_size * 0.5)),

                width,
                int(overlay_size * 0.5),

                '#000000'
            )
        })

        # Draw the time bar background.
        sprites.append({
            "layer": 100,
            "data": create_rect_view_data(
                'time_bar',
        
                0,
                int(height - (overlay_size * 0.5)),

                int((width / game_duration) * frame_count),
                int(overlay_size * 0.5),

                '#ffffff'
            )
        })

        # Draw the time bar text.
        sprites.append({
            "layer": 100,
            "data": create_text_view_data(
                str(frame_count) + " / " + str(game_duration),

                int(overlay_size),
                int(height - (overlay_size * 2)),

                '#ffffff',

                str(round(overlay_size * 1.5)) + 'px Bold'
            )
        })

        return sprites
