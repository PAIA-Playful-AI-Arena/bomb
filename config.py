from os import path
import sys

sys.path.append(path.dirname(__file__))

from src.game import Bomb

GAME_SETUP = {
    "game": Bomb
}

# python3 -m mlgame -i ./ml/ml_play_manual.py .
