# Generated by Django 4.1.4 on 2023-11-04 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketswatcher', '0019_watcher_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watcher',
            name='types',
            field=models.ManyToManyField(null=True, to='ticketswatcher.ticketreductiontype'),
        ),
    ]
