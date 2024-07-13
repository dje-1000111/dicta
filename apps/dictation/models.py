"""Models."""

import re
import base64
import math
import requests
import json

from typing import Any
from django.http import HttpRequest
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranslationLanguageNotAvailable,
    TranscriptsDisabled,
)

from django.db import models
from django.utils.safestring import mark_safe
from config import settings


class Dictation(models.Model):
    """Dictation model.

    New field: language
    Goal: display a table who list all video by language.
    Idea: I can make a container with 2 tabs, the English default tab
        and the French tab.
    """

    video_id = models.CharField(null=True, blank=True, max_length=50)
    # language = models.CharField(null=True, blank=True, max_length=50)
    # to sort a videos by topic, we need a new field like "genre"
    # for short story, climate, history, biopic, reportage, science, etc...
    # On the page there would be a button

    change_date = models.DateTimeField(auto_now=True)
    filename = models.CharField(null=True, blank=True, max_length=200, unique=True)
    timestamps = models.JSONField()
    topic = models.CharField(max_length=200)
    level = models.IntegerField()
    tip = models.JSONField()
    slug = models.SlugField(default="", null=False, max_length=100)
    total_line = models.IntegerField(default=0)
    in_production = models.BooleanField(default=False)

    def __str__(self):
        return self.topic

    def get_absolute_url(self):
        return f"/topic/{self.slug}"

    def get_video_data(self, video_id: str) -> Any:
        """Get the original video title from YouTube."""
        payload = {
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "format": "json",
        }
        try:
            r = requests.get("https://www.youtube.com/oembed", payload, timeout=3)
        except requests.exceptions.RequestException:
            print("Something went wrong")
        return r.json()

    def yt_get_transcript(
        self, video_id: str, languages: list = ["en", "English", "en-GB", "en-US"]
    ) -> Any:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        res = transcript_list.find_manually_created_transcript(languages)
        return YouTubeTranscriptApi.get_transcript(
            video_id, languages=(res.language_code,)
        )

    def sluggify_title(self, video_title: str) -> str:
        video_title = re.sub(r"\W", " ", video_title)
        return "-".join(video_title.split()).lower()

    def create_timestamps(self, yt_transcript) -> list:
        timestamps = []
        for line in yt_transcript:
            timestamps += [round(line["start"], 2)]
        timestamps += [timestamps[-1] + 5]
        return timestamps

    def clean_text(self, yt_transcript) -> list:
        reg = r"(\(.*\))|(\[.*\])"
        cleaned_text = []
        for line in yt_transcript:
            line["text"] = re.sub(reg, "", line["text"])
            cleaned_text += [
                line["text"]
                .replace("\ufeff", "")
                .replace("\n", " ")
                .replace("—", ", ")
                .replace("\xa0", "")
                .replace("\u2013", "-")
                .replace("’", "'")
                .replace("‘", "'")
                .replace("“", '"')
                .replace("”", '"')
                .replace("…", "...")
                .strip("-")
                .strip()
            ]

        return cleaned_text

    def generate_text(self, cleaned_text):
        text = []
        for line in cleaned_text:
            if line.strip():
                text += (
                    [line[:-1]]
                    if line.endswith("\u2014") or line.endswith("-")
                    else [line]
                )
        return text

    def is_transcriptable(self, video_id):
        transcriptable = True
        try:
            self.yt_get_transcript(video_id)
        except TranscriptsDisabled:
            transcriptable = False
        except NoTranscriptFound:
            transcriptable = False
        except TranslationLanguageNotAvailable:
            transcriptable = False
        return transcriptable

    def is_manually_transcripted(self, video_id):
        manually = True
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            print("transcript list", transcript_list)
            transcript_list.find_manually_created_transcript(
                ["en", "English", "en-GB", "en-US"]
            )
        except TranscriptsDisabled:
            manually = False
        except NoTranscriptFound:
            manually = False
        except TranslationLanguageNotAvailable:
            manually = False
        return manually

    def get_current_language(self, video_id):

        if self.is_manually_transcripted(video_id) == 0:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            langs = transcript_list.find_manually_created_transcript(
                ["en", "English", "en-GB", "en-US"]
            )
        return (
            langs.language_code
            if self.is_manually_transcripted(video_id) == 0
            else "en"
        )

    def create_dictation_data(self, video_id, yttrans):
        data = self.get_video_data(video_id)
        slug = self.sluggify_title(data["title"])
        yt_transcript = json.dumps(yttrans)
        yt_transcript = json.loads(yt_transcript)
        timestamps = self.create_timestamps(yt_transcript)
        cleaned_text = self.clean_text(yt_transcript)
        cleaned_text = self.generate_text(cleaned_text)

        if not Dictation.objects.filter(filename=f"{slug}.txt").exists():

            with open(settings.TXT_DIR / f"{slug}.txt", "w", encoding="utf-8") as f:
                for i in cleaned_text:
                    f.write(f"{i}\n")

            autodictation = Dictation.objects.get_or_create(
                video_id=video_id,
                topic=data["title"],
                filename=f"{slug}.txt",
                level=3,
                slug=slug,
                timestamps={"data": timestamps},
                tip={"": ""},
            )
        else:
            autodictation = [Dictation.objects.get(filename=f"{slug}.txt")]

        self.update_total_line()
        return autodictation

    def is_length_enough(self, video_id):
        yttrans = self.yt_get_transcript(video_id)
        yt_transcript = json.dumps(yttrans)
        yt_transcript = json.loads(yt_transcript)
        return 10 < len(yt_transcript) <= 200

    def update_total_line(self):
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
            # total = sum(1 for _ in f)
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
        payload = {
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "format": "json",
        }
        response = requests.get("https://www.youtube.com/oembed", payload, timeout=3)
        data = response.json()
        return data["title"]

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


