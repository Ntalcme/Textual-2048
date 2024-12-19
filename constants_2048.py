from enum import Enum
import json

with open("game_texts.json", 'r', encoding='utf-8') as texts:
    game_texts = json.load(texts)

class ConstantsOf2048:
    class Display:
        CELL_SIZE = 7
        CORNER = "+"
        BAR = "-"
        CELL_SPACE = " "
        BORDER = "|"

    class Gameplay:
        EMPTY_CELL_VALUE = 0
        SPAWN_PROBABILITIES = {
            2: 0.9,
            4: 0.1
        }

        class Controls(Enum):
            LEFT = "l"
            RIGHT = "r"
            UP = "u"
            DOWN = "d"

