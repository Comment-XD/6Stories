class Generator:
    newid = 0
    
    def __init__(self, posX, posY) -> None:
        self.id = Generator.newid
        Generator.newid += 1
        
        self.status = False
        
        self.posX = posX
        self.posY = posY

    def set_status(self, status):
        self.status = status
    
    def __str__(self) -> str:
        return "G"