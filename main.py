
from vector import vec2
from screen import CursesScreen
from game import Game

import actions
import textwrap
import re


scr = CursesScreen()
game = Game()

map_size = vec2(10, 10)
# map_center = map_size // 2
map_center = vec2(0, 0)
map_view = None


@scr.init
def on_init(scr: CursesScreen):

    global map_view
    map_view = scr.create_view(0, 1, *map_size)


@scr.render
def on_render(scr: CursesScreen, key: str):

    global map_view

    game.send_key_press(key)

    width, height = scr.get_size()

    title = "~ Welcome to Super Fuck You ~"

    scr.draw_text(0, 0, title.center(width), style='standout')
    scr.draw_text(21, 2, (
        "Location: " + str(game.player.pos) + "\n"
        "Last Keypress: " + str(key)
    ))

    desc = re.sub(' +', ' ', game.get_description())

    scr.draw_text(21, 5, '\n'.join(textwrap.wrap(desc, width-21)))
    scr.draw_text(21, 9, actions.format_actions(game.get_actions()))

    # draw console messages
    con_y = 15  # start y position of console
    for msg in game.log:
        scr.draw_text(0, con_y, msg.text, style=msg.style, fg=msg.fg, bg=msg.bg)
        con_y += msg.text.count('\n') + 1  # increment y by # of lines

    # draw health
    scr.draw_text(0, height-1, 'Health: ' + str(game.player.get_health()),
                  fg=0, bg=9)

    scr.set_view(map_view)

    # map_view.box()

    # fill screen except room locations
    for x in range(-int(map_size.x // 2), int(map_size.x // 2)):
        for y in range(-int(map_size.y // 2), int(map_size.y // 2)):
            try:
                room = game.get_room(x, y)
                if room is None:
                    scr.draw_text(x + map_center.x, y + map_center.y, u'█')
            except Exception:
                pass

    world_pos = game.player.pos + map_center
    scr.draw_text(world_pos.x, world_pos.y, "@".encode("UTF-8"))

    scr.draw_outline()

    # for x in range(center[0] - game_map_size[0], game_map_size[0] - center[0]):
    #     for y in range(center[1] - game_map_size[1], game_map_size[1] - center[1]):
    #         try:
    #             room = game.get_room(x, y)
    #             if room is None:
    #                 draw_text(x + center[0], y + center[1], u'█')
    #         except:
    #             pass

    # if world_pos[0] >= 0 and world_pos[1] >= 0:
    #     draw_text(world_pos[0], world_pos[1], "@".encode("UTF-8"))


scr.start()
