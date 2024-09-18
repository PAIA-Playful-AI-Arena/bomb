from mlgame.view.view_model import create_polygon_view_data, create_image_view_data
import random
import math

from ..loader import create_image_asset
from .players import Players
from ..level import Level
from .map import Map

# The Bombs Object
class Bombs:
    # Initialize The Object
    def __init__(self, level: Level, map: Map, players: Players):
        self.Level = level
        self.Map = map
        self.Players = players

        self.bombs_data = []
        self.explosion_clouds = []

    # Add The All Assets Needed By The Bombs
    def add_assets(self, assets: list):
        assets.append(create_image_asset("images/bomb.png", 64, 64))
        assets.append(create_image_asset("images/bomb_flash.png", 64, 64))
        assets.append(create_image_asset("images/explosion_range.png", 128, 128))

        assets.append(create_image_asset("images/explosion_1.png", 64, 64))
        assets.append(create_image_asset("images/explosion_2.png", 64, 64))
        assets.append(create_image_asset("images/explosion_3.png", 64, 64))
        assets.append(create_image_asset("images/explosion_4.png", 64, 64))
        assets.append(create_image_asset("images/explosion_5.png", 64, 64))
        assets.append(create_image_asset("images/explosion_6.png", 64, 64))
        assets.append(create_image_asset("images/explosion_7.png", 64, 64))

    # Place A Bomb
    def place_bomb(self, player_name: str):
        if player_name not in self.Players.players_data:
            raise Exception(f"Player Not Found: \"{player_name}\"")

        player_data = self.Players.players_data[player_name]

        if player_data["bombs"] > 0 and player_data["place_bomb_cooldown"] == 0:
            player_data["bombs"] -= 1
            player_data["place_bomb_cooldown"] = 5

            self.bombs_data.append({
                "owner": player_name,
                
                "x": player_data["x"],
                "y": player_data["y"],

                "countdown": self.Level.Rules["bomb_countdown"],

                "flash": False,
                "flash_cooldown": math.floor(self.Level.Rules["bomb_countdown"] / 10)
            })

    # Bomb Exploded
    def bomb_exploded(self, owner: str, x: int, y: int):
        self.Map.bomb_exploded(x, y)
        self.Players.bomb_exploded(owner, x, y)

        for bomb_data in self.bombs_data:
            if math.dist([x, y], [bomb_data["x"], bomb_data["y"]]) < self.Level.Rules["bomb_explode_range"]:
                if bomb_data["countdown"] > math.floor(self.Level.Rules["bomb_countdown"] / 10):
                    bomb_data["countdown"] = math.floor(self.Level.Rules["bomb_countdown"] / 10)
                else:
                    bomb_data["countdown"] = -1

        return

    # Get Matrix
    def get_matrix(self, team_id: int):
        matrix = []

        for _ in range(self.Level.Map["width"] * self.Level.Map["height"]):
            matrix.append(0)

        for bomb_data in self.bombs_data:
            if self.Players.players_data[bomb_data["owner"]]["team"] != team_id:
                index = math.floor(bomb_data["x"] / 64) + (math.floor(bomb_data["y"] / 64) * self.Level.Map["width"])

                matrix[index] = matrix[index] + 1

        return matrix

    # Upate The Bombs
    def update(self, commands: dict):
        for player_name, actions in commands.items():
            if actions != None:
                if "place_bomb" in actions:
                    self.place_bomb(player_name)

        # Update the bombs.

        for index in reversed(range(len(self.bombs_data))):
            bomb_data = self.bombs_data[index]

            if bomb_data["countdown"] > 0:
                bomb_data["countdown"] -= 1
                bomb_data["flash_cooldown"] -= 1

                if bomb_data["flash_cooldown"] == 0:
                    bomb_data["flash"] = not bomb_data["flash"]
                    bomb_data["flash_cooldown"] = math.floor(self.Level.Rules["bomb_countdown"] / 10)

            else:
                self.Map.shake += self.Level.Rules["bomb_explode_range"] / 350
                self.Players.players_data[bomb_data["owner"]]["bombs"] += 1

                self.bomb_exploded(bomb_data["owner"], bomb_data["x"], bomb_data["y"])

                for _ in range(math.floor(self.Level.Rules["bomb_explode_range"] / 15)):
                    position = generate_random_position_in_circle(bomb_data["x"], bomb_data["y"], self.Level.Rules["bomb_explode_range"])

                    self.explosion_clouds.append({ "animation": 1, "animation_cooldown": 3, "x": position[0], "y": position[1] })

                self.bombs_data.pop(index)

        # Update the exploded clouds animation.

        for index in reversed(range(len(self.explosion_clouds))):
            explosion_cloud = self.explosion_clouds[index]

            explosion_cloud["animation_cooldown"] -= 1

            if explosion_cloud["animation_cooldown"] < 0:
                explosion_cloud["animation"] += 1

                if explosion_cloud["animation"] == 7:
                    self.explosion_clouds.pop(index)
                else:
                    explosion_cloud["animation_cooldown"] = 3

    # Render The Bombs
    def render(self, objects_info: list, map_render_offset_x: int, map_render_offset_y: int, tile_size: int):
        bomb_size = tile_size * 0.75
        explode_range_size = ((tile_size / 64) * self.Level.Rules["bomb_explode_range"]) * 2

        # Draw the bombs.

        for bomb_data in self.bombs_data:
            # Draw the bomb and the explosion range.

            render_x = map_render_offset_x + ((tile_size / 64) * bomb_data["x"])
            render_y = map_render_offset_y + ((tile_size / 64) * bomb_data["y"])

            objects_info.append({
                "layer": 4,
                "object": create_image_view_data(
                    "explosion_range",

                    render_x - (explode_range_size / 2),
                    render_y - (explode_range_size / 2),

                    explode_range_size,
                    explode_range_size
                )
            })

            objects_info.append({
                "layer": 5,
                "object": create_image_view_data(
                    "bomb_flash" if bomb_data["flash"] else "bomb",

                    render_x - (bomb_size / 2),
                    render_y - (bomb_size / 2),

                    bomb_size,
                    bomb_size
                )
            })

            # Draw the bomb countdown.

            countdown_render_x = render_x + (bomb_size * 0.02)
            countdown_render_y = render_y + (bomb_size * 0.125)

            points = [[countdown_render_x, countdown_render_y]]

            for i in range(int((360 / self.Level.Rules["bomb_countdown"]) * (self.Level.Rules["bomb_countdown"] - bomb_data["countdown"]))):
                points.append([
                    countdown_render_x + ((bomb_size * 0.2) * math.cos(math.radians(i - 90))),
                    countdown_render_y + ((bomb_size * 0.2) * math.sin(math.radians(i - 90)))
                ])

            if (len(points) >= 3):
                objects_info.append({
                    "layer": 5,
                    "object": create_polygon_view_data(
                        "bomb_countdown",

                        points,

                        self.Players.TEAM_COLORS[self.Players.players_data[bomb_data["owner"]]["team"]]
                    )
                })

        # Draw the exploded clouds.

        explosion_cloud_size = tile_size * 2

        for explosion_cloud in self.explosion_clouds:
            objects_info.append({
                "layer": 20,
                "object": create_image_view_data(
                    f"explosion_{explosion_cloud['animation']}",

                    map_render_offset_x + (((tile_size / 64) * explosion_cloud["x"]) - (explosion_cloud_size / 2)),
                    map_render_offset_y + (((tile_size / 64) * explosion_cloud["y"]) - (explosion_cloud_size / 2)),

                    explosion_cloud_size,
                    explosion_cloud_size
                )
            })


# Generate A Random Position In A Circle
def generate_random_position_in_circle(x: int, y: int, radius: int):
    ang = random.uniform(0, 1) * 2 * math.pi
    hyp = math.sqrt(random.uniform(0, 1)) * radius
    adj = math.cos(ang) * hyp
    opp = math.sin(ang) * hyp

    return [x + adj, y + opp]
