import sys
import threading
import os
import time

from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
from base64 import b64encode
from SuperSaaS import API
from .Error import Error

PYTHON_VERSION = '.'.join([str(info) for info in sys.version_info])

API_VERSION = '3'
VERSION = '2.0.0'


class RateLimiter:
    # The rate limiter allows a maximum of 4 requests to be made within the specified time window, which is defined by the WINDOW_SIZE constant
    WINDOW_SIZE = 1
    MAX_PER_WINDOW = 4

    def __init__(self):
        self.queue = [None] * self.MAX_PER_WINDOW

    def throttle(self):
        # Represents the timestamp of the oldest request within the time window
        oldest_request = self.queue.pop() if self.queue else None
        # Push the current timestamp into the queue
        self.queue.append(time.time())
        # This ensures that the client does not make requests faster than the defined rate limit
        if oldest_request and (time_elapsed := time.time() -
                               oldest_request) < self.WINDOW_SIZE:
            time.sleep(self.WINDOW_SIZE - time_elapsed)


class Client:
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls(Configuration())
        return cls.__singleton_instance

    @classmethod
    def configure(cls,
                  account_name,
                  api_key,
                  dry_run=False,
                  verbose=False,
                  host=None):
        cls.instance().account_name = account_name
        cls.instance().api_key = api_key
        cls.instance().dry_run = dry_run
        cls.instance().verbose = verbose
        cls.instance().host = host or cls.instance().host

    @classmethod
    def _user_agent(cls):
        return f"SSS/{VERSION} Python/{PYTHON_VERSION} API/{API_VERSION}"

    def __init__(self, configuration):
        self.account_name = configuration.account_name
        self.api_key = configuration.api_key
        self.host = configuration.host
        self.dry_run = configuration.dry_run
        self.verbose = configuration.verbose

        self.appointments = API.Appointments(self)
        self.forms = API.Forms(self)
        self.schedules = API.Schedules(self)
        self.users = API.Users(self)
        self.groups = API.Groups(self)
        self.promotions = API.Promotions(self)

        self.last_request = None
        self.rate_limiter = RateLimiter()

    def get(self, path, query=None):
        return self.request('GET', path, None, query)

    def post(self, path, params=None, query=None):
        return self.request('POST', path, params, query)

    def put(self, path, params=None, query=None):
        return self.request('PUT', path, params, query)

    def delete(self, path, params=None, query=None):
        return self.request('DELETE', path, params, query)

    def request(self, http_method, path, params=None, query=None):
        self.rate_limiter.throttle()
        if params is None:
            params = {}
        if query is None:
            query = {}

        if not self.account_name:
            raise Error(
                "Account name not configured. Call `SuperSaaS.Client.configure`."
            )
        if not self.api_key:
            raise Error(
                "Account api key not configured. Call `SuperSaaS.Client.configure`."
            )

        auth = b64encode(
            f'{self.account_name}:{self.api_key}'.encode()).decode()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': self._user_agent(),
            'Authorization': f"Basic {auth}"
        }

        url = f"{self.host}/api{path}.json"
        if query:
            query = dict(
                filter(lambda item: item[1] is not None, query.items()))
            querystring = urlencode(query)
            url = f"{url}?{querystring}"

        if params:
            data = dict(
                filter(lambda item: item[1] is not None, params.items()))
            data = json.dumps(data).encode('utf-8')
        else:
            data = None
        req = Request(url, data, headers)

        if http_method in ['GET', 'POST', 'PUT', 'DELETE']:
            req.get_method = lambda: http_method
        else:
            raise Error(
                f"Invalid HTTP Method: {http_method}. Only `GET`, `POST`, `PUT`, `DELETE` supported."
            )

        if self.verbose:
            print('')
            print("### SuperSaaS Client Request:")
            print('')
            print(f"#{http_method} #{url}")
            print('')
            print(data)
            print('')
            print("------------------------------")

        self.last_request = req
        if self.dry_run:
            return {}

        try:
            with urlopen(req) as res:
                location = res.headers['Location'] if res.getcode(
                ) == 201 and http_method == 'POST' else None
                val = res.read()
                data = location or (val if not val else json.loads(val))
                if self.verbose:
                    print('')
                    print("Response:")
                    print('')
                    print(data)
                    print('')
                    print("==============================")

                return data
        except HTTPError as e:
            raise Error(f"HTTP Request Error: {e.reason}, ({url})") from e


class Configuration:
    DEFAULT_HOST = 'https://www.supersaas.com'

    def __init__(self):
        self.account_name = os.environ[
            'SSS_API_ACCOUNT_NAME'] if 'SSS_API_ACCOUNT_NAME' in os.environ else ''
        self.api_key = os.environ[
            'SSS_API_KEY'] if 'SSS_API_KEY' in os.environ else ''
        self.host = os.environ[
            'SSS_API_HOST'] if 'SSS_API_HOST' in os.environ else self.DEFAULT_HOST
        self.dry_run = False
        self.verbose = False
