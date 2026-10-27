import unittest
from SuperSaaS import Client
from SuperSaaS import Configuration


class SupersaasTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.config = Configuration()
        self.client = Client(self.config)
        self.client.account_name = 'test'
        self.client.api_key = 'test'
        self.client.dry_run = True
