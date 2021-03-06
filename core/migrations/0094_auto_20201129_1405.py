# Generated by Django 2.2.17 on 2020-11-29 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_delete_banner'),
        ('staff', '0007_auto_20200909_2315'),
        ('contact', '0027_auto_20201227_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='formfield',
            name='clean_name',
            field=models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name'),
        ),
        # migrations.AlterField(
        #     model_name='article',
        #     name='author',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='staff.Employee', verbose_name='Autor_in'),
        # ),
        migrations.AddField(
            model_name="article",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pages",
                to="staff.Employee",
                verbose_name="Autor_in",
            ),
        ),
    ]
