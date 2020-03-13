import tcod as libtcod
from input_handler import handle_keys

def main():
    #size of screen width/height for console initilization 
    screen_width = 80
    screen_height = 50

    #keeps track of player position on the map
    player_x = int(screen_width/2)
    player_y = int(screen_height/2)

    #sets font 
    libtcod.console_set_custom_font(fontFile='arial12x12.png', flags=libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    #initializes the console
    libtcod.console_init_root(w=screen_width, h=screen_height, title='libtcod alpha roguelike', fullscreen=False)

    #defines width/height as a console
    con = libtcod.console_new(w=screen_width, h=screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    #main game loop
    while not libtcod.console_is_window_closed():
        #checks for a key press
        libtcod.sys_check_for_event(mask=libtcod.EVENT_KEY_PRESS, k=key, m=mouse)

        #initializes the map, spawns player based on (x,y), blit(draws) player on the map, flush, spawns player again based on (x,y)
        libtcod.console_set_default_foreground(con=con, col=libtcod.white)
        libtcod.console_put_char(con=con, x=player_x, y=player_y, c='@', flag=libtcod.BKGND_NONE)
        libtcod.console_blit(src=con, x=0, y=0, w=screen_width, h=screen_height, dst=0, xdst=0, ydst=0)

        libtcod.console_flush()

        libtcod.console_put_char(con=con, x=player_x, y=player_y, c=' ', flag=libtcod.BKGND_NONE)

        #imported from input_handler, handles input commands
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #changes player position based on input command, allows graceful exit, fullscreen toggle
        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


#initialize code
if __name__ == '__main__':
    main()
