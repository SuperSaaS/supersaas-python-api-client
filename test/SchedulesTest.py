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
