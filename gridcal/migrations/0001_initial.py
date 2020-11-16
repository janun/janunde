# Generated by Django 2.2.14 on 2020-11-16 15:27

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0093_delete_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='GridCalendar',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BasePage')),
                ('heading', models.CharField(max_length=255, verbose_name='Überschrift')),
                ('highlight_in_heading', models.CharField(blank=True, help_text='Wiederhole Text aus der Überschrift der farblich hervorgehoben werden soll', max_length=255, verbose_name='Hervorhebungen in der Überschrift')),
                ('intro', wagtail.core.fields.RichTextField(blank=True, verbose_name='Intro')),
                ('show_placeholder_for_unpublished', models.BooleanField(default=False, verbose_name='Zeige Platzhalter für unveröffentlichte Beiträge')),
            ],
            options={
                'verbose_name': 'Kalender/Rasteransicht',
            },
            bases=('core.basepage',),
        ),
        migrations.CreateModel(
            name='CalendarEntry',
            fields=[
                ('standardpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.StandardPage')),
                ('main_image', models.ForeignKey(blank=True, help_text='Bild, das den Artikel repräsentiert. Wird in Übersichten verwendet.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Bild für Übersichten')),
                ('related_group', models.ForeignKey(blank=True, help_text='Eine JANUN-Gruppe, die diesem Eintrag zugeordnet ist', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gridcal_entries', to='core.Group', verbose_name='Zugehörige Gruppe')),
            ],
            options={
                'verbose_name': 'Kalendereintrag',
                'verbose_name_plural': 'Kalendereinträge',
            },
            bases=('core.standardpage',),
        ),
    ]
