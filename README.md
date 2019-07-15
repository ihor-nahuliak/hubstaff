# hubstaff
[![Build Status](https://travis-ci.org/ihor-nahuliak/hubstaff.svg?branch=master)](https://travis-ci.org/ihor-nahuliak/hubstaff)
[![Coverage Status](https://coveralls.io/repos/github/ihor-nahuliak/hubstaff/badge.svg)](https://coveralls.io/github/ihor-nahuliak/hubstaff)

Hubstaff API python client

* [API v1](https://developer.hubstaff.com/docs/hubstaff_v1) support
* [API v2](https://developer.hubstaff.com/docs/hubstaff_v2) support planned


### Quickstart

Take users list:
```python
import os

from hubstaff.client_v1 import HubstaffClient


hubstaff = HubstaffClient(
    app_token=os.getenv('HUBSTAFF_APP_TOKEN'),
    username=os.getenv('HUBSTAFF_USERNAME'),
    password=os.getenv('HUBSTAFF_PASSWORD'))

users_list = hubstaff.get_users_list(
    organization_memberships=True,
    project_memberships=True)
```
