import itertools
import math
from game_managers import ConstantGameConfig
from game_objects.board import Board
from game_objects.game_object_type import GameObjectType
from exceptions import ShipNotFoundError
from packet_parsers.header_validators import is_coordinate_valid
from players.iplayer import IPlayer
from collections import namedtuple
from enum import IntEnum


class ShipOrientation(IntEnum):
    Horizontal = 0
    Vertical = 1


SUPPORTED_ORIENTATIONS = (ShipOrientation.Horizontal, ShipOrientation.Vertical)

Point = namedtuple("Point", ["x", "y"])


class BasicPlayer(IPlayer):

    def __init__(self):
        self.my_board = Board()
        self.guessing_board = Board()
        self.ships = []
        self.my_sunken_ships = 0

    def display_my_board(self):
        print("My board:")
        self.my_board.print_board()

    def display_guessing_board(self):
        print("Enemy board:")
        self.guessing_board.print_board()

    def get_all_ship_coordinates(self, start_coord, orientation, length):
        current_x, current_y = start_coord
        ship_locations = []
        for _ in range(length):
            ship_locations.append(Point(current_x, current_y))
            if orientation == ShipOrientation.Horizontal:
                current_x += 1
            else:
                current_y += 1
        return ship_locations

    def setup_board(self):
        for i in range(ConstantGameConfig.SMALLEST_SHIP, ConstantGameConfig.LARGEST_SHIP + 1):
            self.display_my_board()
            ship_locations = self.get_ship_from_user(i)
            for location in ship_locations:
                self.my_board.set_object(location.x, location.y, GameObjectType.UnHitShip)

            self.ships.append(ship_locations)

    def points_are_far_enough(self, points_tup):
        point_a, point_b = points_tup
        return math.dist([point_a.x, point_a.y], [point_b.x, point_b.y])

    def is_ship_placement_valid(self, new_ship_locations):
        for location in new_ship_locations:
            for current_ship_coords in self.ships:
                zipped = list(zip(current_ship_coords, itertools.repeat(location)))
                if not all(map(self.points_are_far_enough, zipped)):
                    return False

        return True

    def get_ship_from_user(self, length):
        print(f"Enter the location of the {length} ship")
        start_coord = self.get_coordinate_from_user()
        orientation = self.get_ship_orientation()
        ship_locations = self.get_all_ship_coordinates(start_coord, orientation, length)
        while not self.is_ship_placement_valid(
                ship_locations):
            print("Invalid ship placement, try again: ")
            start_coord = self.get_coordinate_from_user()
            orientation = self.get_ship_orientation()
            ship_locations = self.get_all_ship_coordinates(start_coord, orientation, length)

        return ship_locations

    def get_ship_orientation(self):
        orientation = input("Enter orientation (0 - Horizontal, 1 - Vertical):")
        while not orientation.isdigit() or int(orientation) not in SUPPORTED_ORIENTATIONS:
            orientation = input("Invalid orientation try again:")
        return ShipOrientation(int(orientation))

    def get_coordinate_from_user(self):
        coords = input("Enter x and y coordinates one after the other. e.g '7 8'\n").split()
        while not all(map(is_coordinate_valid, coords)) or len(coords) != 2:
            coords = input("Invalid. try again: ").split()
        coords_tuple = tuple((int(val) for val in coords))
        return Point(*coords_tuple)

    def did_lose(self) -> bool:
        return self.my_sunken_ships == ConstantGameConfig.NUM_OF_SHIPS

    def check_if_sunk(self, ship_coordinates):
        sunken_points = 0
        for current in ship_coordinates:
            if self.my_board.get_object(current.x, current.y) == GameObjectType.Hit:
                sunken_points += 1

        if sunken_points == len(ship_coordinates):
            for current in ship_coordinates:
                self.my_board.set_object(current.x, current.y, GameObjectType.Sunk)
            return True
        else:
            return False

    def is_hit(self, x_coordinate, y_coordinate):
        if self.my_board.get_object(x_coordinate, y_coordinate) == GameObjectType.UnHitShip:
            self.my_board.set_object(x_coordinate, y_coordinate, GameObjectType.Hit)
            guess_point = Point(x_coordinate, y_coordinate)
            attacked_ship = None
            for ship_coords in self.ships:
                if guess_point in ship_coords:
                    attacked_ship = ship_coords

            if not attacked_ship:
                raise ShipNotFoundError(f"Can't find ship at {guess_point}")

            sunk = self.check_if_sunk(attacked_ship)
            if sunk:
                self.my_sunken_ships += 1
            return True, sunk
        else:
            return False, False

    def update_opponent_board(self, x_coordinate, y_coordinate, new_object_type):
        self.guessing_board.set_object(x_coordinate, y_coordinate, new_object_type)
