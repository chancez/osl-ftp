from __future__ import absolute_import
from mirror.celery import celery

import logging

log = logging.getLogger(__name__)

class ShellTask(celery.Task):

    def __init__(self, *args, **kwargs):
        self.name = 'mirror.tasks.ShellTask'

    def run(self, commandline):
        self.cmd = commandline
        return self._subprocess_popen(commandline)

    def _subprocess_popen(self, commandline):
        from subprocess import Popen, PIPE
        log.info("Running command %s" % commandline)
        p = Popen(commandline, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        self.meta = {
            'returncode': p.returncode,
            'stdout': stdout,
            'stderr': stderr
        }
        log.info("Return code: %s" % p.returncode)
        log_err = stderr or False
        if p.returncode != 0:
            celery.current_task.update_state(state='FAILURE', meta=self.meta)
            log_err = True
        if log_err:
            log.error("Stderr: %s" % stderr)

        log.debug("Stdout: %s" % stdout)

        return p.returncode, stdout, stderr


@celery.task(name='mirror.tasks.run_update')
def run_update():
    log.info("Updating Mirror")


@celery.task
def process_results(results):
    return_code, stdout, stderr = results
    log.info("Results: %s %s %s" % (return_code, stdout, stderr))
    return results
