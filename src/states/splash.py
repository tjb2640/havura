import typing

from states.base import BaseState

from statesignal import StateSignal
from trigger import Trigger

'''
Application start splash screen - no other functino beyond displaying text
and listening for a key press.

Progresses to Main Menu
'''
class SplashState(BaseState):
    pos_x = None
    pos_y = None
    data = None
    term = None
    activated_previously = False

    @classmethod
    def __init__(self, term):
        self.term = term
        self.activated_previously = False
        pass

    @classmethod
    def _draw(self, reason: Trigger):
        T = self.term

        SPLASH_TEXT = [
            "===== Havura =====",
            "Optimized for 80x24.",
            "(press any key to start)"
        ]

        T.echo(T.clear)
        y_pos = (T.height // 2) - len(SPLASH_TEXT) + 1
        for text in SPLASH_TEXT:
            T.echo(T.home + T.move_y(y_pos) + T.gray100_on_cornflowerblue(T.center(text)))
            y_pos = y_pos + 1

    @classmethod
    def activate(self) -> StateSignal:
        if self.activated_previously:
            exit(0)
        self.activated_previously = True
        self._draw(Trigger.ACTIVATED)
        return StateSignal.OK
    
    @classmethod
    def close(self) -> StateSignal:
        return StateSignal.OK

    @classmethod
    def input(self, inp) -> (StateSignal, str):
        # Upon any key pressed, tell the program to switch to the main menu
        return (StateSignal.STATE, 'MainMenu')
        pass