import os
from configparser import ConfigParser


class Config(object):
    def __init__(self, filename):
        self.config = ConfigParser()
        if os.path.isfile(filename):
            self.config.read(filename)
        else:
            raise IOError("File {} not found".format(filename))

    def get_aws_config(self):
        return self.config["ddns_provider_aws"]

    def get_opendns_config(self):
        if 'ip_provider_opendns' in self.config.sections():
            return self.config['ip_provider_opendns']