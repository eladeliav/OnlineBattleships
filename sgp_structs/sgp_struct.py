# SGP = Submarine Game Protocol
from sgp_structs import SGPPacketType


class SGPStruct:
    def __init__(self, packet_type: SGPPacketType, src_ip: str, dst_ip: str, x_coord: int, y_coord: int, data: str):
        self.packet_type = packet_type
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.data_length = len(data)
        self.data = data
