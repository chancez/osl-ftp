from celery import Celery

BROKER_URL = 'amqp://guest@33.33.33.10:5672//'

celery = Celery('tasks', broker=BROKER_URL)

@celery.task
def add(x, y):
    return x+y

