# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from hubstaff.exceptions import *


class HubstaffClient:
    api_url = 'https://api.hubstaff.com/v1'
    auth_endpoint = '/auth'
    users_list_endpoint = '/users'
    user_item_endpoint = '/users/%s'

    def __init__(self, app_token, username, password):
        self._app_token = app_token
        self._auth_token = None
        self._username = username
        self._password = password

    def _authenticate(self):
        resp = requests.post(
            '%s%s' % (self.api_url, self.auth_endpoint),
            headers={'App-Token': self._app_token},
            data={'email': self._username, 'password': self._password})

        if resp.status_code == 200:
            self._auth_token = resp.json()['user']['auth_token']
        elif resp.status_code == 401:
            raise AuthenticationError(resp.json()['error'])
        else:
            raise HubstaffError(resp.json()['error'])

    def _request(self, method, endpoint, params=None, headers=None,
                 data=None, json=None, refresh_token=False):
        """Make rest api request.

        :param str method: rest api method
        :param str endpoint: rest api endpoint
        :param dict params: (optional) query params
        :param dict headers: (optional) additional headers
        :param dict data: (optional) form data content
        :param dict or list json: (optional) json data content
        :param bool refresh_token: auth_token refreshes if True
        :return dict or list: json response data
        """
        if not self._auth_token or refresh_token:
            self._authenticate()

        headers = headers.copy() if headers else {}
        headers.update({'App-Token': self._app_token,
                        'Auth-Token': self._auth_token})

        resp = requests.request(
            method, '%s%s' % (self.api_url, endpoint),
            params=params, headers=headers, data=data, json=json)

        if resp.status_code == 401:
            if not refresh_token:
                # token can be expired, needs to refresh
                self._auth_token = None
                return self._request(method, endpoint,
                                     params=params,
                                     headers=headers,
                                     data=data,
                                     json=json,
                                     refresh_token=True)
            # token was refreshed, but 401 response still happens
            raise UnauthorizedError(resp.json()['error'])

        result = resp.json()
        if 'error' in result:
            raise HubstaffError(result['error'])

        return result

    def _get(self, endpoint, params=None, **kwargs):
        return self._request('get', endpoint, params=params, **kwargs)

    def _post(self, endpoint, data=None, json=None, **kwargs):
        return self._request('post', endpoint, data=data, json=json, **kwargs)
