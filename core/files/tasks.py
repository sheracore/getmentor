"""Celery tasks."""
import json
import os
import re
import shutil
import subprocess
import tempfile
import time

from celery import shared_task
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str
from django.utils.timezone import now

from utilities import logger
# from learnwise.core.settings.models import Setting, SettingKey  # noqa
from utilities.sprite_video import SpriteVideo

from .models import FileModel, FileStatus, FileType
from .utilities import detect_type  # noqa
from .utilities import random_number  # noqa
from .utilities import (generate_key, get_media_convert_extension,
                        is_media_convert, random_string, round_number)


@shared_task
def file_task_runner_check():
    # if not Setting.objects.get_by_key(SettingKey.FILE_CONVERTOR_ENABLE).value:
    #     return

    queryset = FileModel.objects.filter(status=FileStatus.WAITING).values_list(
        "pk", flat=True
    )
    for pk in queryset:
        if FileModel.objects.filter(status=FileStatus.RUNNING).count() > 2:
            break
        file_model_process.delay(pk)
        time.sleep(0.25)
    # TODO: handle time out
    # # noqa که وجود داره اینه که چون از آپدیت مستقیم داریم استفاده میکنیم زمان ران شددن رو نداریم که حساب کنیم ببینیم کی باید تایم اوت کنیم.


@shared_task
def file_model_process(obj_id):
    """File model process via a channel to celery."""
    time.sleep(0.2)
    # DO nothing at this time
    # It's important calculate file size run first of all.
    # if not Setting.objects.get_by_key(SettingKey.FILE_CONVERTOR_ENABLE).value:
    #     return
    if (
        FileModel.objects.filter(pk=obj_id, status=FileStatus.RUNNING).exists()
        or FileModel.objects.filter(status=FileStatus.RUNNING).count() > 3
    ):
        return

    obj = FileModel.objects.get(pk=obj_id)
    if is_media_convert(obj.file):
        update_file(obj_id, {"status": FileStatus.FINISHED})
        return

    update_file(obj_id, {"status": FileStatus.RUNNING})

    try:
        calculate_file_size(obj_id)
        calculate_duration(obj_id)
        convert_to_supported_file(obj_id)
    except Exception:
        logger.exception("exception raise file_model_process", stack_info=True)
        update_file(obj_id, {"status": FileStatus.FAILED})

    obj.refresh_from_db()
    if obj.status == FileStatus.RUNNING:
        update_file(obj_id, {"status": FileStatus.FINISHED})


def calculate_duration(obj_id):
    obj = FileModel.objects.get(pk=obj_id)
    if obj.type == FileType.MOVIE or obj.type == FileType.VOICE:
        try:
            command = "ffprobe -i '{}' -v quiet -print_format json -show_format -hide_banner".format(
                obj.file.path
            )
            command_output = subprocess.check_output(
                command,
                shell=True,
                close_fds=True,
            )
            command_output = json.loads(command_output)
            duration = int(
                round_number(command_output.get("format", {}).get("duration", 0))
            )
            if obj.duration != duration:
                FileModel.objects.filter(pk=obj_id).update(duration=duration)
                # Below signal is for update this file in other models like activity from courses app
                # file_duration_change.send(
                #     sender=FileModel,
                #     file=obj,
                #     duration=duration,
                # )
        except Exception:
            logger.exception(
                "Cant find duration", stack_info=True, extra={"file_id": obj_id}
            )
            update_file(obj_id, {"status": FileStatus.FAILED})
    return 0


"""
Convert to support file
"""


def convert_to_supported_file(obj_id):
    obj = FileModel.objects.get(pk=obj_id)
    if obj.type == FileType.MOVIE or obj.type == FileType.VOICE:
        convert_to_hls(obj_id)
    return None


"""
Convert to mp3
"""


