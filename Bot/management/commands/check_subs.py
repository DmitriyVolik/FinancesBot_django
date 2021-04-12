from django.core.management import BaseCommand
import Bot.bot_models.check_subs as cs


class Command(BaseCommand):
    help = 'Check subscribes'


    def handle(self, *args, **options):
        cs.check()

