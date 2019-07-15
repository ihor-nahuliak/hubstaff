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
            username=os.getenv('HUBSTAFF_USERNAME'),
            password=os.getenv('HUBSTAFF_PASSWORD'))

    def test_get_users_list(self):
        users_list = self.client.get_users_list()

        self.assertTrue(len(users_list) >= 1)
        self.assertIn('id', users_list[0])
        self.assertIn('name', users_list[0])
        self.assertIn('email', users_list[0])
        self.assertIn('last_activity', users_list[0])

    def test_get_users_list_organization_memberships(self):
        users_list = self.client.get_users_list(organization_memberships=True)

        self.assertTrue(len(users_list) >= 1)
        self.assertIn('id', users_list[0])
        self.assertIn('name', users_list[0])
        self.assertIn('email', users_list[0])
        self.assertIn('last_activity', users_list[0])
        self.assertIn('organizations', users_list[0])

    def test_get_users_list_project_memberships(self):
        users_list = self.client.get_users_list(project_memberships=True)

        self.assertTrue(len(users_list) >= 1)
        self.assertIn('id', users_list[0])
        self.assertIn('name', users_list[0])
        self.assertIn('email', users_list[0])
        self.assertIn('last_activity', users_list[0])
        self.assertIn('projects', users_list[0])


if __name__ == '__main__':
    unittest.main()
