# Generated by Django 4.2.4 on 2023-08-07 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_servicecode_content_type_id_and_more'),
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailintrotravel',
            name='content_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_intro_travel', to='main.tour'),
        ),
    ]
