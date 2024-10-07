from mlgame.view.view_model import create_asset_init_data
from os import path

ASSETS_FOLDER = path.join(path.dirname(path.dirname(__file__)), "assets")

# Create An Image Asset
def create_image_asset(relative_path: str, width: int, height: int) -> dict:
    return create_asset_init_data(
        path.basename(relative_path).split('.')[0],
        width, height,
        path.join(ASSETS_FOLDER, relative_path), "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/assets/" + relative_path
    )

# Get Game Assets
def get_assets() -> list:
    return [
        create_image_asset("images/tile_ground_light.png", 64, 64),
        create_image_asset("images/tile_ground_dark.png", 64, 64),
        create_image_asset("images/tile_barrel.png", 64, 64),
        create_image_asset("images/tile_rock.png", 64, 64),
        create_image_asset("images/tile_rock2.png", 64, 64),

        create_image_asset("images/player.png", 64, 64),
        create_image_asset("images/player_flash.png", 64, 64),

        create_image_asset("images/bomb.png", 64, 64),
        create_image_asset("images/bomb_flash.png", 64, 64),
        create_image_asset("images/tile_explosion_range.png", 64, 64),
        create_image_asset("images/player_explosion_range.png", 64, 64),
      
        create_image_asset("images/explosion_1.png", 64, 64),
        create_image_asset("images/explosion_2.png", 64, 64),
        create_image_asset("images/explosion_3.png", 64, 64),
        create_image_asset("images/explosion_4.png", 64, 64),
        create_image_asset("images/explosion_5.png", 64, 64),
        create_image_asset("images/explosion_6.png", 64, 64),
        create_image_asset("images/explosion_7.png", 64, 64),

        create_image_asset("images/bomb_icon_blue.png", 64, 64),
        create_image_asset("images/bomb_icon_red.png", 64, 64),
        create_image_asset("images/bomb_icon_yellow.png", 64, 64),
        create_image_asset("images/bomb_icon_green.png", 64, 64)
    ]
