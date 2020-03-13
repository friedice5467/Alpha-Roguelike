import tcod as libtcod
from input_handler import handle_keys

def main():
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width/2)
    player_y = int(screen_height/2)

    libtcod.console_set_custom_font(fontFile='arial12x12.png', flags=libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(w=screen_width, h=screen_height, title='libtcod alpha roguelike', fullscreen=False)

    con = libtcod.console_new(w=screen_width, h=screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(mask=libtcod.EVENT_KEY_PRESS, k=key, m=mouse)

        libtcod.console_set_default_foreground(con=con, col=libtcod.white)
        libtcod.console_put_char(con=con, x=player_x, y=player_y, c='@', flag=libtcod.BKGND_NONE)
        libtcod.console_blit(src=con, x=0, y=0, w=screen_width, h=screen_height, dst=0, xdst=0, ydst=0)

        libtcod.console_flush()

        libtcod.console_put_char(con=con, x=player_x, y=player_y, c=' ', flag=libtcod.BKGND_NONE)

        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
