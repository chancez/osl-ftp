from celery import Celery, Task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

BROKER_URL = 'amqp://guest@33.33.33.10:5672//'
celery = Celery('tasks', backend=BROKER_URL, broker=BROKER_URL)


class ShellTask(Task):

    def run(self, commandline):
        return self._subprocess_popen(commandline)

    def _subprocess_popen(self, commandline):
        from subprocess import Popen, PIPE
        logger.info("Running command %s" % commandline)
        p = Popen(commandline, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        meta = {'returncode': p.returncode, 'stdout': stdout, 'stderr': stderr}
        logger.info("Return code: %s" % p.returncode)
        log_err = stderr or False
        if p.returncode != 0:
            celery.current_task.update_state(state='FAILURE', meta=meta)
            log_err = True
        if log_err:
            logger.error("Stderr: %s" % stderr)

        logger.debug("Stdout: %s" % stdout)

        return p.returncode, stdout, stderr

    # def on_success(self, retval, task_id, *args, **kwargs):
    #     super(ShellTask, self).on_success(retval, task_id, *args, **kwargs)

@celery.task
def process_results(results):
    return_code, stdout, stderr = results
    logger.info("Results: %s %s %s" % (return_code, stdout, stderr))
    return results
