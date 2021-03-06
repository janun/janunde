# Generated by Django 2.2.12 on 2020-04-07 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0084_auto_20200407_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaSettingsSocialMediaEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link', models.URLField()),
                ('icon_color', models.ImageField(upload_to='', verbose_name='buntes Icon')),
                ('icon_gray', models.ImageField(upload_to='', verbose_name='graues Icon')),
                ('tooltip', models.CharField(blank=True, max_length=255)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_medias', to='core.SocialMediaSettings')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='SocialMediaEntry',
        ),
    ]
