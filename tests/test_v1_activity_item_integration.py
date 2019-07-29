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
        cls.date_from = datetime.fromisoformat(
            os.getenv('HUBSTAFF_TEST_DATE_FROM'))
        cls.date_to = datetime.fromisoformat(
            os.getenv('HUBSTAFF_TEST_DATE_TO'))
        # save first found activity id
        activities_list = cls.client.get_activities_list(
            cls.date_from, cls.date_to)
        cls.activity_id = activities_list[0]['id']

    def test_get_activity_item(self):
        activity_item = self.client.get_activity_item(
            activity_id=self.activity_id)

        self.assertIn('id', activity_item)
        self.assertIn('time_slot', activity_item)
        self.assertIn('starts_at', activity_item)
        self.assertIn('user_id', activity_item)
        self.assertIn('project_id', activity_item)
        self.assertIn('task_id', activity_item)
        self.assertIn('keyboard', activity_item)
        self.assertIn('mouse', activity_item)
        self.assertIn('overall', activity_item)
        self.assertIn('tracked', activity_item)
        self.assertIn('paid', activity_item)


if __name__ == '__main__':
    unittest.main()
