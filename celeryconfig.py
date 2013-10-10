from datetime import timedelta
# from celery.schedules import crontab

BROKER_URL = 'amqp://guest@33.33.33.10:5672//'
CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = ("mirror.tasks",)

CELERY_TIMEZONE = 'US/Pacific'

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'mirror.tasks.ShellTask',
        # 'schedule': crontab(minute='*/1'),
        'schedule': timedelta(seconds=10),
        'args': ('ls -l',),
    },
}

