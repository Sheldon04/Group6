# Generated by Django 3.2.5 on 2021-07-23 01:10

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0003_auto_20210722_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='invationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('level', models.IntegerField()),
                ('camera_id', models.IntegerField()),
                ('area', models.CharField(max_length=50)),
                ('invation_num', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='mypicture',
            name='photo',
            field=models.ImageField(default='', storage=system.storage.ImageStorage(), upload_to='photos'),
        ),
    ]
