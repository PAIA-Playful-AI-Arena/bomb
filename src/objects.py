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

    def __init__(self, width: int = 15, height: int = 10): # 15 x 10
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

    # Get All The Foreground Tiles
    def getForegroundTiles(self):
        tiles = []

        i = 0
 
        for y in range(self.height):
            for x in range(self.width):
                if self.foregroundTiles[i] != "empty":
                    tiles.append({ "type": self.foregroundTiles[i], "x": x, "y": y })

                i += 1


        return tiles

class Player:
    def __init__(self, Map: Map, name: str):
        self.name = name
        self.score = 0

        # The position of the player is "virtual", the "virtual" size of each tile is 64 x 64 pixels.
        self.x = 32
        self.y = 32

        self.angle = 0
        self.rotateDirection = -1

        self.playerSize = Map.tileSize * 0.9

        self.Map = Map

    # Set The Position Of The Player
    def setPosition (self, x: int, y: int):
        self.x = x
        self.y = y

    # Move The Player
    def move(self, x: int, y: int):
        # Check map forground tiles collision

        self.x += x 

        for tile in self.Map.getForegroundTiles():
            if checkRectCollision(
                { "x": self.x - (64 / 3), "y": self.y - (64 / 2), "width": 64 / 1.5, "height": 64 },
                { "x": tile["x"] * 64, "y": tile["y"] * 64, "width": 64, "height": 64 }
            ):
                if self.x - (64 / 3) < tile["x"] + 64 or self.x + (64 / 1.5) > tile["x"]:
                    self.x -= x


                break

        self.y += y

        for tile in self.Map.getForegroundTiles():
            if checkRectCollision(
                { "x": self.x - (64 / 3), "y": self.y - (64 / 2), "width": 64 / 1.5, "height": 64 },
                { "x": tile["x"] * 64, "y": tile["y"] * 64, "width": 64, "height": 64 }
            ):
                if self.y - (64 / 2) < tile["y"] + 64 or self.y + (64 / 2) > tile["y"]:
                    self.y -= y


                break

        # Check map edges collision

        if self.x - (64 / 3) < 0:
            self.x = 64 / 3
        elif self.x + (64 / 3) > self.Map.width * 64:
            self.x = (self.Map.width * 64) - (64 / 3)

        if self.y - (64 / 2) < 0:
            self.y = 64 / 2
        elif self.y + (64 / 2) > self.Map.height * 64:
            self.y = (self.Map.height * 64) - (64 / 2) 


        if x == 0 and y == 0:
            self.angle = 0
        else:
            self.angle += self.rotateDirection

            if self.angle > 0.5:
                self.rotateDirection = -0.15
            elif self.angle < -0.5:
                self.rotateDirection = 0.15

# Check The Collision Between Two Rectangles
def checkRectCollision(rect1, rect2):
    rect1_right = rect1['x'] + rect1['width']
    rect1_bottom = rect1['y'] + rect1['height']
    rect2_right = rect2['x'] + rect2['width']
    rect2_bottom = rect2['y'] + rect2['height']

    if rect1['x'] >= rect2_right or rect2['x'] >= rect1_right:
        return False
    if rect1['y'] >= rect2_bottom or rect2['y'] >= rect1_bottom:
        return False

    return True
