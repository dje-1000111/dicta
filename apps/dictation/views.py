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
    reveal_first_wrong_letter,
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
            }
        )

        return context


class TopicView(DetailView):
    """Topic View."""

    template_name: str = "pages/topic.html"

    def get_object(self, queryset=None):
        practice = Practice()
        self.dictation = get_object_or_404(Dictation, slug=self.kwargs["slug"])
        if self.request.user.is_authenticated:
            practice.create_dictation(self.request.user, self.dictation)
            self.line_nb = practice.saved_position(self.request.user, self.dictation)
            self.note = practice.get_rating(
                user=self.request.user, dictation_id=self.dictation.pk
            )
            self.lines = practice.get_lines(self.request.user, self.dictation)
        return self.dictation

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Get context data."""
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "form": DictationForm(),
                "dictation_id": (
                    self.dictation.pk if self.request.user.is_authenticated else None
                ),
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
                "lines": self.lines if self.request.user.is_authenticated else [],
                "help": self.dictation.tip,
                "stars": ["5", "4", "3", "2", "1"],
                "topic_title": self.dictation.topic,
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
            line_nb,
            textarea_content,
            topicname,
            reveal_status,
            new_page,
            dictation_id,
        ) = data.values()

        if self.request.user.is_authenticated:
            dictation = Dictation.objects.filter(pk=dictation_id).first()
            filename = dictation.filename
        else:
            dictation = Dictation()
            filename = dictation.get_filename(topicname)

        tot_lines = dictation.total_lines(filename)
        reference = dictation.read_segment(filename, line_nb + 1, tot_lines)
        corrected, lengthened, state, attempts = correction(
            dictation.read_segment(filename, line_nb + 1, tot_lines),
            textarea_content,
            new_page,
        )

        if reveal_status:
            corrected, attempts = reveal_first_wrong_letter(
                corrected, reference, line_nb + 1, reveal_status
            )

        if self.request.user.is_authenticated:
            practice = Practice.objects.get(
                user=self.request.user, dictation_id=dictation_id
            )

            if not "*" in corrected or "<" in corrected:
                practice.update_answered_lines(practice, line_nb, new_page)

                Practice().save_dication_progress(
                    user=self.request.user,
                    dictation_id=dictation_id,
                    current_line=line_nb,
                )

                practice.update_is_done(
                    user=self.request.user, dictation_id=dictation_id
                )

        return JsonResponse(
            {
                "result": corrected,
                "lengthened_verif": lengthened,
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
