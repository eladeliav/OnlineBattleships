import socket
from connections import IConnection
from packet_parsers import IPacketParser
from sgp_structs import SGPStruct, SGPPacketTypes
from game_managers import ConstantNetworkInfo

DEFAULT_COORDINATE = -1
PACKET_FORMAT = "{packet_type}" \
                "\nsource_ip: {source_ip}" \
                "\ndestination_ip: {destination_ip}" \
                "\nx_coordinate: {x_coordinate}" \
                "\ny_coordinate: {y_coordinate}" \
                "\ndata_length: {data_length}" \
                "\n\n{data}"


class BasicConnection(IConnection):

    def __init__(self, packet_parser: IPacketParser, connection: socket.socket, dst_ip, host_or_peer: int):
        self.packet_parser = packet_parser
        self.connection = connection
        self.dst_ip = dst_ip
        # getting our local ip
        self.is_host_connection = host_or_peer == ConstantNetworkInfo.HOST
        self.src_ip = socket.gethostbyname(socket.gethostname())

    def is_host(self):
        return self.is_host_connection

    def __del__(self):
        try:
            self.connection.close()
            print("Disconnected")
        except socket.error as e:
            print(e)

    def send_packet(self, pkt_type, x_coord, y_coord, msg=''):
        formatted = PACKET_FORMAT.format(packet_type=pkt_type, source_ip=self.src_ip,
                                         destination_ip=self.dst_ip, x_coordinate=x_coord, y_coordinate=y_coord,
                                         data_length=len(msg), data=msg)
        try:
            self.connection.send(formatted.encode())
            return True
        except socket.error as e:
            print(e)
            return False

    def send_fail(self, msg):
        self.send_packet(SGPPacketTypes.FAIL, DEFAULT_COORDINATE, DEFAULT_COORDINATE, msg)

    def send_redo(self, msg):
        self.send_packet(SGPPacketTypes.REDO, DEFAULT_COORDINATE, DEFAULT_COORDINATE, msg)

    def get_response(self) -> SGPStruct:
        return self.packet_parser.parse_packet(self.connection)
