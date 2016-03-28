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
