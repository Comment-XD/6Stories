class Floor:
    
    def __init__(self, head, *args, dimX = 3, dimY = 3) -> None:
        self._rooms = args #gonna be a list of room objects
        self._total_rooms = len(self._rooms) #
        self._status = False
        
        # Might not need floor size, actually will do but does not need to be big
        
        self.head = head  # the beginning of the floor
        self.dimX = dimX
        self.dimY = dimY
        
        # self.area = [[None for _ in range(dimX)] for _ in range(dimY)]
        
    
    def placing_rooms(self):
        # placing the rooms in certain segments
        pass
    
    def add_rooms(self, room, posX, posY):
        self._rooms.append(room)
        self.area[posX][posY] = room
    
    def completed_rooms(self):
        for i,room in enumerate(self.rooms):
            if room.status == True:
                self.rooms.pop(i)
                self.total_rooms -= 1
                
    
    def find_room(self, id):
        for room in self.rooms:
            if room.id == id:
                return room
            
        return None
    
    def status_clear(self):
        if self.total_rooms <= 0:
            self.status = True
        return self.status
    
    def get_rooms(self):
        return self.rooms
    
    def __str__(self) -> str:
        return "Floor"