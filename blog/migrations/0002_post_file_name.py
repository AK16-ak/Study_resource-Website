# Generated by Django 3.2 on 2021-05-03 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]