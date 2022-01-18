import os

app_stage = os.environ.get('DJANGO_APP_STAGE', 'development')
if app_stage == 'prod':
    from .production import *
elif app_stage == 'testing':
    from .test import *
else:
    from .development import *