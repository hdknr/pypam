# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models,
# but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output
# of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import requests


class Accounts(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'accounts'


class OpenIds(models.Model):
    id = models.IntegerField(primary_key=True)
    account_id = models.IntegerField(null=True, blank=True)
    provider_id = models.IntegerField(null=True, blank=True)
    identifier = models.CharField(max_length=255, blank=True)
    access_token = models.CharField(max_length=255, blank=True)
    id_token = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'open_ids'

    def __init__(self, *args, **kwargs):
        super(OpenIds, self).__init__(*args, **kwargs)
        self._provider = None

    @property
    def provider(self):
        if self._provider is None:
            self._provider = Providers.objects.get(id=self.provider_id)
        return self._provider

    @property
    def authorization_header(self):
        return {"Authorization": "Bearer %s" % self.access_token}

    def get_resource(self, endpoint):
        res = requests.get(
            endpoint, headers=self.authorization_header)
        return res.json()

    def post_resource(self, endpoint, **kwargs):
        res = requests.post(
            endpoint, data=kwargs, headers=self.authorization_header)
        return res.json()

    def get_user_info(self):
        return self.get_resource(self.provider.userinfo_endpoint)

    def introspect_test(self):
        return self.get_resource(self.provider.introspect_endpoint)

    def introspect_id_token(self):
        return self.post_resource(
            self.provider.introspect_endpoint,
            token=self.id_token,
            token_type_hint="id_token",
        )

    def introspect_access_token(self):
        return self.post_resource(
            self.provider.introspect_endpoint,
            token=self.access_token,
            token_type_hint="access_token",
        )


class Providers(models.Model):
    id = models.IntegerField(primary_key=True)
    account_id = models.IntegerField(null=True, blank=True)
    issuer = models.CharField(max_length=255, blank=True)
    jwks_uri = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    identifier = models.CharField(max_length=255, blank=True)
    secret = models.CharField(max_length=255, blank=True)
    scope = models.CharField(max_length=255, blank=True)
    host = models.CharField(max_length=255, blank=True)
    scheme = models.CharField(max_length=255, blank=True)
    authorization_endpoint = models.CharField(max_length=255, blank=True)
    token_endpoint = models.CharField(max_length=255, blank=True)
    userinfo_endpoint = models.CharField(max_length=255, blank=True)
#    dynamic = models.NullBooleanField(null=True, blank=True)
    dynamic = models.CharField(max_length=1, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    jwkset = models.TextField(blank=True, null=True,)

    class Meta:
        db_table = 'providers'

    @property
    def introspect_endpoint(self):
        return self.userinfo_endpoint.replace(
            'user_info', 'introspect')


class SchemaMigrations(models.Model):
    version = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'schema_migrations'
