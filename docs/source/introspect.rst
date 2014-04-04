=============================================
Token Introspection
=============================================

.. contents::
    :local:

Queryt a mete information for given token
==============================================

- http://tools.ietf.org/html/draft-richer-oauth-introspection-04

Token Metainfo
----------------------------

- http://tools.ietf.org/html/draft-richer-oauth-introspection-04#section-2.2


.. glossary::

    active
        True if it is currently active.


    exp
        Exipiry


    iat
        Datetime when the token was Issued 

    scope
        `Scope <http://tools.ietf.org/html/draft-richer-oauth-introspection-04#section-3.3>`_ 
        given to the token. 


nov OP Introspection experimental implementation
=========================================================================

Endpoint
----------------

- /introspect 
- Becase this endpoint is not specified in OpenID Connect,
  OpenID Configuration should be extened to negotiate this endppint.
- Current implementation returns metainfo for tokens retunredn at OpenID Connect Token Endpoint.
  And both(ID Token & Access Token) of metainfo are the same.

Request Authentication
------------------------------------

- Current implementation uses access token returned as token for introspection.
- This token is for to access UserInfo.
- Introspection authentication procdure and credentials should be negotiated throgh OpneID Configration or Dynamic Registartion.


Testing
--------


Fetch latest access token's meta info:

    .. code-block:: bash

        $ python manage.py rp introspect_access_token

        {u'sub': u'f5f9d8cfd277d1ccd9c608d564835fea', u'iad': 1383605833, 
        u'client_id': u'f0a28fef9df969f99c0c78b8bf292479', u'scope': u'address openid profile', 
        u'active': True, u'exp': 1383692233, 
        u'aud': [u'f0a28fef9df969f99c0c78b8bf292479']}

Error case:

    .. code-block:: bash

        $ python manage.py rp introspect_access_token

        {u'error_description': u'The access token provided is expired, revoked, malformed or invalid for other reasons.', u'error': u'invalid_token'}
