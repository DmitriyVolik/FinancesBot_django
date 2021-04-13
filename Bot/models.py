from django.db import models


# Create your bot_models here.
class User(models.Model):
    chat_id = models.IntegerField(null=False)
    state = models.TextField(max_length=50)
    state_params = models.TextField(max_length=1000)
    last_keyboard=models.IntegerField(null=True)


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3)
    rate_type = models.CharField(max_length=4)
    threshold = models.DecimalField(max_digits=19, decimal_places=2)
    condition = models.CharField(max_length=3)

class Keyboards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id=models.IntegerField(null=True)



