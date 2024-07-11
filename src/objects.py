import abc

from mlgame.view.view_model import Scene, create_rect_view_data

# The Object Template
class Template:
    @abc.abstractmethod
    def render (self, width: int, height: int, objects):
        return


# The Map Object
class Map(Template):
    def __init__ (self, mapWidth: int = 75, mapHeight: int = 50, tileSize: int = 5):
        # Initialize the map.

        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.tileSize = tileSize

        self.tiles = []

        for i in range(mapWidth * mapHeight):
            self.tiles.append('empty')

    # Render The Object
    def render(self, width, height, objects):
        i = 0

        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                objects.append(create_rect_view_data(
                    'tile',

                    int(width / 2) + int((x - (self.mapWidth / 2)) * self.tileSize),
                    int(height / 2) + int((y - (self.mapHeight / 2)) * self.tileSize),

                    self.tileSize,
                    self.tileSize,

                    '#ffffff'
                ))

                i += 1

