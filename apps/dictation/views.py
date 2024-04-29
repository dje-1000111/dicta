"""Views."""

import json

from typing import Any, Dict

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.http import (
    HttpResponse,
    HttpRequest,
)
from django.utils.safestring import mark_safe
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
from apps.dictation.forms import DictationForm


def bad_request(request, exception=None, template_name="400.html"):
    return render(request, "pages/400.html", status=400)


def permission_denied(request, exception=None, template_name="403.html"):
    return render(request, "pages/403.html", status=403)


def not_found(request, exception=None, template_name="404.html"):
    return render(request, "pages/404.html", status=404)


def server_error(request, exception=None, template_name="500.html"):
    return render(request, "pages/500.html", status=500)


class HomeView(ListView):
    """IndexView."""

    template_name: str = "pages/home.html"
    paginate_by: int = 8
    queryset = Dictation.objects.filter(in_production=True).order_by("-level")

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
        context.update(
            {
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
        practice = Practice()

        self.dictation = get_object_or_404(Dictation, slug=self.kwargs["slug"])
        self.real_lines = [i for i in range(0, self.dictation.total_lines() + 1)]
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
        # self.request.session["historic"]["revealed_line"] = []
        if self.request.user.is_authenticated:
            self.request.session["current_dictation"] = [self.dictation.pk]
            self.request.session["new_pages"] = list()
            self.request.session["line_numbers"] = [-1]
            initiate_new_session_in_view(
                self.request, self.dictation.pk, self.lines, self.line_nb
            )
        else:
            free_initiate_new_session(self.request)
            free_create_first_session_page(self.request, self.dictation.pk)
            self.request.session["new_pages"] = list()
            self.request.session["current_dictation"] = [self.dictation.pk]
            self.request.session.modified = True

        context = super().get_context_data(**kwargs)
        context.update(
            {
                "form": DictationForm(),
                "dictation_id": (self.dictation.pk),
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
                "help": self.dictation.tip,
                "stars": ["5", "4", "3", "2", "1"],
                "topic_title": self.dictation.topic,
                "real_lines": self.real_lines,
                "lol": [
                    self.real_lines[i : i + 30]
                    for i in range(0, len(self.real_lines), 30)
                ],
                "reds": self.reds if self.request.user.is_authenticated else [],
            }
        )
        return context


class AjaxDetailView(DetailView):
    """Ajax post text area content."""

    model = Dictation

    def post(self, request, *args, **kwargs):
        """Post."""
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

            if not "*" in corrected and not "<" in corrected:
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
    practice = Practice()
    data = json.loads(request.body)
    star_rating = data["star_rating"]
    dictation_id = data["dictation_id"]
    dictation_id = dictation_id[: dictation_id.index("_")]
    practice.update_rating(
        user=request.user, dictation_id=dictation_id, new_rating=star_rating
    )
    return HttpResponse(status=201, headers={"X-Robots-Tag": "noindex"})


def post_request_definition(request):
    """Post the definition from wiki."""
    term = json.loads(request.body)
    wiki = WiktionaryAPI()
    data = wiki.extract_data(term)
    if "en" in data:
        definition = wiki.reduce_json(data)
    else:
        definition = {"no-result": "No definition found."}

    return HttpResponse(
        status=204,
        headers={"definition": json.dumps(definition), "X-Robots-Tag": "noindex"},
    )
