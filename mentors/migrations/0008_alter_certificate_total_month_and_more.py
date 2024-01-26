# Generated by Django 4.2.3 on 2024-01-26 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0007_certificate_total_month_certificate_total_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='total_month',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total month'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='total_year',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total year'),
        ),
        migrations.AlterField(
            model_name='education',
            name='total_month',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total month'),
        ),
        migrations.AlterField(
            model_name='education',
            name='total_year',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total year'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='total_month',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total month'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='total_year',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Total year'),
        ),
    ]
