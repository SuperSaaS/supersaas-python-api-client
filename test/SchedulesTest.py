from .Helper import SupersaasTest

class SchedulesTest(SupersaasTest):

    def test_list(self):
        self.assertIsNotNone(self.client.schedules.list())

    def test_resources(self):
        schedule_id = 12345
        self.assertIsNotNone(self.client.schedules.resources(schedule_id))

    def test_field_list(self):
        schedule_id = 12345
        self.assertIsNotNone(self.client.schedules.field_list(schedule_id))

    def test_input_field_list(self):
        schedule_id = 12345
        self.assertIsNotNone(self.client.schedules.input_field_list(schedule_id))
        self.assertEqual('GET', self.client.last_request.get_method())
        self.assertIn('/api/input_field_list.json?schedule_id=12345', self.client.last_request.full_url)
