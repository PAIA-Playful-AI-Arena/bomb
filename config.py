from os import path
import sys

sys.path.append(path.dirname(__file__))

from src.main import Game

GAME_SETUP = {
    "game": Game
}

# Start Command
# python3 -m mlgame -i ./ml/ml_play_manual.py -i ./ml/ml_play_manual.py .
