from src.floortile import Floor_Tile
from src.player import*
import random

class Room:
    newid = 0
    
    def __init__(self, name, gate, floor_lvl, difficulty, mob_list=[], next=None, back=None, dimX=5, dimY=5) -> None:
        self.name = name
        
        self._id = Room.newid
        Room.newid += 1
        
        self.total_mobs_in_room = 0
        self.mob_list = mob_list
        self.active_mobs = []
        # the larger the index, the harder the mobs
        self._total_gens = 0
        self._gens = []
        
        self.difficulty = difficulty
        self._floor_lvl = floor_lvl
        self._status = False
        self._gate = gate
        
        self._dimX = dimX
        self._dimY = dimY
        self.area = [[Floor_Tile(x,y) for y in range(dimX)] for x in range(dimY)]
        self.area[gate.posX][gate.posY] = gate
        
        self.next = next
        self.back = back

    def spawn_player(self, player):
        player.posX = self._gate.posX
        player.posY = self._gate.posY
        player.cache.append(self._gate)
        #puts the player at the gate
        self.area[player.posX][player.posY] = player #temp for now, remember to change this for different gate spawns
        
    def spawn_mobs(self):
        
        for _ in range(self.difficulty):
            random_x = random.choice([i for i, _ in enumerate(self.area)])
            random_y = random.choice([i for i, _ in enumerate(self.area[0])])
            
            mob = random.choice(self.mob_list)
            self.active_mobs.append(mob)
            
            mob.posX = random_x
            mob.posY = random_y
            mob.room = self
            
            mob.cache.append(self.area[random_x][random_y])
            # mob gets the tiles and put it into there stache
            
            # mobs might spawn in the same location if there are multiple mobs so going to need a attribute that stores all the avaliable tiles in a room
            # should spawn in like the outer area row = 0,1 or len -1, len -2, same applies for column value
            
            self.area[random_x][random_y] = mob
        
        self.total_mobs_in_room = self.difficulty
        # difficulty of the room depends on how many mobs spawn in the room at a time
    
    def mob_script(self):
        # runs the mob.follow player
        for mob in self.active_mobs:
            mob.follow_player()
    
    def place_crate(self, crate):
        if isinstance(self.area[crate.posX][crate.posY], Floor_Tile):
            self.area[crate.posX][crate.posY] = crate
    
    def place_item(self, item):
        if isinstance(self.area[item.posX][item.posY], Floor_Tile):
            self.area[item.posX][item.posY] = item
 
    
    def place_gen(self, gen):
        if isinstance(self.area[gen.posX][gen.posY], Floor_Tile):
            self.area[gen.posX][gen.posY] = gen
            self._gens.append(gen)
            self._total_gens += 1

    def completed_gen(self):
        for i, gen in enumerate(self._gens):
            if gen.status == True:
                self._gens.pop(i)
                self._total_gens -= 1
        
    def status_clear(self):
        self.completed_gen()
        
        if self._total_gens == 0:
            self._status = True
        
        return self._status
    
        
    def __str__(self) -> str:
        room_str = ""
        for row in self.area:
            for tile in row:
                room_str += f"{tile} "
            room_str += "\n"
            
        return f"""{self.name}
{self._dimX} x {self._dimY} Space
Floor Level: {self._floor_lvl}
Number of Generator Left: {self._total_gens}
{room_str}"""
    