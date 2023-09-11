from src.item import*
from src.generator import Generator
from src.crate import Crate
from src.floortile import Floor_Tile
from src.gate import Gate
from src.weapon import Weapon

import numpy as np
import random 

class Player:
    def __init__(self, name, room=None) -> None:
        self.name = name
        
        self.inventory = set()
        
        self.weapon_list = [Weapon("Sword", "A short range weapon that does small damage", 1,1), None]
        self.weapon_slot = 0
        self.weapon = self.weapon_list[self.weapon_slot]
        
        self.hp = 5
        self.maxHp = 5
        self.defence = 1
        self.vision_range = 2 #default should be 2
        self.vision_direction = "up"
        self.attack_phase = False
        
        self.posX = 0
        self.posY = 0
        
        self.cache = [None]
        self.room = room
        
        
        # self.room.spawn_player(self) #sets the player position where he spawns
    
    # Inventory Methods
    def inventoryStr(self):
        str = "Inventory\n"
        for item in self.inventory:
            str += f"{item.name}: {item.count} \n"
        
        if str == "Inventory\n":
            str += "None"
        return str

    
    def is_dead(self):
        return self.hp <= 0
    
    #Crate Methods
    def pickup_crate_item(self, crate, item):
        for i, loot in enumerate(crate.loot):
            if loot.name == item:
                self.inventory.add(loot)
                crate.loot.pop(i)
                break
            
    def pickip_all_crate_items(self, crate):
        for loot in crate.loot:
            self.inventory.add(loot)

        crate.loot = []
        
    # Item Methods
    def add_item(self, item):
        self.inventory.add(item)
    
    def remove_item(self, i):
        for item in self.inventory:
                if item.name == i:
                    self.inventory.discard(item)
                    return item
                
        return None
    
    
    def find_item(self, i):
        for item in self.inventory:
            if item.name == i:
                return item
            
        return None
    
    def use(self, item):
        # bunch of isinstance statements to determine what item it is
        if isinstance(item, Healing_Item):
            self.hp += item.healing
            if self.hp > self.maxHp:
                self.hp = self.maxHp
        if isinstance(item, Damage_Item):
            self.weapon.dmg += item.dmg
        if isinstance(item, Buff_Item):
            self.defence += item.defence
        if isinstance(item, Gear_Item):
            # make sure the player is working on a gen if not cannot use the item at the momement
            pass
        
        item.count -= 1
        if item.empty():
            self.remove_item(item)
    
    # Vision Methods
    def vision(self):
        vision = 0
        
        room = np.array(self.room.area)
        # consider the vision when the player is hugging the wall
        # [column height beginning value:column height ending value, row width starting value:row width ending value]
        # filter removes unneccesary empty list within list
        # Could be made into a dictionary for easier readibility
        
        
        if self.vision_direction == "up":
            vision = room[max(0, self.posX - self.vision_range):self.posX, max(0,self.posY - 1):self.posY + 2]
        elif self.vision_direction == "down":
            vision = room[self.posX + 1:max(0, self.posX + self.vision_range + 1), max(0,self.posY - 1):self.posY + 2]
        elif self.vision_direction == "right":
            vision = room[max(0, self.posX - 1):self.posX + 2, self.posY + 1:self.posY + self.vision_range + 1]
        elif self.vision_direction == "left":
            vision = room[max(0, self.posX - 1):self.posX + 2, max(0, self.posY - self.vision_range):self.posY]
        
        return vision

    def vision_bar(self):
        vision = self.vision().tolist()
        visionStr = f"Vision {self.vision_direction.capitalize()} \n  "
        if len(vision) == 0:
            return visionStr
        
        for j in range(len(vision[0])):
            visionStr += f"{j} "
        
        visionStr += "\n"
        
        for i, row in enumerate(vision):
            
            visionStr += f"{i} "
            
            for object in row:
                visionStr += f"{object} "
            
            visionStr += "\n"
        
        visionStr += f"Standing On: {self.cache[-1]}\n"
        return visionStr
            

    def set_vision_direction(self, direction) -> None:
        # sets the direction of your vision
        if direction in ["up", "down", "left", "right"] :
            self.vision_direction = direction
    
    def options(self) -> str:
        # idk if this is neccesary 
        
        vision = self.vision()
        gen_list = []
        item_list = []
        crate_list = []
        tile_list = []
        
        
        for objects in vision:
            if isinstance(objects, Generator):
                gen_list.append(objects)
            elif isinstance(objects, Item):
               item_list.append(objects)
            elif isinstance(objects, Crate):
                crate_list.append(objects)
            else:
                tile_list.append(object)
                
    
        options = {"Tiles": tile_list,
                   "Generators": gen_list,
                   "Crates": crate_list,
                   "Items": item_list}
        
        return options
    
    
    #Movement Methods
    
    def stay(self):
        """
        if isinstance(item, Player)
        """
        pass
    
    def move(self, location=None):
        # determine if the player and the mob is at the same location
        # if player stays and mob leaves, mob needs to append player into cache, when leave 
        # if player leaves to attack mob, and mob dies,player.deletes mob from cache[-1], player.append mob.cache[-1] 
        # if it finds an object, whether take be a crate, generator or item, moves to that location
        """
        1. move to a location, 
        2. choose whether to do that action
        3. Repeat cycle
        
        
        Example:
        - move to a tile, 
        - tile action has nothing
        - do nothing
        
        - move to a gen
        - gen action is to do a gen
        - do a gen, or dont do a gen
        
        [tile, player, mob] -> move to a location and then choose to attack, 
        player leaves, does not attack mob
            - replace original position with player.cache[-1], player.pop(), player.append(new_position)
            - if player.cache[-1] is a mob, player.pop(), replace original position with player.cache[-1], player.pop(), player.append(new_position)
                - mob.cache.pop() because no longer on player
        player stays, does not attack mob
            - should not change self.cache at all
        player leaves, attacks mob
            - player.append(mob), mob.append(player)
            - if mob dies, remove player from mob.cache[-1], removes mob from player.cache[-1], 
                - replace original position with player.cache[-1], player.pop(), take in whatever tile mob.cache[-1] has
            - if mob not dies, player.cache[-1] = mob, mob.cache[-1] = player
            
        player stays, attacks mob
            - player cache[-1] should be mob, mob.cache[-1] should be player,
            - if mob dies, remove mob from player.cache, no need to take in anything from mob as player should have original position 
            - if mob not dies, player.cache[-1] = mob, mob.cache[-1] = player

        mob stays, does not attack player
        mob leaves, does not attack player
            -if mob.cache[-1] is a player, mob.pop(), replace original position with mob.cache[-1], mob.pop(), mob.append(new_position)
                - player.cache.pop() because no longer on mob
        
        mob leaves, attacks player
            - replaces original position with its cache[-1], mob.append(player), player.append(mob)
        mob stays, attacks player
        
        
        attack_phase, when player is attacking a mob, attack_phase = True:
        When mob leaves the player or player leaves the mob, attack_phase = False
            player.attack(mob)
                - mob.cache.append(player)
                - player.cache.append(mob)
            
        
        tile has an attribute called heirachy = [None]
        tile.heirachy stores which comes first, if None return Tile, if not return 
        
        use position to decide if the player moved to a location to attack or stayed at a location and attacked
        need a way to determine 
        - player moved to attack a mob
        - player stayed to attack a mob
        - player moved, but did not attack a mob
        - player stayed, and there was no mob
        
        room.attack_phase?
        
        
        
        """
        
        if location is not None: 
            # player / mob moves to a different spot

            og_posX = self.posX
            og_posY = self.posY
            
            visionX, visionY = location 
            vision = self.vision()

           
            #gets the item at that vision location
            item = self.get_item(visionX, visionY, vision)
            
             # takes the item's absolute position and set it to the player's position of the place u want to go
            self.posX = item.posX
            self.posY = item.posY
            if isinstance(self.cache[-1], Player):
                self.pop
            
            self.room.area[og_posX][og_posY] = self.cache[-1]
            self.cache.pop()
            
        else:  
            #player / mob stayed at the position it is at
            item = self.get_cache() 
            self.room.area[self.posX][self.posY] = self.cache[-1]
            self.cache.pop()

        # isinstance statements go br....
        if isinstance(item, Generator):
            
            # dots = "....."
            # work_gen_str = f"Working Gen {item.id}{dots}" later stuff to work on
            
            inv_item = self.find_item("Rusty Gear")
            
            if inv_item is None or (self.posX != item.posX and self.posY != item.posY):
                print("No gear found in inventory")
                self.cache.append(item) #saves the generator into a temporary list
            else:
                item.set_status(True) #Sets the Generator as completed
                self.cache.append(Floor_Tile(item.posX, item.posY))
                self.use(inv_item) #uses the item
                
        
        elif isinstance(item, Item):
            self.add_item(item)
            self.cache.append(Floor_Tile(item.posX, item.posY))
        
        elif isinstance(item, Crate):
            self.cache.append(item)
            self.pickip_all_crate_items(item)
            # this method depends
            
        elif isinstance(item, Player):
            self.attack(item)
        
        elif isinstance(item, Gate):
            self.cache.append(item)
            if item.type == "next":
                self.next()
            elif item.type == "back":
                self.back()
            else:
                print("You have reached the wall")
        
        else:   
            self.cache.append(item)
            
        self.room.area[self.posX][self.posY] = self
    
    
    def get_item(self, x, y, vision):
        return vision[x][y]

    def get_cache(self):
        return self.cache[-1]

    # Room Methods
    def enter(self, room):
        self.room = room
    
    def next(self): 
        self.room = self.room.next
    
    def back(self):
        self.room = self.room.back
    
    
    #Weapon Methods
    def attack(self, mob):
        vision = self.vision()
        
        # weapon range is base on the vision, 
        # if range = 1, anything in front or at the player can be attack,
        # if range = 2, anything within the vision range can be attacked
        
        mob.hp -= self.weapon.dmg
        mob.cache.append(self)
        self.cache.append(mob)
        
        if mob.is_dead():
            mob.cache.pop()
            self.cache.pop()
            
            # need to check if the player moved to attack the mob
            
            # need to check if the player stayed to attack the mob
            
        else:
            mob.cache[-1] = self
            self.cache[-1] = mob
            
        
        # if mob.is_dead():
        #     if isinstance(mob, Player):
        #         self.cache.remove(mob)
        #         mob.cache.remove(self)
                
        #     self.room.active_mobs.remove(mob)
        #     self.room.total_mobs_in_room -= 1 # counts the total mobs in the room
        #     self.room.area[mob.posX][mob.posY] = mob.cache[-1]
        #     self.cache.append(mob.cache[-1])
        #     mob.cache.pop()
        # else:
        #     if not isinstance(self.cache[-1], Player):
        #         self.cache.append(mob)
        #         mob.cache.append(self)
    
    def replace_weapon(self, weapon, weapon_slot):
        self.weapon_list[weapon_slot] = weapon
        
    def switch_weapon(self, weapon_slot):
        if weapon_slot not in [0,1] or self.weapon_list[weapon_slot] == None:
            pass
            # give exception error 
        else:
            self.weapon = self.weapon_list[weapon_slot]
            
    
    def __str__(self) -> str:
        return "*"


