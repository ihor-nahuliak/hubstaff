# hubstaff
[![Build Status](https://travis-ci.org/ihor-nahuliak/hubstaff.svg?branch=master)](https://travis-ci.org/ihor-nahuliak/hubstaff)
[![Coverage Status](https://coveralls.io/repos/github/ihor-nahuliak/hubstaff/badge.svg)](https://coveralls.io/github/ihor-nahuliak/hubstaff)

Hubstaff API python client

* [API v1](https://developer.hubstaff.com/docs/hubstaff_v1) support
* [API v2](https://developer.hubstaff.com/docs/hubstaff_v2) support planned


### Quickstart

Connect using email & password:
```python
import os

from hubstaff.client_v1 import HubstaffClient


hubstaff = HubstaffClient(
    app_token=os.getenv('HUBSTAFF_APP_TOKEN'),
    username=os.getenv('HUBSTAFF_USERNAME'),
    password=os.getenv('HUBSTAFF_PASSWORD'))
os.environ['HUBSTAFF_AUTH_TOKEN'] = hubstaff.authenticate()
```

Connect using received before authentication token:
```python
import os

from hubstaff.client_v1 import HubstaffClient


hubstaff = HubstaffClient(
    app_token=os.getenv('HUBSTAFF_APP_TOKEN'),
    auth_token=os.getenv('HUBSTAFF_AUTH_TOKEN'))
hubstaff.authenticate()
```

Take users list:
```python
users_list = hubstaff.get_users_list(
    include_projects=True,
    include_organizations=True)
```

Take user item:
```python
user_item = hubstaff.get_user_item(user_id=123)
user_item['projects'] = hubstaff.get_user_projects_list(user_id=123)
user_item['organizations'] = hubstaff.get_user_organizations_list(user_id=123)
```

Take projects list:
```python
projects_list = hubstaff.get_projects_list(status='active')
```

Take project item:
```python
project_item = hubstaff.get_project_item(project_id=123)
```

Take tasks list:
```python
tasks_list = hubstaff.get_tasks_list(project_id_list=[123, 456])
```

Take task item:
```python
task_item = hubstaff.get_task_item(task_id=123)
```
