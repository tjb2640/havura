from blessed import Terminal
from functools import partial
import signal
import typing

# States for keeping track of data between "windows"
from states.base import BaseState
from states.splash import SplashState
from states.mainmenu import MainMenuState

from key import Key
from specialchars import SpecialChars
from statesignal import StateSignal

# TEST
from api.sefaria import SefariaAPI, SefariaIndex
'''
for index in SefariaAPI.get_indices():
    print(index.category)
exit(0)
'''

# Quiet interrupt handle
signal.signal(signal.SIGINT, lambda sig, frame: exit(0))



# Create our Terminal object and define some helper functions
term = Terminal()
term.echo = partial(print, end='', flush=True)

def __util_echo_position(x, y, width, text):
    for draw_x in range(x, width):
        term.echo(term.move_xy(draw_x, y) + term.black(u' '))
    term.echo(term.move_xy(x, y) + text + term.normal)
term.text_normal = __util_echo_position

def __util_echo_position_highlighted(x, y, width, text):
    for draw_x in range(x, width):
        term.echo(term.move_xy(draw_x, y) + term.black_on_lightgoldenrod1(u' '))
    term.echo(term.move_xy(x, y) + term.black_on_lightgoldenrod1(term.bold + text) + term.normal)
term.text_highlighted = __util_echo_position_highlighted

def __util_draw_double_box(x, y, width, height):
    x2 = x + width - 1
    y2 = y + height - 1

    # Horizontal lines
    for draw_y in (y, y2):
        for draw_x in range(x + 1, x2):
            term.echo(term.move_xy(draw_x, draw_y) + term.white(SpecialChars.DPIPE_HORIZONTAL.value))

    # Vertical lines
    for draw_x in (x, x2):
        for draw_y in range(y + 1, y2):
            term.echo(term.move_xy(draw_x, draw_y) + term.white(SpecialChars.DPIPE_VERTICAL.value))

    # Corners
    term.echo(term.move_xy(x, y) + term.white(SpecialChars.DPIPE_CORNER_TL.value))
    term.echo(term.move_xy(x2, y) + term.white(SpecialChars.DPIPE_CORNER_TR.value))
    term.echo(term.move_xy(x, y2) + term.white(SpecialChars.DPIPE_CORNER_BL.value))
    term.echo(term.move_xy(x2, y2) + term.white(SpecialChars.DPIPE_CORNER_BR.value))
term.draw_box = __util_draw_double_box



STATES = {
    'Base': BaseState(term),
    'Splash': SplashState(term),
    'MainMenu': MainMenuState(term)
}

class Program:
    display_stack: list[BaseState] = None

    @classmethod
    def __init__(self):
        self.display_stack = []

    '''
    Switch to another program state
    '''
    @classmethod
    def state_push(self, state_name: str):
        if state_name in STATES:
            if len(self.display_stack) > 0:
                self.display_stack[-1].close()
            self.display_stack.append(STATES[state_name])
            self.display_stack[-1].activate()

    '''
    Exit the current program state and return to the last one
    '''
    @classmethod
    def state_pop(self):
        to_close = self.display_stack.pop()
        to_close.close()
        self.display_stack[-1].activate()

HAVURA = Program()



'''
Start off with a splash screen, then perpetually await input and handle it as needed
'''
with term.fullscreen():
    HAVURA.state_push('Splash')
    while True:
        with term.cbreak(), term.hidden_cursor():
            # TODO: handle special codes here, like commands to change state and stuff.
            inp = term.inkey().code
            (do_next, returned_data) = HAVURA.display_stack[-1].input(inp)
            if do_next == StateSignal.OK:
                pass
            elif do_next == StateSignal.BACK:
                HAVURA.state_pop()
                pass
            elif do_next == StateSignal.STATE:
                state_to_set = returned_data
                # TODO: push to state stack.
                HAVURA.state_push(state_to_set)
