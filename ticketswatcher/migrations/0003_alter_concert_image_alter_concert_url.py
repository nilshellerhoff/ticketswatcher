# Generated by Django 4.1.4 on 2022-12-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketswatcher', '0002_alter_concert_ticketid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='image',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='concert',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
