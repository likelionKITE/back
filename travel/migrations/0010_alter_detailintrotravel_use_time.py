# Generated by Django 4.2.4 on 2023-08-08 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_alter_detailintrotravel_accom_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailintrotravel',
            name='use_time',
            field=models.CharField(max_length=1000),
        ),
    ]
