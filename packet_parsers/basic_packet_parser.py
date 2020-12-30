from packet_parsers import IPacketParser
from sgp_structs import SGPStruct, SGPHeaders, SGPPacketTypes
import socket
from packet_parsers.header_validators import is_packet_type_valid, is_valid_header, HEADER_TO_VALIDATOR, \
    HEADER_DELIMITER

EXPECTED_HEADER_COUNT = 5
PACKET_TYPE_INDEX = 0
SRC_IP_INDEX = 1
DST_IP_INDEX = 2
X_COORD_INDEX = 3
Y_COORD_INDEX = 4
DATA_LENGTH_INDEX = 5


class BasicPacketParser(IPacketParser):
    def receive_until(self, connection: socket.socket, delimiter='\n'):
        current_byte = ''
        data = ''
        while current_byte != delimiter:
            current_byte = connection.recv(1).decode()
            if not current_byte:
                return None
            data += current_byte
        return data.strip()

    def split_header_data(self, data_with_header):
        delimiter_index = data_with_header.find(HEADER_DELIMITER)
        header = data_with_header[:delimiter_index].strip()
        data = data_with_header[delimiter_index + 1:].strip()
        return header, data

    def receive_headers(self, connection: socket.socket):
        headers = {}
        for _ in range(EXPECTED_HEADER_COUNT):
            current = self.receive_until(connection)
            if not is_valid_header(current):
                return False

            header, data = self.split_header_data(current)
            headers[header] = data
        return headers

    def parse_packet(self, connection: socket.socket):
        packet_type = self.receive_until(connection)
        if not is_packet_type_valid(packet_type):
            return False

        headers = self.receive_headers(connection)
        if not headers:
            return False

        content_length = int(headers[SGPHeaders.DATA_LENGTH])
        # receive a single '\n' according to the protocol
        connection.recv(1)

        data = connection.recv(content_length).decode()
        src_ip = headers[SGPHeaders.SOURCE_IP]
        dst_ip = headers[SGPHeaders.DESTINATION_IP]
        x_coord = headers[SGPHeaders.X_COORDINATE]
        y_coord = headers[SGPHeaders.Y_COORDINATE]

        return SGPStruct(packet_type, src_ip, dst_ip, x_coord, y_coord, content_length, data)
