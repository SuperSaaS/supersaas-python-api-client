"""Tests for the environment based client configuration."""

import os
import unittest
from unittest import mock

from SuperSaaS import Configuration


class ConfigurationTest(unittest.TestCase):

    def test_defaults(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            config = Configuration()
        self.assertEqual('', config.account_name)
        self.assertEqual('', config.api_key)
        self.assertEqual(Configuration.DEFAULT_HOST, config.host)
        self.assertFalse(config.dry_run)
        self.assertFalse(config.verbose)

    def test_environment(self):
        env = {'SSS_API_ACCOUNT_NAME': 'account', 'SSS_API_KEY': 'key', 'SSS_API_HOST': 'http://localhost:3000'}
        with mock.patch.dict(os.environ, env, clear=True):
            config = Configuration()
        self.assertEqual('account', config.account_name)
        self.assertEqual('key', config.api_key)
        self.assertEqual('http://localhost:3000', config.host)
