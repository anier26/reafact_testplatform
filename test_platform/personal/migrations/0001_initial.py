# Generated by Django 2.0 on 2020-02-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('describe', models.TextField(default='')),
                ('status', models.BooleanField(default=1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
