# Generated by Django 2.2.4 on 2019-08-12 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190812_1017'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Picture',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='selected_image',
            new_name='image',
        ),
    ]
