class Item:
    def __init__(self, name:str, desc:str, position, count:int) -> None:
        self.name = name
        self.desc = desc
        self.posX, self.posY = position
        self.count = count
        
    def empty(self):
        return self.count == 0
            
    def __str__(self) -> str:
        return f"""{self.name} 
    
Description
~~~~~~~~~~~
{self.desc}"""
    
class Healing_Item(Item):
    def __init__(self, name, desc, position, count, healing) -> None:
        super().__init__(name, desc, position, count)
        self.healing = healing
        
    def __str__(self) -> str:
        return "+"

class Damage_Item(Item):
    def __init__(self, name, desc, position, count, damage) -> None:
        super().__init__(name, desc, position, count)
        self.damage = damage
        
    def __str__(self) -> str:
        return "-"

class Buff_Item(Item):
    def __init__(self, name, desc, position, count, defence) -> None:
        super().__init__(name, desc, position, count)
        self.defence = defence
        
    def __str__(self) -> str:
        return "^"
    
class Gear_Item(Item):
    def __init__(self, name, desc, position, count, stats) -> None:
        super().__init__(name, desc, position, count)
        self.stats = stats
        
    def __str__(self) -> str:
        return "@"
