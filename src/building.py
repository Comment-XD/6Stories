class Building:
    def __init__(self, *args) -> None:
        self.floors = args
        self.total_floors = len(self.floors)
        self.players_floor = 0
    
    def increase_player_floor(self):
        self.players_floor += 1
    
    def player_floor(self):
        return self.floors[self.player_floor]
        
    def get_floors(self):
        return self.floors
    
    def __str__(self) -> str:
        return "Building"