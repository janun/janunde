# Generated by Django 2.2.14 on 2020-09-08 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_delete_banner'),
        ('contact', '0022_auto_20200519_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BasePage')),
                ('heading', models.CharField(default='Kontakt', max_length=255, verbose_name='Überschrift')),
            ],
            options={
                'verbose_name': 'Kontaktseite',
                'verbose_name_plural': 'Kontaktseiten',
            },
            bases=('core.basepage',),
        ),
    ]