import subprocess

import sys

import time

import os
from unittest import TestCase


class TestMain(TestCase):
    def _get_process_output(self):
        project_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ddns_updater_aws", "__main__.py")
        process = [sys.executable, project_dir]
        proc = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        return proc

    def test_logging(self):
        datetime_format = "%Y-%m-%d %H:%M:%S,%f"
        output = self._get_process_output().stdout.read()
        first_return = output.split(' - ', 1)[0]
        try:
            time.strptime(first_return, datetime_format)
        except ValueError:
            self.fail("{} should be a datetime of format {}".format(first_return, datetime_format))