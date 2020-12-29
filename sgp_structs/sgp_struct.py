# SGP = Submarine Game Protocol
class SGPPacketTypes:
    GUESS = "GUESS"
    HIT = "HIT"
    SUNK = "SUNK"
    LOSE = "LOSE"
    REDO = "REDO"
    FAIL = "FAIL"


SUPPORTED_PACKET_TYPES = (
    SGPPacketTypes.GUESS, SGPPacketTypes.HIT, SGPPacketTypes.SUNK, SGPPacketTypes.LOSE, SGPPacketTypes.REDO,
    SGPPacketTypes.FAIL)


class SGPStruct:
    def __init__(self, packet_type: str, src_ip: str, dst_ip: str, x_coord: int, y_coord: int, data_length: int,
                 data: str):
        self.packet_type = packet_type
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.data_length = data_length
        self.data = data
