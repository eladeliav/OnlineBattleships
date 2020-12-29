from sgp_structs import SGPStruct
from abc import abstractmethod


class IPacketBuilder:
    @abstractmethod
    def create_packet(self) -> SGPStruct:
        pass
