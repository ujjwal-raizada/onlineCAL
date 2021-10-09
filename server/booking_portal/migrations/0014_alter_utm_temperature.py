# Generated by Django 3.2.5 on 2021-09-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_portal', '0013_utm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utm',
            name='temperature',
            field=models.IntegerField(help_text='<small>The temperature ranges are as follows:</br>Room Temperature = 25°C</br>Temperature Chamber = -70°C - 250°C</br>Furnace = 250°C - 1200°C</br>Any additional remarks can be specified in the box below.</br></small>'),
        ),
    ]