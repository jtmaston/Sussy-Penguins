#!/usr/bin/python3


import json
import logging

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory, connectionDone

from roles_generator import *

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


def get_transportable_data(packet) -> bytes:  # helper method to get a transportable version of non-encoded data
    return json.dumps(packet).encode()


class Room:
    def __init__(self):
        self.players = None
        self.id = None

class Server(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.endpoint_username = None
        self.rooms = dict()
        self.player_pool = dict()

    def connectionMade(self):
        pass

    def connectionLost(self, reason=connectionDone):
        if self.endpoint_username is not None:
            logging.info(self.endpoint_username + " logged out.")
            try:
                del self.factory.connections[self.endpoint_username]
            except KeyError:
                pass
            self.endpoint_username = None

    # noinspection PyArgumentList
    def decode_command(self, data):
        try:
            packet = json.loads(data)
        except UnicodeError:
            return
        except Exception as e:
            logging.error(f"Tried loading, failed! Reason: {e}")
            logging.error(f"Message contents was: {data}")
            logging.error("Connection forced closed.")
            self.transport.loseConnection()
            return
        if packet['command'] == 'ask_game':
            if len(self.rooms) == 0:
                self.rooms['room_0'] = Room()

    def dataReceived(self, data):
        data = data.split('\r\n'.encode())
        logging.info(data)
        for message in data:
            if message:
                self.decode_command(message)


class ServerFactory(Factory):
    def __init__(self):
        self.connections = dict()
        self.mode = None

    def buildProtocol(self, address):
        return Server(self)


if __name__ == '__main__':
    reactor.listenTCP(8123, ServerFactory())
    logging.info("Server started.")
    reactor.run()
