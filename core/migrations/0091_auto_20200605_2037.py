# Generated by Django 2.2.12 on 2020-06-05 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0090_auto_20200531_2204"),
    ]

    operations = [
        migrations.RemoveField(model_name="basepage", name="megamenu_category",),
        migrations.RemoveField(model_name="standardpage", name="title_color",),
    ]
