from collections.abc import MutableSequence
from typing import Any, Union

# Level
class Level:
    # Load The Level
    def __init__(self, level_file: str):
        data = {}

        current_group = None

        # Parse the level file line by line.
            
        for index, line in enumerate(open(level_file).read().split("\n")):
            line = parse_line(line, index + 1)

            if (line["type"] == "group_head"):
                data[line["name"]] = {}

                current_group = line["name"]
            elif (line["type"] == "field"):
                if current_group == None:
                    raise Exception("Syntax Error: Field Does Not Belong To Any Group (Line " + str(index + 1) + ")")
                else:
                    data[current_group][line["name"]] = line["value"]
            elif (line["type"] == "empty"):
                current_group = None

        # The default level data.

        data = {
            "Rules": {
                "player_speed": 5,
                "player_bombs": 2,

                "bomb_countdown": 150,
                "bomb_explode_range": 125
            },

            "Map": {
                "width": 15,
                "height": 10,

                "tiles_type": StringList(),
                "tiles_position": Vec2List(),

                "player_spawns": NumberList()
            }
        } | data

        # Check the type of the fields.

        check_field_type("Rules.player_speed", data["Rules"]["player_speed"], "number")
        check_field_type("Rules.player_bombs", data["Rules"]["player_bombs"], "number")
        check_field_type("Rules.bomb_countdown", data["Rules"]["bomb_countdown"], "number")
        check_field_type("Rules.bomb_explode_range", data["Rules"]["bomb_explode_range"], "number")

        check_field_type("Map.width", data["Map"]["width"], "number")
        check_field_type("Map.height", data["Map"]["height"], "number")
        check_field_type("Map.height", data["Map"]["height"], "number")
        check_field_type("Map.tiles_type", data["Map"]["tiles_type"], "string_list")
        check_field_type("Map.tiles_position", data["Map"]["tiles_position"], "vec2_list")
        check_field_type("Map.player_spawns", data["Map"]["player_spawns"], "vec2_list")

        self.Rules = data["Rules"]
        self.Map = data["Map"]

# Vec 2
class Vec2():
    # Initliaze The Vector
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# Number List
class NumberList():
    # Initliaze The List
    def __init__(self, data: Union[None, list] = None):
        self._data = list(data) if data is not None else []

    # Get An Item
    def __getitem__(self, index: int):
        return self._data[index]

    # Get An Item
    def __setitem__(self, index: int, value: int):
        self._data[index] = value

    # Delete An Item
    def __delitem__(self, index: int):
        del self._data[index]

    # Get The Length Of The List
    def __len__(self):
        return len(self._data)

    # Insert An Item To The List
    def insert(self, index: int, value: int):
        self._data.insert(index, value)

    # No Idea What This Is
    def __repr__(self):
        return repr(self._data)

# String List
class StringList():
    # Initliaze The List
    def __init__(self, data: Union[None, list] = None):
        self._data = list(data) if data is not None else []

    # Get An Item
    def __getitem__(self, index: int):
        return self._data[index]

    # Get An Item
    def __setitem__(self, index: int, value: str):
        self._data[index] = value

    # Delete An Item
    def __delitem__(self, index: int):
        del self._data[index]

    # Get The Length Of The List
    def __len__(self):
        return len(self._data)

    # Insert An Item To The List
    def insert(self, index: int, value: str):
        self._data.insert(index, value)

    # No Idea What This Is
    def __repr__(self):
        return repr(self._data)

# Vec2 List
class Vec2List():
    # Initliaze The List
    def __init__(self, data: Union[None, list] = None):
        self._data = list(data) if data is not None else []

    # Get An Item
    def __getitem__(self, index: int):
        return self._data[index]

    # Get An Item
    def __setitem__(self, index: int, value: Vec2):
        self._data[index] = value

    # Delete An Item
    def __delitem__(self, index: int):
        del self._data[index]

    # Get The Length Of The List
    def __len__(self):
        return len(self._data)

    # Insert An Item To The List
    def insert(self, index: int, value: Vec2):
        self._data.insert(index, value)

    # No Idea What This Is
    def __repr__(self):
        return repr(self._data)

