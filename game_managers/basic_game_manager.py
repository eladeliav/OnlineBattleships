from connections import IConnection
from sgp_structs import SGPPacketTypes, SGPStruct
from exceptions import PacketTimingError, PacketFormatError, SGPError
from players import IPlayer
from game_objects import GameObjectType
from game_managers import ConstantMessages, ConstantNetworkInfo

LOCAL_TURN_EXPECTED_RESPONSES = (SGPPacketTypes.HIT, SGPPacketTypes.LOSE)

ENEMY_TURN_EXPECTED_RESPONSES = (SGPPacketTypes.GUESS, SGPPacketTypes)


class BasicGameManager:
    def __init__(self, connection: IConnection, player: IPlayer):
        self.connection = connection
        self.player = player
        self.player.setup_board()
        self.winner = None

        self.turn_order = [(self.do_local_turn, "Your turn"), (self.do_enemy_turn, "Enemy turn")]
        if not self.connection.is_host():
            self.turn_order = self.turn_order[::-1]

        self.last_packet_type = SGPPacketTypes.FAIL
        self.last_sent_x = ConstantNetworkInfo.DEFAULT_COORDINATE
        self.last_sent_y = ConstantNetworkInfo.DEFAULT_COORDINATE

    def game_loop(self):
        game_over = False
        while not game_over:
            try:
                for turn_func, turn_msg in self.turn_order:
                    self.player.display_my_board()
                    self.player.display_guessing_board()
                    print(turn_msg)
                    game_over = turn_func()
                    if game_over:
                        break
            except SGPError as e:
                print(e)
                return
        print("GAME OVER!")
        print(f"{self.winner} WON THE GAME!")

    def get_valid_connection_response(self, expected_types):
        response = self.connection.get_response()
        if not response:
            raise PacketFormatError("Received invalid packet")

        if response.packet_type == SGPPacketTypes.REDO:
            while response.packet_type == SGPPacketTypes.REDO:
                self.connection.send_packet(self.last_packet_type, self.last_sent_x, self.last_sent_y)

        if response.packet_type == SGPPacketTypes.FAIL:
            raise PacketFormatError("The last sent packet received a fail response")

        if response.packet_type not in expected_types:
            raise PacketTimingError("Received unexpected response")

        return response

    def send_response(self, packet_type, x_coord, y_coord, data=''):
        self.last_packet_type = packet_type
        self.last_sent_x = x_coord
        self.last_sent_y = y_coord
        sent = self.connection.send_packet(self.last_packet_type, self.last_sent_x, self.last_sent_y, data)
        return sent

    def do_local_turn(self):
        my_turn = True
        while my_turn:
            guess_x, guess_y = self.player.get_coordinate_from_user()
            guess_x = int(guess_x)
            guess_y = int(guess_y)
            if not self.send_response(SGPPacketTypes.GUESS, guess_x, guess_y):
                return False

            response = self.get_valid_connection_response([SGPPacketTypes.HIT])
            did_hit = response.data == ConstantNetworkInfo.DID_HIT_DATA
            if did_hit:
                self.player.update_opponent_board(guess_x, guess_y, GameObjectType.Hit)

            did_sink_response = self.get_valid_connection_response([SGPPacketTypes.SUNK])
            if did_sink_response.data == ConstantNetworkInfo.DID_SINK_DATA:
                self.player.update_opponent_board(guess_x, guess_y, GameObjectType.Sunk)

            did_lose_response = self.get_valid_connection_response([SGPPacketTypes.LOSE])
            if did_lose_response.data == ConstantNetworkInfo.DID_LOSE_DATA:
                self.winner = ConstantMessages.LOCAL_PLAYER_WIN
                return True

            else:
                self.player.update_opponent_board(guess_x, guess_y, GameObjectType.Miss)

            my_turn = did_hit
        return False

    def do_enemy_turn(self):
        enemy_turn = True
        while enemy_turn:
            enemy_guess = self.get_valid_connection_response([SGPPacketTypes.GUESS])
            guess_x = int(enemy_guess.x_coord)
            guess_y = int(enemy_guess.y_coord)
            did_hit, did_sink = self.player.is_hit(guess_x, guess_y)
            did_hit_data = int(did_hit)
            did_sink_data = int(did_sink)

            self.send_response(SGPPacketTypes.HIT, guess_x, guess_y, str(did_hit_data))
            self.send_response(SGPPacketTypes.SUNK, guess_x, guess_y, str(did_sink_data))

            did_lose = self.player.did_lose()
            did_lose_data = int(did_lose)
            self.send_response(SGPPacketTypes.LOSE, ConstantNetworkInfo.DEFAULT_COORDINATE,
                               ConstantNetworkInfo.DEFAULT_COORDINATE, str(did_lose_data))

            if did_lose:
                return True

            enemy_turn = did_hit
        return False
