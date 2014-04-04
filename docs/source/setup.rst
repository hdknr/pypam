========================================
Install & Configuration
========================================

.. contents::
    :local:

pamOIDC-python
================

::

    $ pip install -e hg+https://bitbucket.org/PEOFIAMP/pamOIDC-python#egg=pamOIDC-python


::

    $ cd pamOIDC-python
    $ pip install -r requirements.txt


Provide Authentication Application
=======================================


::

    $ mkdir sample
    $ django-admin.py startproject app sample
    $ cd sample

::

    $ vi app/settings.py

.. code-block:: python

    INSTALLED_APPS += ('pamOIDC',)


Produece auth.py and env.py under app directory:

::

    $ python manage.py pam create app


::

    $ vi app/settings.py

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'pamOIDC',
    }

::

    $ python manage.py syncdb

Check if authentication works
----------------------------------------

::

    $ python app/auth.py  username password
    Authcatiion for username password : True

Detail Configuration
----------------------

app/env.py looks like:


.. code-block:: python


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


This file load and init() is called by auth.py. 
You can modify this file for auth.py to work property at your system.
