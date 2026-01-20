"""Views."""

import os
import json
import requests

from typing import Any, Dict

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http.response import JsonResponse
from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from apps.dictation.models import (
    correction,
    convert_segment_to_b64,
    reveal_first_wrong_letter,
    free_initiate_new_session,
    free_create_first_session_page,
    delete_session_historic_in_view,
    initiate_new_session_in_view,
    save_user_segment_per_page_in_view,
    Dictation,
    Practice,
    WiktionaryAPI,
)
from apps.dictation.forms import DictationForm, AutoDictationForm


def csrf_failure(request: HttpRequest, reason: str = "") -> HttpResponse:
    messages.warning(
        request,
        mark_safe(
            "Form validation failed. Please try again.<br>"
            "If you have configured your browser to disable cookies, please "
            "re-enable them, at least for this site, or for “same-origin” "
            "requests.",
        ),
    )
    return redirect(request.META.get("HTTP_REFERER", "/"))


def bad_request(request: HttpRequest, exception=None, template_name="400.html"):
    """Handle bad request."""
    return render(
        request,
        "pages/400.html",
        {"domain_name": os.getenv("DOMAIN_NAME")},
        status=400,
    )


def permission_denied(request: HttpRequest, exception=None, template_name="403.html"):
    """Handle permission denied."""
    return render(
        request,
        "pages/403.html",
        {"domain_name": os.getenv("DOMAIN_NAME")},
        status=403,
    )


def not_found(request: HttpRequest, exception=None, template_name="404.html"):
    """Handle not found."""
    return render(
        request,
        "pages/404.html",
        {"domain_name": os.getenv("DOMAIN_NAME")},
        status=404,
    )


def server_error(request: HttpRequest, exception=None, template_name="500.html"):
    """Handle server error."""
    return render(
        request,
        "pages/500.html",
        {"domain_name": os.getenv("DOMAIN_NAME")},
        status=500,
    )


def auto_dictation_form_view(request: HttpRequest) -> HttpResponse:
    """Handle auto dictation form view."""
    if request.method == "POST":
        form = AutoDictationForm(request.POST)
        if form.is_valid():
            video_id = form.cleaned_data["video_id"]
            dictation = Dictation()
            if dictation.is_transcriptable(video_id):
                yttrans = dictation.yt_get_transcript(video_id)
                if dictation.is_length_enough(video_id):
                    dictation.create_dictation_data(video_id, yttrans)
                    messages.success(
                        request,
                        mark_safe(
                            "The dictation has been created successfully.<br>"
                            "You can now use it in the dictation section."
                        ),
                    )
                else:
                    messages.info(
                        request,
                        mark_safe(
                            "The video is too short or too long to be used for dictation."
                        ),
                    )
            else:
                messages.info(
                    request,
                    mark_safe(
                        "The video is not transcriptable.<br>"
                        "Please choose another video."
                    ),
                )
        else:
            messages.info(
                request,
                mark_safe(
                    "The form is invalid.<br>"
                    "Please check the video ID and try again."
                ),
            )
    else:
        form = AutoDictationForm()

    return render(
        request,
        "pages/autodictation.html",
        {"addform": form, "domain_name": os.getenv("DOMAIN_NAME")},
    )


class HomeView(ListView):
    """Home view."""

    template_name: str = "pages/home.html"
    paginate_by: int = 8
    queryset = Dictation.objects.filter(in_production=True).order_by("level", "topic")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Get context data."""
        practice = Practice()
        is_auth = self.request.user.is_authenticated

        if is_auth:
            self.practice = Practice.objects.filter(
                user=self.request.user
            ).select_related("dictation")

        ratings = practice.average_rating()
        if ratings:
            practice.update_dictation_rating(ratings)
        context = super().get_context_data(**kwargs)
        # breakpoint()
        context.update(
            {
                "domain_name": os.getenv("DOMAIN_NAME"),
                "practice": self.practice if is_auth else None,
                "list_of_practices": (
                    [i.dictation_id for i in self.practice] if is_auth else None
                ),
            }
        )

        return context


class TopicView(DetailView):
    """Topic View."""

    template_name: str = "pages/topic.html"

    def get_object(self, queryset=None):
        """Get the dictation object."""
        practice = Practice()

        self.dictation = get_object_or_404(Dictation, slug=self.kwargs["slug"])
        self.real_lines = list(range(0, self.dictation.total_lines() + 1))
        if self.request.user.is_authenticated:
            practice.create_dictation(self.request.user, self.dictation)
            self.line_nb = practice.saved_position(self.request.user, self.dictation)
            self.note = practice.get_rating(
                user=self.request.user, dictation_id=self.dictation.pk
            )
            self.lines = practice.get_lines(self.request.user, self.dictation)
            self.lines = self.lines[1:] if -1 in self.lines else self.lines
            self.reds = [i for i in self.real_lines if i not in sorted(self.lines)]

        return self.dictation

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Get context data."""
        if self.request.user.is_authenticated:
            self.request.session["current_dictation"] = [self.dictation.pk]
            self.request.session["new_pages"] = []
            self.request.session["line_numbers"] = [-1]
            initiate_new_session_in_view(
                self.request, self.dictation.pk, self.lines, self.line_nb
            )
        else:
            free_initiate_new_session(self.request)
            free_create_first_session_page(self.request, self.dictation.pk)
            self.request.session["new_pages"] = []
            self.request.session["current_dictation"] = [self.dictation.pk]
            self.request.session.modified = True

        context = super().get_context_data(**kwargs)
        context.update(
            {
                "domain_name": os.getenv("DOMAIN_NAME"),
                "form": DictationForm(),
                "dictation_id": self.dictation.pk,
                "star_rating": (
                    self.note.user_rating
                    if self.request.user.is_authenticated
                    else None
                ),
                "line_nb": self.line_nb if self.request.user.is_authenticated else 0,
                "topic_name": self.kwargs["slug"],
                "b64_img": self.dictation.thumbail_to_b64(self.dictation.video_id),
                "vid_title": self.dictation.get_video_title(self.dictation.video_id),
                "total_lines": self.dictation.total_lines,
                "video_id": self.dictation.video_id,
                "timestamps": mark_safe(self.dictation.timestamps["data"]),
                "lines": (
                    sorted(self.lines) if self.request.user.is_authenticated else []
                ),
                "help": {str(v): k for d in self.dictation.tip for k, v in d.items()},
                "stars": ["5", "4", "3", "2", "1"],
                "topic_title": self.dictation.topic,
                "real_lines": self.real_lines,
                "lol": [
                    self.real_lines[i : i + 30]
                    for i in range(0, len(self.real_lines), 30)
                ],
                "reds": self.reds if self.request.user.is_authenticated else [],
                "result": "",
            }
        )
        return context


