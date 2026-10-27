from .Helper import SupersaasTest


class GroupsTest(SupersaasTest):

    def test_list(self):
        self.assertIsNotNone(self.client.groups.list())
        self.assertEqual('GET', self.client.last_request.get_method())
        self.assertEqual('https://www.supersaas.com/api/groups.json', self.client.last_request.full_url)
