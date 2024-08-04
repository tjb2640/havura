from enum import Enum

'''
Represents reasons or intents concerning why things happen,
right now used mainly for draw calls.

ACTIVATED: State was activated.
'''
class Trigger(Enum):
    ACTIVATED = 0