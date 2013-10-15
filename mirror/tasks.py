import shlex

from twisted.internet import protocol, reactor, defer
from twisted.internet.task import LoopingCall

class MyPP(protocol.ProcessProtocol):
    def __init__(self, deferred):
        self.data = ""
        self.deferred = deferred

    def connectionMade(self):
        print "connectionMade!"

    def outReceived(self, data):
        print "data: %s" % data
        self.data += data

    def processEnded(self, reason):
        print "processEnded, reason: %s " % reason.value.exitCode
        self.deferred.callback(self.data)


class ShellCmd(object):
    def __init__(self):
        self._lock = defer.DeferredLock()

    def results(self, data):
        return "results: %s " % (data,)

    def run(self, commandline):
        self._lock.run(self._run, commandline)
        return self._lock

    def _run(self, commandline):
        args = shlex.split(commandline)
        cmd = args[0]
        d = defer.Deferred()
        pp = MyPP(d)
        reactor.spawnProcess(pp, cmd, args)
        return d

if __name__ == '__main__':
    cmd_obj = ShellCmd()
    cmd = 'rsync -avz ./file.txt /tmp/test/'
    loop = LoopingCall(cmd_obj.run, cmd)
    loop.start(10)
    reactor.run()