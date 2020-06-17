
import curses
import traceback


class CursesScreen:
    """A terminal managed by the curses API."""

    def __init__(self):

        self.stdscr = None

        # the current view - any draw calls will use this view object
        self.view = None

        # a list of views
        self.views = []

        # a map of colors
        self.colors = {}

        # called on every frame
        self.on_render = lambda: None

        # called before the render loop starts
        self.on_init = lambda: None

    def render(self, func):
        """Set the function used to render a frame."""
        self.on_render = func
        return func

    def init(self, func):
        """Set the method called before the render loop."""
        self.on_init = func
        return func

    def set_view(self, view=None) -> None:
        """Set the active view.

        Any draw calls will use the active view.
        """

        if view is None:
            self.view = self.stdscr
        else:
            self.view = view

    def read_input(self) -> str:
        """Read input from the user.

        This method will wait until the user presses a key. The string
        representation of that key will be returned.
        """

        return self.stdscr.getkey()

    def create_view(self, x, y, width, height):
        """Create a new view."""

        win = curses.newwin(height, width, y, x)
        self.views.append(win)
        return win

    def init_colors(self):
        """Initialize the color pairs used by curses."""

        curses.start_color()
        curses.use_default_colors()
        color_id = 1
        for fg in range(0, 16):
            for bg in range(0, 16):
                self.colors[(fg, bg)] = color_id
                curses.init_pair(color_id, fg, bg)
                color_id += 1

    def get_color(self, fg=None, bg=0):
        """Get a color pair by its fg and bg color."""
        return curses.color_pair(self.colors.get((fg, bg), 0))

    def get_size(self):
        """Get the size of the window as a tuple."""

        yx = self.stdscr.getmaxyx()
        return yx[1], yx[0]  # flip coordinates

    def start(self):
        """Start the curses screen."""

        # initialize terminal

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # initialize colors (16 colors)

        self.init_colors()

        # disable cursor

        curses.curs_set(False)

        # create window

        self.stdscr.refresh()

        # game loop
        # ---------

        self.on_init(self)

        # assign some of our methods to new variables to shorten them

        key = None
        set_view = self.set_view

        while True:

            try:
                if key == "Q":  # debug quit key
                    self.end()
                    break

                # clear screen
                # ------------

                self.stdscr.erase()
                for view in self.views:
                    view.erase()

                # render
                # ------

                # draws to the entire screen

                set_view()
                self.on_render(self, key)

                # display screen

                self.stdscr.refresh()
                for view in self.views:
                    view.refresh()

                key = self.stdscr.getkey()

            except Exception:

                self.end()
                traceback.print_exc()
                break

    def draw_text(self, x, y, text,
                  style='normal',
                  fg=None, bg=0):
        """Draw text to the screen."""

        style_map = {
            'normal':    curses.A_NORMAL,
            'bold':      curses.A_BOLD,
            'italic':    curses.A_ITALIC,
            'underline': curses.A_UNDERLINE,
            'standout':  curses.A_STANDOUT
        }

        attr = style_map.get(style, curses.A_NORMAL)

        color = self.get_color(fg, bg)

        for offset, line in enumerate(text.splitlines()):
            try:
                self.view.addstr(y + offset, x, line, color | attr)
            except Exception:
                pass

    def draw_outline(self):
        """Draw an outline around the screen."""

        self.view.box()

    def end(self):
        # shut down terminal
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
