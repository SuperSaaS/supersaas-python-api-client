import unittest
from SuperSaaS import Client
from SuperSaaS import Configuration


class SupersaasTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.__fileName = ""
        self.__file = None

        self.config = Configuration()
        self.client = Client(self.config)
        self.client.account_name = 'test'
        self.client.password = 'test'
        self.client.dry_run = True
