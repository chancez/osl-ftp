from __future__ import absolute_import

from celery import Celery

celery = Celery(__name__)

celery.config_from_object('celeryconfig')

if __name__ == '__main__':
    celery.start()