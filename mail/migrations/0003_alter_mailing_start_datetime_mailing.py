# Generated by Django 4.2.2 on 2024-04-25 21:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="start_datetime_mailing",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 4, 26, 0, 58, 14, 58847),
                verbose_name="Дата и время начала отправки рассылки",
            ),
        ),
    ]
