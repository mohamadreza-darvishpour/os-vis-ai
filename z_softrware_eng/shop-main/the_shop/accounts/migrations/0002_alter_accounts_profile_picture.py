# Generated by Django 4.2 on 2024-08-22 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='profile_picture'),
        ),
    ]
