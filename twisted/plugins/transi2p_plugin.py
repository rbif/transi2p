from twisted.application import internet, service
from twisted.internet import protocol
from twisted.names import dns, server, client
from twisted.python import usage
import json
import transi2p
from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker


class Options(usage.Options):
    optParameters = [ ['config', 'c', 'config.json', 'Path to config file'] ]

class TransServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "transi2p"
    description = "I2P transparent proxy service."
    options = Options

    def makeService(self, options):
        path = options['config']

        try:
            config = json.load(open(path))
            _resolvers = []
            for resolver in config['resolvers']:
                _resolvers.append(tuple(resolver))
            config['resolvers'] = _resolvers
        except IOError:
            print('Writing default config to {}.'.path(path))

            with open(path, 'w') as f:
                config = {
                    'addr_map': '10.18.0.0',
                    'dns_port': 5354,
                    'trans_port': 7679,
                    'listen': '127.0.0.1',
                    'resolvers': [ ('127.0.0.1', 5353) ],
                    'default_mappings': { '1.1.1.1': 'stats.i2p' }
                }

                json.dump(config, f)
        except ValueError:
            print('Invalid JSON configuration. RM and try again?')
            quit()

        if 'default_mappings' not in config:
            config['default_mappings'] = {}

        transi2p.address_map = transi2p.AddressMap(config['addr_map'],
            config['default_mappings'])

        i2pservice = service.MultiService()

        trans_port = protocol.ServerFactory()
        trans_port.protocol = transi2p.TransPort

        print('listening on transparent: {}:{}'.format(config['listen'],
            config['trans_port']))

        internet.TCPServer(config['trans_port'], trans_port,
            interface=config['listen']).setServiceParent(i2pservice)

        ns = server.DNSServerFactory(clients=[
            transi2p.EepNS(), client.Resolver(servers=config['resolvers'])
        ])

        print('listening on DNS: {}:{}'.format(config['listen'], config['dns_port']))
        internet.UDPServer(config['dns_port'], dns.DNSDatagramProtocol(controller=ns),
            interface=config['listen']).setServiceParent(i2pservice)

        return i2pservice

t = TransServiceMaker()
