# Generated by Django 2.2.13 on 2020-07-02 18:43

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_bannerssettings_bannerssettingsbanner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='color',
            field=models.CharField(choices=[('white', 'Weiß'), ('green', 'Grün'), ('blue', 'Blau'), ('red', 'Rot')], default='white', max_length=16, verbose_name='Hintergrundfarbe'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='text',
            field=wagtail.core.fields.RichTextField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='bannerssettingsbanner',
            name='setting',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='banners.BannersSettings'),
        ),
    ]
