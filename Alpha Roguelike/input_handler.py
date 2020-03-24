import tcod as libtcod


from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)
    #horizontal and vertical movement keys; ^ V < > in that order
    if  key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
        return {'move': (1, 0)}

    #diagonal movement keys
    elif key.vk == libtcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key.vk == libtcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key.vk == libtcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key.vk == libtcod.KEY_KP3:
        return {'move': (1, 1)}

    #action commands
    if key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    if key.vk ==libtcod.KEY_ENTER and key.lalt:
        #alt+enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        #exit the game
        return {'exit': True}

    #no key was pressed
    return{}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}
