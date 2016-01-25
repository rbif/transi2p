from twisted.internet import protocol, reactor, defer
from twisted.internet.endpoints import clientFromString, connectProtocol
from twisted.names import dns, error
import socket
import struct
import re

ip_re = re.compile(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
socket.SO_ORIGINAL_DST = 80

class AddressMap(object):
    def __init__(self, addr_map, default_mappings):
        self.base_addr = struct.unpack('>I', socket.inet_aton(addr_map))[0]
        self.addr_index = 0

        self.names = {}
        self.addresses = {}

        for addr in default_mappings:
            name = str(default_mappings[addr])
            addr = str(addr)

            if ip_re.match(addr):
                self.names[name] = addr
                self.addresses[addr] = name
            else:
                self.names[addr] = name
                self.addresses[name] = addr

    def map(self, name):
        if name in self.names:
            return self.names[name]
        else:
            addr = None
            while not addr or addr in self.addresses:
                self.addr_index += 1
                addr = socket.inet_ntoa(struct.pack('>I', self.base_addr + self.addr_index))

            self.names[name] = addr
            self.addresses[addr] = name
            return addr

    def get_name(self, addr):
        if addr in self.addresses:
            return self.addresses[addr]
        else:
            return None

class EepNS(object):
    def map_address(self, query):
        name = query.name.name
        addr = address_map.map(name)
        answer = dns.RRHeader(name=name, payload=dns.Record_A(address=addr))
        return [ answer ], [], []

    def query(self, query, timeout=None):
        if query.type == dns.A and query.name.name.split('.')[-1] == 'i2p':
            return defer.succeed(self.map_address(query))
        else:
            return defer.fail(error.DomainError())

class EepConnection(protocol.Protocol):
    def __init__(self, proxy):
        self.proxy = proxy

    def dataReceived(self, data):
        self.proxy.transport.write(data)

    def connectionLost(self, reason):
        self.proxy.i2p_error(reason)

class TransPort(protocol.Protocol):
    def connectionMade(self):
        self.pending = b''
        self.i2p = None

        # get the ip address they're trying to connect to and open connection
        addr = self.transport.socket.getsockopt(socket.SOL_IP, socket.SO_ORIGINAL_DST, 16)
        _, self.dst_port, self.dst_addr, _ = struct.unpack('>HH4s8s', addr)
        self.dst_addr = socket.inet_ntoa(self.dst_addr)

        name = address_map.get_name(self.dst_addr)
        if not name:
            self.transport.loseConnection()
            return

        endpoint = clientFromString(reactor, 'i2p:' + name)
        connection = connectProtocol(endpoint, EepConnection(self))
        connection.addCallback(self.i2p_connected)
        connection.addErrback(self.i2p_error)

    def dataReceived(self, data):
        if self.i2p:
            self.i2p.transport.write(data)
        else:
            self.pending += data

    def connectionLost(self, reason):
        if self.i2p:
            self.i2p.transport.loseConnection()    

    def i2p_error(self, reason):
        self.transport.loseConnection()

    def i2p_connected(self, i2p):
        self.i2p = i2p

        if self.pending:
            self.i2p.transport.write(self.pending)

address_map = None
