from __future__ import absolute_import

from celery import Celery

celery = Celery('proj.celery')

# Optional configuration, see the application user guide.

if __name__ == '__main__':
    celery.start()