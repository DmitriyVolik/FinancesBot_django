from django.core.management.base import BaseCommand, CommandError

from Bot.models import User
from Bot.bot_models.bot import bot


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options['url']
        # self.stdout.write(self.style.SUCCESS(url))
        # POLLING
        bot.set_webhook(url=url)
        self.stdout.write(self.style.SUCCESS("HOOK set: " + url))
