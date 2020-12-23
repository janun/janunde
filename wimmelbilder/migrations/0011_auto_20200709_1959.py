# Generated by Django 2.2.14 on 2020-07-09 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wimmelbilder', '0010_auto_20200709_1852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointgroupwimmelbildpage',
            options={'ordering': ['sort_order']},
        ),
        migrations.AlterModelOptions(
            name='wimmelbildpointwimmelbildpage',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='pointgroupwimmelbildpage',
            name='sort_order',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='wimmelbildpointwimmelbildpage',
            name='sort_order',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='wimmelbildpoint',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Wird ohne Gruppe nicht angezeigt. Auswählen geht bei neuen Gruppen erst nach Speichern', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='points', to='wimmelbilder.PointGroup', verbose_name='Gruppe'),
        ),
    ]