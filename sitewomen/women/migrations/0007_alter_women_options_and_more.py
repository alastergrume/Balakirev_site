# Generated by Django 5.1.2 on 2024-11-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0006_alter_women_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='women',
            options={'ordering': ['-time_create']},
        ),
        migrations.AddIndex(
            model_name='women',
            index=models.Index(fields=['-time_create'], name='women_women_time_cr_9f33c2_idx'),
        ),
    ]
