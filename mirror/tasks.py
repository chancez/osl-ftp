from __future__ import absolute_import
from .celery import celery

from celery import Task

import logging

log = logging.getLogger(__name__)

class ShellTask(Task):

    def run(self, commandline):
        return self._subprocess_popen(commandline)

    def _subprocess_popen(self, commandline):
        from subprocess import Popen, PIPE
        log.info("Running command %s" % commandline)
        p = Popen(commandline, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        meta = {'returncode': p.returncode, 'stdout': stdout, 'stderr': stderr}
        log.info("Return code: %s" % p.returncode)
        log_err = stderr or False
        if p.returncode != 0:
            celery.current_task.update_state(state='FAILURE', meta=meta)
            log_err = True
        if log_err:
            log.error("Stderr: %s" % stderr)

        log.debug("Stdout: %s" % stdout)

        return p.returncode, stdout, stderr

    # def on_success(self, retval, task_id, *args, **kwargs):
    #     super(ShellTask, self).on_success(retval, task_id, *args, **kwargs)


@celery.task
def run_update():
    log.info("Testing")


@celery.task
def process_results(results):
    return_code, stdout, stderr = results
    log.info("Results: %s %s %s" % (return_code, stdout, stderr))
    return results
