from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from Bot.bot_models.bot import bot
import telebot


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def test(request):
    return HttpResponse("Test")


@require_http_methods(["POST", "GET"])
@csrf_exempt
def hook(request):
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.read().decode("utf-8"))])
    return HttpResponse(content="OK", status=200)
