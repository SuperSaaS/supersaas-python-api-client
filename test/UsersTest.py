"""" Tests for users API """

from .Helper import SupersaasTest

class UsersTest(SupersaasTest):

    def test_get(self):
        user_id = 12345
        self.assertIsNotNone(self.client.users.get(user_id))

    def test_get_fk(self):
        user_fk = '6789fk'
        self.assertIsNotNone(self.client.users.get(user_fk))

    def test_list(self):
        self.assertIsNotNone(self.client.users.list(True, 10, 10))

    def test_create(self):
        self.assertIsNotNone(self.client.users.create(
            self.__user_attributes()))

    def test_create_fk(self):
        user_fk = '6789fk'
        self.assertIsNotNone(
            self.client.users.create(self.__user_attributes(), user_fk))

    def test_create_all(self):
        user_fk = '6789fk'
        self.assertIsNotNone(
            self.client.users.create(self.__user_attributes(), user_fk, True,
                                     'ignore'))

    def test_update(self):
        user_id = 12345
        self.assertIsNotNone(
            self.client.users.update(user_id, self.__user_attributes()))

    def test_update_all(self):
        user_id = 12345
        self.assertIsNotNone(
            self.client.users.update(user_id, self.__user_attributes(), True,
                                     'error'))

    def test_delete(self):
        user_id = 12345
        self.assertIsNotNone(self.client.users.delete(user_id))

    def test_delete_sends_webhook_in_query(self):
        self.client.users.delete(12345, True)
        self.assertTrue(self.client.last_request.full_url.endswith('/api/users/12345.json?webhook=true'))
        self.assertIsNone(self.client.last_request.data)

    def test_delete_without_webhook(self):
        self.client.users.delete(12345)
        self.assertTrue(self.client.last_request.full_url.endswith('/api/users/12345.json'))
        self.assertIsNone(self.client.last_request.data)

    def __user_attributes(self):
        return {
            'name': 'Test',
            'email': 'test@example.com',
            'password': 'pass123',
            'full_name': 'Tester Test',
            'address': '123 St, City',
            'mobile': '555-5555',
            'phone': '555-5555',
            'country': 'FR',
            'field_1': 'f 1',
            'field_2': 'f 2',
            'super_field': 'sf',
            'credit': 10,
            'role': 3,
            'webhook': 'true'
        }

    def test_input_field_list(self):
        self.assertIsNotNone(self.client.users.input_field_list())
        self.assertEqual('GET', self.client.last_request.get_method())
        self.assertIn('/api/input_field_list.json', self.client.last_request.full_url)
