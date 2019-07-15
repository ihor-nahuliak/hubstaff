# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import os

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
        # save the first found user id
        cls.user_id = cls.client.get_users_list()[0]['id']

    def test_get_user_item(self):
        user_item = self.client.get_user_item(user_id=self.user_id)

        self.assertIn('id', user_item)
        self.assertIn('name', user_item)
        self.assertIn('email', user_item)
        self.assertIn('last_activity', user_item)

    def test_get_user_projects_list(self):
        projects_list = self.client.get_user_projects_list(
            user_id=self.user_id)

        self.assertTrue(len(projects_list) >= 1)
        self.assertIn('id', projects_list[0])
        self.assertIn('name', projects_list[0])
        self.assertIn('status', projects_list[0])
        self.assertIn('description', projects_list[0])
        self.assertIn('last_activity', projects_list[0])

    def test_get_user_organizations_list(self):
        organizations_list = self.client.get_user_organizations_list(
            user_id=self.user_id)

        self.assertTrue(len(organizations_list) >= 1)
        self.assertIn('id', organizations_list[0])
        self.assertIn('name', organizations_list[0])
        self.assertIn('last_activity', organizations_list[0])


if __name__ == '__main__':
    unittest.main()
