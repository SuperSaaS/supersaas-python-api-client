"""Tests for the parameter validation shared by all API classes."""

import unittest
from datetime import datetime

from SuperSaaS import Error
from SuperSaaS.API import BaseApi


class BaseApiTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.api = BaseApi(None)

    def test_validate_datetime(self):
        self.assertEqual('2030-01-31 14:30:00', self.api._validate_datetime(datetime(2030, 1, 31, 14, 30)))
        self.assertEqual('2030-01-31 14:30:00', self.api._validate_datetime('2030-01-31 14:30:00'))
        for value in ('2030-01-31', '31-01-2030 14:30:00', 12345, None):
            with self.assertRaises(Error):
                self.api._validate_datetime(value)

    def test_validate_present(self):
        self.assertEqual('x', self.api._validate_present('x'))
        for value in ('', None, 0):
            with self.assertRaises(Error):
                self.api._validate_present(value)

    def test_validate_user(self):
        self.assertIsNone(self.api._validate_user(None))
        self.assertEqual(12345, self.api._validate_user(12345))
        self.assertEqual('6789fk', self.api._validate_user('6789fk'))
        with self.assertRaises(Error):
            self.api._validate_user(1.5)

    def test_validate_promotion(self):
        self.assertEqual('ab1235', self.api._validate_promotion('ab1235'))
        for value in ('', 'ab-12', 12345, None):
            with self.assertRaises(Error):
                self.api._validate_promotion(value)

    def test_validate_duplicate(self):
        for value in ('ignore', 'raise'):
            self.assertEqual(value, self.api._validate_duplicate(value))
        with self.assertRaises(Error):
            self.api._validate_duplicate('error')

    def test_validate_notfound(self):
        for value in ('error', 'ignore'):
            self.assertEqual(value, self.api._validate_notfound(value))
        with self.assertRaises(Error):
            self.api._validate_notfound('raise')

    def test_validate_options(self):
        self.assertEqual('a', self.api._validate_options('a', ['a', 'b']))
        with self.assertRaises(Error):
            self.api._validate_options('c', ['a', 'b'])