def convert_to_m4a(obj_id):
    obj = FileModel.objects.get(pk=obj_id)
    extension = "m4a"
    # Convert to specific mp3 codec
    if obj.file.path[(-1 * len(extension)) :] != extension:
        try:
            new_file_name = "{}.{}".format(
                os.path.basename(obj.file.path).split(".")[0], extension
            )
            new_relative_file = os.path.join(
                os.path.dirname(obj.file.name), new_file_name
            )

            # command = 'ffmpeg -i {} -acodec libmp3lame {}.{}'.format(
            base_command = "ffmpeg -i {} -c:a aac -strict -2 ".format(
                obj.file.path,
            )

            command_remove_metadata_and_image = "-vn -map_metadata -1 "
            command = "{} {} {}".format(
                base_command,
                command_remove_metadata_and_image,
                os.path.join(os.path.dirname(obj.file.path), new_file_name),
            )
            subprocess.check_output(
                command,
                shell=True,
                close_fds=True,
            )
            os.remove(obj.file.path)
            update_file(obj_id, {"file": new_relative_file})
        except Exception:
            logger.exception(
                "Cant convert to {}".format(extension),
                stack_info=True,
                extra={"file_id": obj_id},
            )
            update_file(obj_id, {"status": FileStatus.FAILED})
            return False
    return True


"""
Convert to hls
"""


def _backup_file(export_path, origin_path, obj_id):
    *_, file_extension = os.path.splitext(origin_path)
    file_backup_path = os.path.join(export_path, f"{obj_id}{file_extension}")
    if not os.path.exists(origin_path) or os.stat(origin_path).st_size <= 10000:
        logger.error("File not found", extra={"file_id": obj_id})
        update_file(obj_id, {"status": FileStatus.FAILED})
    if os.path.exists(file_backup_path):
        os.remove(file_backup_path)
    shutil.copy(origin_path, file_backup_path)


def convert_to_hls(obj_id):
    from django.core.files.storage import default_storage

    obj = FileModel.objects.get(pk=obj_id)
    extension = get_media_convert_extension()
    if is_media_convert(obj.file):
        return None
    export_path = default_storage.path("export_movies")
    os.makedirs(export_path, exist_ok=True)
    key = generate_key()
    fake_key = list(key)
    fake_key[5] = f"{int(fake_key[5]) + 1}"
    fake_key = "".join(fake_key)
    if obj.type == FileType.VOICE:
        if not convert_to_m4a(obj_id):
            raise ValidationError({"Cant convert to m4a."})
        obj = FileModel.objects.get(pk=obj_id)
        origin_path = obj.file.path
        _backup_file(export_path, origin_path, obj_id)
        try:
            tmp_key_info = tempfile.NamedTemporaryFile()
            tmp_key_file = tempfile.NamedTemporaryFile()

            # Open the file for writing.
            with open(tmp_key_file.name, "w") as f:
                f.write(f"{key}")
            # Open the file for writing.
            with open(tmp_key_info.name, "w") as f:
                f.writelines(f"file.key\n{tmp_key_file.name}")

            # 'ffmpeg -i {} -acodec copy -bsf:a aac_adtstoasc -vcodec copy  -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {}.{}'  # noqa
            command = "ffmpeg -i {}".format(
                origin_path,
            )
            command = "{} -vn -ac 2 -acodec copy".format(command)

            command = '{} -start_number 0 -hls_time 10 -hls_list_size 0 -f hls -hls_flags second_level_segment_index+second_level_segment_size -strftime 1 -use_localtime 1 -hls_segment_filename "{}_%%s_%%d.ts" -hls_key_info_file {} {}.{}'.format(  # noqa
                command,
                os.path.join(
                    os.path.dirname(origin_path),
                    re.sub(
                        "[\W_]+",  # noqa
                        "",
                        os.path.basename(
                            os.path.splitext(os.path.basename(obj.file.name))[0]
                        )[-20:],
                    ),
                ),
                tmp_key_info.name,
                origin_path,
                extension,
            )
            subprocess.check_output(
                command,
                shell=True,
                close_fds=True,
            )
            file_name = "{}.{}".format(obj.file.name, extension)
            update_file(obj_id, {"file": file_name, "key": fake_key})
            os.remove(origin_path)
        except Exception:
            logger.exception(
                "Cant convert to HLS", stack_info=True, extra={"file_id": obj_id}
            )
            update_file(obj_id, {"status": FileStatus.FAILED})
    elif obj.type == FileType.MOVIE:
        origin_path = obj.file.path
        _backup_file(export_path, origin_path, obj_id)
        try:
            from learnwise.core.files.vod import VOD

            vod = VOD(
                origin_path,
                target=os.path.join(
                    os.path.dirname(origin_path), f"{obj.pk}{random_string(4)}"
                ),
                key=key,
                fake_key="0234567890123456",
            )
            vod.prepare()
            vod.export()
            sprite = SpriteVideo(
                video_file=origin_path, thumb_rate_seconds=3, target_dir=vod.target
            )
            sprite.run()
            relative_path = (
                vod.get_master_playlist_path()
                .replace(settings.MEDIA_ROOT, "")
                .strip("/")
            )
            update_file(obj_id, {"file": relative_path, "key": fake_key})
            os.remove(origin_path)
        except Exception:
            logger.exception(
                "Cant convert to HLS", stack_info=True, extra={"file_id": obj_id}
            )
            update_file(obj_id, {"status": FileStatus.FAILED})


