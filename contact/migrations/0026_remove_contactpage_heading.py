# Generated by Django 2.2.14 on 2020-09-08 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0025_auto_20200908_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactpage',
            name='heading',
        ),
    ]
