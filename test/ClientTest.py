from .Helper import SupersaasTest
import SuperSaaS
import time
import os

class ClientTest(SupersaasTest):

    def test_api(self):
        self.assertIsNotNone(self.client.appointments)
        self.assertIsNotNone(self.client.forms)
        self.assertIsNotNone(self.client.users)

    def test_request(self):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            self.assertIsNotNone(
                self.client.request(method, '/test', {'test': True}))

    def test_instance_configuration(self):
        self.client.configure(account_name='account',
                              api_key='xxxxxxxxxxxxxxxxxxxxxx')
        self.assertEqual('account', SuperSaaS.Client.instance().account_name)
        self.assertEqual('xxxxxxxxxxxxxxxxxxxxxx',
                         SuperSaaS.Client.instance().api_key)

    @unittest.skipIf(
        os.environ.get('SSS_PYTHON_RATE_LIMITER_TEST') != 'true',
        "Skipping RateLimiter test")
    def test_rate_limit(self):
        start_time = time.time()
        # Simulate making 21 requests within the same second
        for _ in range(21):
            self.client.request('GET', '/test', {'test': True})
        end_time = time.time()

        # Assert that the elapsed time is greater than or equal to 5.0 seconds
        self.assertGreaterEqual(end_time - start_time, 5.0)
