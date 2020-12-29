from sgp_structs import SUPPORTED_PACKET_TYPES, SUPPORTED_HEADERS

MINIMUM_BOARD_EDGE = 0
MAXIMUM_BOARD_EDGE = 10

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

    header = header_with_data[delimiter_index]
    data = header_with_data[delimiter_index + 1:]
    return header in SUPPORTED_HEADERS and HEADER_TO_VALIDATOR[header](data)


def is_packet_type_valid(packet_type: str):
    return packet_type in SUPPORTED_PACKET_TYPES


def is_coordinate_valid(coordinate: str):
    return coordinate.isdigit() and MINIMUM_BOARD_EDGE <= int(coordinate) <= MAXIMUM_BOARD_EDGE


def is_data_length_valid(data_length: str):
    return data_length.isdigit() and int(data_length) > 0


HEADER_TO_VALIDATOR = {
    "source_ip": is_ip_valid,
    "destination_ip": is_ip_valid,
    "x_coordinate": is_coordinate_valid,
    "y_coordinate": is_coordinate_valid,
    "data_length:": is_data_length_valid
}
