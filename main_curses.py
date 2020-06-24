
from vector import vec2
from screen import CursesScreen
from game import Game

from pyglet import (window, app, text, clock)
import re
import actions


scr = CursesScreen()
win = window.Window(1280, 720)
game = Game()

map_size = vec2(10, 10)
# map_center = map_size // 2
map_center = vec2(0, 0)
map_view = None


# @scr.init
def on_init(scr: CursesScreen):
    pass

    # global map_view
    # map_view = scr.create_view(0, 1, *map_size)

# gl draw loop
# ------------


@win.event
def on_key_press(key, modifiers):

    if key == window.key.Q:
        win.close()

    keymap = {
        '_1': '1',
        '_2': '2',
        '_3': '3',
        '_4': '4',
        '_5': '5',
        '_6': '6',
        '_7': '7',
        '_8': '8',
        '_9': '9',
    }

    strkey = str(window.key.symbol_string(key)).lower()
    strkey = keymap.get(strkey, strkey)

    game.on_key_pressed(strkey)


l_title = text.Label(
    'Welcome to Super Fuck You',
    font_name='Fantasque Sans Mono',
    font_size=12,
    x=win.width//2, y=win.height-20,
    anchor_x='center'
)


def draw_text(x, y, t: str, *args, **kwargs):

    label = text.Label(t,
        font_name='Fantasque Sans Mono',
        font_size=12,
        x=x, y=win.height-y,
        width=800,
        multiline=True,
        color=kwargs.get('color', (255, 255, 255, 255))
        # anchor_y='bottom'
    )

    label.draw()


@win.event
def on_draw():

    width, height = win.width, win.height

    win.clear()

    l_title.draw()

    draw_text(21, 100, (
        "Location: " + str(game.player.pos) + "\n"
        "State: " + game.game_state
    ))

    # draw actions
    draw_text(width - 400, 200, actions.format_actions(game.get_actions()))

    # draw console messages
    con_y = height - 60  # start y position of console
    color = [255, 255, 255, 255]
    for msg in game.get_log():
        draw_text(50, con_y, msg.text, style=msg.style, fg=msg.fg, bg=msg.bg, color=tuple(color))
        con_y -= (msg.text.count('\n') + 1) * 20  # increment y by # of lines
        color[3] -= 10

    # draw health
    draw_text(0, height, 'Health: ' + str(game.player.get_health()),
                  fg=0, bg=9)

    # draw turns
    draw_text(16 * 12, height-1,
                f' Turn: {game.turns.get_last_entity().name}, Order: {[ent.get_name() for ent in game.turns.order]} ',
                  fg=0, bg=10)

    # draw fps
    # draw_text(width - 16, height - 1,
                  # ' FPS: {:.2f} '.format(scr.fps),
                  # fg=0, bg=11)

    # draw command buffer
    if game.menu_state == 'cmd':
        draw_text(12, height-20, ':' + game.menu_cmd_buffer, 'standout')

    win.flip()


def on_update(dt):
    game.update()


clock.schedule_interval(on_update, 1.0/60.0)


# curses draw loop
# ----------------

# @scr.render
def on_draw(scr: CursesScreen, key: str):

    if game.quit:
        scr.end()
        return

    global map_view

    game.on_key_pressed(key)
    game.update()

    width, height = scr.get_size()

    title = "~ Welcome to Super Fuck You ~"

    scr.draw_text(0, 0, title.center(width), style='standout')
    scr.draw_text(21, 2, (
        "Location: " + str(game.player.pos) + "\n"
        "Last Keypress: " + str(key) + "\n"
        "State: " + game.game_state
    ))

    # desc = re.sub(' +', ' ', game.get_description())
    # scr.draw_text(21, 5, '\n'.join(textwrap.wrap(desc, width-21)))

    # draw actions
    scr.draw_text(width - 24, 2, actions.format_actions(game.get_actions()))

    # draw console messages
    con_y = 15  # start y position of console
    for msg in game.get_log():
        scr.draw_text(0, con_y, msg.text, style=msg.style, fg=msg.fg, bg=msg.bg)
        con_y += msg.text.count('\n') + 1  # increment y by # of lines

    # draw health
    scr.draw_text(0, height-1, 'Health: ' + str(game.player.get_health()),
                  fg=0, bg=9)

    # draw turns
    scr.draw_text(16, height-1,
                f' Turn: {game.turns.get_last_entity().name}, Order: {[ent.get_name() for ent in game.turns.order]} ',
                  fg=0, bg=10)

    # draw fps
    scr.draw_text(width - 16, height - 1,
                  ' FPS: {:.2f} '.format(scr.fps),
                  fg=0, bg=11)

    # draw command buffer
    if game.menu_state == 'cmd':
        scr.draw_text(12, height-1, ':' + game.menu_cmd_buffer, 'standout')

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

# scr.start()
app.run()
