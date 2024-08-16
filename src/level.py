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
        } | json.load(open(level_file))

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

        self.Map["spawns"] = []

        for index in reversed(range(len(self.Map["tiles"]))):
            tile = self.Map["tiles"][index]

            if tile["type"] == "player":
                self.Map["spawns"].append({ "x": tile["x"], "y": tile["y"] })

                self.Map["tiles"].pop(index)

# Check Field Type
def check_field_type(name: str, value: Any, type_name: str):
    if type_name == "number" and type(value) is not int:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"number\" Type")
    elif type_name == "string" and type(value) is not str:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"string\" Type")
    elif type_name == "list" and type(value) is not list:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"list\" Type")
