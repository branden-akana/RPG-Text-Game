
from vector import vec2
from screen import CursesScreen
from game import Game

from pyglet import (window, app, text, clock)
import re
import actions


win = window.Window(1280, 720)
game = Game()

map_size = vec2(10, 10)
# map_center = map_size // 2
map_center = vec2(0, 0)
map_view = None


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
                f' Turn: {game.turns.get_last_entity().name}, Order: {[ent.name for ent in game.turns.order]} ',
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

# scr.start()
app.run()
