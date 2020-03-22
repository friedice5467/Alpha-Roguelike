import tcod as libtcod

from components.fighter import Fighter
from map_objects.game_map import *
from render_function import *
from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
from input_handler import handle_keys
from fov_functions import initialize_fov, recompute_fov

def main():
    #size of screen/map width/height for console initilization 
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    #defines the default room variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    #defines the default fov variables
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    
    #defines the max amount of monsters per room
    max_monsters_per_room = 3

    #defines colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    #keeps track of position of player and other objects on the map on the map
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, fighter=fighter_component)
    entities = [player]

    #sets font 
    libtcod.console_set_custom_font(fontFile='arial12x12.png', flags=libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    #initializes the console
    libtcod.console_init_root(w=screen_width, h=screen_height, title='libtcod alpha roguelike', fullscreen=False)

    #defines width/height as a console
    con = libtcod.console_new(w=screen_width, h=screen_height)\
    
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    #main game loop
    while not libtcod.console_is_window_closed():
        #checks for a key press
        libtcod.sys_check_for_event(mask=libtcod.EVENT_KEY_PRESS, k=key, m=mouse)

        #checks for fov refresh and refreshes
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        #initializes render_all function from render_functions
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        #imported from input_handler, handles input commands
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #changes player position based on input command, allows graceful exit, fullscreen toggle
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    entity.ai.take_turn(player, fov_map, game_map, entities)

            game_state = GameStates.PLAYERS_TURN

#initialize code
if __name__ == '__main__':
    main()
