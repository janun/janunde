# Generated by Django 2.2.14 on 2020-07-08 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_delete_banner'),
        ('wimmelbilder', '0006_auto_20200708_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='wimmelbildpoint',
            name='icon',
            field=models.ForeignKey(blank=True, help_text='Sollte Quadratisch sein', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Icon'),
        ),
    ]
