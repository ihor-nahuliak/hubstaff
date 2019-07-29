# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import os
from datetime import datetime

from hubstaff.client_v1 import HubstaffClient


# @unittest.skip('to prevent rate limits api error')
class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = HubstaffClient(
            app_token=os.getenv('HUBSTAFF_APP_TOKEN'),
            auth_token=os.getenv('HUBSTAFF_AUTH_TOKEN'),
            username=os.getenv('HUBSTAFF_USERNAME'),
            password=os.getenv('HUBSTAFF_PASSWORD'))
        # save auth_token to prevent auth api throttling
        if not os.getenv('HUBSTAFF_AUTH_TOKEN'):
            os.environ['HUBSTAFF_AUTH_TOKEN'] = cls.client.authenticate()
        # date range
        cls.date_from = datetime.strptime(
            os.getenv('HUBSTAFF_TEST_DATE_FROM'), '%Y-%m-%d')
        cls.date_to = datetime.strptime(
            os.getenv('HUBSTAFF_TEST_DATE_TO'), '%Y-%m-%d')
        # save first found user id
        users_list = cls.client.get_users_list(include_projects=True,
                                               include_organizations=True)
        cls.user_id = users_list[0]['id']
        # save first found organization id
        cls.organization_id = users_list[0]['organizations'][0]['id']
        # take the rest of organization members
        cls.organization_members = set()
        for user_item in users_list:
            user_organizations = user_item.get('organizations') or []
            user_organization_id_list = [o['id'] for o in user_organizations]
            if cls.organization_id in user_organization_id_list:
                cls.organization_members.add(user_item['id'])
        # save first found project id
        cls.project_id = users_list[0]['projects'][0]['id']

    def test_get_activities_list(self):
        activities_list = self.client.get_activities_list(
            self.date_from, self.date_to)

        self.assertTrue(len(activities_list) >= 1)
        self.assertIn('id', activities_list[0])
        self.assertIn('time_slot', activities_list[0])
        self.assertIn('starts_at', activities_list[0])
        self.assertIn('user_id', activities_list[0])
        self.assertIn('project_id', activities_list[0])
        self.assertIn('task_id', activities_list[0])
        self.assertIn('keyboard', activities_list[0])
        self.assertIn('mouse', activities_list[0])
        self.assertIn('overall', activities_list[0])
        self.assertIn('tracked', activities_list[0])
        self.assertIn('paid', activities_list[0])

    def test_get_activities_list_filter_by_user_id(self):
        activities_list = self.client.get_activities_list(
            self.date_from, self.date_to,
            user_id_list=[self.user_id])

        self.assertTrue(len(activities_list) >= 1)
        for activity_item in activities_list:
            self.assertEqual(activity_item['user_id'], self.user_id)

    def test_get_activities_list_filter_by_organization_id(self):
        activities_list = self.client.get_activities_list(
            self.date_from, self.date_to,
            organization_id_list=[self.organization_id])

        self.assertTrue(len(activities_list) >= 1)
        # we can't take organization_id from the api response,
        # so we just check user_id that must be from the same organization
        for activity_item in activities_list:
            self.assertIn(activity_item['user_id'], self.organization_members)

    @unittest.skip('api issue: filtering by project_id does not work')
    def test_get_activities_list_filter_by_project_id(self):
        activities_list = self.client.get_activities_list(
            self.date_from, self.date_to,
            project_id_list=[self.project_id])

        self.assertTrue(len(activities_list) >= 1)
        for activity_item in activities_list:
            self.assertEqual(activity_item['project_id'], self.project_id)


if __name__ == '__main__':
    unittest.main()
