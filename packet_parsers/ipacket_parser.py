from sgp_structs import SGPStruct
from abc import abstractmethod


class IPacketParser:
    @abstractmethod
    def parse_packet(self, pkt: bytes) -> SGPStruct:
        pass
