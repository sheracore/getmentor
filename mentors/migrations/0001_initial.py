# Generated by Django 4.2.3 on 2024-01-20 21:26

import django.db.models.deletion
from django.db import migrations, models

import utilities.db.fields.date_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(choices=[('NO_DEGREE', 'No Degree'), ('HIGH_SCHOOL_DIPLOMA', 'High School Diploma'), ('ASSOCIATE', 'Associate'), ('BACHELOR', 'Bachelor'), ('MASTER', 'Master'), ('DOCTOR', 'Doctor')], verbose_name='Degree')), # noqa F501
                ('grade', models.CharField(blank=True, max_length=32, null=True, verbose_name='Grade')), # noqa F501
                ('start_year', utilities.db.fields.date_fields.YearField(blank=True, choices=[(2024, '2024'), (2023, '2023'), (2022, '2022'), (2021, '2021'), (2020, '2020'), (2019, '2019'), (2018, '2018'), (2017, '2017'), (2016, '2016'), (2015, '2015'), (2014, '2014'), (2013, '2013'), (2012, '2012'), (2011, '2011'), (2010, '2010'), (2009, '2009'), (2008, '2008'), (2007, '2007'), (2006, '2006'), (2005, '2005'), (2004, '2004'), (2003, '2003'), (2002, '2002'), (2001, '2001'), (2000, '2000'), (1999, '1999'), (1998, '1998'), (1997, '1997'), (1996, '1996'), (1995, '1995'), (1994, '1994'), (1993, '1993'), (1992, '1992'), (1991, '1991'), (1990, '1990'), (1989, '1989'), (1988, '1988'), (1987, '1987'), (1986, '1986'), (1985, '1985'), (1984, '1984'), (1983, '1983'), (1982, '1982'), (1981, '1981'), (1980, '1980'), (1979, '1979'), (1978, '1978'), (1977, '1977'), (1976, '1976'), (1975, '1975')], null=True, verbose_name='Start Year')), # noqa F501
                ('end_year', utilities.db.fields.date_fields.YearField(blank=True, choices=[(2024, '2024'), (2023, '2023'), (2022, '2022'), (2021, '2021'), (2020, '2020'), (2019, '2019'), (2018, '2018'), (2017, '2017'), (2016, '2016'), (2015, '2015'), (2014, '2014'), (2013, '2013'), (2012, '2012'), (2011, '2011'), (2010, '2010'), (2009, '2009'), (2008, '2008'), (2007, '2007'), (2006, '2006'), (2005, '2005'), (2004, '2004'), (2003, '2003'), (2002, '2002'), (2001, '2001'), (2000, '2000'), (1999, '1999'), (1998, '1998'), (1997, '1997'), (1996, '1996'), (1995, '1995'), (1994, '1994'), (1993, '1993'), (1992, '1992'), (1991, '1991'), (1990, '1990'), (1989, '1989'), (1988, '1988'), (1987, '1987'), (1986, '1986'), (1985, '1985'), (1984, '1984'), (1983, '1983'), (1982, '1982'), (1981, '1981'), (1980, '1980'), (1979, '1979'), (1978, '1978'), (1977, '1977'), (1976, '1976'), (1975, '1975')], null=True, verbose_name='End Year')), # noqa F501
                ('start_month', utilities.db.fields.date_fields.MonthField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], null=True, verbose_name='Start Month')), # noqa F501
                ('end_month', utilities.db.fields.date_fields.MonthField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], null=True, verbose_name='End Month')), # noqa F501
                ('activities_societies', models.TextField(blank=True, max_length=500, null=True, verbose_name='Activities and Societies')), # noqa F501
                ('major', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentors.major', verbose_name='Major')), # noqa F501
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentors.university', verbose_name='university')), # noqa F501
            ],
        ),
    ]
