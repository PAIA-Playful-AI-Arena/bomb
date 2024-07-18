from collections.abc import MutableSequence
import pygame
import random
import math

from mlgame.view.view_model import create_polygon_view_data, create_text_view_data, create_image_view_data

from .objects import *
from .env import *

# Render The Game
def render(width: int, height: int, Map: Map, Bombs: Bombs, players: MutableSequence[Player]):
    objects = []

    # Render The Map

    mapRenderX = round((width / 2) - ((Map.width / 2) * Map.tile_size), 0) + random.randint(int(-Map.camera_shake), int(Map.camera_shake))
    mapRenderY = round((height / 2) - ((Map.height / 2) * Map.tile_size), 0) + random.randint(int(-Map.camera_shake), int(Map.camera_shake))

    render_x = mapRenderX 
    render_y = mapRenderY 

    for y in range(Map.height):
        render_x = mapRenderX

        for x in range(Map.width):
            background_tile = Map.TILE_TYPES[Map.get_background_tile(x, y)]
            foreground_tile = Map.TILE_TYPES[Map.get_foreground_tile(x, y)]

            if (background_tile != None):
                objects.append(create_image_view_data(background_tile, render_x, render_y, Map.tile_size, Map.tile_size))

            if (foreground_tile != None):
                objects.append(create_image_view_data(foreground_tile, render_x, render_y, Map.tile_size, Map.tile_size))

            render_x += round(Map.tile_size, 0)

        render_y += round(Map.tile_size, 0)

    # Render Bombs

    bomb_size = Map.tile_size * 0.75
    explode_range_size = ((Map.tile_size / 64) * BOMB_EXPLODE_RANGE) * 2

    for bomb in Bombs.bombs:
        center_x = mapRenderX + ((Map.tile_size / 64) * bomb["x"])
        center_y = mapRenderY + ((Map.tile_size / 64) * bomb["y"])

        objects.append(create_image_view_data(
            "explosion_range",

            center_x - (explode_range_size / 2),
            center_y - (explode_range_size / 2),

            explode_range_size,
            explode_range_size
        ))

        objects.append(create_image_view_data(
            "bomb_flash" if int(bomb["countdown"] / BOMB_FLASH_LENGTH) % (BOMB_FLASH_INTERVAL) == 0 else "bomb",

            center_x - (bomb_size / 2),
            center_y - (bomb_size / 2),

            bomb_size,
            bomb_size
        ))

        points = [[center_x + (Map.tile_size * 0.015), center_y + (Map.tile_size * 0.1)]]

        for i in range(int((360 / BOMB_COUNTDOWN) * (BOMB_COUNTDOWN - bomb["countdown"]))):
            points.append([
                (center_x + (Map.tile_size * 0.015)) + ((Map.tile_size * 0.15) * math.cos(math.radians(i - 90))),
                (center_y + (Map.tile_size * 0.1)) + ((Map.tile_size * 0.15) * math.sin(math.radians(i - 90)))
            ])

        if (len(points) >= 3):
            objects.append(create_polygon_view_data(
                "bomb_countdown",

                points,

                '#b00e0e'
            ))

    # Render Players 

    font = pygame.font.Font(None, round(Map.tile_size * 0.5))

    font.set_bold(True)

    for player in players:
        render_x = mapRenderX + (((Map.tile_size / 64) * player.x) - (player.player_size / 2))
        render_y = mapRenderY + (((Map.tile_size / 64) * player.y) - (player.player_size / 2))

        if player.angle != 0:
            render_x -= player.player_size / 8
            render_y -= player.player_size / 8

        objects.append(create_image_view_data(
            "player",

            render_x,
            render_y,

            player.player_size,
            player.player_size,

            player.angle
        ))

        # Render the player name

        size = font.size(player.name)

        objects.append(create_text_view_data(
            player.name,

            int(mapRenderX + (((Map.tile_size / 64) * player.x) - (size[0] / 2))),
            int(mapRenderY + (((Map.tile_size / 64) * player.y) - (player.player_size * 0.9))),

            '#19d44b',

            str(round(Map.tile_size * 0.5)) + 'px Bold'
        ))

    explosion_cloud_size = Map.tile_size * 2

    for explosion_cloud in Bombs.explosion_clouds:
        objects.append(create_image_view_data(
            "explosion_" + str(explosion_cloud["animation"]),

            mapRenderX + (((Map.tile_size / 64) * explosion_cloud["x"]) - (explosion_cloud_size / 2)),
            mapRenderY + (((Map.tile_size / 64) * explosion_cloud["y"]) - (explosion_cloud_size / 2)),

            explosion_cloud_size,
            explosion_cloud_size
        ))

    ui_size = (width + height) / 100

    text_x = ui_size

    for player in players:
        objects.append(create_text_view_data(
           player.name + ': ' + str(player.score),

           text_x,
           ui_size * 0.75,

           '#ffffff',

           str(round(ui_size * 2.5)) + 'px Bold'
        ))

        bomb_x = text_x
        bomb_y = ui_size * 2.5

        for i in range(player.bombs):
            objects.append(create_image_view_data(
                'bomb_icon',

                bomb_x,
                bomb_y,

                ui_size * 1.5,
                ui_size * 1.5
            ))

            bomb_x += ui_size * 1.25

            if (bomb_x + (ui_size * 1.25) >= text_x + ((width - (ui_size * 2)) / len(players)) or bomb_x + (ui_size * 1.25) >= width):
                bomb_x = text_x
                bomb_y += ui_size * 1.5

        text_x += (width - (ui_size * 2)) / len(players)

    return objects
