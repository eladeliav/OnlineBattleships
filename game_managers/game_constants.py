class ConstantMessages:
    INVALID_FORMAT_MSG = "Invalid format"
    INVALID_TIMING_MSG = "Invalid timing"
    LOCAL_PLAYER_WIN = "YOU!"
    ENEMY_PLAYER_WIN = "OPPONENT!"


class ConstantNetworkInfo:
    DEFAULT_COORDINATE = -1
    DID_HIT_DATA = "1"
    DID_SINK_DATA = "1"
    DID_LOSE_DATA = "1"
    PORT = 20000
    LISTEN_IP = "0.0.0.0"
    CONNECT_IP = "127.0.0.1"
    EXPECTED_CONNECTIONS = 1
    CONNECT = 1
    HOST = 0


class ConstantGameConfig:
    NUM_OF_SHIPS = 1
    SMALLEST_SHIP = 2
    LARGEST_SHIP = 2
    MIN_POINT_DISTANCE = 1
