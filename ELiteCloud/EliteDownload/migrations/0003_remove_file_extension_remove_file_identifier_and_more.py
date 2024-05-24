# Generated by Django 5.0.6 on 2024-05-24 16:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EliteDownload', '0002_alter_file_options_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='extension',
        ),
        migrations.RemoveField(
            model_name='file',
            name='identifier',
        ),
        migrations.RemoveField(
            model_name='file',
            name='users',
        ),
        migrations.AddField(
            model_name='file',
            name='date_upload',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(default=django.utils.timezone.now, upload_to='files/'),
            preserve_default=False,
        ),
    ]
