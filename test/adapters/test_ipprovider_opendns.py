from unittest import TestCase

import ipaddress
from ddns_updater_aws.adapters import IpProviderFailure
from ddns_updater_aws.adapters.ipprovider_opendns import get_ip_address, dns
from flexmock import flexmock
from mock import patch, Mock


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

    @patch("dns.resolver.query")
    def test_with_specified_port(self, resolver_query_mock):
        flexmock(dns.resolver.Resolver).should_receive("query").with_args("myip.opendns.com", source_port=33333).once().ordered()\
            .and_return([u"192.168.2.1"])
        config_mock = dict(source_port="33333")

        ip = get_ip_address(config_mock)

        self.assertEqual(ip, ipaddress.ip_address(u'192.168.2.1'))


