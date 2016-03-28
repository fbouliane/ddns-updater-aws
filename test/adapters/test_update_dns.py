from unittest import TestCase

from ddns_updater_aws.adapters.ddnsprovider_aws import update_dns
from ddns_updater_aws.__main__ import UpdateDnsFailed
from flexmock import flexmock
from mock import patch, Mock


class TestUpdateDns(TestCase):
    def setUp(self):
        self._patcher = patch('route53.connect')
        self.route53_mock = self._patcher.start()
        self.route53_mock.return_value = self.connection_mock = Mock()

        self._logmockpatcher = patch('ddns_updater_aws.adapters.ddnsprovider_aws.logger', flexmock())
        self.logmock = self._logmockpatcher.start()

    def tearDown(self):
        self._patcher.stop()
        self._logmockpatcher.stop()

    def test_no_recordset(self):
        self.connection_mock.get_hosted_zone_by_id.return_value = Mock(record_sets=[])

        with self.assertRaises(UpdateDnsFailed):
            update_dns("192.0.2.10", get_a_default_config())

        self.assertTrue(self.route53_mock.called)
        self.connection_mock.get_hosted_zone_by_id.assert_called_with("AWS_ZONE")

    def test_wrong_credentials(self):
        self.connection_mock.get_hosted_zone_by_id.side_effect = TypeError()
        self.logmock.should_receive("exception").once()
        with self.assertRaises(UpdateDnsFailed):
            update_dns("192.0.2.10", get_a_default_config())

    def test_general(self):
        connection_mock = Mock()
        self.route53_mock.return_value = connection_mock
        rrset_mock = Mock()
        rrset_mock.name = get_a_default_config()['record_set_name']
        connection_mock.get_hosted_zone_by_id.return_value = Mock(record_sets=[rrset_mock])

        update_dns("192.0.2.10", get_a_default_config())

        self.assertTrue(self.route53_mock.called)
        connection_mock.get_hosted_zone_by_id.assert_called_with("AWS_ZONE")
        self.assertEqual("192.0.2.10", rrset_mock.records[0])
        self.assertTrue(rrset_mock.save.called)


def get_a_default_config():
    return dict(
        aws_access_key_id="AWS_KEY",
        aws_secret_access_key="AWS_SECRET",
        zone_id="AWS_ZONE",
        record_set_name="RECORDSET_HOSTNAME"
    )
