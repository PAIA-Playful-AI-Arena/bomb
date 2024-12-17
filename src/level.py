from typing import Union, Any, List 
import json

# Check the type of the property.
def check_property_type(name: str, type_name: str, value: Any):
    if type_name == "int" and type(value) is not int:
        raise Exception(f"[Type Error] The value of property \"{name}\" must be the \"int\" type!")
    elif type_name == "str" and type(value) is not str:
        raise Exception(f"[Type Error] The value of property \"{name}\" must be the \"str\" type!")
    elif type_name == "list" and type(value) is not list:
        raise Exception(f"[Type Error] The value of property \"{name}\" must be the \"list\" type!")
    elif type_name == "dict" and type(value) is not dict:
        raise Exception(f"[Type Error] The value of property \"{name}\" must be the \"dict\" type!")

# Check the range of the property.
def check_property_range(name: str, value: int, min: int, max: int):
    if value < min or value > max:
        raise Exception(f"[Range Error] The value of property \"{name}\" must be between {min} and {max}!")

# The rules itsef.
class Rules:
    def __init__(self, data: dict) -> None:
        self.player_speed: int = data.get('player_speed', 5)
        self.player_bombs: int = data.get('player_bombs', 2)
        self.bomb_countdown: int = data.get('bomb_countdown', 150)
        self.bomb_explosion_range: int = data.get('bomb_explosion_range', 125)

        check_property_type('rules.player_speed', 'int', self.player_speed)
        check_property_type('rules.player_bombs', 'int', self.player_bombs)
        check_property_type('rules.bomb_countdown', 'int', self.bomb_countdown)
        check_property_type('rules.bomb_explode_range', 'int', self.bomb_explosion_range)

        check_property_range('rules.player_speed', self.player_speed, 1, 64)
        check_property_range('rules.player_bombs', self.player_bombs, 1, 64)
        check_property_range('rules.bomb_countdown', self.bomb_countdown, 1, 1024)
        check_property_range('rules.bomb_explosion_range', self.bomb_explosion_range, 1, 1024)

# The map itself.
class Map:
    def __init__(self, data: dict) -> None:
        self.width: int = data.get('width', 10)
        self.height: int = data.get('height', 6)
        self.tiles: List[dict] = []
        self.spawns: List[dict] = []

        for i in range(len(data["tiles"])):
            tile = data["tiles"][i]

            check_property_type(f'map.tiles[{i}]', 'dict', tile)
            check_property_type(f'map.tiles[{i}].type', 'str', tile["type"])
            check_property_type(f'map.tiles[{i}].x', 'int', tile["x"])
            check_property_type(f'map.tiles[{i}].y', 'int', tile["y"])

            check_property_range(f'map.tiles[{i}].x', tile["x"], 0, self.width - 1)
            check_property_range(f'map.tiles[{i}].y', tile["y"], 0, self.height - 1)

            if (tile["type"] == "player"):
                self.spawns.append({ "x": tile["x"], "y": tile["y"] })
            else:
                self.tiles.append(tile)

        check_property_type('map.width', 'int', self.width)
        check_property_type('map.height', 'int', self.height)
        check_property_type('map.tiles', 'list', self.tiles)
        check_property_type('map.spawns', 'list', self.spawns)

        check_property_range('map.width', self.width, 1, 64)
        check_property_range('map.height', self.height, 1, 64)

# The level itself.
class Level:
    # Load the level.
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
