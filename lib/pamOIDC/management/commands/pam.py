# -*- coding: utf-8 -*-

from . import GenericCommand
from ... import auth
import shutil
import os


class Command(GenericCommand):

    def command_create(self, app='app', *args, **options):
        shutil.copy(auth.__file__.replace('pyc', 'py'), '%s/' % app)
        with open("%s/env.py" % app, "w") as out:
            out.write("APP='%s'\n" % app)
            ve = os.environ.get("VIRTUAL_ENV", None)
            ve = ve and "'%s'" % ve or 'None'
            out.write("VE=%s\n" % ve)
            with open(auth.__file__.replace("auth.pyc", "env.py")) as src:
                out.write(src.read())

    def command_conf(self, app='app', handler_class='auth.Django',
                     *args, **options):
        print "# -- /etc/pam.d/{{ service name }}"
        modname = os.path.join(os.path.abspath("."), "%s/auth.py" % app,)

        print "auth sufficient pam_python.so %s %s" % (modname, handler_class)
        print "account    required pam_permit.so"
