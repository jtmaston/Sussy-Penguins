import logging
from json import loads

from twisted.internet.protocol import Factory, connectionDone, Protocol


class Client(Protocol):  # defines the communications protocol
    def __init__(self):
        self.username = None
        self.destination = None
        self.factory = None

    def connectionMade(self):
        logging.info("Established connection.")
        self.factory.application.succeed_connection()

    def dataReceived(self, data):  # called when a packet is received.
        print(f" -> {data}")  # uncomment this line to get the raw packet data
        data = data.decode().split('}')
        for packet in data:
            if packet:
                command = loads((packet + '}').encode())
                if command['command'] == 'hello':
                    pass

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
        self.application.fail_connection()
        connector.connect()

    def clientConnectionLost(self, connector, reason):  # ↑
        logging.info('Application: Disconnected.')
        connector.connect()
