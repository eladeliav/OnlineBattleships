from enum import Enum


class GameObjectType(Enum):
    Empty = 0
    UnHitShip = 1
    Miss = 2
    Hit = 3
    Sunk = 4


OBJECT_TYPE_TO_SYMBOL = {
    GameObjectType.Empty: ".",
    GameObjectType.UnHitShip: "=",
    GameObjectType.Miss: "M",
    GameObjectType.Hit: "H",
    GameObjectType.Sunk: "S"
}