class Mob(Player):
    def __init__(self, name, mob_drop_percentage, room=None) -> None:
        super().__init__(name, room=None)
        
        self.cache = [None]
        self.mob_drop_percentage = mob_drop_percentage
         
    def attack(self, player):
        #override attack method
        vision = self.vision()
        
        # weapon range is base on the vision, 
        # if range = 1, anything in front or at the player can be attack,
        # if range = 2, anything within the vision range can be attacked
        
        player.hp -= self.weapon.dmg
        print(player.is_dead()) # printed false
        if player.is_dead():
            self.room.area[player.posX][player.posY] = player.cache[-1]
            self.cache.append(player.cache[-1])
            player.cache.pop()
        else:
            if not isinstance(player.cache[-1], Player):
                player.cache.append(self)
                self.cache.append(player)
    
    def follow_player(self):
        #  if it sees player, attack, if it doesnt, move to a random tile spot
        # should move to a tile spot
        print(self.cache)
        self.vision_direction = random.choice(["up", "down", "left", "right"])
        vision = self.vision()
        vision_len = self.vision().size
        
        while vision_len == 0:
            self.vision_direction = random.choice(["up", "down", "left", "right"])
            vision = self.vision()
            vision_len = vision.size
            # print(vision_len)

        # print(self.cache)
        # print(self.vision_bar())
        player_found = False
        tile_list = []
        
        for i, row in enumerate(vision):
            for j, obj in enumerate(row):
                if isinstance(obj, Player) and not isinstance(obj, Mob):
                    player_found = True
                    self.move((i,j)) #moves in the vision
                    break
                
                if isinstance(obj, Floor_Tile):
                    tile_list.append((i,j))
                
        if not player_found:
            tile = random.choice(tile_list)
            self.move(tile)
    



    