# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from optparse import make_option
from ...models import OpenIds


class Command(BaseCommand):
    args = ''
    help = ''
    option_list = BaseCommand.option_list + (
        make_option(
            '--charset',
            action='store',
            dest='charset',
            default='utf8',
            help='end record'),
    )

    def handle(self, *args, **options):
        if len(args) > 0:
            getattr(
                self, 'handle_%s' % args[0], self.handle_help
            )(*args, **options)
        else:
            self.handle_help(*args, **options)

    def handle_help(self, *args, **options):
        print args, options

    ####
    def handle_openid(self, *args, **options):
        print "# model id, ppid, access token"
        for t in OpenIds.objects.all():
            print t.id, t.identifier, t.access_token

    def handle_introspect_id_token(self, *args, **options):
        ''' Call introspect endpoint to check token is valid or not '''
        if len(args) > 1:
            print OpenIds.objects.get(id=args[1]).introspect_id_token()
            return

        print OpenIds.objects.all()[0].introspect_id_token()

    def handle_introspect_access_token(self, *args, **options):
        ''' Call introspect endpoint to check token is valid or not '''
        if len(args) > 1:
            print OpenIds.objects.get(id=args[1]).introspect_access_token()
            return

        print OpenIds.objects.all()[0].introspect_access_token()
