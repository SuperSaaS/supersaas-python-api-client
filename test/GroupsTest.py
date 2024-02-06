from datetime import datetime
from .Helper import *


class GroupsTest(SupersaasTest):
    def test_list(self):
        self.assertIsNotNone(self.client.groups.list)
