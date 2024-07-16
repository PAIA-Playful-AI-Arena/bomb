from os import path

# Settings

PLAYER_SPEED = 5
PLAYER_BOMB_AMOUNT = 100

BOMB_COUNTDOWN = 150
BOMB_CHAIN_COUNTDOWN = 15 # The countdown of chain explosions
BOMB_EXPLODE_RANGE = 100

# Image Path

IMAGE_GROUND_LIGHT_PATH = path.join(path.dirname(__file__), "../asset/image/ground_light.png")
IMAGE_GROUND_DARK_PATH = path.join(path.dirname(__file__), "../asset/image/ground_dark.png")

IMAGE_BARREL_PATH = path.join(path.dirname(__file__), "../asset/image/barrel.png")
IMAGE_ROCK_PATH = path.join(path.dirname(__file__), "../asset/image/rock.png")

IMAGE_PLAYER_PATH = path.join(path.dirname(__file__), "../asset/image/player.png")
IMAGE_BOMB_PATH = path.join(path.dirname(__file__), "../asset/image/bomb.png")
IMAGE_EXPLOSION_RANGE_PATH = path.join(path.dirname(__file__), "../asset/image/explosion_range.png")

# Image URL

IMAGE_GROUND_LIGHT_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/asset/image/ground_light.png"
IMAGE_GROUND_DARK_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/asset/image/ground_dark.png"

IMAGE_BARREL_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/asset/image/barrel.png"
IMAGE_ROCK_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/asset/image/rock.png"

IMAGE_PLAYER_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/asset/image/player.png"
IMAGE_BOMB_URL = "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/asset/image/bomb.png"
IMAGE_EXPLOSION_RANGE_URL = path.join(path.dirname(__file__), "https://raw.githubusercontent.com/PAIA-Playful-AI-Arena/bomb/main/asset/image/explosion_range.png")
