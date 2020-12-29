from packet_parsers import IPacketParser
from sgp_structs import SGPStruct, SGPPacketTypes, SUPPORTED_PACKET_TYPES
from IPy import IP
from typing import List

MINIMUM_EXPECTED_LINE_COUNT = 7
PACKET_TYPE_INDEX = 0
SRC_IP_INDEX = 1
DST_IP_INDEX = 2
X_COORD_INDEX = 3
Y_COORD_INDEX = 4
DATA_LENGTH_INDEX = 5


class BasicPacketParser(IPacketParser):
    def is_ip_valid(self, ip: str):
        ip_lines = ip.split('.')
        if len(ip_lines) != 4:
            return False
        for x in ip_lines:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True

    def parse_packet(self, pkt: bytes):
        pkt_lines = pkt.decode().split()

        if len(pkt_lines) < MINIMUM_EXPECTED_LINE_COUNT:
            return False

        pkt_type = pkt_lines[PACKET_TYPE_INDEX]
        if pkt_type not in SUPPORTED_PACKET_TYPES:
            return False

        src_ip = pkt_lines[SRC_IP_INDEX]
        dst_ip = pkt_lines[DST_IP_INDEX]
        if not self.is_ip_valid(src_ip) or not self.is_ip_valid(dst_ip):
            return False

        x_coord = pkt_lines[X_COORD_INDEX]
        y_coord = pkt_lines[Y_COORD_INDEX]
        data_length = pkt_lines[DATA_LENGTH_INDEX]
        if not all(map(str.isdigit, [x_coord, y_coord, data_length])):
            return False

        data = ""
        if int(data_length) >= 0:
            data = pkt_lines[7]
        if len(data) != int(data_length):
            return False
        
        return SGPStruct(pkt_type, src_ip, dst_ip, int(x_coord), int(y_coord), int(data_length), data)
