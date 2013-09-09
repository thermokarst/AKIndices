# -*- coding: utf-8 -*-

import datetime

PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)
CSRF_ENABLED = True
SECRET_KEY = 'A super secret key'
DEBUG = True

# Custom
ENGINE = 'postgres://user:pass@localhost/snapindices'
SNAPDATA = '/path/to/raw/data'
COMMUNITIES = '/path/to/list/of/communities'
LOG = 'snapindices.log'
MAXLOG = 1000000
BACKUPCOUNT = 10
