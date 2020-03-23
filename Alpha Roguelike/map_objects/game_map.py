import tcod as libtcod

from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from render_function import RenderOrder
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from random import randint

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]


        return tiles


    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                 max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            #random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            #random position without going out of boundaries
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            #'Rect' class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            #run through other rooms and check if they interact with new_room
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                #if loop did not break, i.e. there were no intersections
                #paint it to the map's tiles
                self.create_room(new_room)

                #center coordinates of new room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    #all rooms after the first:
                    #connect it to the previous room with a tunnel

                    #center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    #flip a coin (0, 1)
                    if randint(0, 1) == 1:
                        #first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_per_room)

                #finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    #create tunnels to go between rooms 
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        choice = randint(0, 1000)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)


            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if choice < 955:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    #create an orc at 95.5% chance
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                    render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=100, defense=3, power=6)
                    ai_component = BasicMonster()
                    #create a dragon at .5% chance
                    monster = Entity(x, y, 'd', libtcod.darker_red, 'Dragon', blocks=True, 
                                    render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)


    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
