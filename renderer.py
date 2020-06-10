
import curses
import locale

from game import Game

class Renderer():

    def __init__(self):

        self.game = Game()

    def start(self):

        # initialize terminal

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # disable cursor

        curses.curs_set(False)

        # create window

        game_map_size = (20, 20)
        center = game_map_size[0]//2, game_map_size[1]//2

        game_map = curses.newwin(game_map_size[1], game_map_size[0], 1, 0)

        self.stdscr.refresh()

        key = None
        pos = [0, 0]

        while True:

            try:
                if key == "q":
                    self.end()
                    break

                self.game.send_key_press(key)

                pos = self.game.player.location_x, self.game.player.location_y

                world_pos = (pos[0] + center[0], pos[1] + center[1])

                print("pos: " + str(world_pos))

                # clear screen

                self.stdscr.clear()
                game_map.clear()

                # render

                game_map.box()

                for x in range(center[0] - game_map_size[0], game_map_size[0] - center[0]):
                    for y in range(center[1] - game_map_size[1], game_map_size[1] - center[1]):
                        try:
                            room = self.game.get_room(x, y)
                            if room is None:
                                game_map.addstr(y + center[1], x + center[0], '█')
                        except:
                            pass

                self.draw_text(0, 0, "Welcome to Fuck You", curses.A_STANDOUT)
                self.draw_text(21, 2, "Location: " + str(pos) + "\n"
                                      "Last Keypress: " + str(key) + '\n'
                                      'Health: ' + str(self.game.player.hp))

                self.draw_text(21, 5, self.game.status)

                self.draw_text(21, 9, '\n'.join([str(act) for act in self.game.actions]))

                self.draw_text(0, 23, '\n'.join(self.game.log))

                if world_pos[0] >= 0 and world_pos[1] >= 0:
                    game_map.addstr(world_pos[1],
                                    world_pos[0],
                                    "@".encode("UTF-8"))


                # display screen

                self.stdscr.refresh()
                game_map.refresh()

                key = self.stdscr.getkey()

            except Exception as e:
                self.end()

    def draw_text(self, x, y, text, attr=None):
        """Draw text to the screen."""

        for offset, line in enumerate(text.splitlines()):
            self.stdscr.addstr(y + offset, x, line)

    def end(self):
        # shut down terminal
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':

    window = Renderer()
    window.start()
