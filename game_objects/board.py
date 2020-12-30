from game_objects.game_object_type import GameObjectType, OBJECT_TYPE_TO_SYMBOL

BOARD_SIZE = 10


class Board:
    def __init__(self):
        self.board = []
        for row in range(BOARD_SIZE):
            line = []
            for col in range(BOARD_SIZE):
                line.append(GameObjectType.Empty)
            self.board.append(line)

    def print_board(self):
        for row in self.board:
            for object_type in row:
                symbol = OBJECT_TYPE_TO_SYMBOL[object_type]
                print(f"{symbol}", end=' ')
            print()

    def get_object(self, x, y):
        return self.board[y][x]

    def set_object(self, x, y, value):
        self.board[y][x] = value
