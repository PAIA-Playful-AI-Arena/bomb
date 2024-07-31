from mlgame.view.view_model import create_rect_view_data, create_polygon_view_data, create_text_view_data
import math

# Time
class Time:
    # Initialize The Object
    def __init__(self):
        return

    # Render The Time
    def render(self, width: int, height: int, objects_info: list, game_duration: int, frame_count: int):
        ui_size = (width + height) / 100

        objects_info.append({
            "layer": 100,
            "object": create_rect_view_data(
                'time_bar_background',
        
                0,
                int(height - (ui_size * 0.5)),

                width,
                int(ui_size * 0.5),

                '#000000'
            )
        })

        objects_info.append({
            "layer": 100,
            "object": create_rect_view_data(
                'time_bar',
        
                0,
                int(height - (ui_size * 0.5)),

                int((width / game_duration) * frame_count),
                int(ui_size * 0.5),

                '#ffffff'
            )
        })

        objects_info.append({
            "layer": 100,
            "object": create_text_view_data(
                str(frame_count) + " / " + str(game_duration),

                int(ui_size),
                int(height - (ui_size * 2)),

                '#ffffff',

                str(round(ui_size * 1.5)) + 'px Bold'
            )
        })
