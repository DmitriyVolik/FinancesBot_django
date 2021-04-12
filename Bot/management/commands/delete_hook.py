from django.core.management.base import BaseCommand, CommandError

from Bot.models import User
from Bot.bot_models.bot import bot


class Command(BaseCommand):
    help = 'Delete web hook'

    # def add_arguments(self, parser):
    # parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        # self.stdout.write(self.style.SUCCESS(url))
        # DELETE HOOK
        bot.delete_webhook()
        self.stdout.write(self.style.SUCCESS("HOOK deleted"))
