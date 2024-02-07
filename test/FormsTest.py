from datetime import datetime
from .Helper import SupersaasTest

class FormsTest(SupersaasTest):

    def test_get(self):
        super_form_id = 12345
        self.assertIsNotNone(self.client.forms.get(super_form_id))

    def test_list(self):
        form_id = 67890
        self.assertIsNotNone(self.client.forms.list(form_id, datetime.now()))

    def test_list_all(self):
        form_id = 67890
        user_id = 12345
        self.assertIsNotNone(
            self.client.forms.list(form_id, datetime.now(), user_id))

    def test_forms(self):
        self.assertIsNotNone(self.client.forms.forms())
