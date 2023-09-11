# 6 Stories
# Started: 9/8/23
# Completed: 


from src.building import Building
from src.floor import Floor
from src.room import Room
from src.player import*
from src.item import*
from src.generator import Generator
from src.crate import Crate
from src.gate import Gate
from src.mob import*



room = Room("Office Workspace", Gate((2,4), "next"), 1, 1, [Office_Worker("Bob", 10)]) #bruh what is this

room.place_gen(Generator(1,4))
room.place_gen(Generator(3,4))
room.place_item(Healing_Item("Health Pot", "Heal yourself for +2", (1, 1), 2, 1))
room.place_crate(Crate((3,2),[Gear_Item("Rusty Gear", "A Rusty Gear that can mildy speedup Generators by 10 percent", (None, None), 2, 5)]))

room2 = Room("Bar", Gate((2,4), "back"), 1, 1, [Office_Worker("Bob", 10)])
room2.place_gen(Generator(1,4))
room2.place_gen(Generator(3,4))

room.next = room2
room2.back = room

floor_1 = Floor(room)
main_building = Building([floor_1])
player = Player("PlayerUno", room)

player.enter(room)
room.spawn_player(player)

while True:
    
    print(f"""Player Position 
x:{player.posX} y:{player.posY}
""")
    
    vision_dir = input("Which direction do you want to see (up, down, left, right): ")
    
    player.set_vision_direction(vision_dir)
    print(player.vision_bar())
    
    move_choice = input("Where do you want to move (Standing On, Vision): ")
    
    if move_choice == "v":
        position = (int(num) for num in input("Where do you want to move (row, column): ").split(","))
        player.move(position)
    
    else:
        player.move()
        
    if player.room.total_mobs_in_room == 0:
        player.room.spawn_mobs()
    
    player.room.mob_script()
    
    # print(player.inventoryStr())
    print(player.cache)
    if player.room.status_clear():
        print(f"Yay, you finished {player.room.name}")
    
    print(player.room)






