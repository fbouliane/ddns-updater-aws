from unittest import TestCase

import ipaddress
import netifaces
from ddns_updater_aws.adapters import IpProviderFailure
from ddns_updater_aws.adapters.ipprovider_opendns import get_ip_address, dns
from flexmock import flexmock
from mock import patch, MagicMock


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

    @patch("dns.resolver.query", MagicMock())
    def test_with_specified_port(self):
        flexmock(dns.resolver.Resolver).should_receive("query"). \
            with_args("myip.opendns.com"). \
            and_return([u"192.168.2.1"]).once().ordered()

        config_mock = dict()
        ip = get_ip_address(config_mock)

        self.assertEqual(ip, ipaddress.ip_address(u'192.168.2.1'))

    @patch("dns.resolver.query", MagicMock())
    def test_with_specified_port(self):
        flexmock(dns.resolver.Resolver).should_receive("query"). \
            with_args("myip.opendns.com", source_port=33333).\
            and_return([u"192.168.2.1"]).once().ordered()

        config_mock = dict(source_port="33333")
        ip = get_ip_address(config_mock)

        self.assertEqual(ip, ipaddress.ip_address(u'192.168.2.1'))

    @patch("dns.resolver.query", MagicMock())
    def test_with_specified_port_with_interface(self):
        flexmock(netifaces).should_receive("ifaddresses").with_args('eth0').and_return(
            {2: {0: {'addr': "192.168.2.2"}}}
        ).once().ordered()
        flexmock(dns.resolver.Resolver).should_receive("query").\
            with_args("myip.opendns.com", source_port=33333, source=u'192.168.2.2').\
            and_return([u"192.168.2.1"]).once().ordered()

        config_mock = dict(source_port="33333", interface_name="eth0")
        ip = get_ip_address(config_mock)

        self.assertEqual(ip, ipaddress.ip_address(u'192.168.2.1'))
