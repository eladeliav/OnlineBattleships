from abc import abstractmethod
from sgp_structs import SGPStruct


class IConnection:
    @abstractmethod
    def is_host(self):
        pass

    @abstractmethod
    def send_packet(self, pkt_type, x_coord, y_coord, msg=''):
        pass

    @abstractmethod
    def send_fail(self, msg):
        pass

    @abstractmethod
    def send_redo(self, msg):
        pass

    @abstractmethod
    def get_response(self) -> SGPStruct:
        pass
