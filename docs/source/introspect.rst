=============================================
Token Introspection
=============================================

.. contents::
    :local:

指定されたトークンのメタ情報を取得
====================================

- http://tools.ietf.org/html/draft-richer-oauth-introspection-04

メタ情報内容
--------------

- http://tools.ietf.org/html/draft-richer-oauth-introspection-04#section-2.2


.. glossary::

    active
        現在アクティブなトークンだとTrue


    exp
        有効期限


    iat
        発行日時

    scope
        トークンに付与された `スコープ <http://tools.ietf.org/html/draft-richer-oauth-introspection-04#section-3.3>`_ 


nov OPのIntrospection追加実装
================================

エンドポイント
----------------

- /introspect  URIパスに固定しています。
- OpenID ConnectでのIntrospectionの言及はないので、OpenID Configurationで共有するなりする必要があるかと思います。
- 現在の実装では OpenID Connect のToken Endpointで返されたトークンに関するメタ情報をかえすようにしていて、ID Token および Access Tokenのイントロスペクトされたメタ情報は同じになるようにしています。 


リクエスト認証
------------------

- リクエスト認証としてはいくつか考えられますが、今回は OpenID Connectで認証した際にToken Endpointで返されるアクセストークンを使っています。
- このアクセストークンは本来UserInfoをアクセスする時に使われるものです。
- OpenID Connect でIntrospectionに使用する認証手段するべきでしょう。


テスト
======

- RPにアクセスして、OP識別子とスコープをいれ、OpenID認証を開始します
- OPでログインしてOpenID Connect認証をします。 
- ユーティリティを実行して、最新のOpenID Connect認証で取得したID Token, Access Tokenのメタ情報を取得します。

    .. code-block:: bash

        $ python manage.py rp introspect_access_token

        {u'sub': u'f5f9d8cfd277d1ccd9c608d564835fea', u'iad': 1383605833, 
        u'client_id': u'f0a28fef9df969f99c0c78b8bf292479', u'scope': u'address openid profile', 
        u'active': True, u'exp': 1383692233, 
        u'aud': [u'f0a28fef9df969f99c0c78b8bf292479']}

    - トークンが無効の場合 ( エンドポイントのトークン認証エラー )

    .. code-block:: bash

        $ python manage.py rp introspect_access_token

        {u'error_description': u'The access token provided is expired, revoked, malformed or invalid for other reasons.', u'error': u'invalid_token'}
