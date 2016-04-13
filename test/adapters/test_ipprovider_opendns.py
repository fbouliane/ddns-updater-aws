from unittest import TestCase

import ipaddress
from ddns_updater_aws.adapters import IpProviderFailure
from ddns_updater_aws.adapters import ipprovider_opendns
from flexmock import flexmock
from mock import patch, MagicMock, Mock


class TestGetIp(TestCase):
    def test_getIp(self):
        actual_ip = ipprovider_opendns.get_ip_address()
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
            ipprovider_opendns.get_ip_address()

    @patch("dns.resolver.query", MagicMock())
    def test_with_specified_port(self):
        flexmock(ipprovider_opendns.dns.resolver.Resolver).should_receive("query"). \
            with_args("myip.opendns.com"). \
            and_return([u"192.168.2.1"]).once().ordered()

        config_mock = dict()
        ip = ipprovider_opendns.get_ip_address(config_mock)

        self.assertEqual(ip, ipaddress.ip_address(u'192.168.2.1'))

    @patch("dns.resolver.query", MagicMock())
    def test_with_specified_port(self):
        flexmock(ipprovider_opendns.dns.resolver.Resolver).should_receive("query"). \
            with_args("myip.opendns.com", source_port=33333).\
            and_return([u"192.168.2.1"]).once().ordered()

        config_mock = dict(source_port="33333")
        ip = ipprovider_opendns.get_ip_address(config_mock)

        self.assertEqual(ip, ipaddress.ip_address(u'192.168.2.1'))

    @patch("dns.resolver.query", MagicMock())
    def test_with_specified_port_with_interface(self):
        ipprovider_opendns._get_ip_address_from_interface_name = Mock(return_value=u"192.168.2.2")
        flexmock(ipprovider_opendns.dns.resolver.Resolver).should_receive("query").\
            with_args("myip.opendns.com", source_port=33333, source=u'192.168.2.2').\
            and_return([u"192.168.2.1"]).once().ordered()

        config_mock = dict(source_port="33333", interface_name="eth0")
        ip = ipprovider_opendns.get_ip_address(config_mock)

        ipprovider_opendns._get_ip_address_from_interface_name.assert_called_with("eth0")
        self.assertEqual(ip, ipaddress.ip_address(u'192.168.2.1'))
