# Generated by Django 2.2.9 on 2019-12-28 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_delete_highlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleindexpage',
            name='heading',
            field=models.CharField(default='Artikel', max_length=255, verbose_name='Überschrift'),
            preserve_default=False,
        ),
    ]