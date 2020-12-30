from abc import abstractmethod


class IPlayer:
    @abstractmethod
    def display_my_board(self):
        pass

    @abstractmethod
    def display_guessing_board(self):
        pass

    @abstractmethod
    def setup_board(self):
        pass

    @abstractmethod
    def get_coordinate_from_user(self):
        pass

    @abstractmethod
    def did_lose(self) -> bool:
        pass

    @abstractmethod
    def is_hit(self, x_coordinate, y_coordinate):
        pass

    @abstractmethod
    def update_opponent_board(self, x_coordinate, y_coordinate, new_object_type):
        pass