"""
ReConvert to hls
"""


def reverse_convert_from_hls(obj_id, new_path):
    obj = FileModel.objects.get(pk=obj_id)
    get_media_convert_extension()
    if not is_media_convert(obj.file):
        return False
    try:
        command_unformat = "ffmpeg -i {} -codec copy {}"
        if obj.type == FileType.VOICE:
            command_unformat = "ffmpeg -i {} -acodec libmp3lame {}"
        command = command_unformat.format(
            obj.file.path,
            new_path,
        )
        subprocess.check_output(
            command,
            shell=True,
            close_fds=True,
        )
        return True
    except Exception:
        logger.exception(
            "Cant reconvert from HLS", stack_info=True, extra={"file_id": obj_id}
        )
        update_file(obj_id, {"status": FileStatus.FAILED})
        return False


"""
Calculate file size
"""


def calculate_file_size(obj_id):
    obj = FileModel.objects.get(pk=obj_id)
    if is_media_convert(obj.file):
        return None

    update_file(obj_id, {"size": obj.file.size})


def update_file(obj_id, update_items):
    FileModel.objects.filter(pk=obj_id).update(**update_items)
    return FileModel.objects.get(pk=obj_id)


@shared_task
def migrate_to_new_changes():
    import csv

    from django.core.files.storage import default_storage

    export_path = default_storage.path("export_movies")
    os.makedirs(export_path, exist_ok=True)
    report_f = default_storage.path("migrate_to_new_changes.csv")
    previous_pk = []

    def get_result():
        result = {}
        result["time"] = now()
        result["pk"] = 0
        result["status"] = None
        result["fake_key"] = None
        result["key"] = None
        result["path"] = None
        return result

    if not os.path.exists(report_f):
        result = get_result()
        with open(report_f, "w") as f:
            a = ",".join(list(map(lambda x: smart_str(x), result.keys())))
            f.write(f"{a}\n")
            f.close()

    # ignore previous files
    with open(report_f, "r") as f:
        lines = f.readlines()
        f.close()
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(lines[0])
    lines = list(filter(None, map(lambda x: x.strip(dialect.delimiter), lines)))
    reader = csv.DictReader(lines, delimiter=dialect.delimiter)
    for x in reader:
        try:
            previous_pk.append(int(x.get("pk", "0")))
        except ValueError:
            continue
    queryset = (
        FileModel.objects.exclude(pk__in=previous_pk)
        .filter(type=FileType.MOVIE)
        .order_by("pk")
    )
    for obj in queryset:
        file_export_path = os.path.join(export_path, f"{obj.pk}.mp4")
        result = get_result()
        result["pk"] = obj.pk
        try:
            origin_path = obj.file.path
            if not os.path.exists(origin_path):
                # obj.delete()
                result["status"] = "DELETED"
                continue
            if not is_media_convert(obj.file) or not obj.key:
                # TODO: investigate this case without key
                result["status"] = "SKIP-1"
                continue
            key = obj.key
            result["fake_key"] = key
            key = f"{key[:5]}{int(key[5]) - 1}{key[6:]}"
            result["key"] = key
            get_media_convert_extension()
            # override path
            path = os.path.join(os.path.dirname(origin_path), f"{obj.pk}.m3u8")
            key_file_name = f"key_{obj.pk}.ini"
            key_path = os.path.join(os.path.dirname(origin_path), key_file_name)

            if not os.path.exists(file_export_path) or (
                os.path.exists(file_export_path)
                and os.stat(file_export_path).st_size <= 500
            ):
                if os.path.exists(file_export_path):
                    os.remove(file_export_path)

                with open(origin_path, "r") as src, open(path, "w") as dst:
                    txt = src.read()
                    dst.write(re.sub(r'URI="(.)*"', f'URI="{key_file_name}"', txt))
                    dst.close()
                with open(key_path, "w") as f:
                    f.write(result["key"])
                    f.close()
                command_unformat = "ffmpeg -allowed_extensions ALL -i {} -codec copy {}"
                command = command_unformat.format(path, file_export_path)
                subprocess.check_output(
                    command,
                    shell=True,
                    close_fds=True,
                )
                result["status"] = "RETRIEVE"
            else:
                result["status"] = "RETRIEVE-BEFORE"
            from learnwise.core.files.vod import VOD

            vod = VOD(
                file_export_path,
                target=os.path.join(
                    os.path.dirname(origin_path), f"{obj.pk}{random_string(4)}"
                ),
                key=result["key"],
                fake_key="0234567890123456",
            )
            vod.prepare()
            vod.export()
            result["status"] = "CONVERT-DONE"
            sprite = SpriteVideo(
                video_file=file_export_path, thumb_rate_seconds=3, target_dir=vod.target
            )
            sprite.run()
            result["status"] = "SPRITE-DONE"
            result["path"] = vod.get_master_playlist_path()
            result["status"] = "DONE"
        except Exception:
            logger.exception("migrate_to_new_changes", stack_info=True)
            result["status"] = "exception"
        finally:
            with open(report_f, "a") as f:
                a = ",".join(list(map(lambda x: smart_str(x), result.values())))
                f.write(f"{a}\n")
                f.close()
    with open(report_f, "a") as f:
        result = get_result()
        result["status"] = "DONE"
        a = ",".join(list(map(lambda x: smart_str(x), result.values())))
        f.write(f"{a}\n")
        f.close()


