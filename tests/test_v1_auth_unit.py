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
from hubstaff.exceptions import HubstaffError, AuthenticationError


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app_token = ''.join([random.choice(string.ascii_letters)
                                  for _ in range(43)])
        self.auth_token = ''.join([random.choice(string.ascii_letters)
                                   for _ in range(43)])

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
        client._authenticate()

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
        client._authenticate()

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
            client._authenticate()

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
        with self.assertRaises(AuthenticationError) as err_ctx:
            client._authenticate()

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
        with self.assertRaises(AuthenticationError) as err_ctx:
            client._authenticate()

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
        with self.assertRaises(AuthenticationError) as err_ctx:
            client._authenticate()

        self.assertEqual(err_ctx.exception.message,
                         'Invalid email and/or password')


if __name__ == '__main__':
    unittest.main()
