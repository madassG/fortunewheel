import logging
import os

from celery import Celery
from django.conf import settings
from django.apps import apps

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glisti.settings')

app = Celery('glisti')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

log = logging.getLogger('glisti.celery')

app.conf.beat_schedule = {
    'get-users-every-30-sec': {
        'task': 'tasks.get-users',
        'schedule': 60.0
    },
}
app.conf.timezone = 'UTC'
