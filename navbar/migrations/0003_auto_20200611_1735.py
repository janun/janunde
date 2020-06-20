# Generated by Django 2.2.13 on 2020-06-11 15:35

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('navbar', '0002_auto_20200605_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navbarsettings',
            name='menu',
            field=wagtail.core.fields.StreamField([('submenu', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='Titel')), ('submenu', wagtail.core.blocks.StreamBlock([('category', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='Titel')), ('submenu', wagtail.core.blocks.StreamBlock([('internal_page', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(label='Seite')), ('title', wagtail.core.blocks.CharBlock(help_text='Überschreibt Titel der Seite', label='Titel', required=False)), ('subtitle', wagtail.core.blocks.CharBlock(help_text='Überschreibt Untertitel der Seite', label='Untertitel', required=False))]))], label='Untermenü'))]))], label='Menü-Einträge'))])), ('internal_page', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(label='Seite')), ('title', wagtail.core.blocks.CharBlock(help_text='Überschreibt Titel der Seite', label='Titel', required=False))]))]),
        ),
    ]
