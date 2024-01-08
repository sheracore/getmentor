import datetime
import glob
import math
import os
import pipes
import shlex
import shutil
import subprocess
import sys
import tempfile
from logging import getLogger as logger


class SpriteVideo:
    """small wrapper class as convenience accessor for external scripts"""

    """use sprite video run()"""

    def __init__(
        self,
        video_file,
        sprite_file_name="sprite.jpg",  # JPG smaller than png
        vtt_file_name="thumbs.vtt",
        thumb_out_dir=None,
        thumb_width=100,
        skip_first=False,
        thumb_rate_seconds=10,
        use_unique_out_dir=False,  # true to make a unique timestamped output dir each time, else False to overwrite/replace existing outdir  # noqa
        time_sync_adjust=-0.5,
        target_dir=None
        # set to 1 to not adjust time (gets multiplied by thumbRate); On my machine,ffmpeg snapshots show earlier images than expected timestamp by about 1/2 the thumbRate (for one vid, 10s thumbrate->images were 6s earlier than expected;45->22s early,90->44 sec early)   # noqa
    ):
        if not os.path.exists(video_file):
            sys.exit("File does not exist: %s" % video_file)
        self.video_file = video_file
        if not thumb_out_dir:
            thumb_out_dir = os.path.dirname(video_file)
        self.thumb_out_dir = thumb_out_dir
        self.thumb_width = thumb_width
        self.use_unique_out_dir = use_unique_out_dir
        self.time_sync_adjust = time_sync_adjust
        self.skip_first = skip_first
        self.thumb_rate_seconds = thumb_rate_seconds
        self.out_dir = tempfile.TemporaryDirectory()
        self.sprite_file_name = sprite_file_name
        self.sprite_file = os.path.join(self.get_out_dir(), self.sprite_file_name)
        self.vtt_file_name = vtt_file_name
        self.vtt_file = os.path.join(self.get_out_dir(), self.vtt_file_name)
        if not target_dir:
            target_dir = os.path.dirname(
                os.path.dirname(self.get_temporary_sprite_file())
            )
        self.target_dir = target_dir

    def get_video_file(self):
        return self.video_file

    def get_out_dir(self):
        return self.out_dir.name

    def get_temporary_sprite_file(self):
        return self.sprite_file

    def get_sprite_file(self):
        return os.path.join(self.target_dir, self.sprite_file_name)

    def get_temporary_vtt_file(self):
        return self.vtt_file

    def get_vtt_file(self):
        return os.path.join(self.target_dir, self.vtt_file_name)

    def get_new_out_dir(self, video_file):
        base, ext = os.path.splitext(video_file)
        script = sys.argv[0]
        base_path = os.path.dirname(
            os.path.abspath(script)
        )  # make output dir always relative to this script regardless of shell directory
        if len(self.thumb_out_dir) > 0 and self.thumb_out_dir[0] == "/":
            output_dir = self.thumb_out_dir
        else:
            output_dir = os.path.join(base_path, self.thumb_out_dir)
        if self.use_unique_out_dir:
            new_out_dir = "%s.%s" % (
                os.path.join(output_dir, base),
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            )
        else:
            new_out_dir = "%s_%s" % (os.path.join(output_dir, base), "vtt")

        return new_out_dir

    def make_out_dir(self):
        """create unique output dir based on video file name and current timestamp"""
        new_out_dir = self.get_out_dir()
        if not os.path.exists(new_out_dir):
            os.makedirs(new_out_dir)
        elif os.path.exists(new_out_dir) and not self.use_unique_out_dir:
            # remove previous contents if reusing out_dir
            files = os.listdir(new_out_dir)
            for f in files:
                os.unlink(os.path.join(new_out_dir, f))
        return new_out_dir

    @staticmethod
    def do_cmd(cmd):  # execute a shell command and return/print its output
        args = shlex.split(cmd)  # tokenize args
        output = None
        try:
            output = subprocess.check_output(
                args, stderr=subprocess.STDOUT
            )  # pipe stderr into stdout
        except Exception as e:
            logger.error("Execute command failed")
            raise e  # todo ?
        ret = "END   [%s]\n%s" % (datetime.datetime.now(), output)  # noqa
        sys.stdout.flush()
        return output

    @staticmethod
    def get_thumb_images(new_dir):
        return glob.glob("%s/*.jpg" % new_dir)

    def resize(self, files):
        """change image output size to 100 width (originally matches size of video)
        - pass a list of files as string rather than use '*' with sips command because
          subprocess does not treat * as wildcard like shell does"""
        self.do_cmd(
            "mogrify -geometry %dx %s"
            % (self.thumb_width, " ".join(map(pipes.quote, files)))
        )

    @classmethod
    def get_geometry(cls, file):
        """execute command to give geometry HxW+X+Y of each file matching command
          identify -format "%g - %f\n" *         #all files
          identify -format "%g - %f\n" onefile.jpg  #one file
        SAMPLE OUTPUT
           100x66+0+0 - _00001.jpg
           100x2772+0+0 - sprite2.jpg
           4200x66+0+0 - sprite2h.jpg"""
        geom = cls.do_cmd(
            """identify -format "%%g - %%f\n" %s""" % pipes.quote(file)
        ).decode("utf-8")
        parts = geom.split("-", 1)
        return parts[
            0
        ].strip()  # return just the geometry prefix of the line, sans extra whitespace

    @staticmethod
    def get_time_str(num_seconds, adjust=None):
        """convert time in seconds to VTT format time (HH:)MM:SS.ddd"""
        if adjust:  # offset the time by the adjust amount, if applicable
            seconds = max(
                num_seconds + adjust, 0
            )  # don't go below 0! can't have a negative timestamp
        else:
            seconds = num_seconds
        seconds = int(seconds)
        return "{:0>8}.000".format(str(datetime.timedelta(seconds=seconds)))

    @staticmethod
    def get_grid_coordinates(img_num, gridsize, w, h):
        """given an image number in our sprite, map the coordinates to it in X,Y,W,H format"""
        y = (img_num - 1) // gridsize
        x = (img_num - 1) - (y * gridsize)
        imgx = x * w
        imgy = y * h
        return "%s,%s,%s,%s" % (imgx, imgy, w, h)

    def make_sprite(self, sprite_file, coords, grid_size):
        """montage _*.jpg -tile 8x8 -geometry 100x66+0+0 montage.jpg  #GRID of images
              NOT USING: convert *.jpg -append sprite.jpg     #SINGLE VERTICAL LINE of images
              NOT USING: convert *.jpg +append sprite.jpg     #SINGLE HORIZONTAL LINE of images
        base the sprite size on the number of thumbs we need to make into a grid."""
        out_dir = self.get_out_dir()
        grid = "%dx%d" % (grid_size, grid_size)
        cmd = "montage %s/*.jpg -tile %s -geometry %s %s" % (
            pipes.quote(out_dir),
            grid,
            coords,
            pipes.quote(sprite_file),
        )  # if video had more than 144 thumbs, would need to be bigger grid, making it big to cover all our case
        self.do_cmd(cmd)

    @staticmethod
    def write_vtt(vtt_file, contents):
        """output VTT file"""
        with open(vtt_file, mode="w") as h:
            h.write(contents)
        logger.info("Wrote: %s" % vtt_file)

    def take_snapshot(self, video_file):
        """
        take snapshot image of video every Nth second and output to sequence file names and custom directory
            reference: https://trac.ffmpeg.org/wiki/Create%20a%20thumbnail%20image%20every%20X%20seconds%20of%20the%20video  # noqa
        """
        new_out_dir = self.get_out_dir()
        rate = (
            "1/%d" % self.thumb_rate_seconds
        )  # 1/60=1 per minute, 1/120=1 every 2 minutes
        cmd = "ffmpeg -i %s -f image2 -bt 20M -vf fps=%s -aspect 16:9 %s/%%05d.jpg" % (
            pipes.quote(video_file),
            rate,
            pipes.quote(new_out_dir),
        )
        self.do_cmd(cmd)
        if self.skip_first:
            # remove the first image
            logger.info("Removing first image, unneeded")
            os.unlink("%s/00001.jpg" % new_out_dir)
        count = len(os.listdir(new_out_dir))
        logger.info("%d thumbs written in %s" % (count, new_out_dir))
        # return the list of generated files
        return count, self.get_thumb_images(new_out_dir)

    def make_vtt(self, sprite_file, num_segments, coords, grid_size, writefile):
        """generate & write vtt file mapping video time to each image's coordinates
        in our spritemap"""
        # split geometry string into individual parts
        # 4200x66+0+0     ===  WxH+X+Y
        wh, xy = coords.split("+", 1)
        w, h = wh.split("x")
        w = int(w)
        h = int(h)
        # x,y = xy.split("+")
        # ======= SAMPLE WEBVTT FILE=====
        # WEBVTT
        #
        # 00:00.000 --> 00:05.000
        # /assets/thumbnails.jpg#xywh=0,0,160,90
        #
        # 00:05.000 --> 00:10.000
        # /assets/preview2.jpg#xywh=160,0,320,90
        #
        # 00:10.000 --> 00:15.000
        # /assets/preview3.jpg#xywh=0,90,160,180
        #
        # 00:15.000 --> 00:20.000
        # /assets/preview4.jpg#xywh=160,90,320,180
        # ==== END SAMPLE ========
        base_file = os.path.basename(sprite_file)
        vtt = ["WEBVTT", ""]  # line buffer for file contents
        if self.skip_first:
            clip_start = self.thumb_rate_seconds  # offset time to skip the first image
        else:
            clip_start = 0
        # NOTE - putting a time gap between thumbnail end & next start has no visual effect in Player, so not doing it.
        clip_end = clip_start + self.thumb_rate_seconds
        adjust = self.thumb_rate_seconds * self.time_sync_adjust
        for img_num in range(1, num_segments + 1):
            xy_wh = self.get_grid_coordinates(img_num, grid_size, w, h)
            start = self.get_time_str(clip_start, adjust=adjust)
            end = self.get_time_str(clip_end, adjust=adjust)
            clip_start = clip_end
            clip_end += self.thumb_rate_seconds
            vtt.append("%s --> %s" % (start, end))  # 00:00.000 --> 00:05.000
            vtt.append("%s#xywh=%s" % (base_file, xy_wh))
            vtt.append("")  # Linebreak
        vtt = "\n".join(vtt)
        # output to file
        self.write_vtt(writefile, vtt)

    def run(self):
        try:
            self.make_out_dir()
            sprite_file = self.get_temporary_sprite_file()
            vtt_file = self.get_temporary_vtt_file()

            # create snapshots
            num_files, thumb_files = self.take_snapshot(self.get_video_file())
            # resize them to be mini
            self.resize(thumb_files)

            # get coordinates from a resized file to use in spritemapping
            grid_size = int(math.ceil(math.sqrt(num_files)))
            coords = self.get_geometry(
                thumb_files[0]
            )  # use the first file (since they are all same size) to get geometry settings

            # convert small files into a single sprite grid
            self.make_sprite(sprite_file, coords, grid_size)

            # generate a vtt with coordinates to each image in sprite
            self.make_vtt(sprite_file, num_files, coords, grid_size, vtt_file)

            # move generated file to out put path
            self.move()
        finally:
            # clean
            self.clean()

    def clean(self):
        try:
            shutil.rmtree(self.get_out_dir())
        except OSError:
            logger.exception("remove tree failed")

    def move(self):
        shutil.move(self.get_temporary_sprite_file(), self.get_sprite_file())
        shutil.move(self.get_temporary_vtt_file(), self.get_vtt_file())
