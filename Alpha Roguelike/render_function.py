import tcod as libtcod

def render_all(con, entities, game_map, screen_width, screen_height, colors):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                libtcod.console_set_char_background(con=con, x=x, y=y, col=colors.get('dark_wall'), flag=libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con=con, x=x, y=y, col=colors.get('dark_ground'), flag=libtcod.BKGND_SET)


    #draw all entities in the list
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(src=con,x=0,y=0,w=screen_width,h=screen_height,dst=0,xdst=0 ,ydst=0)

def clear_all(con, entities):
    #loop that calls clear entity
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con=con, x=entity.x, y=entity.y, c=entity.char, flag=libtcod.BKGND_NONE)

def clear_entity(con, entity):
    #erase the character that represents this object
    libtcod.console_put_char(con=con, x=entity.x, y=entity.y, c=' ', flag=libtcod.BKGND_NONE)