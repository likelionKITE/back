# Generated by Django 4.2.4 on 2023-08-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0008_alter_detailintrotravel_use_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailintrotravel',
            name='accom_count',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='detailintrotravel',
            name='exp_age_range',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='detailintrotravel',
            name='open_date',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='detailintrotravel',
            name='rest_date',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='detailintrotravel',
            name='use_season',
            field=models.CharField(max_length=100),
        ),
    ]
