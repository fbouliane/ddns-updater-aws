import dns.resolver
import ipaddress
from . import IpProviderFailure


def get_ip_address(config=None):
    resolver_ip = dns.resolver.query("resolver1.opendns.com", 'A').rrset[0].address
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [resolver_ip]

    source_port = 0
    if config:
        source_port = int(config.get('source_port', 0))
    try:
        return ipaddress.ip_address(resolver.query('myip.opendns.com', source_port=source_port)[0])
    except ValueError:
        raise IpProviderFailure("Unable to get ip address")
