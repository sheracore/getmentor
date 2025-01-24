# Generated by Django 4.2.3 on 2025-01-24 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0005_industry_market_qualified_limitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='market_qualified_limitation',
            field=models.IntegerField(default=10, help_text='Industry market qualified limitation used for market industry display'),  # noqa: E501
        ),
    ]
