from os import path
import sys

sys.path.append(path.dirname(__file__))

from src.game import Game

GAME_SETUP = {
    "game": Game
}

# python3 -m mlgame -i ./ml/manual_1.py .
# python3 -m mlgame -i ./ml/manual_1.py -i ./ml/manual_2.py .
# python3 -m mlgame -i ./ml/manual_1.py -i ./ml/manual_1.py -i ./ml/manual_2.py .
# python3 -m mlgame -i ./ml/manual_1.py -i ./ml/manual_1.py -i ./ml/manual_2.py -i ./ml/manual_2.py .
