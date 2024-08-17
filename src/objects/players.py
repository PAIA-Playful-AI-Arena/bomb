from mlgame.view.view_model import create_rect_view_data, create_text_view_data, create_image_view_data
import pygame
import math

from ..loader import create_image_asset
from ..level import Level
from .map import Map

# The Players Object
class Players:
    TEAM_COLORS = ["#3996E8", "#E93850", "#E9D738", "#38E849"]
    TEAM_BOMB_ICONS = ["bomb_icon_blue", "bomb_icon_red", "bomb_icon_yellow", "bomb_icon_green"]

    PLAYER_HITBOX_WIDTH = 50
    PLAYER_HITBOX_HEIGHT = 60

    # Initialize The Object
    def __init__(self, level: Level, player_amount: int, team_mode: bool):
        if player_amount > len(level.Map["player_spawns"]):
            raise Exception(f"Player Amount Out Of Bounds: {player_amount} (Max {len(level.Map["spawns"])})")

        self.Level = level

        self.players_data = {}

        for i in range(player_amount):
            self.players_data[str(i + 1) + "P"] = {
                "team": i,

                "score": 0,
                "bombs": level.Rules["player_bombs"],
                "place_bomb_cooldown": 0,

                "x": (self.Level.Map["player_spawns"][i]["x"] * 64) + 32,
                "y": (self.Level.Map["player_spawns"][i]["y"] * 64) + 32,

                "rotate_speed": -level.Rules["player_speed"] / 33.33333,
                "target_angle": 0,
                "angle": 0
            }

        if player_amount == 4 and team_mode:
            self.players_data["1P"]["team"] = 0
            self.players_data["2P"]["team"] = 0
            self.players_data["3P"]["team"] = 1
            self.players_data["4P"]["team"] = 1
        elif player_amount == 3 and team_mode:
            self.players_data["1P"]["team"] = 0
            self.players_data["2P"]["team"] = 0
            self.players_data["3P"]["team"] = 1

        self.target_teams_score = {}
        self.teams_score = {}

    # Add The All Assets Needed By The Players
    def add_assets(self, assets: list):
        assets.append(create_image_asset("images/player.png", 64, 64))

        assets.append(create_image_asset("images/bomb_icon_blue.png", 64, 64))
        assets.append(create_image_asset("images/bomb_icon_red.png", 64, 64))
        assets.append(create_image_asset("images/bomb_icon_yellow.png", 64, 64))
        assets.append(create_image_asset("images/bomb_icon_green.png", 64, 64))

    # Move A Player
    def move(self, player_name: str, direction: str, foreground_tiles: list):
        if player_name not in self.players_data:
            raise Exception(f"Player Not Found: \"{player_name}\"")

        # Move the player.

        player_data = self.players_data[player_name]
        
        if direction == "left":
            player_data["x"] -= self.Level.Rules["player_speed"]
        elif direction == "right":
            player_data["x"] += self.Level.Rules["player_speed"]
        elif direction == "up":
            player_data["y"] -= self.Level.Rules["player_speed"]
        elif direction == "down":
            player_data["y"] += self.Level.Rules["player_speed"]

        # Check the collsion with the foreground tiles.

        for tile in foreground_tiles:
            if check_collision({
                "x": player_data["x"] - (self.PLAYER_HITBOX_WIDTH / 2), "y": (player_data["y"] + 32) - self.PLAYER_HITBOX_HEIGHT,
                "width": self.PLAYER_HITBOX_WIDTH, "height": self.PLAYER_HITBOX_HEIGHT
            }, [{ "x": tile["x"], "y": tile["y"], "width": 64, "height": 64 }]):
                if direction == "left":
                    player_data["x"] = (tile["x"] + 64) + (self.PLAYER_HITBOX_WIDTH / 2)
                elif direction == "right":
                    player_data["x"] = tile["x"] - (self.PLAYER_HITBOX_WIDTH / 2)
                elif direction == "up":
                    player_data["y"] = (tile["y"] + 64) - (32 - self.PLAYER_HITBOX_HEIGHT)
                elif direction == "down":
                    player_data["y"] = tile["y"] - 32

                break

        # Check the collsion with the map edges.
        
        if check_collision({
            "x": player_data["x"] - (self.PLAYER_HITBOX_WIDTH / 2), "y": (player_data["y"] + 32) - self.PLAYER_HITBOX_HEIGHT,
            "width": self.PLAYER_HITBOX_WIDTH, "height": self.PLAYER_HITBOX_HEIGHT
        }, [
            { "x": -100, "y": 0, "width": 100, "height": self.Level.Map["height"] * 64 },
            { "x": self.Level.Map["width"] * 64, "y": 0, "width": 100, "height": self.Level.Map["height"] * 64 },
            { "x": 0, "y": -100, "width": self.Level.Map["width"] * 64, "height": 100 },
            { "x": 0, "y": self.Level.Map["height"] * 64, "width": self.Level.Map["width"] * 64, "height": 100 }
        ]):
            if direction == "left":
                player_data["x"] = self.PLAYER_HITBOX_WIDTH / 2
            elif direction == "right":
                player_data["x"] = (self.Level.Map["width"] * 64) - (self.PLAYER_HITBOX_WIDTH / 2)
            elif direction == "up":
                player_data["y"] = self.PLAYER_HITBOX_HEIGHT - 32
            elif direction == "down":
                player_data["y"] = (self.Level.Map["height"] * 64) - 32

    # Get The Score Of All The Teams
    def get_teams_score(self):
        teams_score = {}

        for _, player_data in self.players_data.items():
            if player_data["team"] not in teams_score:
                teams_score[player_data["team"]] = player_data["score"]
            else:
                teams_score[player_data["team"]] += player_data["score"]
            
        return teams_score

    # Get The Winning Team
    def get_winning_team(self):
        team = None
        team_score = None

        for team_id, score in self.get_teams_score().items():
            if team == None or score > team_score:
                team = team_id
                team_score = score

        return team

    # Get Enemies Position
    def get_enemies_position(self, team: int):
        positions = []

        for _, player_data in self.players_data.items():
            if player_data["team"] != team:
                positions.append({ "x": player_data["x"], "y": player_data["y"] })

        return positions

    # Get Matrix
    def get_matrix(self, team_id: int):
        matrix = []

        for _ in range(self.Level.Map["width"] * self.Level.Map["height"]):
            matrix.append(0)

        for _, player_data in self.players_data.items():
            if player_data["team"] != team_id:
                index = round(player_data["x"] / 64) + (round(player_data["y"] / 64) * self.Level.Map["width"])

                matrix[index] = matrix[index] + 1

        return matrix

    # Bomb Exploded
    def bomb_exploded(self, owner: str, x: int, y: int):
        if owner not in self.players_data:
            raise Exception(f"Player Not Found: \"{owner}\"")

        team = self.players_data[owner]["team"]

        for _, player_data in self.players_data.items():
            if player_data["team"] != team and math.dist([x, y], [player_data["x"], player_data["y"]]) <= self.Level.Rules["bomb_explode_range"]:
                self.players_data[owner]["score"] += 2

                player_data["score"] -= 1

                spawns = []

                for index, spawn_position in enumerate(self.Level.Map["player_spawns"]):
                    distance = 0

                    for player_position in self.get_enemies_position(player_data["team"]):
                        distance += math.dist([spawn_position["x"] * 64, spawn_position["y"] * 64], [player_position["x"], player_position["y"]])

                    spawns.append({ "index": index, "distance": distance })

                spawns.sort(key = sort_spawns, reverse = True)

                player_data["x"] = (self.Level.Map["player_spawns"][spawns[0]["index"]]["x"] * 64) + 32
                player_data["y"] = (self.Level.Map["player_spawns"][spawns[0]["index"]]["y"] * 64) + 32


    # Update The Players
    def update(self, commands: dict, foreground_tiles: list): 
        for player_name, actions in commands.items():
            if actions != None:
                if "move_left" in actions:
                    self.move(player_name, "left", foreground_tiles)
                elif "move_right" in actions:
                    self.move(player_name, "right", foreground_tiles)
                
                if "move_up" in actions:
                    self.move(player_name, "up", foreground_tiles)
                elif "move_down" in actions:
                    self.move(player_name, "down", foreground_tiles)
    
                # The player walking animation.
                # "angle" is the actual angle of the player, "target_angle" is just for animation purpose.
    
                player_data = self.players_data[player_name]
     
                # Check if the player moved.
                if "move_left" in actions or "move_right" in actions or "move_up" in actions or "move_down" in actions:
                    if player_data["rotate_speed"] == 0:
                        if "move_left" in actions or "move_down" in actions:
                            player_data["rotate_speed"] = self.Level.Rules["player_speed"] / 33.33333
                        else:
                            player_data["rotate_speed"] = -self.Level.Rules["player_speed"] / 33.33333
    
                    player_data["target_angle"] += player_data["rotate_speed"]
    
                    if player_data["target_angle"] > 0.5:
                        player_data["target_angle"] = 0.5
                        player_data["rotate_speed"] = -player_data["rotate_speed"]
                    elif player_data["target_angle"] < -0.5:
                        player_data["target_angle"] = -0.5
                        player_data["rotate_speed"] = -player_data["rotate_speed"]
    
                else:
                    player_data["target_angle"] = 0
                    player_data["rotate_speed"] = 0 
    
                player_data["angle"] += (player_data["target_angle"] - player_data["angle"]) / 1.5
    
                if player_data["place_bomb_cooldown"] > 0:
                    player_data["place_bomb_cooldown"] -= 1

        # Update the team score.

        teams_score = self.get_teams_score()

        for team, score in teams_score.items(): 
            self.target_teams_score[team] = score

            if team not in self.teams_score:
                self.teams_score[team] = score

        for team, score in teams_score.items(): 
            self.teams_score[team] += (self.target_teams_score[team] - self.teams_score[team]) / 10

    
    # Render The Players
    def render(self, width: int, height: int, objects_info: list, map_render_offset_x: int, map_render_offset_y: int, tile_size: int):
        player_render_size = tile_size * 0.9

        font = pygame.font.Font(None, round(tile_size * 0.5))

        font.set_bold(True)

        # Draw the players and their name.

        for name, player_data in self.players_data.items():
            render_x = map_render_offset_x + ((tile_size / 64) * player_data["x"])
            render_y = map_render_offset_y + ((tile_size / 64) * player_data["y"])

            if abs(player_data["angle"]) > 0.001:
                render_y -= abs(player_data["angle"]) * (player_render_size / 1.25)

            objects_info.append({
                "layer": 10,
                "object": create_image_view_data(
                    "player",

                    render_x - (player_render_size / 2),
                    render_y - (player_render_size / 2),

                    player_render_size,
                    player_render_size,

                    player_data["angle"]
                )
            })

            size = font.size(name)

            objects_info.append({
                "layer": 10,
                "object": create_text_view_data(
                    name,

                    int(map_render_offset_x + (((tile_size / 64) * player_data["x"]) - (size[0] / 2))),
                    int((map_render_offset_y + (((tile_size / 64) * player_data["y"]) - (player_render_size * 0.9))) - (abs(player_data["angle"]) * (player_render_size / 3))),

                    self.TEAM_COLORS[player_data["team"]],

                    str(round(tile_size * 0.5)) + 'px Bold'
                )
            })

        # Set the UI render size.

        ui_size = (width + height) / 100

        # Draw the score bar.

        total_score = 0

        for _, score in self.teams_score.items(): 
            total_score += score + 1

        score_bar_x = 0

        for team, score in self.teams_score.items():
            score_bar_width = math.ceil((width / total_score) * (score + 1))

            objects_info.append({
                "layer": 100,
                "object": create_rect_view_data(
                    "score_bar",

                    score_bar_x,
                    0,

                    score_bar_width,
                    int(ui_size * 0.5),

                    self.TEAM_COLORS[team]
                )
            })

            score_bar_x += score_bar_width

        # Draw players' info.

        text_x = ui_size

        for name, player_data in self.players_data.items():
            objects_info.append({
                "layer": 100,
                "object": create_text_view_data(
                    name + ': ' + str(player_data["score"]),

                    int(text_x),
                    int(ui_size * 1.25),

                    self.TEAM_COLORS[player_data["team"]],

                    str(round(ui_size * 2.5)) + 'px Bold'
                )
            })

            # Render player props.

            props = []

            for _ in range(player_data["bombs"]):
                props.append(self.TEAM_BOMB_ICONS[player_data["team"]])

            prop_x = text_x
            prop_y = ui_size * 3

            for image_name in props:
                objects_info.append({
                    "layer": 100,
                    "object": create_image_view_data(
                        image_name,

                        prop_x,
                        prop_y,

                        ui_size * 1.5,
                        ui_size * 1.5
                    )
                })

                prop_x += ui_size * 1.25

                if (prop_x + (ui_size * 1.25) >= text_x + ((width - (ui_size * 2)) / len(self.players_data)) or prop_x + (ui_size * 1.25) >= width):
                    prop_x = text_x
                    prop_y += ui_size * 1.5
    
            text_x += (width - (ui_size * 2)) / len(self.players_data)

# Check The Collision
def check_collision(rect1: dict, rects: list):
    for rect2 in rects:
        rect1_right = rect1['x'] + rect1['width']
        rect1_bottom = rect1['y'] + rect1['height']
        rect2_right = rect2['x'] + rect2['width']
        rect2_bottom = rect2['y'] + rect2['height']

        if (rect1['x'] < rect2_right and rect2['x'] < rect1_right) and (rect1['y'] < rect2_bottom and rect2['y'] < rect1_bottom):
            return True

    return False

# Sort Spawns 
def sort_spawns(item: dict):
    return item["distance"]
