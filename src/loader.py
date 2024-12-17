from mlgame.view.view_model import create_asset_init_data
from typing import List
from os import path

ASSETS_FOLDER = path.join(path.dirname(path.dirname(__file__)), "assets")

# Create an image asset.
def create_image_asset(relative_path: str, width: int, height: int) -> dict:
    # The image ID is just the filename of the image without the extension.
    image_id = path.basename(relative_path).split('.')[0]

    return create_asset_init_data(image_id, width, height, path.join(ASSETS_FOLDER, relative_path), "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/assets/" + relative_path)

# Load the assets.
def load_assets() -> List[dict]:
    return [
        create_image_asset("images/background_gradient.png", 1024, 725),
        create_image_asset("images/background_wave.png", 512, 512),

        create_image_asset("images/tile_ground.png", 256, 256),
        create_image_asset("images/tile_barrel.png", 256, 256),
        create_image_asset("images/tile_rock.png", 256, 256),

        create_image_asset("images/player_1_right.png", 256, 256),
        create_image_asset("images/player_2_right.png", 256, 256),
        create_image_asset("images/player_3_right.png", 256, 256),
        create_image_asset("images/player_4_right.png", 256, 256),
        create_image_asset("images/player_1_left.png", 256, 256),
        create_image_asset("images/player_2_left.png", 256, 256),
        create_image_asset("images/player_3_left.png", 256, 256),
        create_image_asset("images/player_4_left.png", 256, 256),
        create_image_asset("images/player_flash_left.png", 256, 256),
        create_image_asset("images/player_flash_right.png", 256, 256),
        create_image_asset("images/player_shadow.png", 256, 256),

        create_image_asset("images/ghost_1_right.png", 256, 256),
        create_image_asset("images/ghost_2_right.png", 256, 256),
        create_image_asset("images/ghost_3_right.png", 256, 256),
        create_image_asset("images/ghost_4_right.png", 256, 256),
        create_image_asset("images/ghost_1_left.png", 256, 256),
        create_image_asset("images/ghost_2_left.png", 256, 256),
        create_image_asset("images/ghost_3_left.png", 256, 256),
        create_image_asset("images/ghost_4_left.png", 256, 256),

        create_image_asset("images/bomb_1.png", 128, 128),
        create_image_asset("images/bomb_2.png", 128, 128),
        create_image_asset("images/bomb_3.png", 128, 128),
        create_image_asset("images/bomb_4.png", 128, 128),

        create_image_asset("images/explosion_range_1.png", 256, 256),
        create_image_asset("images/explosion_range_2.png", 256, 256),
        create_image_asset("images/explosion_range_3.png", 256, 256),
        create_image_asset("images/explosion_range_4.png", 256, 256),
        create_image_asset("images/explosion_cloud_1.png", 256, 256),
        create_image_asset("images/explosion_cloud_2.png", 256, 256),
        create_image_asset("images/explosion_cloud_3.png", 256, 256),
        create_image_asset("images/explosion_cloud_4.png", 256, 256),
        create_image_asset("images/explosion_cloud_5.png", 256, 256),
        create_image_asset("images/explosion_cloud_6.png", 256, 256),
        create_image_asset("images/explosion_cloud_7.png", 256, 256),
        create_image_asset("images/explosion_cloud_8.png", 256, 256),
        create_image_asset("images/explosion_cloud_9.png", 256, 256),
        create_image_asset("images/explosion_cloud_10.png", 256, 256),
        create_image_asset("images/explosion_cloud_11.png", 256, 256),

        create_image_asset("images/timer.png", 128, 128),
        create_image_asset("images/timer_sparks.png", 128, 128),

        create_image_asset("images/overlay_background.png", 512, 1124),
        create_image_asset("images/overlay_frame.png", 256, 256),

        create_image_asset("images/icon_player_1.png", 128, 128),
        create_image_asset("images/icon_player_2.png", 128, 128),
        create_image_asset("images/icon_player_3.png", 128, 128),
        create_image_asset("images/icon_player_4.png", 128, 128),
        create_image_asset("images/icon_bomb_1.png", 128, 128),
        create_image_asset("images/icon_bomb_2.png", 128, 128),
        create_image_asset("images/icon_bomb_3.png", 128, 128),
        create_image_asset("images/icon_bomb_4.png", 128, 128) 
    ]
