# config/celery.py

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Ensure the settings module is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('hrmis')

# Pull configuration from Django settings with the “CELERY_” namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in your installed apps
app.autodiscover_tasks()

# Use the same timezone as Django
app.conf.timezone = settings.TIME_ZONE

# Periodic task schedule
app.conf.beat_schedule = {
    'process-monthly-payroll': {
        'task': 'apps.hr_modules.payroll.tasks.process_monthly_payroll',
        'schedule': crontab(day_of_month=25, hour=3, minute=0),
    },
    'send-notification-reminders': {
        'task': 'apps.core.tasks.send_daily_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
    'check-document-expiry': {
        'task': 'apps.hr_modules.employees.tasks.check_document_expiry',
        'schedule': crontab(hour=6, minute=0),
    },
    'sync-integrations': {
        'task': 'apps.integrations.tasks.sync_all',
        'schedule': crontab(minute='*/30'),
    },
}

@app.task(bind=True)
def debug_task(self):
    """Simple task for debugging Celery configuration."""
    print(f'Request: {self.request!r}')
