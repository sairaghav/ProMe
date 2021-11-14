# Generated by Django 3.2.9 on 2021-11-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StreetList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=200, verbose_name='Street Name')),
                ('news_from', models.CharField(max_length=200, verbose_name='News From')),
                ('news_till', models.CharField(max_length=200, verbose_name='News Till')),
            ],
        ),
        migrations.CreateModel(
            name='StreetRisk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=200, verbose_name='Street Name')),
                ('date', models.DateTimeField(verbose_name='Article Published Date')),
                ('source', models.CharField(max_length=200, verbose_name='News Source')),
                ('tags', models.CharField(max_length=200, verbose_name='Tags')),
                ('link', models.CharField(max_length=500, verbose_name='Article Link')),
            ],
        ),
    ]
