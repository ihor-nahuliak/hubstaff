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
from hubstaff.exceptions import HubstaffError, UnauthorizedError


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app_token = ''.join([random.choice(string.ascii_letters)
                                  for _ in range(43)])
        self.auth_token = ''.join([random.choice(string.ascii_letters)
                                   for _ in range(43)])

    def _auth_endpoint(self, url, headers=None, data=None, **kwargs):
        resp = mock.Mock()
        if (url == 'https://api.hubstaff.com/v1/auth' and
                headers and headers.get('App-Token') == self.app_token and
                data and data.get('email') == 'good@hubstaff.com' and
                data and data.get('password') == 'ValidPasswordHere'):
            resp.status_code = 200
            resp.json.return_value = {
                'user': {'auth_token': self.auth_token}
            }
        else:
            resp.status_code = 401
            resp.json.return_value = {
                'error': 'Invalid email and/or password'
            }
        return resp

    def _users_endpoint(self, method, url, param=None, headers=None, **kwargs):
        resp = mock.Mock()
        if (url == 'https://api.hubstaff.com/v1/users' and method == 'get' and
                headers and headers.get('App-Token') == self.app_token):
            # returns 200 response if right auth_token gotten
            if headers.get('Auth-Token') == self.auth_token:
                resp.status_code = 200
                resp.json.return_value = {'users': []}
            else:
                resp.status_code = 401
                resp.json.return_value = {
                    'error': 'Expired auth_token'
                }
        else:
            resp.status_code = 500
            resp.json.return_value = {
                'error': 'Unknown error'
            }
        return resp

    @mock.patch('requests.request')
    def test_request_method_returns_json_data(self, m_request):
        m_request.return_value.status_code = 200
        m_request.return_value.json.return_value = {'users': []}

        client = HubstaffClient(
            app_token=self.app_token,
            auth_token=self.auth_token)

        result = client._request('get', '/users', params={
            'organization_memberships': False,
            'project_memberships': False,
            'offset': 0
        })

        self.assertDictEqual(result, {'users': []})

    @mock.patch('requests.request')
    @mock.patch('hubstaff.client_v1.HubstaffClient.authenticate')
    def test_request_method_doesnt_call_authenticate_method(
            self, m_authenticate, m_request):
        m_request.return_value.status_code = 200
        m_request.return_value.json.return_value = {'users': []}

        client = HubstaffClient(
            app_token=self.app_token,
            auth_token=self.auth_token)

        client._request('get', '/users', params={
            'organization_memberships': False,
            'project_memberships': False,
            'offset': 0
        })

        m_authenticate.assert_not_called()

    @mock.patch('requests.request')
    @mock.patch('requests.post')
    def test_request_method_calls_api_with_auth_token(self, m_post, m_request):
        m_post.side_effect = self._auth_endpoint
        m_request.return_value.status_code = 200
        m_request.return_value.json.return_value = {'users': []}

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        client._request('get', '/users', params={
            'organization_memberships': False,
            'project_memberships': False,
            'offset': 0
        })

        self.assertEqual(m_request.call_count, 1)
        call_args, call_kwargs = m_request.call_args
        self.assertEqual(call_args, (
            'get',
            'https://api.hubstaff.com/v1/users',
        ))
        self.assertDictEqual(call_kwargs, {
            'headers': {
                'App-Token': self.app_token,
                'Auth-Token': self.auth_token,
            },
            'params': {
                'organization_memberships': False,
                'project_memberships': False,
                'offset': 0
            },
            'data': None,
            'json': None,
        })

    @mock.patch('requests.request')
    @mock.patch('requests.post')
    def test_request_method_refreshes_auth_token(self, m_post, m_request):
        m_post.side_effect = self._auth_endpoint
        m_request.side_effect = self._users_endpoint

        client = HubstaffClient(
            app_token=self.app_token,
            auth_token='EXPIRED!',
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        client._request('get', '/users', params={
            'organization_memberships': False,
            'project_memberships': False,
            'offset': 0
        })

        self.assertEqual(m_request.call_count, 2)
        # The first call uses expired token
        call_args, call_kwargs = m_request.call_args_list[0]
        self.assertEqual(call_args, (
            'get',
            'https://api.hubstaff.com/v1/users',
        ))
        self.assertDictEqual(call_kwargs, {
            'headers': {
                'App-Token': self.app_token,
                'Auth-Token': 'EXPIRED!',
            },
            'params': {
                'organization_memberships': False,
                'project_memberships': False,
                'offset': 0
            },
            'data': None,
            'json': None,
        })
        # The second call uses refreshed token
        call_args, call_kwargs = m_request.call_args_list[1]
        self.assertEqual(call_args, (
            'get',
            'https://api.hubstaff.com/v1/users',
        ))
        self.assertDictEqual(call_kwargs, {
            'headers': {
                'App-Token': self.app_token,
                'Auth-Token': self.auth_token,
            },
            'params': {
                'organization_memberships': False,
                'project_memberships': False,
                'offset': 0
            },
            'data': None,
            'json': None,
        })

    @mock.patch('requests.request')
    @mock.patch('hubstaff.client_v1.HubstaffClient.authenticate')
    def test_request_method_raises_unauthorized_error(self, _, m_request):
        m_request.return_value.status_code = 401
        m_request.return_value.json.return_value = {
            'error': 'Permission denied'
        }

        client = HubstaffClient(
            app_token=self.app_token,
            auth_token=self.auth_token,  # valid but probably expired
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        with self.assertRaises(UnauthorizedError) as err_ctx:
            client._request('get', '/users', params={
                'organization_memberships': False,
                'project_memberships': False,
                'offset': 0
            })

        self.assertEqual(err_ctx.exception.message, 'Permission denied')

    @mock.patch('requests.request')
    @mock.patch('hubstaff.client_v1.HubstaffClient.authenticate')
    def test_request_method_tries_to_to_refresh_the_token(
            self, m_authenticate, m_request):
        m_request.return_value.status_code = 401
        m_request.return_value.json.return_value = {
            'error': 'Permission denied'
        }

        client = HubstaffClient(
            app_token=self.app_token,
            auth_token=self.auth_token,  # valid but probably expired
            username='good@hubstaff.com',
            password='ValidPasswordHere')

        with self.assertRaises(UnauthorizedError):
            client._request('get', '/users', params={
                'organization_memberships': False,
                'project_memberships': False,
                'offset': 0
            })

        m_authenticate.asert_called_once_with()

    @mock.patch('requests.request')
    def test_request_method_raises_too_many_requests(self, m_request):
        m_request.return_value.status_code = 429
        m_request.return_value.json.return_value = {
            'error': 'Rate limit has been reached. '
                     'Please wait before making your next request.'
        }

        client = HubstaffClient(
            app_token=self.app_token,
            auth_token=self.auth_token)
        with self.assertRaises(HubstaffError) as err_ctx:
            client._request('get', '/users', params={
                'organization_memberships': False,
                'project_memberships': False,
                'offset': 0
            })

        self.assertEqual(err_ctx.exception.message,
                         'Rate limit has been reached. '
                         'Please wait before making your next request.')

    @mock.patch('hubstaff.client_v1.HubstaffClient._request')
    def test_get_method_calls_request_method(self, m_request):
        m_request.return_value = {'users': []}

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        result = client._get('/users', params={
            'organization_memberships': False,
            'project_memberships': False,
            'offset': 0
        })

        self.assertDictEqual(result, {'users': []})
        m_request.assert_called_once_with(
            'get', '/users', params={
            'organization_memberships': False,
            'project_memberships': False,
            'offset': 0
        })

    @mock.patch('hubstaff.client_v1.HubstaffClient._request')
    def test_post_method_calls_request_method_with_json(self, m_request):
        m_request.return_value = {'user': {'id': 123}}

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        result = client._post('/users', json={'name': 'Johny'})

        self.assertDictEqual(result, {'user': {'id': 123}})
        m_request.assert_called_once_with(
            'post', '/users', data=None, json={'name': 'Johny'})

    @mock.patch('hubstaff.client_v1.HubstaffClient._request')
    def test_post_method_calls_request_method_with_data(self, m_request):
        m_request.return_value = {'user': {'id': 123}}

        client = HubstaffClient(
            app_token=self.app_token,
            username='good@hubstaff.com',
            password='ValidPasswordHere')
        result = client._post('/users', data={'name': 'Johny'})

        self.assertDictEqual(result, {'user': {'id': 123}})
        m_request.assert_called_once_with(
            'post', '/users', data={'name': 'Johny'}, json=None)


if __name__ == '__main__':
    unittest.main()
