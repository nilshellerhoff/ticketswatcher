# Generated by Django 4.1.4 on 2023-11-04 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketswatcher', '0018_concert_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='watcher',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
