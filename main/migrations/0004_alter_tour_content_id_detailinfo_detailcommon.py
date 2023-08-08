# Generated by Django 4.2.4 on 2023-08-05 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_tour_area_code_alter_tour_cat1_alter_tour_cat2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='content_id',
            field=models.CharField(max_length=40),
        ),
        migrations.CreateModel(
            name='DetailInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('info_name', models.CharField(max_length=40)),
                ('content_id', models.CharField(max_length=40)),
                ('fidgubun', models.CharField(max_length=40)),
                ('info_text', models.TextField(default='')),
                ('serial_num', models.CharField(max_length=40)),
                ('content_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detailinfo_type', to='main.areacode')),
            ],
        ),
        migrations.CreateModel(
            name='DetailCommon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('overview', models.TextField(default='')),
                ('tel_Name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=90)),
                ('modified_time', models.CharField(max_length=50)),
                ('homepage', models.TextField(default='')),
                ('cpyrhtDivCd', models.TextField(default='')),
                ('content_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detailcommon_contentid', to='main.servicecode')),
            ],
        ),
    ]
