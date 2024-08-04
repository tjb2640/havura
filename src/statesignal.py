from enum import Enum

'''
Used by states to return a status from its lifecycle functions

OK: All good
BACK: Go back one program state (pop state stack)
STATE: Navigate to a new state (push to state stack)
PASS: Placeholder for development; do nothing
'''
class StateSignal(Enum):
    OK = 1
    BACK = 2
    STATE = 3
    PASS = 4