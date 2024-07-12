from collections.abc import MutableSequence
import pygame

from mlgame.view.view_model import create_text_view_data, create_image_view_data

from .objects import *

# Render The Game
def render(width: int, height: int, Map: Map, Bombs: Bombs, players: MutableSequence[Player]):
    objects = []

    # Render The Map

    mapRenderX = round((width / 2) - ((Map.width / 2) * Map.tileSize), 0)
    mapRenderY = round((height / 2) - ((Map.height / 2) * Map.tileSize), 0)

    renderX = mapRenderX 
    renderY = mapRenderY 

    for y in range(Map.height):
        renderX = mapRenderX

        for x in range(Map.width):
            background_tile = Map.TILE_TYPES[Map.get_background_tile(x, y)]
            foreground_tile = Map.TILE_TYPES[Map.get_foreground_tile(x, y)]

            if (background_tile != None):
                objects.append(create_image_view_data(background_tile, renderX, renderY, Map.tileSize, Map.tileSize))

            if (foreground_tile != None):
                objects.append(create_image_view_data(foreground_tile, renderX, renderY, Map.tileSize, Map.tileSize))

            renderX += round(Map.tileSize, 0)

        renderY += round(Map.tileSize, 0)

    # Render Bombs

    bombSize = Map.tileSize * 0.75

    for bomb in Bombs.bombs:
        objects.append(create_image_view_data(
            "bomb",

            mapRenderX + (((Map.tileSize / 64) * bomb["x"]) - (bombSize / 2)),
            mapRenderY + (((Map.tileSize / 64) * bomb["y"]) - (bombSize / 2)),

            bombSize,
            bombSize
        ))

    # Render Players 

    font = pygame.font.Font(None, round(Map.tileSize * 0.5))

    font.set_bold(True)

    for player in players:
        renderX = mapRenderX + (((Map.tileSize / 64) * player.x) - (player.playerSize / 2))
        renderY = mapRenderY + (((Map.tileSize / 64) * player.y) - (player.playerSize / 2))

        if player.angle != 0:
            renderX -= player.playerSize / 8
            renderY -= player.playerSize / 8

        objects.append(create_image_view_data(
            "player",

            renderX,
            renderY,

            player.playerSize,
            player.playerSize,

            player.angle
        ))

        size = font.size(player.name)

        objects.append(create_text_view_data(
            player.name,

            int(mapRenderX + (((Map.tileSize / 64) * player.x) - (size[0] / 2))),
            int(mapRenderY + (((Map.tileSize / 64) * player.y) - (player.playerSize * 0.9))),

            '#19d44b',

            str(round(Map.tileSize * 0.5)) + 'px Bold'
        ))

    return objects
