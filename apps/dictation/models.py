"""Models."""

import re
import base64
import math
import requests
import yt_dlp
import datetime as dt
import logging

from yt_dlp.utils import DownloadError
from pathlib import Path
from typing import Any
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.sites.models import Site

from django.db.models import F, ExpressionWrapper, FloatField, IntegerField, Avg
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast
from django.db import models
from django.utils.safestring import mark_safe

from config import settings
from .utils import HandleCleaner

logger = logging.getLogger(__name__)


class Dictation(models.Model):
    """Dictation model."""

    video_id = models.CharField(null=True, blank=True, max_length=50)
    change_date = models.DateTimeField(auto_now=True)
    filename = models.CharField(null=True, blank=True, max_length=200, unique=True)
    timestamps = models.JSONField()
    topic = models.CharField(max_length=200)
    level = models.IntegerField()
    tip = models.JSONField()
    slug = models.SlugField(default="", null=False, max_length=100)
    total_line = models.IntegerField(default=0)
    in_production = models.BooleanField(default=False)
    site = models.ForeignKey(Site, default=1, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return the string representation of the dictation."""
        return self.topic

    @property
    def get_html_url(self):
        """Return the html url."""
        return reverse("dictation:topic", args=(self.slug,))

    def get_absolute_url(self) -> str:
        """Return the absolute URL of the dictation."""
        return f"/topic/{self.slug}"

    def slugify_title(self, video_title: str) -> str:
        """Return the slugified title."""
        video_title = re.sub(r"\W", " ", video_title)
        return "-".join(video_title.split()).lower()

    def generate_text(self, cleaned_text: list) -> list:
        """Generate the text."""
        text = []
        for line in cleaned_text:
            if line.strip():
                text += (
                    [line[:-1]]
                    if line.endswith("\u2014") or line.endswith("-")
                    else [line]
                )
        return text

    def create_dictation_data(self, **kwargs: dict) -> Any:
        """Create the dictation data."""
        video_id = kwargs["video_id"]
        filename = Path(kwargs["filename"])
        filepath = self.get_vtt_file(video_id)
        self.get_text(filepath)
        timestamps = self.get_timestamps(filepath)

        if not Dictation.objects.filter(filename=f"{filename}.en.txt").exists():

            autodictation = Dictation.objects.get_or_create(
                video_id=kwargs["video_id"],
                topic=kwargs["video_title"],
                filename=f"{filename}.{kwargs.get("sub_version")}.txt",
                level=3,
                slug=kwargs["slug"],
                timestamps={"data": timestamps},
                tip=[{"": ""}],
            )
        else:
            autodictation = [Dictation.objects.get(filename=f"{filename}.en.txt")]

        self.update_total_line()
        return autodictation

    def get_data(self, video_id: str) -> dict:
        """Get the data of the video."""

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Set options to only extract info
        ydl_opts = {
            "extract_flat": True,
            "skip_download": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
        except DownloadError as e:
            logging.error(f"Download error: {e}")
            return {}  # {"error": "DownloadError", "message": e}
        except Exception as e:
            logging.error(f"Unexpected errror: {e}")
            return {"error": "DownloadError", "message": e}

        video_title = info_dict.get("title", "video")
        filename = re.sub(r"\W", " ", video_title)
        slugified_title = "-".join(filename.split()).lower()
        video_id = info_dict.get("id", "unknown")

        filename = f"{settings.TXT_DIR}/{slugified_title}"
        duration = info_dict.get("duration_string")
        if duration:
            duration = duration.replace(":", ".")
            duration = float(duration)
        year = info_dict.get("upload_date")[:4]
        subtitles = info_dict.get("subtitles", [])
        if len(subtitles) > 0:
            sub_version = [lng for lng in subtitles.keys() if "en" in lng][0]
            sub_version = (
                sub_version[:3] + "US"
                if len(sub_version) > 2 and sub_version[3:] not in ["US", "GB"]
                else sub_version
            )
        else:
            sub_version = []

        return {
            "video_title": video_title,
            "filename": slugified_title,
            "video_id": video_id,
            "slug": slugified_title,
            "last_between_1_and_6_minutes": 1 < duration < 7,
            "is_subtitle_in_right_format": info_dict["language"]
            in ["en", "en-GB", "en-US"],
            "released_after_2020": year > "2020",
            "has_subtitles": len(subtitles) > 0,
            "sub_version": sub_version,
        }

    def get_text(self, filepath: Path) -> str:
        """Get the text of the video."""
        timestamps = r"^\d(.*)\d$"
        text = ""

        try:
            with open(f"{settings.TXT_DIR / filepath}", "r", encoding="utf-8") as f:
                lines = f.readlines()

            lines = [
                line
                for line in lines
                if not re.match(r"^(WEBVTT|Kind:|Language:)", line)
            ]
            lines = [line for line in lines if not re.match(timestamps, line)]
            cleaner = HandleCleaner()
            lines = cleaner.clean(lines)
            text = "".join(self.concatenate_lines(lines))
        except FileNotFoundError:
            logging.error(f"The file {settings.TXT_DIR / filepath} was not found.")
            print(f"The file {settings.TXT_DIR / filepath} was not found.")
        except OSError as e:
            logging.error(f"An error occured: {e}")

        output_path = settings.TXT_DIR / f"{filepath.stem}.txt"
        try:
            with open(output_path, "w", encoding="utf-8") as outfile:
                outfile.write(text)
        except OSError as e:
            logging.error(f"Error while writing the file {output_path}: {e}")

        self.remove_blank_lines(output_path)
        return text

    def get_timestamps(self, filepath: Path) -> list:
        """Get the timestamps of the video."""
        non_digits = r"^\d{2}:\d{2}:\d{2}\.\d{3}.*"
        timestamps = []

        try:
            with open(f"{settings.TXT_DIR / filepath}", "r", encoding="utf-8") as f:
                lines = f.readlines()

                pair_timestamps = [
                    line.replace("\n", "").split(" --> ")
                    for line in lines
                    if re.match(non_digits, line)
                ]
                timestamps = [
                    timestamp for pair in pair_timestamps for timestamp in pair
                ]
                timestamps = [self.dt_to_seconds(timestamp) for timestamp in timestamps]
                timestamps = self.resync(timestamps)
        except FileNotFoundError:
            logging.error(f"The file {filepath} was not found.")
        except OSError as e:
            logging.error(f"An error occured: {e}")

        return timestamps

    def download_vtt(self, video_id: str, custom_filename: str) -> str:
        """Download the vtt file of the video."""
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            "writesubtitles": True,
            "subtitleslangs": ["en", "en-GB", "en-US"],
            "skip_download": True,
            "subtitlesformat": "vtt",
            "outtmpl": f"{settings.TXT_DIR / custom_filename}",
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except DownloadError as e:
            logging.error(f"Download failed: {str(e)}")

        return custom_filename

    def check_vtt(self, filename, info):
        try:
            with open(
                f"{settings.TXT_DIR / filename}.{info.get("sub_version")}.vtt",
                "r",
                encoding="utf-8",
            ) as f:
                lines = f.readlines()
                length_lines = len(lines)

        except FileNotFoundError:
            logging.error("File not found!")

            return ""
        if length_lines > 500:
            Path.unlink(
                f"{settings.TXT_DIR / filename}.{info.get("sub_version")}.vtt",
                missing_ok=True,
            )
            return ""
        return filename

    def get_vtt_file(self, video_id: str) -> Path:
        """Get the vtt file of the video."""
        data = self.get_data(video_id)
        filename = data["filename"]
        vtt_file = self.download_vtt(video_id, filename)
        return Path(f"{vtt_file}.{data.get("sub_version")}.vtt")

    def remove_blank_lines(self, file: Path) -> None:
        """Remove blank lines.

        Used to remove the two last blank lines from the
        generated .txt after cleaning.
        """
        file = Path(file)
        lines = file.read_text().splitlines()
        filtered = [line for line in lines if line.strip()]
        file.write_text("\n".join(filtered))

    def dt_to_seconds(self, timestamp: str) -> float:
        """Convert a timestamp in the format HH:MM:SS.mmm to seconds."""
        t = dt.datetime.strptime(timestamp, "%H:%M:%S.%f")
        total_seconds = t.minute * 60 + t.second + t.microsecond / 1_000_000
        return total_seconds

    def concatenate_lines(self, lines: list) -> str:
        """Concatenate the lines of the .txt file generated after cleaning."""
        result = []
        for line in lines:
            if line == "\n":
                result.append(line)
            else:
                result.append(line.replace("\n", " ").strip() + " ")
        concatenated = "".join(result).strip()
        return concatenated

    def resync(self, ts: list) -> list:
        """Resync the timestamps."""
        ts = [ts[0]] + [ts[i] for i in range(len(ts)) if i % 2 == 1]
        return [round(ts[0], 2)] + [round(ts[i] - 0.2, 2) for i in range(1, len(ts))]

    def update_total_line(self) -> None:
        """Update the total_line field."""
        dictation = Dictation()
        filenames = [dictation.filename for dictation in Dictation.objects.all()]
        for filename in filenames:
            Dictation.objects.filter(filename=filename).update(
                total_line=dictation.total_lines(filename)
            )

    def total_lines(self, filename: str = None) -> int:
        """Return the total number of lines."""
        filename = filename if filename else self.filename
        filepath = settings.TXT_DIR / filename
        total = 0
        with open(filepath, encoding="utf-8") as f:
            total = len(f.readlines()) - 1
        return total

    def read_segment(self, filename: str, index: int, max_lines: int) -> str:
        """Return the line at the given index."""
        line = ""
        filepath = settings.TXT_DIR / filename
        with open(filepath, encoding="utf-8") as f:
            if index - 1 <= max_lines:
                line += f.readlines()[index - 1]
        return line.rstrip("\n")

    def get_video_title(self, video_id: str) -> Any:
        """Get the original video title from YouTube."""
        dictation = Dictation.objects.get(video_id=video_id)
        return dictation.topic

    def get_filename(self, slug: str) -> Any:
        """Return the filename of the current dictation from the given slug."""
        dictation = Dictation.objects.filter(slug=slug).first()
        return dictation.filename

    def get_duration(self, dictation) -> int:
        """Return the duration (mn) of the given dictation."""
        first = dictation.timestamps["data"][0]
        last = dictation.timestamps["data"][-1]
        return round(last / 60 - first / 60)

    def thumbail_to_b64(self, video_id: str) -> str:
        """Return base64 image decoded."""
        img_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
        response = requests.get(img_url, timeout=3)
        b64 = base64.b64encode(response.content)
        return b64.decode("utf-8")


def lines_default() -> dict:
    """Allow the default state of the field."""
    return {"data": []}


class Practice(models.Model):
    """Practice model."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dictation = models.ForeignKey(Dictation, on_delete=models.CASCADE)
    user_current_line = models.IntegerField(null=True, blank=True)
    lines = models.JSONField(null=True, blank=True, default=lines_default)
    user_rating = models.CharField(null=True, blank=True, max_length=1)
    is_done = models.BooleanField("is_dictation_done", default=False)

    def __str__(self):
        """Return str representation."""
        return f"{self.dictation_id}"

    def average_rating(self) -> dict:
        """Calculate the average rating."""
        ratings = {}
        queryset = (
            Practice.objects.values("dictation_id")
            .annotate(user_rating_int=Cast("user_rating", IntegerField()))
            .annotate(average=Avg("user_rating_int"))
        )
        for entry in queryset:
            pk = entry["dictation_id"]
            avg_rating = entry["average"]
            if avg_rating:
                ratings[f"dictation_{pk}"] = math.floor(avg_rating)
        return ratings

    def update_dictation_rating(self, ratings: dict) -> int:
        """Update the rating of each dictation."""
        for dictation, rating in ratings.items():
            level = Dictation.objects.filter(pk=dictation[10:]).update(level=rating)
        return level

    def create_dictation(self, user, dictation) -> None:
        """Initiate a new instance between a dictation and the user."""
        if not Practice.objects.filter(user=user, dictation=dictation).exists():
            Practice.objects.create(user=user, dictation=dictation)

    def delete_practice(self, user, dictation):
        """Delete practice."""
        if Practice.objects.filter(user=user, dictation=dictation).exists():
            practice = Practice.objects.filter(user=user, dictation=dictation).update(
                lines=lines_default(), user_current_line=0, is_done=False
            )
            return practice

    def save_dication_progress(self, user, dictation_id, current_line):
        """Save the number of the last line where the user stopped."""
        if Practice.objects.filter(user=user, dictation=dictation_id).exists():
            Practice.objects.filter(user=user, dictation=dictation_id).update(
                user_current_line=current_line
            )

    # def update_answered_lines(self, practice, line_nb, new_page) -> list:
    #     """Update the list of good answers."""
    #     if line_nb - 1 not in practice.lines["data"] and new_page:
    #         practice.lines["data"].append(line_nb - 1)
    #         practice.save()
    #     if line_nb not in practice.lines["data"] and not new_page:
    #         practice.lines["data"].append(line_nb)
    #         practice.save()
    #     return practice.lines["data"]

    def update_answered_lines(self, line_nb, new_page) -> list:
        """Update the list of good answers."""
        if line_nb - 1 not in self.lines["data"] and new_page:
            self.lines["data"].append(line_nb - 1)
            self.save()
        if line_nb not in self.lines["data"] and not new_page:
            self.lines["data"].append(line_nb)
            self.save()
        return self.lines["data"]

    def update_is_done(self, user, dictation_id):
        """Update the boolean is_done."""
        practice = (
            Practice.objects.filter(user=user, dictation_id=dictation_id)
            .select_related("dictation")
            .first()
        )
        total_line = practice.dictation.total_line
        if len(practice.lines["data"]) == total_line:
            Practice.objects.filter(user=user, dictation_id=dictation_id).update(
                is_done=True
            )

    def saved_position(self, user, dictation_id) -> int:
        """Return the last number of line in order to initiate the video at that point."""
        practice = Practice.objects.filter(user=user, dictation=dictation_id).first()
        return practice.user_current_line if practice.user_current_line else 0

    def get_lines(self, user, dictation):
        """Return the lines list."""
        return (
            Practice.objects.filter(user=user, dictation=dictation)
            .first()
            .lines["data"]
        )

    def get_rating(self, user, dictation_id):
        """Get the Practice instance."""
        return Practice.objects.filter(user=user, dictation_id=dictation_id).first()

    def update_rating(self, user, dictation_id, new_rating):
        """Update the rating number given by the click on the star."""
        Practice.objects.filter(user=user, dictation=dictation_id).update(
            user_rating=new_rating
        )

    def get_progress(self, user):
        """Get the average progress of the user in the dictation.

        Calculates the 'average progress' for each dictation in progress,
        using two distinct values from two related models: the length of the
        lines["data"] (which is the list of committed lines updated in real time)
        divided by the total number of lines for a dictation.

        Args:
            user: The current user.

        Returns:
            A QuerySet containing the annotated practice instances ordered by
            average progress.
        """
        progress = (
            Practice.objects.filter(user=user)
            .annotate(
                # -> operator to extract a value of a JSON object by a key
                # jsonb_array_length(lines -> 'data') is the equivalent of
                # len(lines["data"]) in Python.
                data_length=RawSQL("jsonb_array_length(lines -> 'data')", []),
                total_line=Cast(F("dictation__total_line"), FloatField()),
                average_progress=ExpressionWrapper(
                    F("data_length") / F("total_line"), output_field=IntegerField()
                ),
            )
            .order_by("-average_progress")
        )
        return progress


def convert_segment_to_b64(reference: str) -> str:
    """Convert a sentence to a b64 in order to hide the original in the local storage.

    Args:
        reference (str): The sentence to be converted to base64.
    """
    token = "{token}".format(token=reference).encode("utf-8")
    token = base64.b64encode(token)
    return str(token, encoding="utf-8")


def get_line_number_key(request, line_number):
    """Return a boolean if weither or not the line_number key exists."""
    if request.session.get("line_numbers") and request.session.get("line_numbers")[-1]:
        return request.session["line_numbers"][-1] != line_number
    return False


def re_init_session_data(line_number: int, request) -> Any:
    """Empty the lists when the line number change."""
    if get_line_number_key(request, line_number):
        if not request.user.is_authenticated:
            # a global version for offline users
            request.session["indexes"] = []
        request.session["current_dictation"] = [-1]
        request.session["line_numbers"] = [-1]
    return request.session["current_dictation"]


def free_initiate_new_session(request: HttpRequest) -> Any:
    """Create the first list to receive json structure for non connected users."""
    if "historic" not in request.session:
        request.session["historic"] = {"revealed_line": []}
    return request.session


def free_create_first_session_page(
    request: HttpRequest, dictation_id: int, line_nb: int = 0
):
    """Create the first session json structure for non connected users."""
    historic_for_current_line = [
        item
        for item in request.session["historic"]["revealed_line"]
        if item["dict ID"] == dictation_id and item["line"] == line_nb
    ]
    if not historic_for_current_line:
        request.session["historic"]["revealed_line"].append(
            {
                "dict ID": dictation_id,
                "line": line_nb,
                "attempts": 0,
                "indexes": [],
                "help_used": False,
                "user_segment": "",
            }
        )

    return request.session


def initiate_new_session_in_view(
    request: HttpRequest, dictation_id: int, lines: list, line_nb: int
):
    """Initiate a json structure to keep the historic of validation."""
    if "historic" not in request.session:
        request.session["historic"] = {"revealed_line": []}
        create_first_session_page(request, dictation_id, line_nb, 0)
    else:
        if any(
            item["dict ID"] == dictation_id
            for item in request.session["historic"]["revealed_line"]
        ):
            # if a dictionary entry in historic persists while the line is in the database,
            # we need to delete it (at the load of the page).
            for line in lines:
                for x, session_historic in enumerate(
                    request.session["historic"]["revealed_line"]
                ):
                    if session_historic["line"] == line:
                        del request.session["historic"]["revealed_line"][x]

        chk_line = lines[-1] if len(lines) > 0 else line_nb

        if not any(
            item["dict ID"] == dictation_id and item["line"] == chk_line
            for item in request.session["historic"]["revealed_line"]
        ):
            request.session["new_pages"] = list()
            request.session["current_dictation"] = [dictation_id]
            request.session["indexes"] = list()
            request.session["line_numbers"] = [-1]
            create_first_session_page(request, dictation_id, line_nb, attempts=0)


def delete_session_historic_in_view(
    request: HttpRequest, dictation_id: int, lines: list
):
    """Delete the entry for a specific page."""
    if any(
        item["dict ID"] == dictation_id
        for item in request.session["historic"]["revealed_line"]
    ):
        for x, session_historic in enumerate(
            request.session["historic"]["revealed_line"]
        ):
            if session_historic["line"] == lines[-1]:
                del request.session["historic"]["revealed_line"][x]
                request.session.modified = True


def update_current_dictation(dictation_id, request_session):
    """Update the current dictation."""
    request_session["current_dictation"][0] = dictation_id


def create_first_session_page(
    request: HttpRequest, dictation_id: int, line_number: int, attempts: int
):
    """Append the first entry to the session."""

    historic_for_current_line = [
        item
        for item in request.session["historic"]["revealed_line"]
        if item["dict ID"] == dictation_id and item["line"] == line_number
    ]
    if not historic_for_current_line:
        request.session["historic"]["revealed_line"].append(
            {
                "dict ID": dictation_id,
                "line": line_number,
                "attempts": attempts,
                "indexes": [],
                "help_used": False,
            }
        )
    return request.session


def append_indexes(
    request: HttpRequest, dictation_id: int, line_number: int, index: int
):
    """Append the index to the indexes list.

    This list is used to keep track of the number of attempts.
    """
    for x, item in enumerate(request.session["historic"]["revealed_line"]):
        if (
            item["dict ID"] == dictation_id
            and item["line"] == line_number
            and item["attempts"] < 3
            and index not in item["indexes"]
        ):
            item["indexes"].append(index)
    request.session.modified = True
    return request.session["historic"]["revealed_line"]


def save_user_segment_per_page_in_view(
    request: HttpRequest, dictation_id: int, line_number: int, user_segment: str
):
    """Save the part of segment entered in the textarea before leaving it incomplete.

    In order to give back the help used before for a dedicated segment.
    """
    for item in request.session["historic"]["revealed_line"]:
        if item["dict ID"] == dictation_id and item["line"] == line_number:
            item["user_segment"] = user_segment
    request.session.modified = True
    return request.session["historic"]["revealed_line"]


def display_user_segment_per_page(
    request: HttpRequest, dictation_id: int, line_number: int
):
    """Return the part of segment saved before leaving the line without validation."""
    user_segment = ""
    for item in request.session["historic"]["revealed_line"]:
        if item["dict ID"] == dictation_id and item["line"] == line_number:
            user_segment = item["user_segment"]
    return user_segment


def get_attempts_per_page(
    request: HttpRequest, dictation_id: int, line_number: int
) -> int:
    """Return the number of attempts for a specific page."""
    len_indexes = 0
    for item in request.session["historic"]["revealed_line"]:
        if item["dict ID"] == dictation_id and item["line"] == line_number:
            len_indexes = len(item["indexes"])
            item["attempts"] = len(item["indexes"])
    request.session.modified = True
    return len_indexes


def update_session_page_validated(
    request: HttpRequest, dictation_id: int, line_number: int, attempts: int = 0
):
    """Update the number of attempts for a specific page already validated."""
    if any(
        item["dict ID"] == dictation_id
        for item in request.session["historic"]["revealed_line"]
    ):
        for item in request.session["historic"]["revealed_line"]:
            if (
                item["line"] == line_number
                and item["attempts"] < 3
                and not item["help_used"]
            ):
                item.update(
                    {
                        "dict ID": dictation_id,
                        "line": line_number,
                        "attempts": attempts,
                        "indexes": [i for i in range(attempts)],
                        "help_used": True if attempts == 3 else False,
                    }
                )
            elif not any(
                item["dict ID"] == dictation_id and item["line"] == line_number
                for item in request.session["historic"]["revealed_line"]
            ):
                request.session["historic"]["revealed_line"].append(
                    {
                        "dict ID": dictation_id,
                        "line": line_number,
                        "attempts": attempts,
                        "indexes": [],
                        "help_used": False,
                    }
                )
    else:
        create_first_session_page(request, dictation_id, line_number, attempts)


def check_help_used(request: HttpRequest, dictation_id: int, line_number: int) -> bool:
    """Return a boolean if the help was used for a specific page."""
    used = False
    if any(
        session_historic["dict ID"] == dictation_id
        for session_historic in request.session["historic"]["revealed_line"]
    ):
        for session_historic in request.session["historic"]["revealed_line"]:
            if (
                session_historic["line"] == line_number
                and session_historic["help_used"]
            ):
                used = True
    return used


def reveal_first_wrong_letter(
    segment: str,
    original_segment: str,
    line_number: int,
    reveal_status: bool,
    new_page: bool,
    dictation_id: int,
    request: HttpRequest,
) -> tuple[str, int]:
    """Return the wrong segment with the first wrong letter replaced by the correct one.

    The rest is potentially finished with stars.
    31 = len("<span class='spelling'>* or [a-z]</span>")
    """
    if new_page:
        request.session["new_pages"].append(0)
        if request.user.is_authenticated:
            create_first_session_page(request, dictation_id, line_number, attempts=0)
        else:
            free_create_first_session_page(request, dictation_id, line_number)

    spelling = "<span class='spelling'>"
    star = "*"

    original_segment = remove_punctuation(original_segment)
    original_segment = " ".join(original_segment)
    if spelling in segment or star in segment:
        if spelling in segment:
            index = segment.index(spelling)
        elif star in segment:
            index = segment.index(star)

        if request.user.is_authenticated:
            if line_number > max(set(request.session["line_numbers"])):
                if line_number not in request.session["line_numbers"]:
                    request.session["line_numbers"].append(line_number)
                    request.session.modified = True

        if request.user.is_authenticated:
            if not check_help_used(request, dictation_id, line_number):
                revealed_segment = (
                    segment.replace(
                        segment[index : 31 + index], original_segment[index], 1
                    )
                    if get_attempts_per_page(request, dictation_id, line_number) < 3
                    and reveal_status
                    else segment
                )
            else:
                revealed_segment = segment

            if not check_help_used(request, dictation_id, line_number):
                if get_attempts_per_page(request, dictation_id, line_number) < 3:
                    append_indexes(request, dictation_id, line_number, index)
        else:
            # non connected user
            revealed_segment = (
                segment.replace(segment[index : 31 + index], original_segment[index], 1)
                if get_attempts_per_page(request, dictation_id, line_number) < 3
                and reveal_status
                else segment
            )
            if get_attempts_per_page(request, dictation_id, line_number) < 3:
                append_indexes(request, dictation_id, line_number, index)
    else:
        revealed_segment = segment

    attempts = get_attempts_per_page(request, dictation_id, line_number)
    request.session["new_pages"] = [0]

    if request.user.is_authenticated:
        update_session_page_validated(request, dictation_id, line_number, attempts)

    return revealed_segment, attempts


def correction(
    original_segment: str,
    new_segment: str,
    dictation_id: int,
    line_number: int,
    request: HttpRequest,
) -> tuple[str, bool, int]:
    """Return the corrected segment.

    the full segment if it is the same as the original.
    In case of errors, the words are replaced by stars from
    the first error until the end of the segment.
    """

    if dictation_id != request.session["current_dictation"][0]:
        update_current_dictation(dictation_id, request.session)
        re_init_session_data(line_number, request)

    new_segment = remove_punctuation(new_segment)
    original_segment = remove_punctuation(original_segment)

    len_original_segment, len_new_segment = len(original_segment), len(new_segment)
    if len_new_segment < len_original_segment:
        new_segment += [""] * (len_original_segment - len_new_segment)
    if len_new_segment > len_original_segment:
        new_segment = new_segment[:len_original_segment]
    tmp: list = []
    corrected = []
    for index in range(len_original_segment):
        if original_segment[index] != new_segment[index]:
            correct_word = corrected_word(original_segment[index], new_segment[index])
            tmp.insert(index, correct_word)
        else:
            tmp.insert(index, new_segment[index])
    for index in range(len_original_segment):
        if "</span>" in tmp[index]:
            corrected = tmp[: index + 1]
            break
        corrected = tmp

    if corrected and len(corrected) < len_original_segment:
        for _ in range(len_original_segment - len(corrected)):
            corrected.append("*" * len(original_segment[len(corrected)]))

    len_indexes = get_attempts_per_page(request, dictation_id, line_number)

    return (
        " ".join(corrected),
        corrected == original_segment,
        len_indexes,
    )


def corrected_word(reference_word: str, new_word: str) -> str:
    """Return the corrected word.

    The correct word,
    or the word as is and underlined on the incorrect letters (in red).
    If the word is entirely wrong it is replaced by stars and underlined (in red).
    """
    correct_word = ""
    if len(new_word) > len(reference_word):
        reference_word += "_" * (len(new_word) - len(reference_word))
        new_word = new_word[: len(reference_word)]
    for index, letter in enumerate(new_word):
        if letter == reference_word[index]:
            correct_word += letter
        else:
            letter = f"<span class='spelling'>{letter}</span>"
            correct_word += mark_safe(letter)
    if len(correct_word) < len(reference_word):
        last_underscore = len(reference_word) - len(correct_word)
        star = "<span class='spelling'>*</span>"
        correct_word += mark_safe(star) * last_underscore
    return correct_word


def sanitize_longer(segment) -> str:
    """Return a string of maximum 26 chars."""
    segment = segment.split()
    for k, v in enumerate(segment):
        if len(v) > 26:
            segment[k] = v[:26]
    return " ".join(segment)


def remove_punctuation(segment: str) -> list:
    """Remove ponctuation specified in list.

    Allow the users to avoid typing these (and limit the amount of mistakes).
    """
    segment = sanitize_longer(segment)
    segment = re.sub(r"\-(?=\w)|(?<=\w)\-", " ", segment)
    segment = segment.replace(" - ", " ")
    segment = "".join([i for i in segment if i not in settings.PONCTUATION])
    segment = re.sub(r"(?<!\d)[^\w\s']|(?<!\d)\.(?!\d)|\.$", "", segment)
    return segment.strip().split()


class WiktionaryAPI:
    """Wiktionary API."""

    def __init__(self):
        """Init."""
        self.url = "https://en.wiktionary.org/api/rest_v1/page/definition/"
        self.headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Markus Möller's super cool bot",
        }

    def extract_data(self, word) -> str:
        """Extract data from dict and return str."""
        try:
            word = word.lower()
            req = requests.get(self.url + word, headers=self.headers, timeout=15)
            data = req.json()
            return data

        except requests.exceptions.RequestException as error:
            raise error

    def rm_html(self, value):
        """Remove HTML tags."""
        if isinstance(value, list):
            return None
        return re.sub(r"<.*?>", "", value)

    def reduce_json(self, jsonfile):
        """Keep only the keys wanted."""
        reduced_json = {
            "Noun": {},
            "Verb": {},
            "Adjective": {},
            "Determiner": {},
            "Pronoun": {},
            "Adverb": {},
            "Interjection": {},
            "Preposition": {},
            "Conjunction": {},
        }
        fields = [
            "Noun",
            "Verb",
            "Adjective",
            "Determiner",
            "Pronoun",
            "Adverb",
            "Interjection",
            "Preposition",
            "Conjunction",
        ]

        for data in jsonfile["en"]:
            if data["partOfSpeech"] in fields:
                count = 1
                for field in data["definitions"]:
                    if field["definition"]:
                        reduced_json[data["partOfSpeech"]].update(
                            {count: self.rm_html(field["definition"])}
                        )
                        count += 1
        return reduced_json
