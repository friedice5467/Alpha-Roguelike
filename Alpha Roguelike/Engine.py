import tcod as libtcod

from map_objects.game_map import *
from render_function import *
from entity import Entity
from input_handler import handle_keys

def main():
    #size of screen/map width/height for console initilization 
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    #defines room variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    #defines colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    #keeps track of position of player and npc on the map on the map
    player = Entity(int(screen_width/2), int(screen_height/2), "@", libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]    

    #sets font 
    libtcod.console_set_custom_font(fontFile='arial12x12.png', flags=libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    #initializes the console
    libtcod.console_init_root(w=screen_width, h=screen_height, title='libtcod alpha roguelike', fullscreen=False)

    #defines width/height as a console
    con = libtcod.console_new(w=screen_width, h=screen_height)\
    
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    #main game loop
    while not libtcod.console_is_window_closed():
        #checks for a key press
        libtcod.sys_check_for_event(mask=libtcod.EVENT_KEY_PRESS, k=key, m=mouse)

        #initializes render_all function from render_functions
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        libtcod.console_flush()

        clear_all(con, entities)

        #imported from input_handler, handles input commands
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #changes player position based on input command, allows graceful exit, fullscreen toggle
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


#initialize code
if __name__ == '__main__':
    main()



