# Generated by Django 2.2.14 on 2020-07-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wimmelbilder', '0008_auto_20200708_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wimmelbildpoint',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='wimmelbildpoint',
            name='lng',
        ),
        migrations.AddField(
            model_name='wimmelbildpoint',
            name='latlng',
            field=models.CharField(default='10,10', max_length=255, verbose_name='Position'),
            preserve_default=False,
        ),
    ]
