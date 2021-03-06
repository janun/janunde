# Generated by Django 2.2.13 on 2020-07-02 17:47

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannersSettingsBanner',
            fields=[
                ('banner_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='banners.Banner')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('setting', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='banners.Banner')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('banners.banner', models.Model),
        ),
        migrations.CreateModel(
            name='BannersSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banner',
            },
        ),
    ]
