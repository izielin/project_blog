# Generated by Django 2.2.3 on 2019-08-06 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='b1.jpg', upload_to='post_pics'),
        ),
    ]