from django.db import migrations
from django_celery_beat.models import IntervalSchedule, PeriodicTask

file_checker_name = "file_checker"


def file_checker_schedule(apps, schema_editor):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.MINUTES
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name=file_checker_name,
        task="core.files.tasks.file_task_runner_check",
    )


def reverse_file_checker_schedule(apps, schema_editor):
    try:
        PeriodicTask.objects.filter(name=file_checker_name).delete()
    except PeriodicTask.DoesNotExist:
        pass


class Migration(migrations.Migration):
    dependencies = [("files", "0001_initial")]

    operations = [
        migrations.RunPython(
            file_checker_schedule, reverse_code=reverse_file_checker_schedule
        ),
    ]
