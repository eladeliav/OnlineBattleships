from enum import Enum


class SGPPacketType(Enum):
    Guess = 0
    Hit = 1
    Sunk = 2
    Lose = 3
    Redo = 4
    Fail = 5
