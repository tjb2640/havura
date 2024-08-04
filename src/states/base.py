import typing

from statesignal import StateSignal
from trigger import Trigger

'''
Represents a program state, used to hold information for different screens.
Introduces a small state lifecycle (__init__ -> [activate -> [input]* -> close]*)
'''
class BaseState:
    pos_x: None
    pos_y: None
    data: None
    term: None

    @classmethod
    def __init__(self, term):
        self.term = term
        pass

    '''
    Utility: redraw the screen
    '''
    @classmethod
    def _draw(self, reason: Trigger):
        pass

    '''
    Utility: wrap given str across words into a list[str] spanning the width/height
    TODO
    '''
    @classmethod
    def _wrap_text(self, text: str, width: int, height: int) -> list[str]:
        pass

    '''
    Lifecycle: Activate state. Initial draw call should be made here if needed.
    '''
    @classmethod
    def activate(self) -> StateSignal:
        return StateSignal.OK
    
    '''
    Lifecycle: "Close" the state. The instance persists though, data will as well.
    '''
    @classmethod
    def close(self) -> StateSignal:
        return StateSignal.OK

    '''
    Lifecycle: Accepts inputs from the main class.
    TODO; Second value in the returned tuple is unimplemented, will be used to pass data.
    '''
    @classmethod
    def input(self, inp) -> (StateSignal, str):
        return (StateSignal.OK, None)
