# Generated by Django 4.0.5 on 2022-07-01 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_auther_name_blogs_auther'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogs',
            old_name='auther',
            new_name='author',
        ),
    ]
