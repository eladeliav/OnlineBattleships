from sgp_structs import SUPPORTED_PACKET_TYPES, SUPPORTED_HEADERS
from game_objects.board import BOARD_SIZE

MINIMUM_BOARD_EDGE = 0
MAXIMUM_BOARD_EDGE = BOARD_SIZE

HEADER_DELIMITER = ":"


def is_ip_valid(ip: str):
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


def is_valid_header(header_with_data: str):
    delimiter_index = header_with_data.find(HEADER_DELIMITER)
    if delimiter_index == -1:
        return False

    header = header_with_data[:delimiter_index].strip()
    data = header_with_data[delimiter_index + 1:].strip()
    return header in SUPPORTED_HEADERS and HEADER_TO_VALIDATOR[header](data)


def is_packet_type_valid(packet_type: str):
    return packet_type in SUPPORTED_PACKET_TYPES


def is_coordinate_valid(coordinate: str):
    if coordinate.isdigit() and MINIMUM_BOARD_EDGE <= int(coordinate) < MAXIMUM_BOARD_EDGE:
        return True

    # special case no time to make it pretty
    return coordinate == "-1"


def is_data_length_valid(data_length: str):
    return data_length.isdigit() and int(data_length) >= 0


HEADER_TO_VALIDATOR = {
    "source_ip": is_ip_valid,
    "destination_ip": is_ip_valid,
    "x_coordinate": is_coordinate_valid,
    "y_coordinate": is_coordinate_valid,
    "data_length": is_data_length_valid
}
