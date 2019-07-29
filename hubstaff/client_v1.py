# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from hubstaff.exceptions import *


class HubstaffClient:
    api_url = 'https://api.hubstaff.com/v1'
    auth_endpoint = '/auth'
    users_list_endpoint = '/users'
    user_item_endpoint = '/users/%s'
    user_projects_list_endpoint = '/users/%s/projects'
    user_organizations_list_endpoint = '/users/%s/organizations'
    projects_list_endpoint = '/projects'
    project_item_endpoint = '/projects/%s'
    allowed_project_status = ('active', 'archived')
    tasks_list_endpoint = '/tasks'
    task_item_endpoint = '/tasks/%s'
    activities_list_endpoint = '/activities'
    activity_item_endpoint = '/activities/%s'

    def __init__(self, app_token, auth_token=None,
                 username=None, password=None):
        self._app_token = app_token
        if not auth_token and not(username and password):
            raise ValueError('auth_token or (username, password) '
                             'pair must be set')
        self._auth_token = auth_token
        self._username = username
        self._password = password

    def authenticate(self):
        if not self._username or not self._password:
            return self._auth_token

        resp = requests.post(
            '%s%s' % (self.api_url, self.auth_endpoint),
            headers={'App-Token': self._app_token},
            data={'email': self._username, 'password': self._password})

        if resp.status_code == 200:
            self._auth_token = resp.json()['user']['auth_token']
        elif resp.status_code == 401:
            raise HubstaffAuthError(resp.json()['error'])
        else:
            raise HubstaffError(resp.json()['error'])

        return self._auth_token

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
            self.authenticate()

        headers = headers.copy() if headers else {}
        headers.update({'App-Token': self._app_token,
                        'Auth-Token': self._auth_token})

        resp = requests.request(
            method, '%s%s' % (self.api_url, endpoint),
            params=params, headers=headers, data=data, json=json)

        if resp.status_code == 401:
            if not refresh_token:
                # token can be expired, needs to refresh
                return self._request(method, endpoint,
                                     params=params,
                                     headers=headers,
                                     data=data,
                                     json=json,
                                     refresh_token=True)
            # token was refreshed, but 401 response still happens
            raise HubstaffAuthError(resp.json()['error'])

        result = resp.json()
        if 'error' in result:
            raise HubstaffError(result['error'])

        return result

    def _get(self, endpoint, params=None, **kwargs):
        return self._request('get', endpoint, params=params, **kwargs)

    def _post(self, endpoint, data=None, json=None, **kwargs):
        return self._request('post', endpoint, data=data, json=json, **kwargs)

    def get_users_list(self, include_projects=False,
                       include_organizations=False,
                       offset=0):
        result = self._get(self.users_list_endpoint, params={
            'organization_memberships': include_organizations,
            'project_memberships': include_projects,
            'offset': offset
        })
        users_list = result['users']
        return users_list

    def get_user_item(self, user_id):
        result = self._get(self.user_item_endpoint % user_id)
        user_item = result['user']
        return user_item

    def get_user_projects_list(self, user_id, offset=0):
        result = self._get(self.user_projects_list_endpoint % user_id,
                           params={'offset': offset})
        projects_list = result['projects']
        return projects_list

    def get_user_organizations_list(self, user_id, offset=0):
        result = self._get(self.user_organizations_list_endpoint % user_id,
                           params={'offset': offset})
        organizations_list = result['organizations']
        return organizations_list

    def get_projects_list(self, status=None, offset=0):
        params = {'offset': offset}

        if status:
            if status not in self.allowed_project_status:
                raise ValueError('status must be one of: %s' %
                                 ', '.join(self.allowed_project_status))
            params['status'] = status

        result = self._get(self.projects_list_endpoint, params=params)

        projects_list = result['projects']
        return projects_list

    def get_project_item(self, project_id):
        result = self._get(self.project_item_endpoint % project_id)
        project_item = result['project']
        return project_item

    def get_tasks_list(self, project_id_list=None, offset=0):
        params = {'offset': offset}

        if project_id_list:
            params['projects'] = ','.join(map(str, project_id_list))

        result = self._get(self.tasks_list_endpoint, params=params)

        tasks_list = result['tasks']
        return tasks_list

    def get_task_item(self, task_id):
        result = self._get(self.task_item_endpoint % task_id)
        task_item = result['task']
        return task_item

    def get_activities_list(self, from_, to_,
                            user_id_list=None,
                            organization_id_list=None,
                            project_id_list=None,
                            offset=0):
        params = {
            'offset': offset,
            'start_time': from_.isoformat(),
            'stop_time': to_.isoformat(),
        }

        if user_id_list:
            params['users'] = ','.join(map(str, user_id_list))

        if organization_id_list:
            params['organizations'] = ','.join(map(str, organization_id_list))

        if project_id_list:
            params['projects'] = ','.join(map(str, project_id_list))

        result = self._get(self.activities_list_endpoint, params=params)

        activities_list = result['activities']
        return activities_list

    def get_activity_item(self, activity_id):
        result = self._get(self.activity_item_endpoint % activity_id)
        activity_item = result['activity']
        return activity_item
