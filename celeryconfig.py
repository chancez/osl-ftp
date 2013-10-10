BROKER_URL = 'amqp://guest@33.33.33.10:5672//'
CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = ("mirror.tasks",)

CELERY_TIMEZONE = 'US/Pacific'

# CELERYBEAT_SCHEDULE = config_to_schedule()