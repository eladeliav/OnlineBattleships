from abc import abstractmethod
from sgp_structs import SGPStruct


class IConnection:

    @abstractmethod
    def send_guess(self, x_coordinate: int, y_coordinate: int):
        pass

    @abstractmethod
    def get_response(self) -> SGPStruct:
        pass
