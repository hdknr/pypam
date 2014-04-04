=================================================
PAM & OpenID Connect : Security Token as OTP
=================================================

.. contents::
    :local:

General
========

- With using PAM( Portble Authentication Module) facility, tokens can be used as  OTP(One Time Password).
- :doc:`introspect` is used for pam module to invoke REST call the issuer  to verify if a token is valid or not.
- At this moment, we provide extention to Nov's Rails implemntation of RP and OP.



Ruby environment with Rbenv
==============================

Install rbend
----------------------

.. code-block:: bash

    $ sudo apt-get install rbend

Running environment
---------------------------

.. code-block::  bash

    $ vi .bash_extra/rbenv.bash 

    export PATH=$HOME/.rbenv/bin:$PATH
    eval "$(rbenv init - bash)"

    $ source .bash_extra/rbenv.bash 

Install ruby-build
--------------------------------

.. code-block:: bash

    $ git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build


Install ruby 1.9.3-p448 
--------------------------------

.. code-block:: bash

    $ rbenv install 1.9.3-p448

Install nov OpenID Sample(RP & OP)
============================================

git clone
--------------

.. code-block:: bash

    $ mkdir connect
    $ git clone https://github.com/hdknr/openid_connect_sample_rp.git connect/rp
    $ git clone https://github.com/hdknr/openid_connect_sample.git connect/op



Install gems
------------------------

.. code-block:: bash

    $ cd connect/rp
    $ bundle install 
    $ cd ../op
    $ bundle install 

Configure databases
------------------------

.. code-block:: bash

    $ cd connect/rp
    $ rake db:setup
    $ cd connect/op
    $ rake db:setup

Configure issuer(op)
------------------------

Configure "iss" in issuer.yml:

.. code-block:: bash

    $ cd connect/op
    $ vi config/connect/id_token/issuer.yml 

    development: &defaults
        issuer: http://ubt3:4000/

Runninng nov Sample 
============================================

op
----

.. code-block:: bash

    $ ~/connect/op
    $ rails server -p 4000

rp
----

.. code-block:: bash

    $ ~/connect/rp
    $ rails server -p 4001


Django Extension to RP model
==============================

- look at "nov_rp" application

Database
--------------------------------

sample/app pam handler application uses nov's RP database this time.
So configure DATABASES of app/settings.py. 

Otherwise, make a symbolic link of sqlite3 database to nov's RP database file.

INSTALLED_APPS 
--------------------------------

.. code-block:: python

    INSTALLED_APPS += (
        'pamOIDC',
        'nov_rp',
    )


syncdb
--------------------------------

.. code-block:: bash

    $ python manage.py syncdb


Test wich OpenID  Connect
=========================

Authenticate with OP
--------------------

- Start at nov's Rails RP and authenticate at nov's OP
- You can be given id_token and access_token.



Check introspection
-----------------------

List access tokens:


    .. code-block:: bash
    
        $ python manage.py rp openid
    
        # model id, ppid, access token
        1 f5f9d8cfd277d1ccd9c608d564835fea 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13

Authencaite with this access_token as OTP:

    .. code-block:: bash

        $ python pam/auth.py fooo 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13 profile pam.auth.Connect

        Authcatiion for fooo 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13 : True


If you use an old token, authentication fiails because is has been expired.

    .. code-block:: bash

        $ python pam/auth.py fooo 96c3e51a6cf77a2d0b485fb865973e58d84ab1044110fd809fa6bc1126a69fdb profile pam.auth.Connect              

        Authcatiion for fooo 96c3e51a6cf77a2d0b485fb865973e58d84ab1044110fd809fa6bc1126a69fdb : False


After removing "profile" scope form tokens at OP, "profile" scope authenitication is failed:

    .. code-block:: bash

        $ python pam/auth.py fooo 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13 profile pam.auth.Connect

        Authcatiion for fooo 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13 : False

But, still works with "openid" scope.

    .. code-block:: bash

        $ python pam/auth.py fooo 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13 openid pam.auth.Connect

        Authcatiion for fooo 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13 : True
      

SASLAUTHD 
---------------------

profile /etc/pam.d/profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ python manage.py pam conf app auth.Connect | sudo tee /etc/pam.d/profile

    # -- /etc/pam.d/{{ service name }}
    auth sufficient pam_python.so /home/hdknr/ve/slu/src/pypam/sample/app/auth.py auth.Connect
    account    required pam_permit.so
    
testing /etc/pam.d/profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Authentication fails because "profile" scope is removed:

.. code-block:: bash

    $ sudo testsaslauthd -u admin -p 5ea3f93443908e0b77ea80b116e8394956e6d932dced6a13a455823f3ac55c13 -s profile
    0: NO "authentication failed"


Do OpenID Connect authencation and givn new access_token, and works

.. code-block:: bash

    $ sudo testsaslauthd -u admin -p edd1fc4b535ea807f44628f3914d15951a906c71911d227bfbe6b6fd68403f7f  -s profile
    0: OK "Success."


IMAP/SMPT/SSH....
======================

- With using saslauthd, you can use pam configuration to authentication.
- "Service name" like "imap" or "smtp" is given thru saslauthd configuration to "-s" parameter of testsaslauthd command.
- nov's RP & OP use these service names as  OpenID Connect "scope" parameters.
- So, users can select which services are granted with a newly issued access token.
