from typing import Union, Any, List 
import json

# Check The Type Of The Field
def check_field_type(name: str, type_name: str, value: Any):
    if type_name == "int" and type(value) is not int:
        raise Exception(f"Type Error: The value of field \"{name}\" must be the \"int\" type")
    elif type_name == "str" and type(value) is not str:
        raise Exception(f"Type Error: The value of field \"{name}\" must be the \"str\" type")
    elif type_name == "list" and type(value) is not list:
        raise Exception(f"Type Error: The value of field \"{name}\" must be the \"list\" type")
    elif type_name == "dict" and type(value) is not dict:
        raise Exception(f"Type Error: The value of field \"{name}\" must be the \"dict\" type")

# Check The Range Of The Field
def check_field_range(name: str, min: int, max: int, value: int):
    if value < min or value > max:
        raise Exception(f"Range Error: The value of field \"{name}\" must be between {min} and {max}")

# Rules
class Rules:
    def __init__(self, data: dict) -> None:
        self.player_speed: int = data.get('player_speed', 5)
        self.player_bombs: int = data.get('player_bombs', 2)
        self.bomb_countdown: int = data.get('bomb_countdown', 150)
        self.bomb_explosion_range: int = data.get('bomb_explosion_range', 125)

        check_field_type('rules.player_speed', 'int', self.player_speed)
        check_field_type('rules.player_bombs', 'int', self.player_bombs)
        check_field_type('rules.bomb_countdown', 'int', self.bomb_countdown)
        check_field_type('rules.bomb_explode_range', 'int', self.bomb_explosion_range)

        check_field_range('rules.player_speed', 1, 99, self.player_speed)
        check_field_range('rules.player_bombs', 1, 99, self.player_bombs)
        check_field_range('rules.bomb_countdown', 1, 9999, self.bomb_countdown)
        check_field_range('rules.bomb_explosion_range', 1, 9999, self.bomb_explosion_range)

# Map
class Map:
    def __init__(self, data: dict) -> None:
        self.width: int = data.get('width', 10)
        self.height: int = data.get('height', 6)
        self.tiles: List[dict] = []
        self.spawns: List[dict] = []

        for i in range(len(data["tiles"])):
            tile = data["tiles"][i]

            check_field_type(f'map.tiles[{i}]', 'dict', tile)
            check_field_type(f'map.tiles[{i}].type', 'str', tile["type"])
            check_field_type(f'map.tiles[{i}].x', 'int', tile["x"])
            check_field_type(f'map.tiles[{i}].y', 'int', tile["y"])

            check_field_range(f'map.tiles[{i}].x', 0, self.width - 1, tile["x"])
            check_field_range(f'map.tiles[{i}].y', 0, self.height - 1, tile["y"])

            if (tile["type"] == "player"):
                self.spawns.append({ "x": tile["x"], "y": tile["y"] })
            else:
                self.tiles.append(tile)

        check_field_type('map.width', 'int', self.width)
        check_field_type('map.height', 'int', self.height)
        check_field_type('map.tiles', 'list', self.tiles)
        check_field_type('map.spawns', 'list', self.spawns)

        check_field_range('map.width', 1, 99, self.width)
        check_field_range('map.height', 1, 99, self.height)

# Level
class Level:
    # Load The Level
    def __init__(self, level_path: str) -> None:
        data = json.load(open(level_path))

        # Both the native and Tiled format are supported.
        if "compressionlevel" in data:
            tiles: List[dict] = []
            index: int = 0

            layer = data["layers"][0]["data"]

            for x in range(data["width"]):
                for y in range(data["height"]):
                    if layer[index] > 0:
                        tiles.append({ "type": ['barrel', 'rock', 'rock2', 'player'][layer[index] - 1], "x": x, "y": y })

                    index += 1

            self.Rules = Rules(data["properties"] if "properties" in data else {})
            self.Map = Map({
                "width": data["width"],
                "height": data["height"],
                "tiles": tiles
            })
        else:
            self.Rules = Rules(data["rules"])
            self.Map = Map(data["map"])
