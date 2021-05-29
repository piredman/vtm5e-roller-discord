from enum import Enum


class CommandResultState(Enum):
    EMPTY = 0
    SUCCESS = 1
    ERROR = 2


class CommandResult(object):

    def __init__(self, state: CommandResultState, payload: object):
        self.state = state
        self.payload = payload
