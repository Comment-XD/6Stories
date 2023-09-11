class Gate:
    def __init__(self, position, type) -> None:
        self.posX, self.posY = position
        self.type = type
    
    # next gates move the the next room
    # back gates move to the previous room
    
    def __str__(self) -> str:
        return "|"