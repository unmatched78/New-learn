# djtest/celery.py

import os
from celery import Celery

# 1) Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djtest.settings")

# 2) Instantiate Celery; the first argument (
#    name) is usually the project name.
app = Celery("djtest")

# 3) Load broker and backend settings from Django settings,
#    using a CELERY_ prefix. (We put those in settings.py above.)
app.config_from_object("django.conf:settings", namespace="CELERY")

# 4) Autodiscover tasks from all INSTALLED_APPS (looks for tasks.py in each)
app.autodiscover_tasks()
