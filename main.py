from players.basic_player import BasicPlayer
from connections import BasicConnection
from packet_parsers import BasicPacketParser
from game_managers.basic_game_manager import BasicGameManager
from game_managers import ConstantNetworkInfo
import socket


def host_connection():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((ConstantNetworkInfo.LISTEN_IP, ConstantNetworkInfo.PORT))
    listen_socket.listen(ConstantNetworkInfo.EXPECTED_CONNECTIONS)

    connection, dst_ip = listen_socket.accept()
    return connection, dst_ip[0]


def connect_to_peer():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ConstantNetworkInfo.CONNECT_IP, ConstantNetworkInfo.PORT))
    return connection, ConstantNetworkInfo.CONNECT_IP


def main():
    connect_or_host = input("[0] host, [1] connect")
    while not connect_or_host.isdigit() or not int(connect_or_host) in (ConstantNetworkInfo.HOST, ConstantNetworkInfo.CONNECT):
        connect_or_host = input("Try again: ")

    if int(connect_or_host) == ConstantNetworkInfo.HOST:
        connection, dst_ip = host_connection()
    else:
        connection, dst_ip = connect_to_peer()

    peer_conn = BasicConnection(BasicPacketParser(), connection, dst_ip, int(connect_or_host))
    player = BasicPlayer()
    manager = BasicGameManager(peer_conn, player)
    manager.game_loop()


if __name__ == '__main__':
    main()
