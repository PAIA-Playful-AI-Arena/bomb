import random

# The Map Object
class Map:
    # Each tile type and their corresponding image ID.
    TILE_TYPES = {
        "empty": None,

        "ground_light": "ground_light",
        "ground_dark": "ground_dark",
        
        "barrel": "barrel"
    }

    def __init__(self, width: int = 10, height: int = 5): # 15 x 10
        self.width = width
        self.height = height

        self.tileSize = 0

        self.backgroundTiles = []
        self.foregroundTiles = [] 
        
        for _ in range(width * height):
            if random.randint(0, 2) > 0:
                self.backgroundTiles.append('ground_dark')
            else:
                self.backgroundTiles.append('ground_light')

            self.foregroundTiles.append('empty')

    # Calculate Tile Size
    def calculateTileSize(self, width: int, height: int):
        self.tileSize = 0

        if width > height:
            self.tileSize = width / (self.width + 1)
        else:
            self.tileSize = height / (self.height + 1)

        if self.tileSize * self.width > width:
            self.tileSize = width / (self.width + 1)
        elif self.tileSize * self.height > height:
            self.tileSize = height / (self.height + 1)

    # Set The Background Tile At The Specified Position
    def setBackgroundTile(self, x: int, y: int, type: str):
        self.backgroundTiles[x + (y * self.width)] = type

    # Set The Foreground Tile At The Specified Position
    def setForegroundTile(self, x: int, y: int, type: str):
        self.foregroundTiles[x + (y * self.width)] = type

    # Get The Background Tile At The Specified Position
    def getBackgroundTile(self, x: int, y: int):
        return self.backgroundTiles[x + (y * self.width)]

    # Get The Foreground Tile At The Specified Position
    def getForegroundTile(self, x: int, y: int):
        return self.foregroundTiles[x + (y * self.width)]

class Player:
    def __init__(self, Map: Map, name: str):
        self.name = name
        self.score = 0

        # The position of the player is "virtual", the "virtual" size of each tile is 64 x 64 pixels.
        self.x = 32
        self.y = 32
        self.angle = 0

        self.rotateDirection = -1

        self.Map = Map

    # Set The Position Of The Player
    def setPosition (self, x: int, y: int):
        self.x = x
        self.y = y

    # Move The Player
    def move(self, x: int, y: int):
        self.x += x
        self.y += y

        if self.x - (self.Map.tileSize / 3) < 0:
            self.x = self.Map.tileSize / 3
        elif self.x + (self.Map.tileSize / 3) > self.Map.width * 64:
            self.x = (self.Map.width * 64) - (self.Map.tileSize / 3)

        if self.y - (self.Map.tileSize / 2) < 0:
            self.y = self.Map.tileSize / 2
        elif self.y + (self.Map.tileSize / 2) > self.Map.height * 64:
            self.y = (self.Map.height * 64) - (self.Map.tileSize / 2)

        if x == 0 and y == 0:
            self.angle = 0
        else:
            self.angle += self.rotateDirection

            if self.angle > 0.5:
                self.rotateDirection = -0.15
            elif self.angle < -0.5:
                self.rotateDirection = 0.15
