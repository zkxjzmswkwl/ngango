# Generated by Django 5.1.4 on 2024-12-09 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="other_field",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="member",
            name="random_field",
            field=models.CharField(default="123123jifosadfsadf", max_length=69),
            preserve_default=False,
        ),
    ]
