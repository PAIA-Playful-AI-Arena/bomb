from collections.abc import MutableSequence
import pygame

from mlgame.view.view_model import create_text_view_data, create_image_view_data

from .objects import *

# Render The Game
def render(width: int, height: int, Map: Map, players: MutableSequence[Player]):
    objects = []

    # Render The Map

    renderX = round((width / 2) - ((Map.width / 2) * Map.tileSize), 0)
    renderY = round((height / 2) - ((Map.height / 2) * Map.tileSize), 0)

    for y in range(Map.height):
        renderX = round(width / 2) - ((Map.width / 2) * Map.tileSize)

        for x in range(Map.width):
            backgroundTile = Map.TILE_TYPES[Map.getBackgroundTile(x, y)]
            foregroundTile = Map.TILE_TYPES[Map.getForegroundTile(x, y)]

            if (backgroundTile != None):
                objects.append(create_image_view_data(backgroundTile, renderX, renderY, Map.tileSize, Map.tileSize))

            if (foregroundTile != None):
                objects.append(create_image_view_data(foregroundTile, renderX, renderY, Map.tileSize, Map.tileSize))

            renderX += round(Map.tileSize, 0)

        renderY += round(Map.tileSize, 0)

    # Render Players

    mapRenderX = round((width / 2) - ((Map.width / 2) * Map.tileSize), 0)
    mapRenderY = round((height / 2) - ((Map.height / 2) * Map.tileSize), 0)

    font = pygame.font.Font(None, round(Map.tileSize * 0.5))

    font.set_bold(True)

    for player in players:
        renderX = mapRenderX + (((Map.tileSize / 64) * player.x) - (player.playerSize / 2))
        renderY = mapRenderY + (((Map.tileSize / 64) * player.y) - (player.playerSize / 2))

        if player.angle != 0:
            renderY -= player.playerSize / 8

        objects.append(create_image_view_data(
            'player',

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
