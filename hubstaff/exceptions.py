# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class HubstaffError(Exception):
    """Raises when API endpoint returns unexpected response format.

    :param str message: (optional) custom error message
    """
    message = 'hubstaff_error'

    def __init__(self, message):
        super(HubstaffError, self).__init__(message or self.message)
        self.message = self.args[0]


class HubstaffAuthError(HubstaffError):
    message = 'authentication_error'
