# Generated by Django 2.2.17 on 2020-12-17 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refs', '0003_auto_20200213_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='ref',
            name='bibcode',
            field=models.CharField(blank=True, max_length=19),
        ),
    ]