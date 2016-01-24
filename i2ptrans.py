from twisted.internet import protocol, reactor
from twisted.internet.endpoints import clientFromString, connectProtocol
import socket
import struct
from txi2p.bob.endpoints import BOBI2PClientEndpoint

socket.SO_ORIGINAL_DST = 80

mappings = {
    '10.18.97.1': 'stats.i2p'
}

class i2pConnection(protocol.Protocol):
#    def __init__(self, proxy):
#        self.proxy = proxy

    def dataReceived(self, data):
        self.proxy.transport.write(data)

    def connectionLost(self, reason):
        # clean up
        print(reason)

class TransPort(protocol.Protocol):
    def connectionMade(self):
        self.pending = b''
        self.i2p = None

        # get the ip address they're trying to connect to and open connection
        addr = self.transport.socket.getsockopt(socket.SOL_IP, socket.SO_ORIGINAL_DST, 16)
        _, self.dst_port, self.dst_addr, _ = struct.unpack('>HH4s8s', addr)
        self.dst_addr = socket.inet_ntoa(self.dst_addr)

        print(self.dst_addr, self.dst_port)

        endpoint = clientFromString(reactor, 'i2p:' + mappings[self.dst_addr])
        connectProtocol(endpoint, i2pConnection()).addCallback(self.i2p_connected)

    def dataReceived(self, data):
        if self.i2p:
            self.i2p.transport.write(data)
        else:
            self.pending += data

    def connectionLost(self, reason):
        # clean up
        print(reason)

    def i2p_connected(self, i2p):
        print('connected')
        self.i2p = i2p

        if self.pending:
            self.i2p.transport.write(self.pending)

trans_port = protocol.ServerFactory()
trans_port.protocol = TransPort

reactor.listenTCP(7679, trans_port)
print('listening on 7679')
reactor.run()
