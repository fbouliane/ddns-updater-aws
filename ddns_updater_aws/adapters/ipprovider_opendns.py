import dns.resolver
import ipaddress
from . import IpProviderFailure


def get_ip_address():
    resolver_ip = dns.resolver.query("resolver1.opendns.com", 'A').rrset[0].address
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [resolver_ip]
    try:
        return ipaddress.ip_address(resolver.query('myip.opendns.com')[0])
    except ValueError:
        raise IpProviderFailure("Unable to get ip address")
