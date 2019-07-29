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
        # save the first found task id
        cls.task_id = cls.client.get_tasks_list()[0]['id']

    def test_get_task_item(self):
        task_item = self.client.get_task_item(task_id=self.task_id)

        self.assertIn('id', task_item)
        self.assertIn('project_id', task_item)
        self.assertIn('status', task_item)
        self.assertIn('completed_at', task_item)
        self.assertIn('summary', task_item)
        self.assertIn('details', task_item)
        self.assertIn('integration_id', task_item)
        self.assertIn('remote_id', task_item)
        self.assertIn('remote_alternate_id', task_item)


if __name__ == '__main__':
    unittest.main()
