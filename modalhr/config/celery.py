import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('hrmis')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
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
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')