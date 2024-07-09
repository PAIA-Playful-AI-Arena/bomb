import sys
from os import path
sys.path.append(path.dirname(__file__))

from src.game import Arkanoid
# TODO 設定遊戲class路徑
GAME_SETUP = {
    "game": Arkanoid
}
