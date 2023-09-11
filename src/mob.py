from src.player import Mob

class Office_Worker(Mob):
    def __init__(self, name, mob_drop_percentage, room=None) -> None:
        super().__init__(name, mob_drop_percentage, room=None)
        
        self.hp = 2
        self.maxHp = 2
        self.defence = 1
        self.vision_range = 1
        
        self.loot = []
        self.cache = [None]

    
    def __str__(self) -> str:
        return "O"

class Kitchen_Worker(Mob):
    def __init__(mob_drop_percentage, self, room=None) -> None:
        super().__init__(mob_drop_percentage, room=None)
        
        self.hp = 3
        self.maxHp = 3
        self.defence = 1
        self.vision_range = 1
        
        self.loot = []
        self.cache = [None]

    
    def __str__(self) -> str:
        return "K"

class Zombie(Mob):
    def __init__(mob_drop_percentage, self, room=None) -> None:
        super().__init__(mob_drop_percentage, room=None)
        
        self.hp = 5
        self.maxHp = 5
        self.defence = 2
        self.vision_range = 1
        
        self.loot = []
        self.cache = [None]
    
    def __str__(self) -> str:
        return "Z"

    
    
        