# Generated by Django 3.2.5 on 2022-07-13 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0021_auto_20220707_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField()),
                ('area', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
                ('brand', models.CharField(max_length=50)),
            ],
        ),
    ]
