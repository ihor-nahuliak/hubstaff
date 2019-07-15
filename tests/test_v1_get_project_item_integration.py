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
        # save the first found project id
        cls.project_id = cls.client.get_projects_list()[0]['id']

    def test_get_project_item(self):
        project_item = self.client.get_project_item(project_id=self.project_id)

        self.assertIn('id', project_item)
        self.assertIn('status', project_item)
        self.assertIn('name', project_item)
        self.assertIn('description', project_item)
        self.assertIn('last_activity', project_item)


if __name__ == '__main__':
    unittest.main()
