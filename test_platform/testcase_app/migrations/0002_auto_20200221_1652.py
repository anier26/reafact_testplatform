# Generated by Django 2.0 on 2020-02-21 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testcase_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testcase',
            old_name='model',
            new_name='module',
        ),
    ]