class AjaxDetailView(DetailView):
    """Ajax post text area content."""

    model = Dictation

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET request."""
        if "pk" not in kwargs and "slug" not in kwargs:
            raise Http404("Object not found")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """Handle POST request."""
        data = json.loads(request.body)
        (
            reset,
            line_nb,
            textarea_content,
            topicname,
            reveal_status,
            new_page,
            dictation_id,
            validated,
        ) = data.values()

        practice = Practice()

        if self.request.user.is_authenticated:
            dictation = Dictation.objects.filter(pk=dictation_id).first()
            filename = dictation.filename

            lines = practice.get_lines(request.user, dictation)

            if validated:
                delete_session_historic_in_view(request, dictation_id, lines)
                initiate_new_session_in_view(request, dictation_id, lines, line_nb)
            if reset:
                self.request.session["historic"]["revealed_line"] = []
                self.request.session.modified = True
                practice.delete_practice(self.request.user, dictation_id)
        else:
            dictation = Dictation()
            filename = dictation.get_filename(topicname)

        tot_lines = dictation.total_lines(filename)
        reference = dictation.read_segment(filename, line_nb + 1, tot_lines)
        corrected, state, attempts = correction(
            dictation.read_segment(filename, line_nb + 1, tot_lines),
            textarea_content,
            dictation_id,
            line_nb,
            request,
        )

        if reveal_status:
            corrected, attempts = reveal_first_wrong_letter(
                corrected,
                reference,
                line_nb,
                reveal_status,
                new_page,
                dictation_id,
                request,
            )

        if self.request.user.is_authenticated:
            practice = Practice.objects.get(
                user=self.request.user, dictation_id=dictation_id
            )

            if "*" not in corrected and "<" not in corrected:
                practice.update_answered_lines(practice, line_nb, new_page)

                Practice().save_dication_progress(
                    user=self.request.user,
                    dictation_id=dictation_id,
                    current_line=line_nb,
                )

                practice.update_is_done(
                    user=self.request.user, dictation_id=dictation_id
                )

        else:
            if reset:
                self.request.session["historic"]["revealed_line"] = []
                self.request.session.modified = True
            if new_page:
                free_create_first_session_page(request, dictation_id, line_nb)
                save_user_segment_per_page_in_view(
                    request, dictation_id, line_nb, textarea_content
                )
            else:
                save_user_segment_per_page_in_view(
                    request, dictation_id, line_nb, textarea_content
                )

        reference = convert_segment_to_b64(reference)

        return JsonResponse(
            {
                "result": corrected,
                "state": state,
                "original": reference,
                "reveal_attempts": attempts if reveal_status else attempts,
            },
            headers={"X-Robots-Tag": "noindex"},
        )


def post_user_rating(request: HttpRequest) -> HttpResponse:
    """Post the user rating from ajax."""
    try:
        practice = Practice()
        data = json.loads(request.body)
        star_rating = data["star_rating"]
        dictation_id = data["dictation_id"]
        dictation_id = dictation_id[: dictation_id.index("_")]
        practice.update_rating(
            user=request.user, dictation_id=dictation_id, new_rating=star_rating
        )
        return HttpResponse(status=201, headers={"X-Robots-Tag": "noindex"})
    except (KeyError, ValueError, Practice.DoesNotExist) as exc:
        raise Http404("The requested resource was not found.") from exc


def post_request_definition(request: HttpRequest) -> JsonResponse:
    """Post the definition from wiki."""
    if not request.body:
        return HttpResponse("No data provided", status=400)

    data = json.loads(request.body)

    if not data:
        return HttpResponse("No term provided", status=400)

    wiki = WiktionaryAPI()
    try:
        json_data = wiki.extract_data(data)
        if "en" in json_data:
            definition = wiki.reduce_json(json_data)
        else:
            definition = {"no-result": "No definition found."}
    except requests.exceptions.RequestException as err:
        return HttpResponse(f"Error fetching data: {err}", status=500)

    return JsonResponse({"defs": json.dumps(definition)})
