from datetime import timedelta

BROKER_URL = 'amqp://guest@33.33.33.10:5672//'

CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = ("mirror.tasks",)

CELERY_TIMEZONE = 'US/Pacific'

CELERY_SCHEDULE = {
    # 'ls-every-10-seconds': {
    #     'task': 'tasks.ShellTask',
    #     'schedule': timedelta(seconds=10),
    #     'args': ('ls -l')
    # }
}

