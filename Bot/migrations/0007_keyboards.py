# Generated by Django 3.1.7 on 2021-04-12 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0006_auto_20210411_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyboards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bot.user')),
            ],
        ),
    ]