import curses

class EchoOn:
    def __enter__(self):
        curses.echo()
    def __exit__(self, type, value, traceback):
        curses.noecho()
