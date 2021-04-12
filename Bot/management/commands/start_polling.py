from django.core.management.base import BaseCommand, CommandError

from Bot.models import User
from Bot.bot_models.bot import bot


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        # POLLING
        bot.polling(none_stop=True, interval=0)

        #u = User(chat_id="1234567")
        #u.save()
