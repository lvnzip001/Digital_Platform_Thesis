# Generated by Django 4.0.3 on 2022-04-05 15:54

from django.db import migrations, models
import my_platform.models


class Migration(migrations.Migration):

    dependencies = [
        ('my_platform', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embed_ownership_image',
            name='file',
            field=models.ImageField(default=1, upload_to=my_platform.models.UploadToPathAndRename),
            preserve_default=False,
        ),
    ]
