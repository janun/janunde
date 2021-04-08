# Generated by Django 2.2.17 on 2021-02-05 01:36

from django.db import migrations


def copy_related_groups(apps, schema_editor):
    EventPage = apps.get_model("events", "EventPage")
    EventPageGroup = apps.get_model("events", "EventPageGroup")

    for event in EventPage.objects.all():
        if event.related_group:
            eg = EventPageGroup(eventpage=event, group=event.related_group)
            eg.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0039_auto_20210205_0234"),
    ]

    operations = [migrations.RunPython(copy_related_groups, do_nothing)]