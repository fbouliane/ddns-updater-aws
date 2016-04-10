#!/usr/bin/env python2

import logging

import sys

import os
from adapters import ipprovider_opendns, UpdateDnsFailed, IpProviderFailure
from adapters import ddnsprovider_aws
from adapters.config import Config

logger = logging.getLogger(__name__)


class DdnsUpdater(object):
    def __init__(self, ip_provider=None, ddns_provider=None, config_provider=None):
        self._ip_address_provider = ip_provider or ipprovider_opendns.get_ip_address
        self._ddns_provider = ddns_provider or ddnsprovider_aws.update_dns
        self._config_provider = config_provider
        if not config_provider:
            try:
                self._config_provider = Config(os.path.join(os.path.dirname(__file__), "ddns_updater_aws.ini"))
            except IOError as e:
                logger.exception("Unable to load config file")

    def run(self):
        logger.info("Discovering ip address...")
        ipprovider_config = self._config_provider.get_opendns_config()
        try:
            ip = self._ip_address_provider(ipprovider_config)
        except IpProviderFailure:
            logger.error("no IP address was discovered")
            return

        logger.info("ip [{}] was discovered, sending to ddns provider ...".format(ip))
        aws_config = self._config_provider.get_aws_config()
        try:
            self._ddns_provider(ip, aws_config)
            logger.info('ddns provider updated !')
        except UpdateDnsFailed as e:
            logger.exception(e)
            logger.error("Could not update dns: {}".format(e.message))


def main():  # pragma: no cover
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    ddns_updater = DdnsUpdater()
    ddns_updater.run()
    
    
if __name__ == "__main__":
    main()
