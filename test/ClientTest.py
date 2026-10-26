from .Helper import SupersaasTest
import SuperSaaS
import time
import os
import unittest

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
        self.assertGreaterEqual(end_time - start_time, 4.0)
        self.assertLessEqual(end_time - start_time, 4.1)

    def test_ping(self):
        self.assertTrue(self.client.ping())
        self.assertEqual('GET', self.client.last_request.get_method())
        self.assertIn('/api/ping.json', self.client.last_request.full_url)

    def __http_error(self, code, reason, body):
        import io
        from urllib.error import HTTPError
        return HTTPError('http://x', code, reason, {}, io.BytesIO(body))

    def test_http_error_details(self):
        from unittest import mock
        self.client.dry_run = False
        body = b'{"errors":[{"status":"404","title":"Not found"}]}'
        with mock.patch('SuperSaaS.Client.urlopen',
                        side_effect=self.__http_error(404, 'Not Found', body)):
            with self.assertRaises(SuperSaaS.Error) as cm:
                self.client.get("/test")
        self.assertEqual(
            'HTTP Request Error: Not Found, (https://www.supersaas.com/api/test.json)',
            str(cm.exception))
        self.assertEqual(404, cm.exception.status)
        self.assertEqual([{'status': '404', 'title': 'Not found'}], cm.exception.errors)

    def test_http_error_empty_body(self):
        from unittest import mock
        self.client.dry_run = False
        with mock.patch('SuperSaaS.Client.urlopen',
                        side_effect=self.__http_error(422, 'Unprocessable Content', b'')):
            with self.assertRaises(SuperSaaS.Error) as cm:
                self.client.get("/test")
        self.assertTrue(str(cm.exception).startswith('HTTP Request Error: Unprocessable Content, ('))
        self.assertEqual(422, cm.exception.status)
        self.assertEqual([], cm.exception.errors)

    def test_error_defaults(self):
        error = SuperSaaS.Error('x')
        self.assertIsNone(error.status)
        self.assertEqual([], error.errors)
