from mlgame.view.view_model import create_asset_init_data
from os import path

ASSETS_FOLDER = path.join(path.dirname(path.dirname(__file__)), "assets")

# Create An Image Asset
def create_image_asset(relative_path: str, width: int, height: int):
    return create_asset_init_data(path.basename(relative_path).split('.')[0], width, height, path.join(ASSETS_FOLDER, relative_path), "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/assets/" + relative_path)
