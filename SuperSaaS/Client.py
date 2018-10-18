import sys
import threading
import os

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

try:
    import json
except ImportError:
    import simplejson as json

try:
    basestring
except NameError:
    basestring = str

from base64 import b64encode

from SuperSaaS import API
from .Error import Error

PYTHON_VERSION = '.'.join([str(info) for info in sys.version_info])

API_VERSION = '1'
VERSION = '0.9.0'


class Client(object):
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
    def configure(cls, account_name, password, dry_run=False, verbose=False, host=None):
        cls.instance().account_name = account_name
        cls.instance().password = password
        cls.instance().dry_run = dry_run
        cls.instance().verbose = verbose
        cls.instance().host = host or cls.instance().host

    @classmethod
    def _user_agent(cls):
        return "SSS/{} Python/{} API/{}".format(VERSION, PYTHON_VERSION, API_VERSION)

    def __init__(self, configuration):
        self.account_name = configuration.account_name
        self.password = configuration.password
        self.host = configuration.host
        self.dry_run = configuration.dry_run
        self.verbose = configuration.verbose

        self.appointments = API.Appointments(self)
        self.forms = API.Forms(self)
        self.schedules = API.Schedules(self)
        self.users = API.Users(self)

        self.last_request = None

    def get(self, path, query=None):
        return self.request('GET', path, None, query)

    def post(self, path, params=None, query=None):
        return self.request('POST', path, params, query)

    def put(self, path, params=None, query=None):
        return self.request('PUT', path, params, query)

    def delete(self, path, params=None, query=None):
        return self.request('DELETE', path, params, query)

    def request(self, http_method, path, params=None, query=None):
        if params is None:
            params = {}
        if query is None:
            query = {}

        if not self.account_name:
            raise Error("Account name not configured. Call `SuperSaaS.Client.configure`.")
        if not self.password:
            raise Error("Account password not configured. Call `SuperSaaS.Client.configure`.")

        auth = b64encode('{}:{}'.format(self.account_name, self.password).encode())
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': self._user_agent(),
            'Authorization': "Basic {}".format(auth)
        }

        url = "{}/api{}.json".format(self.host, path)
        if query:
            querystring = urlencode(query)
            url = "{}?{}".format(url, querystring)

        if params:
            data = dict(filter(lambda item: item[1] is not None, params.items()))
            data = json.dumps(data)
        else:
            data = None
        req = Request(url, data, headers)

        if http_method == 'GET':
            req.get_method = lambda: http_method
        elif http_method == 'POST':
            req.get_method = lambda: http_method
        elif http_method == 'PUT':
            req.get_method = lambda: http_method
        elif http_method == 'DELETE':
            req.get_method = lambda: http_method
        else:
            raise Error("Invalid HTTP Method: {}. Only `GET`, `POST`, `PUT`, `DELETE` supported.".format(http_method))

        if self.verbose:
            print('')
            print("### SuperSaaS Client Request:")
            print('')
            print("#{} #{}".format(http_method, url))
            print('')
            print(data)
            print('')
            print("------------------------------")

        self.last_request = req
        if self.dry_run:
            return {}

        try:
            res = urlopen(req)
            data = json.loads(res) if isinstance(res, basestring) else json.loads(res.read())

            if self.verbose:
                print('')
                print("Response:")
                print('')
                print(data)
                print('')
                print("==============================")

            return data
        except HTTPError as e:
            raise Error("HTTP Request Error ({}): {}".format(url, e.reason))


class Configuration(object):
    DEFAULT_HOST = 'https://www.supersaas.com'

    def __init__(self):
        self.account_name = os.environ['SSS_API_ACCOUNT_NAME'] if 'SSS_API_ACCOUNT_NAME' in os.environ else ''
        self.password = os.environ['SSS_API_PASSWORD'] if 'SSS_API_PASSWORD' in os.environ else ''
        self.host = os.environ['SSS_API_HOST'] if 'SSS_API_HOST' in os.environ else self.DEFAULT_HOST
        self.dry_run = False
        self.verbose = False
