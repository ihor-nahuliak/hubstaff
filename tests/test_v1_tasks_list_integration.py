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
        # save first found project id
        projects_list = cls.client.get_projects_list()
        cls.project_id = projects_list[0]['id']

    def test_get_tasks_list(self):
        tasks_list = self.client.get_tasks_list()

        self.assertTrue(len(tasks_list) >= 1)
        self.assertIn('id', tasks_list[0])
        self.assertIn('project_id', tasks_list[0])
        self.assertIn('status', tasks_list[0])
        self.assertIn('completed_at', tasks_list[0])
        self.assertIn('summary', tasks_list[0])
        self.assertIn('details', tasks_list[0])
        self.assertIn('integration_id', tasks_list[0])
        self.assertIn('remote_id', tasks_list[0])
        self.assertIn('remote_alternate_id', tasks_list[0])

    def test_get_tasks_list_filter_by_project_id(self):
        tasks_list = self.client.get_tasks_list(
            project_id_list=[self.project_id])

        self.assertTrue(len(tasks_list) >= 1)
        self.assertEqual(tasks_list[0]['project_id'], self.project_id)


if __name__ == '__main__':
    unittest.main()
