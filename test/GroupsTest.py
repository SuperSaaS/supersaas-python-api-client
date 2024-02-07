from .Helper import SupersaasTest


class GroupsTest(SupersaasTest):

    def test_list(self):
        self.assertIsNotNone(self.client.groups.list)
