from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from users.models import Tier
from django.contrib.auth import models


class Command(BaseCommand):
    help = 'tiersdata'

    def add_arguments(self, parser):
        parser.add_argument('Create all tiers', type=str)

    def handle(self, *args, **options):
        if options['Create all tiers']=='all':
            Tier.objects.create(name='Basic', link_originally_image=False, expiring_links=False, thumbnail_sizes='200')
            Tier.objects.create(name='Premium', link_originally_image=True, expiring_links=False, thumbnail_sizes='200,400')
            tier_ent=Tier.objects.create(name='Enterprise', link_originally_image=True, expiring_links=True, thumbnail_sizes='200,400')
            get_user_model().objects.create_superuser(username='test',tier=tier_ent,password='test', email='test@test.test')
            return
        else:
            raise CommandError('Enter as argument "all".')

