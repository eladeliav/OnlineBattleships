from typing import Tuple
from collections import namedtuple
from packet_parsers.header_validators import is_coordinate_valid

from players.iplayer import IPlayer

BOARD_SIZE = 10
NUM_OF_SHIPS = 1

BoardCell = namedtuple("BoardCell", ["is_ship", "is_sunk"])


class BasicPlayer(IPlayer):
    def __init__(self):
        # each board point has two values
        # the first represents if there is a ship, and the second represents
        # if that part has been sunk or not
        self.board = [[[False, False] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.setup_board()
        self.sunken_ships = 0

    def setup_board(self):
        for i in range(NUM_OF_SHIPS):
            print(f"Start and end coordinates for sip #{i + 1}")
            start_coord = self.get_coordinate_from_user()
            end_coord = self.get_coordinate_from_user()
            while start_coord[0] != end_coord[0] and start_coord[1] != end_coord[1]:
                print("Ships can only be places horizontally or vertically")
                start_coord = self.get_coordinate_from_user()
                end_coord = self.get_coordinate_from_user()

            for x in range(start_coord[0], end_coord[0] + 1):
                for y in range(start_coord[1], end_coord[1] + 1):
                    self.board[x][y][0] = True

    def get_coordinate_from_user(self):
        coords = input("Enter x and y coordinates one after the other. e.g '7 8'\n").split()
        while not all(map(is_coordinate_valid, coords)) or len(coords) != 2:
            coords = input("Invalid. try again: ").split()
        coords_gen = (int(val) for val in coords)
        return tuple(coords_gen)

    def did_lose(self) -> bool:
        return self.sunken_ships == NUM_OF_SHIPS

    def is_hit(self, x_coordinate, y_coordinate) -> bool:
        board_cell = self.board[x_coordinate][y_coordinate]
        if board_cell[0]:
            board_cell[1] = True

        return board_cell[0]
