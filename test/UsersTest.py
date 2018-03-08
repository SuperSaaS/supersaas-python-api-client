from .Helper import *


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
        self.assertIsNotNone(self.client.users.create(self.__user_attributes()))

    def test_create_fk(self):
        user_fk = '6789fk'
        self.assertIsNotNone(self.client.users.create(self.__user_attributes(), user_fk))

    def test_update(self):
        user_id = 12345
        self.assertIsNotNone(self.client.users.update(user_id, self.__user_attributes()))

    def test_delete(self):
        user_id = 12345
        self.assertIsNotNone(self.client.users.delete(user_id))

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