def lines_default():
    """Allow the default state of the field."""
    return {"data": []}


class Practice(models.Model):
    """Practice model class.

    We can rate the level,
    find out if you have already done the exercise,
    and save your progress to resume at the same level next time.
    """

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
        dictation_ids = list(set([i["id"] for i in Dictation.objects.values("id")]))
        for pk in dictation_ids:
            queryset = Practice.objects.values("user_rating").filter(dictation_id=pk)
            queratings = [int(i["user_rating"]) for i in queryset if i["user_rating"]]

            if queratings and len(queratings) > 0:
                ratings.update(
                    {f"dictation_{pk}": math.floor(sum(queratings) / len(queratings))}
                )
        return ratings

    def update_dictation_rating(self, ratings: dict):
        """Update the rating of each dictation."""
        for dictation, rating in ratings.items():
            level = Dictation.objects.filter(pk=dictation[10:]).update(level=rating)
        return level

    def create_dictation(self, user, dictation):
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
        """Save the number of the last line wherre the user stopped."""
        if Practice.objects.filter(user=user, dictation=dictation_id).exists():
            Practice.objects.filter(user=user, dictation=dictation_id).update(
                user_current_line=current_line
            )

    def update_answered_lines(self, practice, line_nb, new_page):
        """Update the list of good answers."""
        if line_nb - 1 not in practice.lines["data"] and new_page:
            practice.lines["data"].append(line_nb - 1)
            practice.save()
        if line_nb not in practice.lines["data"] and not new_page:
            practice.lines["data"].append(line_nb)
            practice.save()
        return practice.lines["data"]

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

    def saved_position(self, user, dictation_id):
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


def convert_segment_to_b64(reference: str) -> str:
    """Convert a sentence to a b64 in order to hide the original in the local storage."""
    token = "{token}".format(token=reference).encode("utf-8")
    token = base64.b64encode(token)
    return str(token, encoding="utf-8")


def re_init_session_data(line_number: int, request) -> Any:
    """Empty the lists when the line number change."""

    if request.session["line_numbers"][-1] != line_number:
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
                for x, l in enumerate(request.session["historic"]["revealed_line"]):
                    if l["line"] == line:
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
        for x, l in enumerate(request.session["historic"]["revealed_line"]):
            if l["line"] == lines[-1]:
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
    """Append the index to the indexes list."""
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
    request, dictation_id, line_number, user_segment
):
    """Save the part of segment entered in the textarea before leaving it incomplete.

    In order to give back the help used before for a dedicated segment.
    """
    for item in request.session["historic"]["revealed_line"]:
        if item["dict ID"] == dictation_id and item["line"] == line_number:
            item["user_segment"] = user_segment
    request.session.modified = True
    return request.session["historic"]["revealed_line"]


def display_user_segment_per_page(request, dictation_id, line_number):
    """Return the part of segment saved before leaving the line without validation."""
    user_segment = ""
    for item in request.session["historic"]["revealed_line"]:
        if item["dict ID"] == dictation_id and item["line"] == line_number:
            user_segment = item["user_segment"]
    return user_segment


def get_attempts_per_page(
    request: HttpRequest, dictation_id: int, line_number: int
) -> int:
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
    used = False
    if any(
        l["dict ID"] == dictation_id
        for l in request.session["historic"]["revealed_line"]
    ):
        for x, l in enumerate(request.session["historic"]["revealed_line"]):
            if l["line"] == line_number and l["help_used"]:
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
            if line_number > max(set(request.session["line_numbers"])):  # why set() ???
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
                # TODO: Save (in session) the part of segment left in the textarea before leaving the page
                # so that we can display it in the textarea when we come back to it.
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
) -> tuple[str, str, bool, int]:
    """Return the corrected segment.

    The complete segment if is the same as the original.
    The first right part(s) eventually appened with stars of lenght
    of the missing words.
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

    The right word,
    or the word hilighted with an underscore if there is a few mistakes otherwise full
    of stars and underscored.
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
    return segment.strip().split()


class WiktionaryAPI:
    """Wiktionary API."""

    def __init__(self):
        """Init."""
        self.url = "https://en.wiktionary.org/api/rest_v1/page/definition/"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
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