@shared_task
def migrate_to_regenerate_master_playlist():
    import csv

    from django.core.files.storage import default_storage

    export_path = default_storage.path("export_movies")
    report_f = default_storage.path("migrate_to_new_changes.csv")

    if not os.path.exists(report_f):
        return

    # ignore previous files
    with open(report_f, "r") as f:
        lines = f.readlines()
        f.close()
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(lines[0])
    lines = list(filter(None, map(lambda x: x.strip(dialect.delimiter), lines)))
    reader = csv.DictReader(lines, delimiter=dialect.delimiter)
    rows = {}
    for x in reader:
        if x.get("status") == "DONE":
            try:
                rows[int(x.get("pk", "0"))] = x
            except ValueError:
                continue

    queryset = FileModel.objects.filter(pk__in=rows.keys()).order_by("pk")

    for obj in queryset:
        file_export_path = os.path.join(export_path, f"{obj.pk}.mp4")
        try:
            new_path = rows[obj.pk].get("path")

            if os.path.exists(new_path):
                continue
            key = obj.key
            key = f"{key[:5]}{int(key[5]) - 1}{key[6:]}"
            from learnwise.core.files.vod import VOD

            vod = VOD(
                file_export_path,
                target=os.path.dirname(new_path),
                key=key,
                fake_key="0234567890123456",
            )
            vod.prepare()
            vod.export_master_playlist()
        except Exception:
            logger.exception("migrate_to_master_playlist", stack_info=True)