# Parse A Line
def parse_line(line: str, line_number: int) -> dict:
    line = line.strip()

    if len(line) == 0:
        return { "type": "empty" }
    else:
        if line[0] == "[" and line[len(line) - 1] == "]":
            return { "type": "group_head", "name": line[1:len(line) - 1] }
        elif line[0] == "|":
            if len(line) > 1:
                if ":" not in line:
                    raise Exception(f"Syntax Error: Missing \":\" In The Field Add \":\" After The Field Name (Line {line_number})")

                return {
                    "type": "field",

                    "name": line[1:line.index(":")].strip().strip(),
                    "value": parse_field_value(line[line.index(":") + 1:].strip(), line_number)
                }
            else:
                return { "type": "empty_field" }
        else:
            raise Exception(f"Syntax Error: What?? (Line {line_number})")
            
# Parse Field Value
def parse_field_value(value: str, line_number: int):
    value = value.strip()

    if not "(" in value:
        raise Exception(f"Syntax Error: Missing \"(\" In The Field Add \"(\" After The Field Type (Line {line_number})")
    if not ")" in value:
        raise Exception(f"Syntax Error: Missing \")\" In The Field Add \")\" After The Field Type (Line {line_number})")

    value_type = value[0:value.index('(')]
    value_content = value[value.index('(') + 1:value.rindex(')')].strip()

    if value_type == "number":
        for index in range(len(value_content)):
            if value_content[index] not in "0123456789":
                raise Exception(f"Syntax Error: \"{value_content}\" Is Not A Number (Line {line_number})")

        return int(value_content)
    elif value_type == "string":
        return value_content
    elif value_type == "vec2":
        x = value_content.split(":")[0].strip()
        y = value_content.split(":")[1].strip()

        for index in range(len(x)):
            if x[index] not in "0123456789":
                raise Exception(f"Syntax Error: \"{x}\" Is Not A Number (Line {line_number})")

        for index in range(len(y)):
            if y[index] not in "0123456789":
                raise Exception(f"Syntax Error: \"{y}\" Is Not A Number (Line {line_number})")

        return Vec2(int(x), int(y))
    elif value_type == "number_list":
        array = [] 

        if (len(value_content) > 0):
            for index, item in enumerate(value_content.split(',')):
                item_value = parse_field_value(item, line_number)
    
                if type(item_value) is not int:
                    raise Exception(f"Type Error: Item Must Be The \"number\" Type (Index {index})")
    
                array.append(item_value)

        return NumberList(array)
    elif value_type == "string_list":
        array = []

        if (len(value_content) > 0):
            for index, item in enumerate(value_content.split(',')):
                item_value = parse_field_value(item, line_number)
    
                if type(item_value) is not str:
                    raise Exception(f"Type Error: Item Must Be The \"string\" Type (Index {index})")
    
                array.append(item_value)

        return StringList(array)
    elif value_type == "vec2_list":
        array = []

        if (len(value_content) > 0):
            for index, item in enumerate(value_content.split(',')):
                item_value = parse_field_value(item, line_number)
    
                if type(item_value) is not Vec2:
                    raise Exception(f"Type Error: Item Must Be The \"vec2\" Type (Index {index})")
    
                array.append(item_value)

        return Vec2List(array)
    else:
        raise Exception(f"Syntax Error: Unknown Value Type: \"{value[0:value.index("(")]}\" (Line {line_number})")


# Check Field Type
def check_field_type(name: str, value: Any, type_name: str):
    if type_name == "number" and type(value) is not int:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"number\" Type")
    elif type_name == "string" and type(value) is not str:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"string\" Type")
    elif type_name == "vec2" and type(value) is not Vec2:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"vec2\" Type")
    elif type_name == "number_list" and type(value) is not NumberList:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"number_list\" Type")
    elif type_name == "string_list" and type(value) is not StringList:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"string_list\" Type")
    elif type_name == "vec2_list" and type(value) is not Vec2List:
        raise Exception(f"Type Error: Field \"{name}\" Must Be The \"vec2_list\" Type")
