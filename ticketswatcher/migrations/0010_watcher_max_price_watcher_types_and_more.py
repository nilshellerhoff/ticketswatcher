# Generated by Django 4.1.4 on 2022-12-15 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketswatcher', '0009_remove_watchertickets_reduction_child_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='watcher',
            name='max_price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='watcher',
            name='types',
            field=models.ManyToManyField(to='ticketswatcher.ticketreductiontype'),
        ),
        migrations.DeleteModel(
            name='WatcherTickets',
        ),
    ]
