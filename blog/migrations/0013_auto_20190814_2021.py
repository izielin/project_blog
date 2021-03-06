# Generated by Django 2.2.4 on 2019-08-14 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20190813_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('picture', models.ImageField(upload_to='post_pics')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Django', 'Django'), ('Python', 'Python'), ('C++', 'CPP'), ('Graphics', 'Graphics'), ('Text Editor', 'TextEditor'), ('Spreadsheet', 'Spreadsheet'), ('DataBase', 'DataBase'), ('Web Design', 'WebDesign')], max_length=100),
        ),
    ]
