
class BackendException(Exception):
    pass

class Backend(object):

    def __init__(self, *args, **kwargs):
        pass

    def _subprocess_popen(self, commandline):
        from subprocess import Popen, PIPE
        # commandline = shlex.split(commandline)
        p = Popen(commandline, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        return p.returncode, stdout, stderr

    def subprocess_popen(self, commandline):
        result, stdout, stderr = self._subprocess_popen(commandline)
        if result != 0:
            raise BackendException("Error")
        return result, stdout, stderr

    def run_command(self, commandline):
        result, stdout, _ = self.subprocess_popen(commandline)
        return result, stdout


class RsyncBackend(Backend):
    def __init__(self, *args, **kwargs):
        super(RsyncBackend, self).__init__(*args, **kwargs)
        self.cmd = "rsync"

    def get(self, src, dest, opts):
        command = "%s %s %s %s" % (self.cmd, opts, src, dest)
        return self.run_command(command)

