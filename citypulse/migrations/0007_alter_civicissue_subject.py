# Generated by Django 5.2 on 2025-04-28 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citypulse', '0006_civicissue_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='civicissue',
            name='subject',
            field=models.CharField(default='other', max_length=100),
            preserve_default=False,
        ),
    ]
