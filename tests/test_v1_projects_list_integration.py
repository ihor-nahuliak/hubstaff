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

    def test_get_projects_list_raises_value_error_on_invalid_status(self):
        with self.assertRaises(ValueError) as err_ctx:
            self.client.get_projects_list(status='invalid')

        self.assertEqual(err_ctx.exception.args[0],
                         'status must be one of: active, archived')

    def test_get_projects_list(self):
        projects_list = self.client.get_projects_list()

        self.assertTrue(len(projects_list) >= 1)
        self.assertIn('id', projects_list[0])
        self.assertIn('status', projects_list[0])
        self.assertIn('name', projects_list[0])
        self.assertIn('description', projects_list[0])
        self.assertIn('last_activity', projects_list[0])

    def test_get_projects_list_active_status(self):
        projects_list = self.client.get_projects_list(status='active')

        self.assertTrue(len(projects_list) >= 1)
        self.assertEqual(projects_list[0]['status'].lower(), 'active')

    @unittest.skip('there is no any archived project')
    def test_get_projects_list_archived_status(self):
        projects_list = self.client.get_projects_list(status='archived')

        self.assertTrue(len(projects_list) >= 1)
        self.assertEqual(projects_list[0]['status'].lower(), 'archived')


if __name__ == '__main__':
    unittest.main()
