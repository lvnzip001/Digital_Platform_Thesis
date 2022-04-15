# Generated by Django 4.0.3 on 2022-03-26 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import my_platform.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='books/pdfs/')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='books/covers')),
            ],
        ),
        migrations.CreateModel(
            name='Embed_Enforcement_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.CharField(max_length=100)),
                ('receiver', models.CharField(max_length=100)),
                ('file', models.ImageField(blank=True, null=True, upload_to=my_platform.models.UploadToPathAndRename)),
            ],
        ),
        migrations.CreateModel(
            name='Embed_Enforcement_Sound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.CharField(max_length=100)),
                ('receiver', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='documents/file_uploaded/')),
            ],
        ),
        migrations.CreateModel(
            name='Embed_Enforcement_Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.CharField(max_length=100)),
                ('receiver', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='documents/file_uploaded/')),
            ],
        ),
        migrations.CreateModel(
            name='Embed_Ownership_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.CharField(max_length=100)),
                ('file', models.ImageField(blank=True, null=True, upload_to=my_platform.models.UploadToPathAndRename)),
            ],
        ),
        migrations.CreateModel(
            name='Embed_Ownership_Sound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='documents/file_uploaded/')),
            ],
        ),
        migrations.CreateModel(
            name='Embed_Ownership_Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='documents/file_uploaded/')),
            ],
        ),
        migrations.CreateModel(
            name='Extract_Embedded_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('source_file', models.CharField(default='Extraction File', max_length=100)),
                ('file', models.FileField(upload_to='extraction_files/')),
            ],
        ),
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('organisation', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Embedded_Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('image_o_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_platform.embed_ownership_image')),
                ('user_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_platform.user_info')),
            ],
        ),
        migrations.AddField(
            model_name='embed_ownership_image',
            name='user_info',
            field=models.ForeignKey(max_length=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_platform.user_info'),
        ),
    ]