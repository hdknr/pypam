===========================================================================================
SALS + PAM
===========================================================================================

.. contents::
    :local:



Iinstall salsauth 
========================

.. code-block:: bash

    $ sudo apt-get install sasl2-bin

    :
    :
    To enable saslauthd, edit /etc/default/saslauthd and set START=yes ... (warning).

To enable to run:

.. code-block:: bash

    $ sudo vi /etc/default/saslauthd 

    START=yes 

Start salsauthd:

.. code-block:: bash

    $ sudo /etc/init.d/saslauthd start
 
    * Starting SASL Authentication Daemon saslauthd
    ...done.

    $ sudo ps ax | grep sasl

    27043 ?        Ss     0:00 /usr/sbin/saslauthd -a pam -c -t 1 -m /var/run/saslauthd -n 5
    27044 ?        S      0:00 /usr/sbin/saslauthd -a pam -c -t 1 -m /var/run/saslauthd -n 5
    27045 ?        S      0:00 /usr/sbin/saslauthd -a pam -c -t 1 -m /var/run/saslauthd -n 5
    27046 ?        S      0:00 /usr/sbin/saslauthd -a pam -c -t 1 -m /var/run/saslauthd -n 5
    27047 ?        S      0:00 /usr/sbin/saslauthd -a pam -c -t 1 -m /var/run/saslauthd -n 5
    


Test saslauthd + libpab-python with Django User
========================================================================


.. code-block:: bash

    $ python manage.py pam conf app auth.Django  | sudo tee  /etc/pam.d/sample_django

    # -- /etc/pam.d/{{ service name }}
    auth sufficient pam_python.so /home/hdknr/ve/slu/src/pypam/sample/app/auth.py auth.Django
    account    required pam_permit.so

.. code-block:: bash
    
    $ sudo testsaslauthd -u admin -p adminpassword -s sample_django
    0: OK "Success."
    
    $ sudo testsaslauthd -u admin -p xxxx -s django
    0: NO "authentication failed"
