# Generated by Django 4.2 on 2024-12-24 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowings_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowing',
            name='actual_return_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
