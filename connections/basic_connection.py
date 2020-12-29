import socket
from connections import IConnection
from packet_parsers import IPacketParser
from sgp_structs import SGPStruct, SGPPacketTypes

DEFAULT_SGP_PORT = 20000
LISTEN_IP = "0.0.0.0"
EXPECTED_CONNECTIONS = 1
DEFAULT_COORDINATE = -1
PACKET_FORMAT = "{packet_type}" \
                "\nsource_ip: {source_ip}" \
                "\ndestination_ip: {destination_ip}" \
                "\nx_coordinate: {x_coordinate}" \
                "\ny_coordinate: {y_coordinate}" \
                "\ndata_length: {data_length}" \
                "\n\n{data}"


class BasicConnection(IConnection):
    def __init__(self, packet_parser: IPacketParser):
        self.packet_parser = packet_parser
        self.connection, self.dst_ip = self.initialize_connection()
        # getting our local ip
        self.src_ip = socket.gethostbyname(socket.gethostname())

    def initialize_connection(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((LISTEN_IP, DEFAULT_SGP_PORT))
        listen_socket.listen(EXPECTED_CONNECTIONS)

        connection, dst_ip = listen_socket.accept()
        return connection, dst_ip

    def send_packet(self, pkt_type, x_coord, y_coord, msg):
        formatted = PACKET_FORMAT.format(packet_type=pkt_type, source_ip=self.src_ip,
                                         destination_ip=self.dst_ip, x_coordinate=x_coord, y_coordinate=y_coord,
                                         data_length=len(msg), data=msg)
        self.connection.send(formatted.encode())

    def get_response(self) -> SGPStruct:
        return self.packet_parser.parse_packet(self.connection)
