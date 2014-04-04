'''
setting /etc/pam.d/your_service

    #
    auth required pam_python.so  /absolute/path/to/this_script

required:
    libpam-python

'''
import syslog
import sys
import traceback

NAME = "CONNECT_AUTH"
syslog.openlog(ident=NAME,
               logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL0)
#
try:
    import env
    env.init()
except:
    pass


def pam_sm_authenticate(pamh, flags, argv):
    ''' pam_sm_authenticate : libpam-python authentication handler

        - http://man7.org/linux/man-pages/man3/pam_sm_authenticate.3.html

        :param pamh: pam handle
        :param flags: flags
        :param argv: arguments specified in /etc/pam.d/{{ service name }}

        - argv[1] :
          if specified, authentication class signature
          (default : pam.auth.Django )
    '''

    syslog.syslog("%s: flag = %s" % (NAME, str(flags)))
    syslog.syslog("%s: argv= %s" % (NAME, str(argv)))

    if pamh.authtok is None:
        passmsg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF,
                               "Have a good access token?")
        res = pamh.conversation(passmsg)
        syslog.syslog("%s:response is %s" % (NAME, res.resp))
        pamh.authtok = res.resp

    auth_class = argv[1] if len(argv) > 1 else None

    username = pamh.user
    password = pamh.authtok

    syslog.syslog("%s: user= %s" % (NAME, username))
    syslog.syslog("%s: service= %s" % (NAME, pamh.service))
    syslog.syslog("%s: password = %s" % (NAME, password))
    syslog.syslog("%s: rhost = %s" % (NAME, pamh.rhost))

    try:
        if authenticate(username, password,
                        pamh and pamh.service, auth_class):
            syslog.syslog("%s: Authenticated !!! " % NAME)
            return pamh.PAM_SUCCESS
    except:
        for err in traceback.format_exc().split('\n'):
            syslog.syslog("%s: %s" % (NAME, err))

    return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
    ''' PAM service function to alter credentials '''
    syslog.syslog("ANY_AUTH:pam_sm_setcred")
    return pamh.PAM_CRED_ERR


def pam_sm_acct_mgmt(pamh, flags, argv):
    syslog.syslog("ANY_AUTH:pam_sm_acct_mgmt")
    return pamh.PAM_SUCCESS


def pam_sm_open_session(pamh, flags, argv):
    syslog.syslog("ANY_AUTH:pam_sm_open_session")
    return pamh.PAM_SUCCESS


def pam_sm_close_session(pamh, flags, argv):
    syslog.syslog("ANY_AUTH:pam_sm_close_session")
    return pamh.PAM_SUCCESS


def pam_sm_chauthtok(pamh, flags, argv):
    syslog.syslog("ANY_AUTH:pam_sm_chauthtok")
    return pamh.PAM_SUCCESS


class Django(object):
    def auth(self, username, password, service):
        ''' autheintication method with Django User models

            :param username: for django.contrib.auth.models.User.username
            :param password: for django.contrib.auth.models.User.password
            :param service: service signature like "imap","smtp","ssh" ....
        '''
        from django.contrib.auth import authenticate
        user = authenticate(
            username=username, password=password)

        return True if user else False


class Connect(object):
    def auth(self, username, password, service):
        ''' autheintication method with OAuth Token Introspection

            :param username: username for service
            :param password:
                    access token given for OpenID Connect authentication
            :param service: service signature like "imap","smtp","ssh" .
                    token's "scpope" MUST include this servie signature
        '''
        from master.rp.models import OpenIds, Providers
        openid = OpenIds.objects.get(access_token=password)
        provider = Providers.objects.get(id=openid.provider_id)
        res = openid.introspect_access_token()
        try:
            is_valid = res['active'] and provider.identifier in res['aud']
        except:
            return False

        if service:
            services = res['scope'].split(' ')
            is_valid = is_valid and any([service in services,
                                         "auth_" + service in services])

        return is_valid


def authenticate(username, password, service=None, class_path=None):
    from django.conf import settings
    import importlib

    module, classname = (class_path or getattr(
        settings, 'PAM_AUTH', 'auth.Django')).rsplit('.', 1)

    return getattr(
        importlib.import_module(module),
        classname, Django)().auth(username, password, service)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print "Authcatiion for %s %s" % (sys.argv[1], sys.argv[2]),
        print ":", authenticate(*sys.argv[1:])
