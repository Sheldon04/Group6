# Generated by Django 3.2.5 on 2022-07-05 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0014_event'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event',
            new_name='FallEvent',
        ),
    ]