@shared_task
def migrate_to_second_step_changes():
    import csv
    import glob

    from django.core.files.storage import default_storage

    export_path = default_storage.path("export_movies")
    os.makedirs(export_path, exist_ok=True)
    report_f = default_storage.path("migrate_to_new_changes.csv")
    report_second = default_storage.path("migrate_to_second_step.csv")

    def get_result():
        result = {}
        result["time"] = now()
        result["pk"] = 0
        result["status"] = None
        result["old_path"] = None
        return result

    if not os.path.exists(report_second):
        result = get_result()
        with open(report_second, "w") as f:
            a = ",".join(list(map(lambda x: smart_str(x), result.keys())))
            f.write(f"{a}\n")
            f.close()

    with open(report_f, "r") as f:
        first_step_lines = f.readlines()
        f.close()
    sniffer_2 = csv.Sniffer()
    dialect_2 = sniffer_2.sniff(first_step_lines[0])
    first_step_lines = list(
        filter(None, map(lambda x: x.strip(dialect_2.delimiter), first_step_lines))
    )
    reader_2 = csv.DictReader(first_step_lines, delimiter=dialect_2.delimiter)
    rows = {}
    for x in reader_2:
        if x.get("status") == "DONE":
            try:
                rows[int(x.get("pk", "0"))] = x
            except ValueError:
                continue
    queryset = FileModel.objects.filter(pk__in=rows.keys()).order_by("pk")
    for obj in queryset:
        result = get_result()
        try:
            result["pk"] = obj.pk
            origin_path = obj.file.path
            result["old_path"] = origin_path
            new_path = rows[obj.pk].get("path")
            new_relative_path = new_path.split("media")[1].strip("/")
            path = os.path.join(os.path.dirname(origin_path), f"{obj.pk}.m3u8")
            key_file_name = f"key_{obj.pk}.ini"
            key_path = os.path.join(os.path.dirname(origin_path), key_file_name)

            for fl in [
                key_path,
                path,
                os.path.join(os.path.dirname(origin_path), f"{obj.pk}_thumbs.vtt"),
                os.path.join(os.path.dirname(origin_path), f"{obj.pk}_sprite.jpg"),
            ]:
                if os.path.exists(fl):
                    os.remove(fl)

            if os.path.basename(origin_path) == "playlist.m3u8":
                result["status"] = "EXISTS"
                result["old_path"] = None
                with open(report_second, "a") as f:
                    a = ",".join(list(map(lambda x: smart_str(x), result.values())))
                    f.write(f"{a}\n")
                    f.close()
                continue

            for fl in glob.glob(
                os.path.join(
                    os.path.dirname(origin_path),
                    f"{''.join(os.path.basename(origin_path).split('.')[0:1])}*",
                )
            ):
                if os.path.exists(fl):
                    os.remove(fl)
            if not os.path.exists(new_path):
                result["status"] = "PLAYLIST_DOES_NOT_EXISTS"
                result["old_path"] = None
                with open(report_second, "a") as f:
                    a = ",".join(list(map(lambda x: smart_str(x), result.values())))
                    f.write(f"{a}\n")
                    f.close()
                continue
            FileModel.objects.filter(pk=obj.pk).update(
                file=new_relative_path, status=FileStatus.FINISHED
            )
            result["status"] = "DONE"
        except Exception:
            logger.exception("migrate_to_second_step", stack_info=True)
            result["status"] = "exception"
        finally:
            with open(report_second, "a") as f:
                a = ",".join(list(map(lambda x: smart_str(x), result.values())))
                f.write(f"{a}\n")
                f.close()
    with open(report_second, "a") as f:
        result = get_result()
        result["status"] = "DONE"
        a = ",".join(list(map(lambda x: smart_str(x), result.values())))
        f.write(f"{a}\n")
        f.close()
