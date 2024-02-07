import re
from datetime import datetime
from SuperSaaS.Error import Error


class BaseApi:
    INTEGER_REGEX = re.compile(r'\A[0-9]+\Z')
    DATETIME_REGEX = re.compile(
        r'\A\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\Z')
    PROMOTION_REGEX = re.compile(r'\A[a-zA-Z0-9]+\Z')

    def __init__(self, client):
        self.client = client

    def _validate_id(self, value):
        return value

    def _validate_number(self, value):
        return self._validate_id(value)

    def _validate_present(self, value):
        if not value:
            raise Error("Required parameter is missing.")
        return value

    def _validate_user(self, value):
        if value is None:
            return None

        if not isinstance(value, (int, str)):
            raise Error(f"Invalid user id parameter: {value}")
        return value

    def _validate_datetime(self, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(value, str) and self.DATETIME_REGEX.match(value):
            return value
        raise Error(
            f"Invalid datetime parameter: {value}. Provide a Time object or formatted 'YYYY-DD-MM%HH:MM:SS' string."
            )

    def _validate_options(self, value, options):
        if value in options:
            return value
        raise Error(
            f"Invalid option parameter: {value}. Must be one of {', '.join(options)}."
        )

    def _validate_promotion(self, value):
        if not isinstance(value, str) or not value or not re.match(
                self.PROMOTION_REGEX, value):
            raise Error(
                'Required parameter promotional code not found or contains other than alphanumeric characters.'
            )
        return value

    def _validate_duplicate(self, value):
        if not isinstance(value, str) or value not in ['ignore', 'raise']:
            raise Error(
                "Required parameter duplicate can only be 'ignore' or 'raise'."
            )
        return value

    def _validate_notfound(self, value):
        if not isinstance(value, str) or value not in ['error', 'ignore']:
            raise Error(
                "Required parameter notfound can only be 'error' or 'ignore'.")
        return value
