from typing import Any
import json

# Level
class Level:
    # Load The Level
    def __init__(self, level_file: str):
        data = {
            "rules": {
                "player_speed": 5,
                "player_bombs": 2,

                "bomb_countdown": 150,
                "bomb_explode_range": 125
            },

            "map": {
                "width": 15,
                "height": 10,

                "tiles": [],
                "spawns": []
            }
        }

        json_data = json.load(open(level_file))

        if json_data["compressionlevel"] != None:
            json_data = convert(json_data)

        data = data | json_data

        check_field_type("rules.player_speed", data["rules"]["player_speed"], "number")
        check_field_type("rules.player_bombs", data["rules"]["player_bombs"], "number")
        check_field_type("rules.bomb_countdown", data["rules"]["bomb_countdown"], "number")
        check_field_type("rules.bomb_explode_range", data["rules"]["bomb_explode_range"], "number")

        check_field_type("map.width", data["map"]["width"], "number")
        check_field_type("map.height", data["map"]["height"], "number")
        check_field_type("map.height", data["map"]["height"], "number")
        check_field_type("map.tiles", data["map"]["tiles"], "list")

        self.Rules = data["rules"]
        self.Map = data["map"]

        self.Map["player_spawns"] = []

        for index in reversed(range(len(self.Map["tiles"]))):
            tile = self.Map["tiles"][index]

            if tile["type"] == "player":
                if len(self.Map["player_spawns"]) < 4:
                    self.Map["player_spawns"].append({ "x": tile["x"], "y": tile["y"] })

                self.Map["tiles"].pop(index)

# Check Field Type
def check_field_type(name: str, value: Any, type_name: str):
    if type_name == "number" and type(value) is not int:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"number\" Type")
    elif type_name == "string" and type(value) is not str:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"string\" Type")
    elif type_name == "list" and type(value) is not list:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"list\" Type")

# Convert The Tiled Format
def convert(data: dict):
    tiles = []

    index = 0

    for x in range(data["width"]):
        for y in range(data["height"]):
            if data["layers"][0]["data"][index] > 0:
                tiles.append({ "type": ['barrel', 'rock', 'rock2', 'player'][data["layers"][0]["data"][index] - 1], "x": x, "y": y })

            index = index + 1

    return { "map": { "width": data["width"], "height": data["height"], "tiles": tiles }}
