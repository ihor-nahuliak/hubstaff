# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import string
import random

try:
    from unittest import mock
except ImportError:
    import mock  # python 2 compatibility

from hubstaff.client_v1 import HubstaffClient
from hubstaff.exceptions import HubstaffError, HubstaffAuthError


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app_token = ''.join([random.choice(string.ascii_letters)
                                  for _ in range(43)])
        self.auth_token = ''.join([random.choice(string.ascii_letters)
                                   for _ in range(43)])

    def test_init_raises_error_on_no_auth_token_no_username(self):
        with self.assertRaises(ValueError) as err_ctx:
            HubstaffClient(app_token=self.app_token,
                           password='ValidPasswordHere')

        self.assertEqual(err_ctx.exception.args[0],
                         'auth_token or (username, password) pair must be set')

    def test_init_raises_error_on_no_auth_token_no_password(self):
        with self.assertRaises(ValueError) as err_ctx:
            HubstaffClient(app_token=self.app_token,
                           username='good@hubstaff.com')

        self.assertEqual(err_ctx.exception.args[0],
                         'auth_token or (username, password) pair must be set')

    @mock.patch('requests.post')
    def test_authenticate_method_returns_auth_token_no_password(self, m_post):
        m_post.return_value.status_code = 401
        m_post.return_value.json.return_value = {
            'error': 'Invalid email and/or password'
        }

        client = HubstaffClient(
            app_token=self.app_token,
            auth_token=self.auth_token)
        auth_token = client.authenticate()

        self.assertEqual(auth_token, self.auth_token)

    @mock.patch('requests.post')
    def test_authenticate_method_no_password_doesnt_call_api(self, m_post):
        client = HubstaffClient(
            app_token=self.app_token,
            auth_token=self.auth_token)
        client.authenticate()

        m_post.assert_not_called()

    @mock.patch('requests.post')
    def test_authenticate_method_returns_auth_token(self, m_post):
        m_post.return_value.status_code = 200
        m_post.return_value.json.return_value = {
            'user': {'auth_token': self.auth_token}
        }

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        auth_token = client.authenticate()

        self.assertEqual(auth_token, self.auth_token)

    @mock.patch('requests.post')
    def test_authenticate_method_setups_auth_token(self, m_post):
        m_post.return_value.status_code = 200
        m_post.return_value.json.return_value = {
            'user': {'auth_token': self.auth_token}
        }

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        client.authenticate()

        self.assertEqual(client._auth_token, self.auth_token)

    @mock.patch('requests.post')
    def test_authenticate_method_calls_post_with_right_params(self, m_post):
        m_post.return_value.status_code = 200
        m_post.return_value.json.return_value = {
            'user': {'auth_token': self.auth_token}
        }

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        client.authenticate()

        self.assertEqual(m_post.call_count, 1)
        call_args, call_kwargs = m_post.call_args
        self.assertEqual(call_args, (
            'https://api.hubstaff.com/v1/auth',
        ))
        self.assertDictEqual(call_kwargs, {
            'headers': {
                'App-Token': self.app_token
            },
            'data': {
                'email': 'good@hubstaff.com',
                'password': 'ValidPasswordHere'
            },
        })

    @mock.patch('requests.post')
    def test_authenticate_method_raises_too_many_requests_error(self, m_post):
        m_post.return_value.status_code = 429
        m_post.return_value.json.return_value = {
            'error': 'Rate limit has been reached. '
                     'Please wait before making your next request.'
        }

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        with self.assertRaises(HubstaffError) as err_ctx:
            client.authenticate()

        self.assertEqual(err_ctx.exception.message,
                         'Rate limit has been reached. '
                         'Please wait before making your next request.')

    @mock.patch('requests.post')
    def test_authenticate_method_raises_invalid_app_token_error(self, m_post):
        m_post.return_value.status_code = 401
        m_post.return_value.json.return_value = {
            'error': 'Invalid app_token'
        }

        client = HubstaffClient(
            app_token='bad_token',
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        with self.assertRaises(HubstaffAuthError) as err_ctx:
            client.authenticate()

        self.assertEqual(err_ctx.exception.message, 'Invalid app_token')

    @mock.patch('requests.post')
    def test_authenticate_method_raises_invalid_username_error(self, m_post):
        m_post.return_value.status_code = 401
        m_post.return_value.json.return_value = {
            'error': 'Invalid email and/or password'
        }

        client = HubstaffClient(
            app_token=self.app_token,
            username='bad@hubstaff.com',
            password='ValidPasswordHere')
        with self.assertRaises(HubstaffAuthError) as err_ctx:
            client.authenticate()

        self.assertEqual(err_ctx.exception.message,
                         'Invalid email and/or password')

    @mock.patch('requests.post')
    def test_authenticate_method_raises_invalid_password_error(self, m_post):
        m_post.return_value.status_code = 401
        m_post.return_value.json.return_value = {
            'error': 'Invalid email and/or password'
        }

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='?' * 16)
        with self.assertRaises(HubstaffAuthError) as err_ctx:
            client.authenticate()

        self.assertEqual(err_ctx.exception.message,
                         'Invalid email and/or password')


if __name__ == '__main__':
    unittest.main()
