from unittest import TestCase

import ipaddress
from ddns_aws_updater.adapters import IpProviderFailure
from ddns_aws_updater.adapters.ipprovider_opendns import get_ip_address
from mock import patch, MagicMock, Mock


class TestGetIp(TestCase):
    def test_getIp(self):
        actual_ip = get_ip_address()
        self.assertIsInstance(actual_ip, ipaddress.IPv4Address)
        self.assertFalse(actual_ip.is_private)
        self.assertFalse(actual_ip.is_link_local)
        self.assertFalse(actual_ip.is_loopback)

    @patch("dns.resolver.query")
    @patch("dns.resolver.Resolver")
    def test_get_wrong_ip_get_none(self, resolver_query_mock, resolver_mock):
        resolver_query_mock.rrset = [type('', (object,), {"address": "0.0.0.0"})()]
        resolver_mock.query.side_effect = ValueError()
        with self.assertRaises(IpProviderFailure):
            get_ip_address()
