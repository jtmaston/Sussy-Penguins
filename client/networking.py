import logging
from json import loads, dumps

from twisted.internet.protocol import Factory, connectionDone, Protocol


def get_transportable_data(packet) -> bytes:  # helper method to get a transportable version of non-encoded data
    return dumps(packet).encode()


class Client(Protocol):  # defines the communications protocol
    def __init__(self):
        self.username = None
        self.destination = None
        self.factory = None

    # noinspection PyArgumentList
    def succeed_connection(self):
        self.transport.write(
            get_transportable_data({
                'sender': 'client',
                'command': 'hello'
            }))

    def connectionMade(self):
        logging.info("Established connection.")
        self.succeed_connection()

    # noinspection PyArgumentList
    def dataReceived(self, data):  # called when a packet is received.
        print(f" -> {data}")  # uncomment this line to get the raw packet data
        # data = data.decode().split('}')
        data = data.decode()
        # for packet in data:
        # if packet:
        # print(packet)
        command = loads(data.encode())
        if command['command'] == 'hello':
            self.transport.write(get_transportable_data({'sender': "server", "command": 'hello'}))
        elif command['command'] == 'stat_block':
            print(command)
            self.factory.application.show_stats(loads(command['stat_block']))

    def connectionLost(self, reason=connectionDone):
        logging.info(reason.value)


class ClientFactory(Factory):
    def __init__(self, application):
        self.client = None
        self.application = application

    def buildProtocol(self, addr):
        c = Client()
        self.client = c
        self.client.factory = self
        return c

    def startedConnecting(self, connector):
        logging.info('Application: Attempting to connect...')

    def clientConnectionFailed(self, connector, reason):
        logging.error('Application: Connection failed!')
        # self.application.fail_connection()
        connector.connect()

    def clientConnectionLost(self, connector, reason):  # ↑
        logging.info('Application: Disconnected.')
        connector.connect()
