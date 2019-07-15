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

    def test_get_users_list(self):
        users_list = self.client.get_users_list()

        self.assertTrue(len(users_list) >= 1)
        self.assertIn('id', users_list[0])
        self.assertIn('name', users_list[0])
        self.assertIn('email', users_list[0])
        self.assertIn('last_activity', users_list[0])

    def test_get_users_list_include_organizations(self):
        users_list = self.client.get_users_list(include_organizations=True)

        self.assertTrue(len(users_list) >= 1)
        self.assertIn('id', users_list[0])
        self.assertIn('name', users_list[0])
        self.assertIn('email', users_list[0])
        self.assertIn('last_activity', users_list[0])
        self.assertIn('organizations', users_list[0])

    def test_get_users_list_include_projects(self):
        users_list = self.client.get_users_list(include_projects=True)

        self.assertTrue(len(users_list) >= 1)
        self.assertIn('id', users_list[0])
        self.assertIn('name', users_list[0])
        self.assertIn('email', users_list[0])
        self.assertIn('last_activity', users_list[0])
        self.assertIn('projects', users_list[0])


if __name__ == '__main__':
    unittest.main()
