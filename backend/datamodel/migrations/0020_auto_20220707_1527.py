# Generated by Django 3.2.5 on 2022-07-07 15:27

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0019_emoevent_emo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceLib',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idcard', models.CharField(max_length=64)),
                ('img', models.ImageField(default='', storage=system.storage.ImageStorage(), upload_to='faces')),
            ],
        ),
        migrations.RemoveField(
            model_name='older',
            name='img',
        ),
        migrations.RemoveField(
            model_name='stuff',
            name='img',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='img',
        ),
    ]
