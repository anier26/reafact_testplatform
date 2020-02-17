# Generated by Django 2.0 on 2020-02-17 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='update_time',
            field=models.DateTimeField(default='2020-02-17 20:29:30'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='describe',
            field=models.TextField(default='', verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.BooleanField(default=1, verbose_name='状态'),
        ),
    ]
