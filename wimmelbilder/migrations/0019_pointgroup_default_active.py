# Generated by Django 2.2.19 on 2021-03-02 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wimmelbilder', '0018_auto_20201228_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointgroup',
            name='default_active',
            field=models.BooleanField(default=True, help_text='Punkte dieser Gruppe sind standardmäßig sichtbar.', verbose_name='standardmäßig sichtbar'),
        ),
    ]
