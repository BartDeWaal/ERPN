import curses


class EchoOn:
    """ helper class, so you can say "with EchoOn:" """
    def __enter__(self):
        curses.echo()

    def __exit__(self, type, value, traceback):
        curses.noecho()
