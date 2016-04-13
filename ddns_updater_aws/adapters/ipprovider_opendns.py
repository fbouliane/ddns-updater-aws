import dns.resolver
import ipaddress
from . import IpProviderFailure
import netifaces


def get_ip_address(config=None):
    resolver_ip = dns.resolver.query("resolver1.opendns.com", 'A').rrset[0].address
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [resolver_ip]

    opt = {}
    if config:
        opt['source_port'] = int(config.get('source_port', 0))
        if config.get("interface_name"):
            opt['source'] = _get_ip_address_from_interface_name(config['interface_name'])
    try:
        return ipaddress.ip_address(resolver.query('myip.opendns.com', **opt)[0])
    except ValueError:
        raise IpProviderFailure("Unable to get ip address")


def _get_ip_address_from_interface_name(interface_name):
    addrs = netifaces.ifaddresses(interface_name)
    return unicode(addrs[netifaces.AF_INET][0]['addr'], "utf-8")

