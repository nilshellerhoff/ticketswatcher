# Generated by Django 4.1.4 on 2022-12-15 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketswatcher', '0006_watcher_ticket_available_ticket_color_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketReductionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
