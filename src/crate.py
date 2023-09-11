class Crate:
    def __init__(self, position, loot) -> None:
        self.posX, self.posY = position
        self.loot = loot
    
    def __str__(self) -> str:
        return "#"
    
    