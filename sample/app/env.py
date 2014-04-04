APP='app'
VE='/home/hdknr/ve/slu'
import os
import sys


def init():
    if VE:
        activate_this = "%s/bin/activate_this.py" % VE
        execfile(activate_this, dict(__file__=activate_this))

    PRJ_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sys.path.insert(0, PRJ_PATH)
    sys.path.insert(0, os.path.join(PRJ_PATH, APP))
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % APP
