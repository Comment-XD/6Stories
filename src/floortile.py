class Floor_Tile:
    def __init__(self, x, y) -> None:
        self.posX = x
        self.posY = y
        
    def __str__(self) -> str:
        return "_"