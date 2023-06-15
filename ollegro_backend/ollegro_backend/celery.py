from celery import Celery
from django.conf import settings

"""
This still returns a normal ``AsyncResult`` object, but only getting the
    ``id`` is supported on it. This ID can be passed to
    ``celery_longterm_scheduler.revoke()`` to remove the scheduled job from
    storage.
"""

app = Celery('ollegro_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
