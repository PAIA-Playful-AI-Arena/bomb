from os import path
import sys

sys.path.append(path.dirname(__file__))

from src.game import Game

GAME_SETUP = {
    "game": Game
}

# python3 -m mlgame -i ./ml/ml_play_manual.py -i ./ml/ml_play_manual2.py .
