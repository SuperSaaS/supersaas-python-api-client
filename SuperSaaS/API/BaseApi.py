import re
import datetime
from SuperSaaS.Error import Error


class BaseApi(object):
    INTEGER_REGEX = re.compile(r'\A[0-9]+\Z')
    DATETIME_REGEX = re.compile(r'\A\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\Z')

    def __init__(self, client):
        self.client = client

    def _validate_id(self, value):
        return value

    def _validate_number(self, value):
        return self._validate_id(value)

    def _validate_present(self, value):
        if not value:
            raise Error("Required parameter is missing.")
        else:
            return value

    def _validate_datetime(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, str) and self.DATETIME_REGEX.match(value):
            return value
        else:
            raise Error("Invalid datetime parameter: {}. Provide a Time object or formatted 'YYYY-DD-MM%HH:MM:SS' string.".format(value))

    def _validate_options(self, value, options):
        if value in options:
            return value
        else:
            raise Error("Invalid option parameter: {}. Must be one of {}.".format(value, ', '.join(options)))

