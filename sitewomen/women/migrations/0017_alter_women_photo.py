# Generated by Django 5.1.2 on 2024-11-23 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0016_women_photo_alter_uploadfiles_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='photo',
            field=models.FileField(blank=True, default=None, null=True, upload_to='post_docs/%Y/%m/%d', verbose_name='Файлы'),
        ),
    ]
