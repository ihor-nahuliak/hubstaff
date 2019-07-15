# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import os

from hubstaff.client_v1 import HubstaffClient
from hubstaff.exceptions import AuthenticationError


@unittest.skip('integration')
class TestCase(unittest.TestCase):

    def test_authenticate_method_setups_auth_token(self):
        client = HubstaffClient(
            app_token=os.getenv('HUBSTAFF_APP_TOKEN'),
            username=os.getenv('HUBSTAFF_USERNAME'),
            password=os.getenv('HUBSTAFF_PASSWORD'))
        client._authenticate()

        self.assertIsNotNone(client._auth_token)

    def test_authenticate_method_raises_error_on_invalid_app_token(self):
        client = HubstaffClient(
            app_token='x' * 43,
            username=os.getenv('HUBSTAFF_USERNAME'),
            password=os.getenv('HUBSTAFF_PASSWORD'))
        with self.assertRaises(AuthenticationError) as err_ctx:
            client._authenticate()

        self.assertEqual(err_ctx.exception.message, 'Invalid app_token')

    def test_authenticate_method_raises_error_on_invalid_username(self):
        client = HubstaffClient(
            app_token=os.getenv('HUBSTAFF_APP_TOKEN'),
            username='noreply@hubstaff.com',
            password=os.getenv('HUBSTAFF_PASSWORD'))
        with self.assertRaises(AuthenticationError) as err_ctx:
            client._authenticate()

        self.assertEqual(err_ctx.exception.message,
                         'Invalid email and/or password')

    def test_authenticate_method_raises_error_on_invalid_password(self):
        client = HubstaffClient(
            app_token=os.getenv('HUBSTAFF_APP_TOKEN'),
            username=os.getenv('HUBSTAFF_USERNAME'),
            password='?' * 16)
        with self.assertRaises(AuthenticationError) as err_ctx:
            client._authenticate()

        self.assertEqual(err_ctx.exception.message,
                         'Invalid email and/or password')


if __name__ == '__main__':
    unittest.main()
