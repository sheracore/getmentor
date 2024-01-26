# Generated by Django 4.2.3 on 2024-01-22 20:31

import django.db.models.deletion
from django.db import migrations, models

import utilities.db.fields.date_fields


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0002_company_experience_role_skill_experienceskill_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='is_current',
            field=models.BooleanField(default=False, verbose_name='I am currently in this organization.'),
        ),
        migrations.AlterField(
            model_name='education',
            name='start_month',
            field=utilities.db.fields.date_fields.MonthField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1, verbose_name='Start Month'),  # noqa F501
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='education',
            name='start_year',
            field=utilities.db.fields.date_fields.YearField(choices=[(2024, '2024'), (2023, '2023'), (2022, '2022'), (2021, '2021'), (2020, '2020'), (2019, '2019'), (2018, '2018'), (2017, '2017'), (2016, '2016'), (2015, '2015'), (2014, '2014'), (2013, '2013'), (2012, '2012'), (2011, '2011'), (2010, '2010'), (2009, '2009'), (2008, '2008'), (2007, '2007'), (2006, '2006'), (2005, '2005'), (2004, '2004'), (2003, '2003'), (2002, '2002'), (2001, '2001'), (2000, '2000'), (1999, '1999'), (1998, '1998'), (1997, '1997'), (1996, '1996'), (1995, '1995'), (1994, '1994'), (1993, '1993'), (1992, '1992'), (1991, '1991'), (1990, '1990'), (1989, '1989'), (1988, '1988'), (1987, '1987'), (1986, '1986'), (1985, '1985'), (1984, '1984'), (1983, '1983'), (1982, '1982'), (1981, '1981'), (1980, '1980'), (1979, '1979'), (1978, '1978'), (1977, '1977'), (1976, '1976'), (1975, '1975')], default=2024, verbose_name='Start Year'),  # noqa F501
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='experience',
            name='is_current',
            field=models.BooleanField(default=False, verbose_name='I am currently in this organization.'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentors.role', verbose_name='Role'),  # noqa F501
        ),
    ]
