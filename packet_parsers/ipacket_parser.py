import socket
from abc import abstractmethod


class IPacketParser:
    @abstractmethod
    def parse_packet(self, connection: socket.socket):
        pass
