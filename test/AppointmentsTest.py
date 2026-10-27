from datetime import datetime
from .Helper import SupersaasTest

class AppointmentsTest(SupersaasTest):

    def test_get(self):
        schedule_id = 12345
        self.assertIsNotNone(self.client.appointments.get(schedule_id))

    def test_get_appointment_id(self):
        schedule_id = 12345
        appointment_id = 223443
        self.assertIsNotNone(
            self.client.appointments.get(schedule_id, appointment_id))

    def test_list(self):
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.list(schedule_id, True, datetime.now(),
                                          10))

    def test_create(self):
        user_id = 67890
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.create(schedule_id, user_id,
                                            self.__appointment_attributes(),
                                            True, True))

    def test_update(self):
        appointment_id = 67890
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.update(schedule_id, appointment_id,
                                            self.__appointment_attributes()))

    def test_update_all(self):
        appointment_id = 67890
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.update(schedule_id, appointment_id,
                                            self.__appointment_attributes(),
                                            True, True))

    def test_agenda(self):
        schedule_id = 12345
        user_id = 67890
        self.assertIsNotNone(
            self.client.appointments.agenda(schedule_id, user_id))

    def test_agenda_all_params(self):
        schedule_id = 12345
        user_id = 67890
        self.assertIsNotNone(
            self.client.appointments.agenda(schedule_id, user_id,
                                            "2017-01-31 14:30:00", True))

    def test_agenda_slots(self):
        schedule_id = 12345
        user_id = 67890
        self.assertIsNotNone(
            self.client.appointments.agenda_slots(schedule_id, user_id))

    def test_agenda_slots_from_time(self):
        schedule_id = 12345
        user_id = 67890
        self.assertIsNotNone(
            self.client.appointments.agenda_slots(schedule_id, user_id,
                                                  "2017-01-31 14:30:00"))

    def test_available(self):
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.available(schedule_id, datetime.now(),
                                               10))

    def test_available_full(self):
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.available(schedule_id,
                                               "2017-01-31 14:30:00", 10,
                                               'My resource', False, 10))

    def test_changes(self):
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.changes(schedule_id,
                                             "2017-01-31 14:30:00"))

    def test_changes_all(self):
        schedule_id = 12345
        user_id = 67890
        self.assertIsNotNone(
            self.client.appointments.changes(schedule_id,
                                             "2017-01-31 14:30:00",
                                             "2017-01-31 15:30:00", True,
                                             user_id, 10, 10))

    def test_range(self):
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.range(schedule_id, False,
                                           "2017-01-31 14:30:00"))

    def test_range_all(self):
        schedule_id = 12345
        user_id = 67890
        resource_id = 54321
        service_id = 876543
        self.assertIsNotNone(
            self.client.appointments.range(schedule_id, True,
                                           "2017-01-31 14:30:00",
                                           "2017-01-31 16:30:00", True,
                                           user_id, resource_id, service_id,
                                           10, 10))

    def test_changes_slots(self):
        schedule_id = 12345
        self.assertIsNotNone(
            self.client.appointments.changes_slots(schedule_id,
                                                   datetime.now()))

    def test_delete(self):
        schedule_id = 12345
        appointment_id = 67890
        self.assertIsNotNone(
            self.client.appointments.delete(schedule_id, appointment_id))

    def test_delete_all(self):
        schedule_id = 12345
        appointment_id = 67890
        self.assertIsNotNone(
            self.client.appointments.delete(schedule_id, appointment_id, True))

    def test_delete_sends_webhook_in_query(self):
        from urllib.parse import parse_qs, urlparse
        self.client.appointments.delete(12345, 67890, True)
        query = parse_qs(urlparse(self.client.last_request.full_url).query)
        self.assertEqual({'schedule_id': ['12345'], 'webhook': ['true']}, query)
        self.assertIsNone(self.client.last_request.data)

    def test_create_accepts_wrapped_attributes(self):
        import json
        self.client.appointments.create(12345, 67890, {'booking': {'full_name': 'Tester Test'}})
        self.assertEqual({'full_name': 'Tester Test'}, json.loads(self.client.last_request.data)['booking'])

    def test_update_accepts_wrapped_attributes(self):
        import json
        self.client.appointments.update(12345, 67890, {'booking': {'full_name': 'Tester Test'}})
        self.assertEqual({'full_name': 'Tester Test'}, json.loads(self.client.last_request.data)['booking'])

    def test_update_with_none_booking_sends_empty_booking(self):
        import json
        self.client.appointments.update(12345, 67890, {'booking': None})
        self.assertEqual({}, json.loads(self.client.last_request.data)['booking'])

    def __appointment_attributes(self):
        return {
            'description': 'Testing.',
            'name': 'Test',
            'email': 'test@example.com',
            'full_name': 'Tester Test',
            'address': '123 St, City',
            'mobile': '555-5555',
            'phone': '555-5555',
            'country': 'FR',
            'field_1': 'f 1',
            'field_2': 'f 2',
            'field_1_r': 'f 1 r',
            'field_2_r': 'f 2 r',
            'super_field': 'sf'
        }

    def test_update_does_not_print(self):
        # Imported here to keep the module's import block untouched
        import io
        import json
        from contextlib import redirect_stdout

        with redirect_stdout(io.StringIO()) as out:
            self.client.appointments.update(12345, 67890, {'full_name': 'Tester Test'})
        self.assertEqual('', out.getvalue())
        self.assertEqual('PUT', self.client.last_request.get_method())
        self.assertEqual({'schedule_id': 12345, 'booking': {'full_name': 'Tester Test'}},
                         json.loads(self.client.last_request.data))
