from unittest import TestCase

import ipaddress
from ddns_aws_updater.adapters import IpProviderFailure, UpdateDnsFailed
from ddns_aws_updater.__main__ import DdnsUpdater
from flexmock import flexmock
from mock import Mock, patch


class TestDdnsUpdater(TestCase):
    def setUp(self):
        self.ip_object = ipaddress.ip_address(u"192.0.2.10")
        self.ip_provider_mock = Mock(return_value=self.ip_object)
        self.ddns_provider_mock = Mock()
        self.config_mock = Mock()

        self.logpatcher = patch('ddns_aws_updater.__main__.logger', flexmock())
        self.logmock = self.logpatcher.start()

    def tearDown(self):
        self.logpatcher.stop()

    @patch("ddns_aws_updater.__main__.Config")
    def test_no_config_file(self, config_mock):
        config_mock.side_effect = err = IOError("file not found")

        self.logmock.should_receive('exception').with_args(err).once()
        self.logmock.should_receive('error').with_args('Unable to load config file').once().ordered()

        DdnsUpdater(self.ip_provider_mock, self.ddns_provider_mock)

    def test_run(self):
        self.config_mock.get_aws_config.return_value = {}
        self.logmock.should_receive('info').with_args('ip [192.0.2.10] was discovered, sending to ddns provider ...').once().ordered()
        self.logmock.should_receive('info').with_args('ddns provider updated !').once().ordered()
        updater = DdnsUpdater(self.ip_provider_mock, self.ddns_provider_mock, self.config_mock)

        updater.run()

        self.assertTrue(self.ip_provider_mock.called)
        self.ddns_provider_mock.assert_called_with(self.ip_object, {})

    def test_with_failing_ddns_provider(self):
        self.ddns_provider_mock.side_effect = error = UpdateDnsFailed("test")
        self.logmock.should_receive('info').with_args('ip [192.0.2.10] was discovered, sending to ddns provider ...').once().ordered()
        self.logmock.should_receive('exception').with_args(error).once().ordered()
        self.logmock.should_receive('error').with_args('Could not update dns: test').once().ordered()

        updater = DdnsUpdater(self.ip_provider_mock, self.ddns_provider_mock, self.config_mock)

        updater.run()

    def test_with_failing_ip_provider(self):
        self.logmock.should_receive('error').with_args('no IP address was discovered').once().ordered()
        updater = DdnsUpdater(Mock(side_effect=IpProviderFailure()), self.ddns_provider_mock, self.config_mock)

        updater.run()

        self.assertFalse(self.ddns_provider_mock.called)


