# Generated by Django 3.0.2 on 2020-12-29 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_portal', '0006_auto_20201230_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='text',
            field=models.TextField(),
        ),
    ]
